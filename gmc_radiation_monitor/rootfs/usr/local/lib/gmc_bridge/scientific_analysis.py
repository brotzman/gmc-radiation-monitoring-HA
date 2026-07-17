from __future__ import annotations

import math
import statistics
from collections import defaultdict
from collections.abc import Iterable
from datetime import UTC, datetime
from typing import Any

from .history import HistoryRow


def _poisson_limit(count: int, *, z: float, upper: bool) -> float:
    """Wilson-Hilferty approximation to a Garwood Poisson count limit."""
    n = max(0, int(count))
    if upper:
        k = n + 1
        return k * max(0.0, 1.0 - 1.0 / (9.0 * k) + z / (3.0 * math.sqrt(k))) ** 3
    if n == 0:
        return 0.0
    return n * max(0.0, 1.0 - 1.0 / (9.0 * n) - z / (3.0 * math.sqrt(n))) ** 3


def counting_uncertainty(rows: Iterable[HistoryRow], *, confidence_z: float = 1.0) -> dict[str, Any]:
    """Estimate Poisson counting uncertainty from stored one-minute CPM counts.

    GMC CPM values represent counts in an approximately one-minute counting window.
    Each accepted row therefore contributes its observed CPM as an impulse count and
    60 seconds of effective counting time. Gaps are not treated as exposure time.
    """
    clean = [row for row in rows if int(row.cpm) >= 0]
    if not clean:
        return {
            "available": False,
            "sample_count": 0,
            "impulses": 0,
            "duration_seconds": 0,
            "rate_cpm": None,
            "lower_cpm": None,
            "upper_cpm": None,
            "minus_cpm": None,
            "plus_cpm": None,
            "relative_uncertainty_percent": None,
        }
    impulses = sum(int(row.cpm) for row in clean)
    duration_seconds = len(clean) * 60
    duration_minutes = duration_seconds / 60.0
    rate = impulses / duration_minutes
    lower = _poisson_limit(impulses, z=confidence_z, upper=False) / duration_minutes
    upper = _poisson_limit(impulses, z=confidence_z, upper=True) / duration_minutes
    symmetric = math.sqrt(impulses) / duration_minutes if impulses > 0 else upper
    return {
        "available": True,
        "sample_count": len(clean),
        "impulses": impulses,
        "duration_seconds": duration_seconds,
        "rate_cpm": rate,
        "lower_cpm": lower,
        "upper_cpm": upper,
        "minus_cpm": max(0.0, rate - lower),
        "plus_cpm": max(0.0, upper - rate),
        "sigma_cpm": symmetric,
        "relative_uncertainty_percent": (100.0 * symmetric / rate) if rate > 0 else None,
        "confidence_z": confidence_z,
    }


def _hourly_count_rates(rows: Iterable[HistoryRow]) -> list[dict[str, Any]]:
    buckets: dict[int, list[HistoryRow]] = defaultdict(list)
    for row in rows:
        buckets[int(row.timestamp_utc) // 3600 * 3600].append(row)
    points: list[dict[str, Any]] = []
    for timestamp, bucket in sorted(buckets.items()):
        impulses = sum(max(0, int(row.cpm)) for row in bucket)
        minutes = len(bucket)
        if minutes <= 0:
            continue
        rate = impulses / minutes
        points.append({
            "timestamp_utc": timestamp,
            "rate_cpm": rate,
            "impulses": impulses,
            "minutes": minutes,
        })
    return points


def _segment_stats(points: list[dict[str, Any]]) -> dict[str, float] | None:
    if len(points) < 6:
        return None
    impulses = sum(int(point["impulses"]) for point in points)
    minutes = sum(int(point["minutes"]) for point in points)
    if minutes <= 0:
        return None
    rate = impulses / minutes
    hourly = [float(point["rate_cpm"]) for point in points]
    median = float(statistics.median(hourly))
    mad = float(statistics.median(abs(value - median) for value in hourly))
    robust_sigma = 1.4826 * mad
    poisson_se = math.sqrt(max(impulses, 1)) / minutes
    empirical_se = robust_sigma / math.sqrt(len(hourly)) if robust_sigma > 0 else 0.0
    return {
        "rate_cpm": rate,
        "median_cpm": median,
        "standard_error_cpm": max(poisson_se, empirical_se, 1e-9),
        "hours": float(len(points)),
        "impulses": float(impulses),
        "minutes": float(minutes),
    }


def detect_persistent_level_shift(
    rows: Iterable[HistoryRow],
    *,
    minimum_pre_hours: int = 24,
    minimum_post_hours: int = 6,
    comparison_hours: int = 24,
    minimum_change_percent: float = 5.0,
) -> dict[str, Any]:
    """Detect a persistent mean-level shift by robust two-segment comparison.

    Candidate change times are evaluated on hourly count-rate aggregates. The
    detector requires a substantial pre-change reference and a persistent
    post-change segment; significance combines Poisson counting uncertainty with
    observed hour-to-hour variability. It is contextual and never changes alarms.
    """
    points = _hourly_count_rates(rows)
    if len(points) < minimum_pre_hours + minimum_post_hours:
        return {
            "available": False,
            "detected": False,
            "state": "Insufficient history for level-shift detection",
            "hourly_points": len(points),
            "minimum_pre_hours": minimum_pre_hours,
            "minimum_post_hours": minimum_post_hours,
        }
    latest = int(points[-1]["timestamp_utc"])
    earliest_candidate = int(points[0]["timestamp_utc"]) + minimum_pre_hours * 3600
    latest_candidate = latest - minimum_post_hours * 3600
    best: dict[str, Any] | None = None
    for candidate in (int(point["timestamp_utc"]) for point in points):
        if candidate < earliest_candidate or candidate > latest_candidate:
            continue
        before = [
            point for point in points
            if candidate - comparison_hours * 3600 <= int(point["timestamp_utc"]) < candidate
        ]
        after = [
            point for point in points
            if candidate <= int(point["timestamp_utc"]) <= min(latest, candidate + comparison_hours * 3600)
        ]
        before_stats = _segment_stats(before)
        after_stats = _segment_stats(after)
        if before_stats is None or after_stats is None:
            continue
        delta = after_stats["rate_cpm"] - before_stats["rate_cpm"]
        percent = 100.0 * delta / before_stats["rate_cpm"] if before_stats["rate_cpm"] > 0 else 0.0
        combined_se = math.sqrt(
            before_stats["standard_error_cpm"] ** 2 + after_stats["standard_error_cpm"] ** 2
        )
        score = abs(delta) / combined_se if combined_se > 0 else 0.0
        candidate_result = {
            "timestamp_utc": candidate,
            "timestamp_iso": datetime.fromtimestamp(candidate, tz=UTC).isoformat(),
            "before_cpm": before_stats["rate_cpm"],
            "after_cpm": after_stats["rate_cpm"],
            "change_cpm": delta,
            "change_percent": percent,
            "significance_sigma": score,
            "pre_hours": int(before_stats["hours"]),
            "post_hours": int(after_stats["hours"]),
        }
        if best is None or score * abs(percent) > float(best["significance_sigma"]) * abs(float(best["change_percent"])):
            best = candidate_result
    if best is None:
        return {
            "available": False,
            "detected": False,
            "state": "Insufficient history for level-shift detection",
            "hourly_points": len(points),
        }
    magnitude = abs(float(best["change_percent"]))
    sigma = float(best["significance_sigma"])
    pronounced = magnitude >= minimum_change_percent and sigma >= 3.0
    possible = magnitude >= max(3.0, minimum_change_percent * 0.6) and sigma >= 2.0
    if pronounced:
        state = "Persistent level shift detected"
        confidence = "High" if sigma >= 5.0 and int(best["post_hours"]) >= 12 else "Medium"
    elif possible:
        state = "Possible persistent level shift"
        confidence = "Low"
    else:
        state = "No persistent level shift detected"
        confidence = "Low"
    return {
        "available": True,
        "detected": pronounced or possible,
        "pronounced": pronounced,
        "state": state,
        "confidence": confidence,
        "hourly_points": len(points),
        "minimum_change_percent": minimum_change_percent,
        **best,
        "statistical_only": True,
    }


def relative_device_response(
    pairs: Iterable[tuple[HistoryRow, HistoryRow]],
    *,
    orientation_changes: int = 0,
    orientation_verified: bool = False,
    minimum_pairs: int = 500,
    minimum_span_days: float = 14.0,
) -> dict[str, Any]:
    """Learn a robust relative response factor from co-located paired readings.

    Ratios are formed from daily impulse totals rather than individual low-count
    CPM ratios. This reduces small-number bias while retaining day-level robust
    rejection of unusual geometry or device periods.
    """
    clean = [
        (left, right)
        for left, right in pairs
        if int(left.cpm) > 0 and int(right.cpm) > 0
    ]
    if not clean:
        return {
            "available": False,
            "learning": True,
            "pairs": 0,
            "span_days": 0.0,
            "orientation_stable": (orientation_changes == 0) if orientation_verified else None,
            "orientation_verified": orientation_verified,
        }

    daily: dict[int, dict[str, Any]] = defaultdict(lambda: {"left": 0, "right": 0, "pairs": []})
    for left, right in clean:
        day = int(left.timestamp_utc) // 86400
        daily[day]["left"] += int(left.cpm)
        daily[day]["right"] += int(right.cpm)
        daily[day]["pairs"].append((left, right))
    daily_items = [
        (day, values, float(values["left"]) / float(values["right"]))
        for day, values in sorted(daily.items())
        if int(values["left"]) > 0 and int(values["right"]) > 0 and len(values["pairs"]) >= 5
    ]
    if not daily_items:
        daily_items = [
            (0, {"left": sum(int(left.cpm) for left, _ in clean),
                 "right": sum(int(right.cpm) for _, right in clean),
                 "pairs": clean},
             sum(int(left.cpm) for left, _ in clean) / sum(int(right.cpm) for _, right in clean))
        ]
    ratios = [item[2] for item in daily_items]
    median_ratio = float(statistics.median(ratios))
    mad = float(statistics.median(abs(value - median_ratio) for value in ratios))
    robust_sigma = 1.4826 * mad
    retained_days = [
        item for item in daily_items
        if mad == 0.0 or abs(item[2] - median_ratio) <= max(0.08 * median_ratio, 6.0 * robust_sigma)
    ]
    retained_pairs = [pair for _, values, _ in retained_days for pair in values["pairs"]]
    if not retained_pairs:
        retained_pairs = clean
    total_left = sum(int(left.cpm) for left, _ in retained_pairs)
    total_right = sum(int(right.cpm) for _, right in retained_pairs)
    center = float(total_left) / float(total_right) if total_right > 0 else None
    retained_ratios = [item[2] for item in retained_days] or ratios
    retained_median = float(statistics.median(retained_ratios))
    retained_mad = float(statistics.median(abs(value - retained_median) for value in retained_ratios))
    robust_relative_spread = (
        100.0 * 1.4826 * retained_mad / retained_median if retained_median > 0 else None
    )
    relative_counting_uncertainty = (
        100.0 * math.sqrt(1.0 / total_left + 1.0 / total_right)
        if total_left > 0 and total_right > 0 else None
    )
    timestamps = [int(left.timestamp_utc) for left, _ in retained_pairs]
    span_days = (max(timestamps) - min(timestamps)) / 86400.0 if len(timestamps) > 1 else 0.0
    pair_count = len(retained_pairs)
    orientation_stable = (orientation_changes == 0) if orientation_verified else None
    learning = pair_count < minimum_pairs or span_days < minimum_span_days or (orientation_verified and not orientation_stable)
    confidence = "Insufficient"
    spread_for_confidence = robust_relative_spread if robust_relative_spread is not None else 999.0
    counting_for_confidence = relative_counting_uncertainty if relative_counting_uncertainty is not None else 999.0
    if not learning:
        if (
            pair_count >= 2000 and span_days >= 30.0 and spread_for_confidence <= 10.0
            and counting_for_confidence <= 1.0 and orientation_verified
        ):
            confidence = "High"
        elif spread_for_confidence <= 20.0 and counting_for_confidence <= 3.0:
            confidence = "Medium"
        else:
            confidence = "Low"
    return {
        "available": center is not None,
        "learning": learning,
        "pairs": pair_count,
        "excluded_pairs": len(clean) - pair_count,
        "daily_groups": len(retained_days),
        "excluded_daily_groups": len(daily_items) - len(retained_days),
        "span_days": span_days,
        "factor_right_to_left": center,
        "factor_left_to_right": (1.0 / center) if center and center > 0 else None,
        "relative_spread_percent": robust_relative_spread,
        "counting_uncertainty_percent": relative_counting_uncertainty,
        "total_left_impulses": total_left,
        "total_right_impulses": total_right,
        "orientation_stable": orientation_stable,
        "orientation_verified": orientation_verified,
        "orientation_changes": orientation_changes,
        "minimum_pairs": minimum_pairs,
        "minimum_span_days": minimum_span_days,
        "confidence": confidence,
        "relative_only": True,
        "co_location_required": True,
    }

