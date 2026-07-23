from __future__ import annotations

import math
import statistics
from typing import Any

from .history import HistoryRow
from .time_series import time_weighted_summary


def percentile(values: list[float], percent: float) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    rank = (len(ordered) - 1) * percent
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[lower]
    weight = rank - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def pearson_correlation(pairs: list[tuple[float, float]]) -> tuple[float | None, str]:
    if len(pairs) < 2:
        return None, "insufficient paired samples"
    x_values = [pair[0] for pair in pairs]
    y_values = [pair[1] for pair in pairs]
    if len(set(x_values)) < 2:
        return None, "no CPM variation"
    if len(set(y_values)) < 2:
        return None, "no sensor variation"
    return statistics.correlation(x_values, y_values), "ok"


def build_statistics(
    rows: list[HistoryRow],
    *,
    expected_count: int,
    start_utc: int | None = None,
    end_utc: int | None = None,
    scan_interval_seconds: int | None = None,
) -> dict[str, Any]:
    """Build descriptive and time-aware statistics for a requested period.

    The arithmetic distribution statistics remain sample based, while the period
    mean and completeness become time based whenever explicit period boundaries
    and a sampling cadence are supplied. This prevents dense retry bursts from
    compensating for long gaps.
    """

    cpm_values = [float(row.cpm) for row in rows]
    sample_completeness = (
        min(100.0, 100.0 * len(rows) / expected_count) if expected_count else 0.0
    )
    weighted = None
    if (
        start_utc is not None
        and end_utc is not None
        and scan_interval_seconds is not None
        and end_utc > start_utc
    ):
        weighted = time_weighted_summary(
            rows,
            timestamp=lambda row: row.timestamp_utc,
            value=lambda row: row.cpm,
            start_utc=start_utc,
            end_utc=end_utc,
            expected_interval_seconds=scan_interval_seconds,
        )
    completeness = weighted.coverage_percent if weighted is not None else sample_completeness
    stats: dict[str, Any] = {
        "samples": len(rows),
        "expected_samples": expected_count,
        "missing_samples": max(0, expected_count - len(rows)),
        "completeness_percent": completeness,
        "time_coverage_percent": completeness if weighted is not None else None,
        "sample_completeness_percent": sample_completeness,
        "covered_seconds": weighted.covered_seconds if weighted is not None else None,
        "gap_seconds": weighted.gap_seconds if weighted is not None else None,
        "gap_count": weighted.gap_count if weighted is not None else None,
    }
    if not cpm_values:
        stats.update(
            {
                "cpm_min": None,
                "cpm_max": None,
                "cpm_mean": None,
                "cpm_median": None,
                "cpm_standard_deviation": None,
                "cpm_95th_percentile": None,
            }
        )
        return stats
    stats.update(
        {
            "cpm_min": min(cpm_values),
            "cpm_max": max(cpm_values),
            "cpm_mean": (
                weighted.mean
                if weighted is not None and weighted.available
                else statistics.fmean(cpm_values)
            ),
            "cpm_median": statistics.median(cpm_values),
            "cpm_standard_deviation": (
                statistics.stdev(cpm_values) if len(cpm_values) > 1 else 0.0
            ),
            "cpm_95th_percentile": percentile(cpm_values, 0.95),
        }
    )
    return stats
