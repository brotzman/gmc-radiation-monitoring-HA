from __future__ import annotations

import math
from collections.abc import Callable, Iterable
from dataclasses import dataclass
from itertools import pairwise
from typing import Any, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class TimeWeightedSummary:
    available: bool
    mean: float | None
    covered_seconds: float
    requested_seconds: float
    coverage_percent: float
    gap_seconds: float
    gap_count: int
    interval_count: int
    maximum_gap_seconds: float
    threshold_seconds: float | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "mean": self.mean,
            "covered_seconds": self.covered_seconds,
            "requested_seconds": self.requested_seconds,
            "coverage_percent": self.coverage_percent,
            "gap_seconds": self.gap_seconds,
            "gap_count": self.gap_count,
            "interval_count": self.interval_count,
            "maximum_gap_seconds": self.maximum_gap_seconds,
            "threshold_seconds": self.threshold_seconds,
        }


def _ordered_unique(
    rows: Iterable[T],
    *,
    timestamp: Callable[[T], int],
) -> list[T]:
    by_timestamp: dict[int, T] = {}
    for row in rows:
        by_timestamp[int(timestamp(row))] = row
    return [by_timestamp[key] for key in sorted(by_timestamp)]


def independent_count_windows(
    rows: Iterable[T],
    *,
    timestamp: Callable[[T], int],
    minimum_separation_seconds: int = 60,
) -> list[T]:
    """Select conservative non-overlapping approximately one-minute CPM windows.

    GMC CPM values are rolling/overlapping one-minute count rates when the bridge
    polls faster than once per minute. Treating every poll as an independent
    counting minute understates Poisson uncertainty. This selector keeps at most
    one row per minimum-separation interval while preserving the newest endpoint.
    """

    ordered = _ordered_unique(rows, timestamp=timestamp)
    if not ordered:
        return []
    separation = max(1, int(minimum_separation_seconds))
    selected: list[T] = [ordered[0]]
    last_timestamp = int(timestamp(ordered[0]))
    for row in ordered[1:]:
        current = int(timestamp(row))
        if current - last_timestamp >= separation:
            selected.append(row)
            last_timestamp = current
    if selected[-1] is not ordered[-1]:
        last = ordered[-1]
        if int(timestamp(last)) - int(timestamp(selected[-1])) >= max(1, separation // 2):
            selected.append(last)
    return selected


def time_weighted_summary(
    rows: Iterable[T],
    *,
    timestamp: Callable[[T], int],
    value: Callable[[T], float | int | None],
    start_utc: int,
    end_utc: int,
    expected_interval_seconds: int,
    maximum_gap_factor: float = 1.5,
    threshold: float | None = None,
) -> TimeWeightedSummary:
    """Integrate a rate over observed time without bridging material data gaps.

    Values are trapezoid-integrated between adjacent observations. Intervals
    longer than ``maximum_gap_factor`` times the expected cadence are classified
    as gaps and excluded. Boundary support is limited to half one expected cadence
    so dense bursts cannot compensate for long missing periods.
    """

    start = int(start_utc)
    end = int(end_utc)
    requested = max(0.0, float(end - start))
    if end <= start:
        raise ValueError("end_utc must be greater than start_utc")
    ordered = [
        row
        for row in _ordered_unique(rows, timestamp=timestamp)
        if start <= int(timestamp(row)) <= end and value(row) is not None
    ]
    if not ordered:
        return TimeWeightedSummary(False, None, 0.0, requested, 0.0, requested, 0, 0, 0.0, None)

    cadence = max(1.0, float(expected_interval_seconds))
    maximum_gap = max(cadence, cadence * max(1.0, float(maximum_gap_factor)))
    weighted_sum = 0.0
    covered = 0.0
    threshold_seconds = 0.0 if threshold is not None else None
    gap_seconds = 0.0
    gap_count = 0
    interval_count = 0

    if len(ordered) == 1:
        support = min(cadence, requested)
        sample_value = float(value(ordered[0]))
        covered = support
        weighted_sum = sample_value * support
        if threshold_seconds is not None and sample_value >= float(threshold):
            threshold_seconds = support
    else:
        for left, right in pairwise(ordered):
            left_ts = int(timestamp(left))
            right_ts = int(timestamp(right))
            raw_dt = right_ts - left_ts
            if raw_dt <= 0:
                continue
            clipped_start = max(start, left_ts)
            clipped_end = min(end, right_ts)
            dt = clipped_end - clipped_start
            if dt <= 0:
                continue
            if raw_dt > maximum_gap:
                gap_count += 1
                gap_seconds += float(dt)
                continue
            left_value = float(value(left))
            right_value = float(value(right))
            mean_value = (left_value + right_value) / 2.0
            weighted_sum += mean_value * dt
            covered += dt
            interval_count += 1
            if threshold_seconds is not None:
                level = float(threshold)
                if left_value >= level and right_value >= level:
                    threshold_seconds += dt
                elif (left_value - level) * (right_value - level) < 0:
                    fraction = abs((level - left_value) / (right_value - left_value))
                    threshold_seconds += dt * (1.0 - fraction if left_value < level else fraction)

        # Give the first and last point no more than half a cadence of endpoint
        # support. This avoids the common 98.3% artefact for exact hourly windows
        # without allowing a burst of measurements to hide a long outage.
        endpoint_half = cadence / 2.0
        first = ordered[0]
        last = ordered[-1]
        first_support = max(0.0, min(endpoint_half, int(timestamp(first)) - start))
        last_support = max(0.0, min(endpoint_half, end - int(timestamp(last))))
        for row, support in ((first, first_support), (last, last_support)):
            if support <= 0:
                continue
            sample_value = float(value(row))
            weighted_sum += sample_value * support
            covered += support
            if threshold_seconds is not None and sample_value >= float(threshold):
                threshold_seconds += support

    covered = min(requested, covered)
    gap_seconds = max(gap_seconds, requested - covered)
    mean = weighted_sum / covered if covered > 0 else None
    coverage = 100.0 * covered / requested if requested > 0 else 0.0
    return TimeWeightedSummary(
        available=mean is not None and math.isfinite(mean),
        mean=mean,
        covered_seconds=covered,
        requested_seconds=requested,
        coverage_percent=max(0.0, min(100.0, coverage)),
        gap_seconds=max(0.0, gap_seconds),
        gap_count=gap_count,
        interval_count=interval_count,
        maximum_gap_seconds=maximum_gap,
        threshold_seconds=threshold_seconds,
    )
