from __future__ import annotations

import itertools
import math
import statistics
from typing import Any

from .history import HistoryRow


def longest_gap_seconds(rows: list[HistoryRow]) -> int:
    if len(rows) < 2:
        return 0
    ordered = sorted(rows, key=lambda row: row.timestamp_utc)
    return max(
        int(current.timestamp_utc - previous.timestamp_utc)
        for previous, current in itertools.pairwise(ordered)
    )


def interval_diagnostics(rows: list[HistoryRow], scan_interval_seconds: int) -> dict[str, int]:
    ordered = sorted(rows, key=lambda row: row.timestamp_utc)
    timestamps = [row.timestamp_utc for row in ordered]
    duplicate_count = len(timestamps) - len(set(timestamps))
    short_count = 0
    long_count = 0
    for previous, current in itertools.pairwise(ordered):
        delta = current.timestamp_utc - previous.timestamp_utc
        if 0 < delta < scan_interval_seconds * 0.5:
            short_count += 1
        elif delta > scan_interval_seconds * 1.5:
            long_count += 1
    return {
        "duplicate_timestamps": duplicate_count,
        "short_intervals": short_count,
        "long_intervals": long_count,
    }


def data_quality_summary(
    rows: list[HistoryRow],
    *,
    expected_count: int,
    scan_interval_seconds: int,
    ingest_diagnostics: dict[str, int] | None = None,
    capabilities: dict[str, bool] | None = None,
) -> dict[str, Any]:
    completeness = min(100.0, 100.0 * len(rows) / expected_count) if expected_count else 0.0
    longest_gap = longest_gap_seconds(rows)
    interval = interval_diagnostics(rows, scan_interval_seconds)
    ingest = ingest_diagnostics or {}
    capabilities = capabilities or {"temperature": True, "voltage": True}

    optional_total = max(1, len(rows))
    temperature_coverage = 100.0 * sum(row.temperature_c is not None for row in rows) / optional_total
    voltage_coverage = 100.0 * sum(row.voltage_v is not None for row in rows) / optional_total

    score = completeness
    reasons: list[str] = []
    if completeness < 99.0:
        reasons.append(f"{completeness:.1f}% time-window coverage")
    if longest_gap > round(scan_interval_seconds * 1.5):
        score -= min(20.0, 4.0 + longest_gap / max(scan_interval_seconds, 1))
        reasons.append(f"longest gap {longest_gap} s")
    if interval["short_intervals"]:
        score -= min(8.0, interval["short_intervals"] * 0.5)
        reasons.append(f"{interval['short_intervals']} unusually short intervals")
    if interval["long_intervals"]:
        score -= min(10.0, interval["long_intervals"] * 0.5)
        reasons.append(f"{interval['long_intervals']} long intervals")

    duplicate_count = interval["duplicate_timestamps"] + int(ingest.get("duplicate_timestamp_count", 0))
    clock_regressions = int(ingest.get("clock_regression_count", 0))
    if duplicate_count:
        score -= min(12.0, duplicate_count * 2.0)
        reasons.append(f"{duplicate_count} duplicate timestamps observed")
    if clock_regressions:
        score -= min(20.0, clock_regressions * 5.0)
        reasons.append(f"{clock_regressions} clock regressions observed")

    if capabilities.get("temperature", False) and rows and temperature_coverage < 95.0:
        score -= min(8.0, (95.0 - temperature_coverage) / 10.0)
        reasons.append(f"temperature coverage {temperature_coverage:.1f}%")
    if capabilities.get("voltage", False) and rows and voltage_coverage < 95.0:
        score -= min(8.0, (95.0 - voltage_coverage) / 10.0)
        reasons.append(f"voltage coverage {voltage_coverage:.1f}%")

    score = max(0.0, min(100.0, score))
    if score >= 95.0:
        label = "Excellent"
    elif score >= 85.0:
        label = "Good"
    elif score >= 65.0:
        label = "Limited"
    else:
        label = "Poor"
    if not reasons:
        reasons.append("complete and regularly spaced data")

    return {
        "label": label,
        "score": score,
        "reasons": reasons,
        "completeness_percent": completeness,
        "longest_gap_seconds": longest_gap,
        "temperature_coverage_percent": temperature_coverage,
        "voltage_coverage_percent": voltage_coverage,
        "duplicate_timestamps": duplicate_count,
        "clock_regressions": clock_regressions,
        "short_intervals": interval["short_intervals"] + int(ingest.get("short_interval_count", 0)),
        "long_intervals": interval["long_intervals"] + int(ingest.get("long_interval_count", 0)),
    }


def baseline_drift_summary(rows: list[HistoryRow]) -> dict[str, Any]:
    if len(rows) < 4:
        return {
            "available": False,
            "percent": None,
            "first_half_mean": None,
            "second_half_mean": None,
        }
    ordered = sorted(rows, key=lambda row: row.timestamp_utc)
    midpoint = len(ordered) // 2
    first = [float(row.cpm) for row in ordered[:midpoint]]
    second = [float(row.cpm) for row in ordered[midpoint:]]
    first_mean = statistics.fmean(first)
    second_mean = statistics.fmean(second)
    percent = 100.0 * (second_mean - first_mean) / first_mean if first_mean > 0 else None
    return {
        "available": percent is not None,
        "percent": percent,
        "first_half_mean": first_mean,
        "second_half_mean": second_mean,
    }


def temperature_bin_summary(
    rows: list[HistoryRow], *, bin_width_c: float = 1.0
) -> list[dict[str, Any]]:
    bins: dict[float, list[float]] = {}
    for row in rows:
        if row.temperature_c is None:
            continue
        lower = math.floor(float(row.temperature_c) / bin_width_c) * bin_width_c
        bins.setdefault(lower, []).append(float(row.cpm))
    return [
        {
            "lower_c": lower,
            "upper_c": lower + bin_width_c,
            "samples": len(values),
            "mean_cpm": statistics.fmean(values),
            "median_cpm": statistics.median(values),
        }
        for lower, values in sorted(bins.items())
    ]
