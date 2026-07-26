from __future__ import annotations

import math
import random
import statistics
from collections import defaultdict
from datetime import UTC, datetime, timedelta
from typing import Any, Iterable
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .history import HistoryRow, HistoryStore

WINDOWS: tuple[tuple[str, int], ...] = (
    ("24h", 1),
    ("7d", 7),
    ("30d", 30),
    ("90d", 90),
    ("365d", 365),
)
LAG_HOURS: tuple[int, ...] = (0, 3, 6, 12, 24)

# Minimum evidence requirements. These thresholds are deliberately conservative
# and govern wording/evidence levels rather than hiding the underlying data.
WINDOW_MINIMUM_COVERAGE: dict[str, float] = {
    "24h": 90.0,
    "7d": 85.0,
    "30d": 80.0,
    "90d": 80.0,
    "365d": 80.0,
}

MINIMUM_REQUIREMENTS: dict[str, dict[str, float]] = {
    "trend": {"days": 30.0, "coverage_percent": 80.0, "effective_samples": 14.0},
    "annual_projection": {"days": 90.0, "coverage_percent": 80.0},
    "seasonal_exploratory": {"months": 6.0},
    "seasonal_supported": {"months": 12.0},
    "environment": {"pairs": 100.0},
    "control_chart": {"days": 30.0},
}


def _quantile(values: list[float], fraction: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    position = max(0.0, min(1.0, fraction)) * (len(ordered) - 1)
    lower = int(math.floor(position))
    upper = int(math.ceil(position))
    if lower == upper:
        return ordered[lower]
    weight = position - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def _safe_timezone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError:
        return ZoneInfo("UTC")


def _rank(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda item: item[1])
    ranks = [0.0] * len(values)
    start = 0
    while start < len(indexed):
        end = start + 1
        while end < len(indexed) and indexed[end][1] == indexed[start][1]:
            end += 1
        average_rank = (start + 1 + end) / 2.0
        for index in range(start, end):
            ranks[indexed[index][0]] = average_rank
        start = end
    return ranks


def _pearson(left: list[float], right: list[float]) -> float | None:
    if len(left) != len(right) or len(left) < 4:
        return None
    mean_left = statistics.fmean(left)
    mean_right = statistics.fmean(right)
    numerator = sum((x - mean_left) * (y - mean_right) for x, y in zip(left, right, strict=True))
    denominator_left = sum((x - mean_left) ** 2 for x in left)
    denominator_right = sum((y - mean_right) ** 2 for y in right)
    denominator = math.sqrt(denominator_left * denominator_right)
    if denominator <= 0:
        return None
    return numerator / denominator


def _spearman(left: list[float], right: list[float]) -> float | None:
    return _pearson(_rank(left), _rank(right))


def _autocorrelation(values: list[float], lag: int) -> float | None:
    if lag <= 0 or len(values) <= lag + 2:
        return None
    return _pearson(values[:-lag], values[lag:])


def _effective_sample_size(values: list[float], maximum_lag: int = 30) -> dict[str, Any]:
    n = len(values)
    if n < 8:
        return {"available": False, "observations": n, "effective": None, "correlation_days": None}
    positive_sum = 0.0
    correlations: list[dict[str, float]] = []
    for lag in range(1, min(maximum_lag, n // 3) + 1):
        value = _autocorrelation(values, lag)
        if value is None:
            break
        correlations.append({"lag_days": float(lag), "correlation": value})
        if value <= 0:
            break
        positive_sum += value
    inflation = max(1.0, 1.0 + 2.0 * positive_sum)
    effective = max(1.0, min(float(n), n / inflation))
    return {
        "available": True,
        "observations": n,
        "effective": effective,
        "correlation_days": inflation,
        "correlations": correlations,
    }


def _moving_block_bootstrap(values: list[float], *, seed: int = 910, replicates: int = 300) -> dict[str, Any]:
    if len(values) < 14:
        return {"available": False, "replicates": 0, "block_length": None}
    effective = _effective_sample_size(values)
    correlation_days = float(effective.get("correlation_days") or 1.0)
    block_length = max(2, min(len(values) // 3, int(round(correlation_days))))
    rng = random.Random(seed + len(values))
    mean_samples: list[float] = []
    median_samples: list[float] = []
    starts = max(1, len(values) - block_length + 1)
    for _ in range(replicates):
        sample: list[float] = []
        while len(sample) < len(values):
            start = rng.randrange(starts)
            sample.extend(values[start : start + block_length])
        sample = sample[: len(values)]
        mean_samples.append(statistics.fmean(sample))
        median_samples.append(float(statistics.median(sample)))
    return {
        "available": True,
        "replicates": replicates,
        "block_length": block_length,
        "mean_ci95": [_quantile(mean_samples, 0.025), _quantile(mean_samples, 0.975)],
        "median_ci95": [_quantile(median_samples, 0.025), _quantile(median_samples, 0.975)],
    }


def _mann_kendall(values: list[float]) -> dict[str, Any]:
    n = len(values)
    if n < 14:
        return {"available": False, "days": n}
    score = 0
    ties: dict[float, int] = defaultdict(int)
    for value in values:
        ties[value] += 1
    for index in range(n - 1):
        current = values[index]
        for later in values[index + 1 :]:
            score += (later > current) - (later < current)
    variance = n * (n - 1) * (2 * n + 5)
    variance -= sum(count * (count - 1) * (2 * count + 5) for count in ties.values() if count > 1)
    variance /= 18.0
    if variance <= 0:
        z = 0.0
    elif score > 0:
        z = (score - 1) / math.sqrt(variance)
    elif score < 0:
        z = (score + 1) / math.sqrt(variance)
    else:
        z = 0.0
    p_value = math.erfc(abs(z) / math.sqrt(2.0))
    tau = score / (0.5 * n * (n - 1))

    stride = max(1, math.ceil(n / 500))
    sampled = values[::stride]
    slopes: list[float] = []
    for index in range(len(sampled) - 1):
        for later_index in range(index + 1, len(sampled)):
            slopes.append((sampled[later_index] - sampled[index]) / ((later_index - index) * stride))
    slope = float(statistics.median(slopes)) if slopes else 0.0
    significant = p_value < 0.05
    direction = "stable"
    if significant and slope > 0:
        direction = "increasing"
    elif significant and slope < 0:
        direction = "decreasing"
    return {
        "available": True,
        "days": n,
        "tau": tau,
        "z": z,
        "p_value": p_value,
        "sen_slope_cpm_per_day": slope,
        "significant": significant,
        "direction": direction,
        "sample_stride": stride,
    }


def _daily_control_chart(values: list[float]) -> dict[str, Any]:
    if len(values) < 30:
        return {"available": False, "days": len(values)}
    baseline_count = min(60, max(20, len(values) // 3))
    baseline = values[:baseline_count]
    center = float(statistics.median(baseline))
    mad = float(statistics.median(abs(value - center) for value in baseline))
    sigma = max(1.0, 1.4826 * mad, math.sqrt(max(center, 1.0)) * 0.35)
    lambda_value = 0.2
    ewma = center
    ewma_alarm_days = 0
    ewma_limit = 3.0 * sigma * math.sqrt(lambda_value / (2.0 - lambda_value))
    cusum_positive = 0.0
    cusum_negative = 0.0
    cusum_alarm_days = 0
    allowance = 0.5 * sigma
    decision = 5.0 * sigma
    for value in values[baseline_count:]:
        ewma = lambda_value * value + (1.0 - lambda_value) * ewma
        if abs(ewma - center) > ewma_limit:
            ewma_alarm_days += 1
        cusum_positive = max(0.0, cusum_positive + value - center - allowance)
        cusum_negative = min(0.0, cusum_negative + value - center + allowance)
        if cusum_positive > decision or abs(cusum_negative) > decision:
            cusum_alarm_days += 1
    return {
        "available": True,
        "days": len(values),
        "baseline_days": baseline_count,
        "center_cpm": center,
        "robust_sigma_cpm": sigma,
        "ewma_cpm": ewma,
        "ewma_limit_cpm": ewma_limit,
        "ewma_signal": ewma_alarm_days > 0,
        "ewma_signal_days": ewma_alarm_days,
        "cusum_positive": cusum_positive,
        "cusum_negative": cusum_negative,
        "cusum_decision_cpm": decision,
        "cusum_signal": cusum_alarm_days > 0,
        "cusum_signal_days": cusum_alarm_days,
        "statistical_only": True,
    }


def _hourly_episodes(points: list[dict[str, Any]], threshold_cpm: float) -> dict[str, Any]:
    episodes: list[dict[str, Any]] = []
    current: list[dict[str, Any]] = []

    def finish() -> None:
        if not current:
            return
        covered_hours = sum(float(item["covered_seconds"]) for item in current) / 3600.0
        if covered_hours <= 0:
            current.clear()
            return
        values = [float(item["mean_cpm"]) for item in current]
        episodes.append({
            "start_utc": int(current[0]["timestamp_utc"]),
            "end_utc": int(current[-1]["timestamp_utc"]) + 3600,
            "duration_hours": covered_hours,
            "mean_cpm": statistics.fmean(values),
            "maximum_cpm": max(values),
            "area_above_threshold_cpm_h": sum(
                max(0.0, float(item["mean_cpm"]) - threshold_cpm)
                * float(item["covered_seconds"]) / 3600.0
                for item in current
            ),
            "persistent": covered_hours >= 2.0,
        })
        current.clear()

    previous_timestamp: int | None = None
    for point in points:
        timestamp = int(point["timestamp_utc"])
        elevated = float(point["mean_cpm"]) >= threshold_cpm
        continuous = previous_timestamp is None or timestamp - previous_timestamp <= 5400
        if elevated and continuous:
            current.append(point)
        elif elevated:
            finish()
            current.append(point)
        else:
            finish()
        previous_timestamp = timestamp
    finish()
    persistent = [item for item in episodes if item["persistent"]]
    persistent.sort(key=lambda item: (item["duration_hours"], item["maximum_cpm"]), reverse=True)
    return {
        "threshold_cpm": threshold_cpm,
        "event_count": len(persistent),
        "all_event_count": len(episodes),
        "total_hours": sum(float(item["duration_hours"]) for item in persistent),
        "maximum_duration_hours": max((float(item["duration_hours"]) for item in persistent), default=0.0),
        "maximum_cpm": max((float(item["maximum_cpm"]) for item in persistent), default=None),
        "area_above_threshold_cpm_h": sum(float(item["area_above_threshold_cpm_h"]) for item in persistent),
        "items": persistent[:20],
    }


def _normal_two_sided_p(z_value: float) -> float:
    """Conservative two-sided normal approximation used without scipy."""
    return max(0.0, min(1.0, math.erfc(abs(float(z_value)) / math.sqrt(2.0))))


def _correlation_p_value(correlation: float, pairs: int) -> float | None:
    if pairs < 4 or abs(correlation) >= 1.0:
        return 0.0 if abs(correlation) >= 1.0 and pairs >= 4 else None
    denominator = max(1e-12, 1.0 - correlation * correlation)
    statistic = correlation * math.sqrt(max(1.0, (pairs - 2) / denominator))
    return _normal_two_sided_p(statistic)


def _benjamini_hochberg(items: list[dict[str, Any]], *, alpha: float = 0.05) -> None:
    """Attach FDR-adjusted p-values to a small set of exploratory tests."""
    valid = [(index, float(item["p_value"])) for index, item in enumerate(items) if item.get("p_value") is not None]
    if not valid:
        return
    ordered = sorted(valid, key=lambda pair: pair[1])
    count = len(ordered)
    adjusted = [1.0] * count
    running = 1.0
    for reverse_index in range(count - 1, -1, -1):
        _original_index, p_value = ordered[reverse_index]
        rank = reverse_index + 1
        running = min(running, p_value * count / rank)
        adjusted[reverse_index] = min(1.0, running)
    for ordered_index, (original_index, _p_value) in enumerate(ordered):
        items[original_index]["p_value_fdr"] = adjusted[ordered_index]
        items[original_index]["significant_fdr"] = adjusted[ordered_index] < alpha


def _evidence_level(
    *,
    duration_days: float,
    coverage_percent: float,
    effective_samples: float | None = None,
    minimum_days: float = 0.0,
    minimum_coverage: float = 0.0,
    minimum_effective: float = 0.0,
) -> dict[str, Any]:
    reasons: list[str] = []
    if duration_days < minimum_days:
        reasons.append("duration")
    if coverage_percent < minimum_coverage:
        reasons.append("coverage")
    if minimum_effective and (effective_samples is None or effective_samples < minimum_effective):
        reasons.append("effective_sample_size")
    if reasons:
        return {"level": "not_evaluable", "reasons": reasons}
    score = 0
    score += 1 if duration_days >= minimum_days * 1.25 else 0
    score += 1 if coverage_percent >= max(minimum_coverage, 90.0) else 0
    if minimum_effective:
        score += 1 if effective_samples is not None and effective_samples >= minimum_effective * 2.0 else 0
    if score >= 3:
        level = "well_supported"
    elif score >= 2:
        level = "supported"
    elif score >= 1:
        level = "preliminary"
    else:
        level = "exploratory"
    return {"level": level, "reasons": []}


def _trend_effect(slope_cpm_per_day: float | None, background_cpm: float | None) -> dict[str, Any]:
    if slope_cpm_per_day is None or not background_cpm or background_cpm <= 0:
        return {"level": "unknown", "percent_per_month": None}
    percent_per_month = 100.0 * float(slope_cpm_per_day) * 30.4375 / float(background_cpm)
    magnitude = abs(percent_per_month)
    if magnitude < 1.0:
        level = "very_small"
    elif magnitude < 5.0:
        level = "small"
    elif magnitude < 15.0:
        level = "moderate"
    else:
        level = "large"
    return {"level": level, "percent_per_month": percent_per_month}


def _best_lagged_environment(points: list[dict[str, Any]], field: str) -> dict[str, Any]:
    by_hour = {int(point["timestamp_utc"]): point for point in points}
    results: list[dict[str, Any]] = []
    minimum_pairs = int(MINIMUM_REQUIREMENTS["environment"]["pairs"])
    for lag in LAG_HOURS:
        radiation: list[float] = []
        environment: list[float] = []
        offset = lag * 3600
        for timestamp, point in by_hour.items():
            source = by_hour.get(timestamp - offset)
            if source is None or source.get(field) is None:
                continue
            radiation.append(float(point["mean_cpm"]))
            environment.append(float(source[field]))
        correlation = _spearman(radiation, environment)
        if correlation is not None:
            pairs = len(radiation)
            results.append({
                "lag_hours": lag,
                "correlation": correlation,
                "pairs": pairs,
                "p_value": _correlation_p_value(correlation, pairs),
                "meets_minimum_pairs": pairs >= minimum_pairs,
            })
    _benjamini_hochberg(results)
    eligible = [item for item in results if item.get("meets_minimum_pairs")]
    if not eligible:
        maximum_pairs = max((int(item.get("pairs") or 0) for item in results), default=0)
        return {
            "available": False,
            "field": field,
            "results": results,
            "minimum_pairs": minimum_pairs,
            "maximum_pairs": maximum_pairs,
            "evidence": {"level": "not_evaluable", "reasons": ["paired_samples"]},
            "causal": False,
        }
    best = max(eligible, key=lambda item: abs(float(item["correlation"])))
    evidence = {
        "level": "preliminary" if bool(best.get("significant_fdr")) else "exploratory",
        "reasons": [] if bool(best.get("significant_fdr")) else ["multiple_testing"],
    }
    return {
        "available": True,
        "field": field,
        "best": best,
        "results": results,
        "minimum_pairs": minimum_pairs,
        "tests": len(results),
        "fdr_method": "Benjamini-Hochberg",
        "evidence": evidence,
        "causal": False,
    }


def _aggregate_daily(points: list[dict[str, Any]], timezone: ZoneInfo) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for point in points:
        local = datetime.fromtimestamp(int(point["timestamp_utc"]), UTC).astimezone(timezone)
        groups[local.date().isoformat()].append(point)
    result: list[dict[str, Any]] = []
    for day, items in sorted(groups.items()):
        covered = sum(float(item["covered_seconds"]) for item in items)
        if covered <= 0:
            continue
        weighted_cpm = sum(float(item["mean_cpm"]) * float(item["covered_seconds"]) for item in items) / covered
        hourly = [float(item["mean_cpm"]) for item in items]
        dose = sum(float(item.get("dose_usv") or 0.0) for item in items)
        # A local civil day can contain 23 or 25 hours at a daylight-saving
        # transition. Use the actual UTC duration between local midnights so a
        # complete transition day is not incorrectly marked incomplete.
        local_start = datetime.fromisoformat(day).replace(tzinfo=timezone)
        local_end = (datetime.fromisoformat(day) + timedelta(days=1)).replace(tzinfo=timezone)
        expected_seconds = max(1.0, (local_end.astimezone(UTC) - local_start.astimezone(UTC)).total_seconds())
        result.append({
            "date": day,
            "timestamp_utc": int(items[0]["timestamp_utc"]),
            "mean_cpm": weighted_cpm,
            "median_cpm": float(statistics.median(hourly)),
            "p95_cpm": _quantile(hourly, 0.95),
            "minimum_cpm": min(hourly),
            "maximum_cpm": max(hourly),
            "coverage_percent": min(100.0, 100.0 * covered / expected_seconds),
            "expected_hours": expected_seconds / 3600.0,
            "covered_hours": covered / 3600.0,
            "dose_usv": dose,
        })
    return result


def _aggregate_monthly(days: list[dict[str, Any]]) -> list[dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in days:
        groups[str(item["date"])[:7]].append(item)
    result: list[dict[str, Any]] = []
    for month, items in sorted(groups.items()):
        covered = sum(float(item["covered_hours"]) for item in items)
        values = [float(item["median_cpm"]) for item in items]
        weighted_mean = (
            sum(float(item["mean_cpm"]) * float(item["covered_hours"]) for item in items) / covered
            if covered > 0
            else None
        )
        result.append({
            "month": month,
            "days": len(items),
            "covered_hours": covered,
            "mean_cpm": weighted_mean,
            "median_cpm": float(statistics.median(values)) if values else None,
            "minimum_cpm": min(values) if values else None,
            "maximum_cpm": max(values) if values else None,
            "dose_usv": sum(float(item.get("dose_usv") or 0.0) for item in items),
        })
    return result


def _window_summary(
    points: list[dict[str, Any]],
    *,
    latest_end_utc: int,
    days: int,
    minimum_coverage_percent: float,
    warning_cpm: float,
    danger_cpm: float,
) -> dict[str, Any]:
    start = latest_end_utc - days * 86400
    selected = [point for point in points if int(point["timestamp_utc"]) >= start]
    covered = sum(float(point["covered_seconds"]) for point in selected)
    requested = float(days * 86400)
    coverage = min(100.0, 100.0 * covered / requested) if requested > 0 else 0.0
    values = [float(point["mean_cpm"]) for point in selected]
    weighted_mean = (
        sum(float(point["mean_cpm"]) * float(point["covered_seconds"]) for point in selected) / covered
        if covered > 0
        else None
    )
    first_timestamp = min((int(point["timestamp_utc"]) for point in selected), default=None)
    span_ready = first_timestamp is not None and first_timestamp <= start + 5400
    ready = bool(values) and span_ready and coverage >= minimum_coverage_percent
    warning_seconds = sum(
        float(point["covered_seconds"]) for point in selected
        if warning_cpm <= float(point["mean_cpm"]) < danger_cpm
    )
    danger_seconds = sum(
        float(point["covered_seconds"]) for point in selected if float(point["mean_cpm"]) >= danger_cpm
    )
    dose_values = [float(point.get("dose_usv") or 0.0) for point in selected]
    dose_available = any(bool(point.get("dose_available")) for point in selected)
    return {
        "days": days,
        "available": bool(values),
        "ready": ready,
        "coverage_percent": coverage,
        "minimum_coverage_percent": minimum_coverage_percent,
        "covered_days": covered / 86400.0,
        "hours": len(values),
        "mean_cpm": weighted_mean,
        "median_cpm": float(statistics.median(values)) if values else None,
        "p05_cpm": _quantile(values, 0.05),
        "p95_cpm": _quantile(values, 0.95),
        "minimum_cpm": min(values) if values else None,
        "maximum_cpm": max(values) if values else None,
        "dose_usv": sum(dose_values) if dose_available else None,
        "dose_available": dose_available,
        "warning_hours": warning_seconds / 3600.0,
        "danger_hours": danger_seconds / 3600.0,
        "start_utc": start,
        "end_utc": latest_end_utc,
        "reason": (
            "ready"
            if ready
            else "insufficient_coverage"
            if coverage < minimum_coverage_percent and span_ready
            else "insufficient_duration"
        ),
    }


def _hourly_points(
    store: HistoryStore,
    *,
    start_utc: int,
    end_utc: int,
    device_serial: str,
    scan_interval_seconds: int,
    cpm_per_usvh: float,
) -> list[dict[str, Any]]:
    rows = store.aggregate_range(
        start_utc,
        end_utc,
        bucket_seconds=3600,
        expected_interval_seconds=scan_interval_seconds,
        device_serial=device_serial,
    )
    result: list[dict[str, Any]] = []
    for row in rows:
        covered_seconds = min(3600.0, float(row.get("occupied_slots") or 0) * scan_interval_seconds)
        mean_cpm = float(row["mean_cpm"])
        derived = row.get("mean_derived_dose_usvh")
        dose_rate = float(derived) if derived is not None else (mean_cpm / cpm_per_usvh if cpm_per_usvh > 0 else None)
        result.append({
            **row,
            "covered_seconds": covered_seconds,
            "dose_rate_usvh": dose_rate,
            "dose_usv": (dose_rate * covered_seconds / 3600.0) if dose_rate is not None else None,
            "dose_available": dose_rate is not None,
            "dose_source": "stored" if derived is not None else "configured_factor" if dose_rate is not None else "unavailable",
        })
    return result


def build_long_term_analysis(
    store: HistoryStore,
    *,
    device_serial: str,
    scan_interval_seconds: int,
    cpm_per_usvh: float,
    timezone_name: str,
    warning_cpm: float,
    danger_cpm: float,
    minimum_coverage_percent: float = 80.0,
    maximum_days: int = 730,
) -> dict[str, Any]:
    first, last = store.bounds(device_serial=device_serial)
    if first is None or last is None:
        return {"available": False, "device_serial": device_serial, "windows": {}}
    end_utc = int(last) + max(1, scan_interval_seconds)
    start_utc = max(int(first), end_utc - max(365, maximum_days) * 86400)
    points = _hourly_points(
        store,
        start_utc=start_utc,
        end_utc=end_utc,
        device_serial=device_serial,
        scan_interval_seconds=scan_interval_seconds,
        cpm_per_usvh=cpm_per_usvh,
    )
    if not points:
        return {"available": False, "device_serial": device_serial, "windows": {}}

    timezone = _safe_timezone(timezone_name)
    daily = _aggregate_daily(points, timezone)
    monthly = _aggregate_monthly(daily)
    windows = {
        key: _window_summary(
            points,
            latest_end_utc=end_utc,
            days=days,
            minimum_coverage_percent=max(
                minimum_coverage_percent,
                WINDOW_MINIMUM_COVERAGE.get(key, minimum_coverage_percent),
            ),
            warning_cpm=warning_cpm,
            danger_cpm=danger_cpm,
        )
        for key, days in WINDOWS
    }

    qualifying_daily = [item for item in daily if float(item["coverage_percent"]) >= 50.0]
    daily_values = [float(item["median_cpm"]) for item in qualifying_daily]
    background_source = qualifying_daily[-90:] if len(qualifying_daily) >= 14 else qualifying_daily
    background_values = [float(item["median_cpm"]) for item in background_source]
    background_median = float(statistics.median(background_values)) if background_values else None
    background_mad = (
        float(statistics.median(abs(value - background_median) for value in background_values))
        if background_median is not None
        else None
    )
    robust_sigma = 1.4826 * background_mad if background_mad is not None else None
    recent_values = daily_values[-7:]
    recent_median = float(statistics.median(recent_values)) if recent_values else None
    deviation_percent = (
        100.0 * (recent_median - background_median) / background_median
        if recent_median is not None and background_median and background_median > 0
        else None
    )
    relative_threshold = (
        max(background_median * 1.5, background_median + 3.0 * max(robust_sigma or 0.0, 1.0))
        if background_median is not None
        else warning_cpm
    )
    episodes = _hourly_episodes(points, relative_threshold)
    trend = _mann_kendall(daily_values)
    effective = _effective_sample_size(daily_values)
    bootstrap = _moving_block_bootstrap(daily_values)
    control = _daily_control_chart(daily_values)

    hourly_values = [float(point["mean_cpm"]) for point in points]
    hourly_mean = statistics.fmean(hourly_values) if hourly_values else None
    hourly_variance = statistics.variance(hourly_values) if len(hourly_values) > 1 else None
    overdispersion = (
        hourly_variance / hourly_mean
        if hourly_variance is not None and hourly_mean is not None and hourly_mean > 0
        else None
    )
    total_covered_seconds = sum(float(point["covered_seconds"]) for point in points)
    total_dose_available = any(bool(point.get("dose_available")) for point in points)
    total_dose = sum(float(point.get("dose_usv") or 0.0) for point in points) if total_dose_available else None
    annual_projection = None
    window_90d = windows["90d"]
    if window_90d["ready"] and window_90d["dose_usv"] is not None and float(window_90d["covered_days"]) > 0:
        annual_projection = float(window_90d["dose_usv"]) / float(window_90d["covered_days"]) * 365.25

    by_month_of_year: dict[int, list[float]] = defaultdict(list)
    for item in qualifying_daily:
        by_month_of_year[int(str(item["date"])[5:7])].append(float(item["median_cpm"]))
    seasonal = [
        {"month": month, "median_cpm": float(statistics.median(values)), "days": len(values)}
        for month, values in sorted(by_month_of_year.items())
        if values
    ]

    overall_coverage = min(100.0, 100.0 * total_covered_seconds / max(1.0, end_utc - start_utc))
    effective_value = float(effective.get("effective") or 0.0) if effective.get("available") else None
    trend_evidence = _evidence_level(
        duration_days=len(qualifying_daily),
        coverage_percent=overall_coverage,
        effective_samples=effective_value,
        minimum_days=MINIMUM_REQUIREMENTS["trend"]["days"],
        minimum_coverage=MINIMUM_REQUIREMENTS["trend"]["coverage_percent"],
        minimum_effective=MINIMUM_REQUIREMENTS["trend"]["effective_samples"],
    )
    trend["evidence"] = trend_evidence
    trend["effect"] = _trend_effect(trend.get("sen_slope_cpm_per_day"), background_median)
    represented_months = len(seasonal)
    seasonal_evidence = {
        "level": (
            "supported" if represented_months >= MINIMUM_REQUIREMENTS["seasonal_supported"]["months"]
            else "exploratory" if represented_months >= MINIMUM_REQUIREMENTS["seasonal_exploratory"]["months"]
            else "not_evaluable"
        ),
        "represented_months": represented_months,
        "minimum_exploratory_months": int(MINIMUM_REQUIREMENTS["seasonal_exploratory"]["months"]),
        "minimum_supported_months": int(MINIMUM_REQUIREMENTS["seasonal_supported"]["months"]),
    }
    control_evidence = _evidence_level(
        duration_days=len(qualifying_daily),
        coverage_percent=overall_coverage,
        minimum_days=MINIMUM_REQUIREMENTS["control_chart"]["days"],
        minimum_coverage=MINIMUM_REQUIREMENTS["trend"]["coverage_percent"],
    )
    control["evidence"] = control_evidence
    environment_temperature = _best_lagged_environment(points, "temperature_c")
    environment_pressure = _best_lagged_environment(points, "pressure_hpa")

    return {
        "available": True,
        "device_serial": device_serial,
        "generated_at_utc": int(datetime.now(UTC).timestamp()),
        "timezone": timezone.key,
        "start_utc": start_utc,
        "end_utc": end_utc,
        "span_days": max(0.0, (end_utc - start_utc) / 86400.0),
        "hourly_points": len(points),
        "daily_points": len(daily),
        "covered_days": total_covered_seconds / 86400.0,
        "coverage_percent": overall_coverage,
        "minimum_coverage_percent": minimum_coverage_percent,
        "windows": windows,
        "background": {
            "available": background_median is not None,
            "reference_days": len(background_values),
            "median_cpm": background_median,
            "mad_cpm": background_mad,
            "robust_sigma_cpm": robust_sigma,
            "p05_cpm": _quantile(background_values, 0.05),
            "p95_cpm": _quantile(background_values, 0.95),
            "recent_7d_median_cpm": recent_median,
            "recent_deviation_percent": deviation_percent,
            "relative_event_threshold_cpm": relative_threshold,
        },
        "trend": trend,
        "effective_sample_size": effective,
        "bootstrap": bootstrap,
        "control_chart": control,
        "overdispersion": {
            "available": overdispersion is not None,
            "fano_like_ratio": overdispersion,
            "contextual_only": True,
            "hourly_points": len(hourly_values),
        },
        "episodes": episodes,
        "dose": {
            "available": total_dose_available,
            "total_usv": total_dose,
            "covered_hours": total_covered_seconds / 3600.0,
            "annual_projection_usv": annual_projection,
            "projection_basis_days": 90 if annual_projection is not None else None,
            "derived": True,
        },
        "threshold_time": {
            "warning_cpm": warning_cpm,
            "danger_cpm": danger_cpm,
            "below_warning_hours": sum(
                float(point["covered_seconds"]) / 3600.0
                for point in points if float(point["mean_cpm"]) < warning_cpm
            ),
            "warning_hours": sum(
                float(point["covered_seconds"]) / 3600.0
                for point in points if warning_cpm <= float(point["mean_cpm"]) < danger_cpm
            ),
            "danger_hours": sum(
                float(point["covered_seconds"]) / 3600.0
                for point in points if float(point["mean_cpm"]) >= danger_cpm
            ),
        },
        "environment": {
            "temperature": environment_temperature,
            "pressure": environment_pressure,
        },
        "daily": daily[-730:],
        "calendar": daily[-366:],
        "monthly": monthly[-36:],
        "seasonal": seasonal,
        "seasonal_evidence": seasonal_evidence,
        "evidence_levels": {
            "trend": trend_evidence,
            "seasonal": seasonal_evidence,
            "control_chart": control_evidence,
            "environment_temperature": environment_temperature.get("evidence") or {},
            "environment_pressure": environment_pressure.get("evidence") or {},
        },
        "minimum_requirements": MINIMUM_REQUIREMENTS,
        "notes": {
            "dose_is_derived": True,
            "correlation_is_not_causation": True,
            "control_charts_are_contextual": True,
            "no_interpolation": True,
        },
    }


__all__ = ["build_long_term_analysis"]
