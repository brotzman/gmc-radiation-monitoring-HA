from __future__ import annotations

import itertools
import math
import statistics
import time
from dataclasses import dataclass
from typing import Any

from .history import HistoryRow, HistoryStore
from .quality_pipeline import (
    filter_history_rows,
    filter_pair_outliers,
    pair_rows_one_to_one,
    robust_trimmed_mean,
)
from .scientific_analysis import relative_device_response


@dataclass(frozen=True)
class DeviceStability:
    serial: str
    label: str
    score: float
    status: str
    availability_percent: float
    samples: int
    expected_samples: int
    longest_gap_seconds: int
    serial_errors: int
    reconnects: int
    last_sample_age_seconds: int | None
    valid_samples: int = 0
    excluded_samples: int = 0
    quality_weight: float = 0.0
    scan_interval_seconds: int = 60
    gap_status: str | None = None
    total_stored_samples: int = 0
    analysis_window_seconds: int = 86400
    interval_deviation_seconds: int | None = None


def measurement_gap_status(longest_gap_seconds: int, scan_interval_seconds: int) -> str | None:
    """Classify a measurement gap relative to the configured device interval."""
    interval = max(1, int(scan_interval_seconds))
    gap = max(0, int(longest_gap_seconds))
    if gap >= interval * 2.5:
        return "Critical"
    if gap >= interval * 1.5:
        return "Warning"
    return None


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 10 or len(xs) != len(ys):
        return None
    mean_x, mean_y = statistics.fmean(xs), statistics.fmean(ys)
    dx = [value - mean_x for value in xs]
    dy = [value - mean_y for value in ys]
    denominator = math.sqrt(sum(value * value for value in dx) * sum(value * value for value in dy))
    return None if denominator == 0 else sum(a * b for a, b in zip(dx, dy, strict=False)) / denominator


def _longest_gap(rows: list[HistoryRow]) -> int:
    return max((later.timestamp_utc - earlier.timestamp_utc for earlier, later in itertools.pairwise(rows)), default=0)


def _orientation_timestamps(store: HistoryStore, serial: str) -> list[int]:
    return [
        int(event["timestamp_utc"])
        for event in store.recent_operational_events(limit=200, device_serial=serial)
        if event.get("event_type") == "orientation_changed"
    ]


def _comparison_confidence(valid_pairs: int, excluded_pairs: int, weights: list[float]) -> str:
    if valid_pairs < 10:
        return "Insufficient"
    acceptance = valid_pairs / max(1, valid_pairs + excluded_pairs)
    minimum_weight = min(weights) if weights else 0.0
    if valid_pairs >= 30 and acceptance >= 0.9 and minimum_weight >= 0.8:
        return "High"
    if valid_pairs >= 20 and acceptance >= 0.75 and minimum_weight >= 0.6:
        return "Medium"
    return "Low"


def build_fleet_snapshot(store: HistoryStore, *, window_seconds: int = 86400) -> dict[str, Any]:
    now = int(time.time())
    # Use an exact half-open interval [start, end).  With integer timestamps,
    # end=now+1 includes a sample stored in the current second while excluding
    # the sample exactly one full window earlier.  This prevents a regular
    # 120-second series from alternating between 720 and 721 samples.
    end = now + 1
    start = end - window_seconds
    devices = [item for item in store.list_devices() if bool(item.get("runtime_online"))]
    stability: list[DeviceStability] = []
    rows_by_serial: dict[str, list[HistoryRow]] = {}
    filtered_by_serial: dict[str, list[HistoryRow]] = {}
    weights_by_serial: dict[str, float] = {}
    filter_summaries: dict[str, dict[str, Any]] = {}

    for device in devices:
        serial = str(device.get("serial") or "")
        rows = store.query_range(start, end, device_serial=serial)
        rows_by_serial[serial] = rows
        orientation_times = _orientation_timestamps(store, serial)
        filtered = filter_history_rows(
            rows,
            purpose="comparison",
            excluded_timestamps=orientation_times,
            timestamp_exclusion_seconds=180,
        )
        clean_rows = filtered.rows
        filtered_by_serial[serial] = clean_rows
        filter_summaries[serial] = {
            "raw": filtered.raw_count,
            "valid": len(clean_rows),
            "excluded": filtered.rejected_count,
            "reasons": dict(filtered.rejected_by_reason),
        }
        interval = max(1, int(float(device.get("scan_interval_seconds") or 60)))
        observed_seconds = window_seconds
        if rows:
            observed_seconds = max(interval, min(window_seconds, now - rows[0].timestamp_utc + interval))
        expected = max(1, observed_seconds // interval)
        availability = min(100.0, 100.0 * len(clean_rows) / expected)
        errors = int(device.get("serial_error_count") or 0)
        reconnects = int(device.get("serial_reconnect_count") or 0)
        gap = _longest_gap(clean_rows)
        interval_deviation = None if len(clean_rows) < 2 else gap - interval
        age = None if not clean_rows else max(0, now - clean_rows[-1].timestamp_utc)
        score = 100.0
        score -= min(35.0, (100.0 - availability) * 0.6)
        score -= min(25.0, errors * 4.0)
        score -= min(20.0, reconnects * 6.0)
        if gap > interval * 3:
            score -= min(20.0, (gap / (interval * 3) - 1.0) * 8.0)
        rejection_percent = 100.0 * filtered.rejected_count / max(1, filtered.raw_count)
        score -= min(20.0, rejection_percent * 0.5)
        score = max(0.0, min(100.0, score))
        status = "Stable" if score >= 90 else "Slightly noticeable" if score >= 75 else "Unstable" if score >= 45 else "Critical"
        freshness = 0.0 if age is None else max(0.0, 1.0 - age / max(interval * 6.0, 300.0))
        acceptance = len(clean_rows) / max(1, len(rows))
        quality_weight = max(0.0, min(1.0, (score / 100.0) * (availability / 100.0) * acceptance * freshness))
        weights_by_serial[serial] = quality_weight
        stability.append(DeviceStability(
            serial=serial,
            label=str(device.get("device_model") or device.get("configured_name") or serial),
            score=score,
            status=status,
            availability_percent=availability,
            samples=len(rows),
            expected_samples=expected,
            longest_gap_seconds=gap,
            serial_errors=errors,
            reconnects=reconnects,
            last_sample_age_seconds=age,
            valid_samples=len(clean_rows),
            excluded_samples=filtered.rejected_count,
            quality_weight=quality_weight,
            scan_interval_seconds=interval,
            gap_status=measurement_gap_status(gap, interval),
            total_stored_samples=int(device.get("stored_samples") or 0),
            analysis_window_seconds=window_seconds,
            interval_deviation_seconds=interval_deviation,
        ))

    comparison: dict[str, Any] | None = None
    shared_event: dict[str, Any] | None = None
    relative_calibration: dict[str, Any] | None = None
    if len(devices) >= 2:
        first, second = devices[:2]
        first_serial = str(first["serial"])
        second_serial = str(second["serial"])
        first_rows = filtered_by_serial[first_serial]
        second_rows = filtered_by_serial[second_serial]
        tolerance = max(
            int(float(first.get("scan_interval_seconds") or 60)),
            int(float(second.get("scan_interval_seconds") or 60)),
        )
        pairing = pair_rows_one_to_one(first_rows, second_rows, tolerance_seconds=tolerance)
        valid_pairs, pair_outliers = filter_pair_outliers(pairing.pairs)
        excluded_measurements = (
            filter_summaries[first_serial]["excluded"]
            + filter_summaries[second_serial]["excluded"]
        )
        excluded_pairs = pair_outliers
        if valid_pairs or pairing.pairs:
            xs = [float(left.cpm) for left, _ in valid_pairs]
            ys = [float(right.cpm) for _, right in valid_pairs]
            differences = [abs(left - right) for left, right in zip(xs, ys, strict=True)]
            relative_differences = [
                abs(left - right) / max(1.0, (left + right) / 2.0)
                for left, right in zip(xs, ys, strict=True)
            ]
            correlation = _pearson(xs, ys)
            median_relative = statistics.median(relative_differences) if relative_differences else 1.0
            agreement = max(0.0, 100.0 - median_relative * 100.0)
            confidence = _comparison_confidence(
                len(valid_pairs), pair_outliers,
                [weights_by_serial.get(first_serial, 0.0), weights_by_serial.get(second_serial, 0.0)],
            )
            last_pair = valid_pairs[-1] if valid_pairs else None
            first_hour = [float(row.cpm) for row in first_rows if row.timestamp_utc >= now - 3600]
            second_hour = [float(row.cpm) for row in second_rows if row.timestamp_utc >= now - 3600]
            comparison = {
                "a_label": str(first.get("device_model") or first["serial"]),
                "b_label": str(second.get("device_model") or second["serial"]),
                "a_serial": first_serial,
                "b_serial": second_serial,
                "pairs": len(valid_pairs),
                "candidate_pairs": len(pairing.pairs),
                "excluded_pairs": excluded_pairs,
                "excluded_measurements": excluded_measurements,
                "pair_outliers": pair_outliers,
                "unmatched_a": pairing.unmatched_a,
                "unmatched_b": pairing.unmatched_b,
                "correlation": correlation,
                "correlation_available": correlation is not None,
                "minimum_pairs_for_correlation": 10,
                "confidence": confidence,
                "mean_difference": robust_trimmed_mean(differences) or 0.0,
                "agreement_percent": agreement,
                "current_difference": (
                    float(last_pair[0].cpm) - float(last_pair[1].cpm)
                    if last_pair else None
                ),
                "a_current_cpm": float(last_pair[0].cpm) if last_pair else None,
                "b_current_cpm": float(last_pair[1].cpm) if last_pair else None,
                "a_mean_1h": robust_trimmed_mean(first_hour),
                "b_mean_1h": robust_trimmed_mean(second_hour),
                "quality_filtered": True,
            }

            recent_first = [float(row.cpm) for row in first_rows if row.timestamp_utc >= now - 900]
            recent_second = [float(row.cpm) for row in second_rows if row.timestamp_utc >= now - 900]
            baseline_first = [float(row.cpm) for row in first_rows if now - 21600 <= row.timestamp_utc < now - 900]
            baseline_second = [float(row.cpm) for row in second_rows if now - 21600 <= row.timestamp_utc < now - 900]
            recent_level_first = robust_trimmed_mean(recent_first)
            recent_level_second = robust_trimmed_mean(recent_second)
            baseline_level_first = statistics.median(baseline_first) if len(baseline_first) >= 6 else None
            baseline_level_second = statistics.median(baseline_second) if len(baseline_second) >= 6 else None
            if all(value is not None for value in (recent_level_first, recent_level_second, baseline_level_first, baseline_level_second)):
                first_change = (recent_level_first / baseline_level_first - 1.0) * 100.0 if baseline_level_first else 0.0
                second_change = (recent_level_second / baseline_level_second - 1.0) * 100.0 if baseline_level_second else 0.0
                active = (
                    len(valid_pairs) >= 10
                    and confidence != "Insufficient"
                    and first_change >= 30.0
                    and second_change >= 30.0
                )
                shared_event = {
                    "active": active,
                    "a_change_percent": first_change,
                    "b_change_percent": second_change,
                    "confidence": "High" if active and correlation is not None and correlation >= 0.5 else "Low",
                    "quality_filtered": True,
                }

    if len(devices) >= 2:
        first, second = devices[:2]
        first_serial = str(first["serial"])
        second_serial = str(second["serial"])
        learning_start = now - 30 * 86400
        first_orientation_times = [
            int(event["timestamp_utc"])
            for event in store.recent_operational_events(limit=500, device_serial=first_serial)
            if event.get("event_type") == "orientation_changed" and int(event.get("timestamp_utc") or 0) >= learning_start
        ]
        second_orientation_times = [
            int(event["timestamp_utc"])
            for event in store.recent_operational_events(limit=500, device_serial=second_serial)
            if event.get("event_type") == "orientation_changed" and int(event.get("timestamp_utc") or 0) >= learning_start
        ]
        first_long = filter_history_rows(
            store.query_range(learning_start, now + 1, device_serial=first_serial),
            purpose="comparison",
            excluded_timestamps=first_orientation_times,
            timestamp_exclusion_seconds=180,
        ).rows
        second_long = filter_history_rows(
            store.query_range(learning_start, now + 1, device_serial=second_serial),
            purpose="comparison",
            excluded_timestamps=second_orientation_times,
            timestamp_exclusion_seconds=180,
        ).rows
        tolerance = max(
            int(float(first.get("scan_interval_seconds") or 60)),
            int(float(second.get("scan_interval_seconds") or 60)),
        )
        long_pairing = pair_rows_one_to_one(first_long, second_long, tolerance_seconds=tolerance)
        long_pairs, long_outliers = filter_pair_outliers(long_pairing.pairs)
        first_capabilities = str(first.get("capabilities") or "")
        second_capabilities = str(second.get("capabilities") or "")
        orientation_verified = "gyro" in first_capabilities.split(",") and "gyro" in second_capabilities.split(",")
        relative_calibration = relative_device_response(
            long_pairs,
            orientation_changes=len(first_orientation_times) + len(second_orientation_times),
            orientation_verified=orientation_verified,
        )
        relative_calibration.update({
            "a_label": str(first.get("device_model") or first_serial),
            "b_label": str(second.get("device_model") or second_serial),
            "a_serial": first_serial,
            "b_serial": second_serial,
            "candidate_pairs": len(long_pairing.pairs),
            "pair_outliers": long_outliers,
        })

    orientation_events: list[dict[str, Any]] = []
    for device in devices:
        serial = str(device["serial"])
        for event in store.recent_operational_events(limit=20, device_serial=serial):
            if event.get("event_type") == "orientation_changed":
                orientation_events.append({"serial": serial, "label": str(device.get("device_model") or serial), **event})
    orientation_events.sort(key=lambda event: event["timestamp_utc"], reverse=True)
    return {
        "generated_at_utc": now,
        "stability": stability,
        "comparison": comparison,
        "relative_calibration": relative_calibration,
        "shared_event": shared_event,
        "orientation_events": orientation_events[:10],
        "device_weights": weights_by_serial,
        "filter_summaries": filter_summaries,
    }
