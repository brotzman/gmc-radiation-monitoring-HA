from __future__ import annotations

import bisect
import math
import statistics
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from .history import HistoryRow

_REJECTED_QUALITY = {"rejected", "corrupt", "invalid", "pending"}


@dataclass(frozen=True)
class QualityFilterResult:
    rows: list[HistoryRow]
    raw_count: int
    rejected_count: int
    rejected_by_reason: dict[str, int]
    median_cpm: float | None
    mad_cpm: float | None
    robust_sigma_cpm: float | None

    @property
    def acceptance_percent(self) -> float:
        return 100.0 if self.raw_count == 0 else 100.0 * len(self.rows) / self.raw_count


@dataclass(frozen=True)
class PairingResult:
    pairs: list[tuple[HistoryRow, HistoryRow]]
    unmatched_a: int
    unmatched_b: int


@dataclass(frozen=True)
class FusedSeriesResult:
    rows: list[HistoryRow]
    paired_samples: int
    single_device_samples: int
    rejected_samples: int
    contributing_devices: tuple[str, ...]


def _median(values: Sequence[float]) -> float | None:
    return float(statistics.median(values)) if values else None


def _mad(values: Sequence[float], center: float) -> float:
    return float(statistics.median(abs(value - center) for value in values)) if values else 0.0


def robust_trimmed_mean(values: Iterable[float], *, trim_fraction: float = 0.10) -> float | None:
    ordered = sorted(float(value) for value in values if math.isfinite(float(value)))
    if not ordered:
        return None
    if len(ordered) < 5:
        return float(statistics.fmean(ordered))
    trim = min((len(ordered) - 1) // 2, int(len(ordered) * trim_fraction))
    kept = ordered[trim : len(ordered) - trim] if trim else ordered
    return float(statistics.fmean(kept))


def robust_sigma(values: Iterable[float]) -> float | None:
    finite = [float(value) for value in values if math.isfinite(float(value))]
    if len(finite) < 2:
        return None
    center = float(statistics.median(finite))
    mad = _mad(finite, center)
    # Poisson-like counting data still has a non-zero expected spread when MAD is zero.
    return max(1.0, 1.4826 * mad, math.sqrt(max(center, 1.0)) * 0.35)


def filter_history_rows(
    rows: Iterable[HistoryRow],
    *,
    purpose: str = "analysis",
    excluded_timestamps: Iterable[int] | None = None,
    timestamp_exclusion_seconds: int = 180,
) -> QualityFilterResult:
    """Return a robustly filtered series with an explainable rejection summary.

    ``baseline`` is intentionally strict so events and corrupt high values cannot be
    learned as normal background. ``comparison`` permits a confirmed, repeatedly
    observed high cluster; pair-level validation still requires agreement with the
    second device.
    """
    ordered = sorted(rows, key=lambda row: row.timestamp_utc)
    reasons: dict[str, int] = {}

    def reject(reason: str) -> None:
        reasons[reason] = reasons.get(reason, 0) + 1

    excluded = sorted(int(value) for value in (excluded_timestamps or ()))

    candidates: list[HistoryRow] = []
    for row in ordered:
        try:
            cpm = float(row.cpm)
        except (TypeError, ValueError):
            reject("invalid_value")
            continue
        if not math.isfinite(cpm) or cpm < 0 or cpm > 100_000_000:
            reject("invalid_value")
            continue
        if str(row.cpm_quality).strip().lower() in _REJECTED_QUALITY:
            reject("rejected_quality")
            continue
        if excluded:
            position = bisect.bisect_left(excluded, row.timestamp_utc)
            nearby = []
            if position < len(excluded):
                nearby.append(excluded[position])
            if position:
                nearby.append(excluded[position - 1])
            if any(abs(row.timestamp_utc - timestamp) <= timestamp_exclusion_seconds for timestamp in nearby):
                reject("operational_context")
                continue
        candidates.append(row)

    if len(candidates) < 5:
        values = [float(row.cpm) for row in candidates]
        center = _median(values)
        accepted = list(candidates)
        if center is not None and len(candidates) >= 3:
            # Even a short series can reject a single many-orders-of-magnitude spike.
            # A genuine sustained high level remains because its median is also high.
            small_sample_upper = max(center * 10.0, center + 500.0)
            accepted = []
            for row in candidates:
                if float(row.cpm) > small_sample_upper:
                    reject("robust_outlier")
                else:
                    accepted.append(row)
        accepted_values = [float(row.cpm) for row in accepted]
        accepted_center = _median(accepted_values)
        mad = _mad(accepted_values, accepted_center) if accepted_center is not None else None
        sigma = robust_sigma(accepted_values)
        return QualityFilterResult(
            accepted, len(ordered), len(ordered) - len(accepted), reasons, accepted_center, mad, sigma
        )

    values = [float(row.cpm) for row in candidates]
    center = float(statistics.median(values))
    mad = _mad(values, center)
    sigma = max(1.0, 1.4826 * mad, math.sqrt(max(center, 1.0)) * 0.35)
    sorted_values = sorted(values)

    if purpose == "baseline":
        sigma_multiplier = 8.0
        ratio_multiplier = 4.0
        absolute_margin = 50.0
    else:
        sigma_multiplier = 12.0
        ratio_multiplier = 8.0
        absolute_margin = 100.0

    upper_limit = max(center + sigma_multiplier * sigma, center * ratio_multiplier, center + absolute_margin)
    # A low CPM value can legitimately reach zero. Only discard impossible negatives above.
    accepted: list[HistoryRow] = []
    for row in candidates:
        value = float(row.cpm)
        if value <= upper_limit:
            accepted.append(row)
            continue

        # Comparison mode may retain a confirmed high cluster, but never a lone spike.
        supported_cluster = False
        if purpose == "comparison" and str(row.cpm_quality).lower() == "confirmed_high":
            lower = value * 0.85
            upper = value * 1.15
            cluster_count = bisect.bisect_right(sorted_values, upper) - bisect.bisect_left(
                sorted_values, lower
            )
            supported_cluster = cluster_count >= 3
        if supported_cluster:
            accepted.append(row)
        else:
            reject("robust_outlier")

    return QualityFilterResult(
        accepted,
        len(ordered),
        len(ordered) - len(accepted),
        reasons,
        center,
        mad,
        sigma,
    )


def pair_rows_one_to_one(
    rows_a: Iterable[HistoryRow], rows_b: Iterable[HistoryRow], *, tolerance_seconds: int
) -> PairingResult:
    a = sorted(rows_a, key=lambda row: row.timestamp_utc)
    b = sorted(rows_b, key=lambda row: row.timestamp_utc)
    pairs: list[tuple[HistoryRow, HistoryRow]] = []
    unmatched_a = 0
    unmatched_b = 0
    i = j = 0
    while i < len(a) and j < len(b):
        left = a[i]
        # Choose the closest not-yet-used B sample.
        if (
            j + 1 < len(b)
            and abs(b[j + 1].timestamp_utc - left.timestamp_utc)
            < abs(b[j].timestamp_utc - left.timestamp_utc)
            and b[j].timestamp_utc < left.timestamp_utc - tolerance_seconds
        ):
            unmatched_b += 1
            j += 1
            continue
        delta = b[j].timestamp_utc - left.timestamp_utc
        if abs(delta) <= tolerance_seconds:
            pairs.append((left, b[j]))
            i += 1
            j += 1
        elif delta < -tolerance_seconds:
            unmatched_b += 1
            j += 1
        else:
            unmatched_a += 1
            i += 1
    unmatched_a += len(a) - i
    unmatched_b += len(b) - j
    return PairingResult(pairs, unmatched_a, unmatched_b)


def filter_pair_outliers(
    pairs: Iterable[tuple[HistoryRow, HistoryRow]],
) -> tuple[list[tuple[HistoryRow, HistoryRow]], int]:
    candidates = list(pairs)
    if not candidates:
        return [], 0
    relative = [
        abs(float(a.cpm) - float(b.cpm)) / max(1.0, (float(a.cpm) + float(b.cpm)) / 2.0)
        for a, b in candidates
    ]
    center = float(statistics.median(relative))
    mad = _mad(relative, center)
    sigma = max(0.02, 1.4826 * mad)
    # Never allow a pair with >75% relative disagreement into the comparison.
    limit = min(0.75, max(0.25, center + 8.0 * sigma))
    accepted: list[tuple[HistoryRow, HistoryRow]] = []
    rejected = 0
    for pair, difference in zip(candidates, relative, strict=True):
        absolute = abs(float(pair[0].cpm) - float(pair[1].cpm))
        if difference > limit and absolute > 25.0:
            rejected += 1
        else:
            accepted.append(pair)
    return accepted, rejected


def fuse_device_rows(
    rows_by_serial: dict[str, Iterable[HistoryRow]],
    *,
    weights: dict[str, float] | None = None,
    tolerance_seconds: int = 90,
    include_single_device_samples: bool = True,
) -> FusedSeriesResult:
    """Build a quality-filtered measurement-site series from one or two devices."""
    weights = weights or {}
    # Materialize once because callers commonly pass lists but may also pass iterators.
    materialized = {serial: list(rows) for serial, rows in rows_by_serial.items()}
    serials = tuple(sorted(serial for serial, rows in materialized.items() if rows))
    if not serials:
        return FusedSeriesResult([], 0, 0, 0, ())

    filtered: dict[str, QualityFilterResult] = {
        serial: filter_history_rows(rows, purpose="baseline") for serial, rows in materialized.items() if rows
    }
    rejected = sum(result.rejected_count for result in filtered.values())
    if len(serials) == 1:
        serial = serials[0]
        rows = [
            HistoryRow(
                "site:single",
                row.timestamp_utc,
                int(row.cpm),
                row.temperature_c,
                row.voltage_v,
                None,
                None,
                None,
                "normal",
                pressure_hpa=row.pressure_hpa,
            )
            for row in filtered[serial].rows
        ]
        return FusedSeriesResult(rows, 0, len(rows), rejected, serials)

    a_serial, b_serial = serials[:2]
    a_rows = filtered[a_serial].rows
    b_rows = filtered[b_serial].rows
    pairing = pair_rows_one_to_one(a_rows, b_rows, tolerance_seconds=tolerance_seconds)
    valid_pairs, pair_rejected = filter_pair_outliers(pairing.pairs)
    rejected += pair_rejected
    wa = max(0.05, min(1.0, float(weights.get(a_serial, 1.0))))
    wb = max(0.05, min(1.0, float(weights.get(b_serial, 1.0))))

    fused: list[HistoryRow] = []
    paired_a_times: set[int] = set()
    paired_b_times: set[int] = set()
    for left, right in valid_pairs:
        paired_a_times.add(left.timestamp_utc)
        paired_b_times.add(right.timestamp_utc)
        cpm = round((float(left.cpm) * wa + float(right.cpm) * wb) / (wa + wb))
        temperatures = [
            (float(left.temperature_c), wa) if left.temperature_c is not None else None,
            (float(right.temperature_c), wb) if right.temperature_c is not None else None,
        ]
        temperatures = [item for item in temperatures if item is not None]
        temperature = (
            sum(value * weight for value, weight in temperatures) / sum(weight for _, weight in temperatures)
            if temperatures
            else None
        )
        pressures = [
            (float(left.pressure_hpa), wa) if left.pressure_hpa is not None else None,
            (float(right.pressure_hpa), wb) if right.pressure_hpa is not None else None,
        ]
        pressures = [item for item in pressures if item is not None]
        pressure = (
            sum(value * weight for value, weight in pressures) / sum(weight for _, weight in pressures)
            if pressures
            else None
        )
        fused.append(
            HistoryRow(
                "site:fused",
                round((left.timestamp_utc + right.timestamp_utc) / 2),
                cpm,
                temperature,
                None,
                None,
                None,
                None,
                "normal",
                pressure_hpa=pressure,
            )
        )

    single_count = 0
    if include_single_device_samples:
        # Single-device samples are retained as a reduced-confidence fallback. Samples
        # near a rejected mismatch are not reintroduced.
        valid_pair_ids = {(id(a), id(b)) for a, b in valid_pairs}
        rejected_pair_times_a = {
            a.timestamp_utc for a, b in pairing.pairs if (id(a), id(b)) not in valid_pair_ids
        }
        rejected_pair_times_b = {
            b.timestamp_utc for a, b in pairing.pairs if (id(a), id(b)) not in valid_pair_ids
        }
        for serial, rows, paired_times, rejected_times in (
            (a_serial, a_rows, paired_a_times, rejected_pair_times_a),
            (b_serial, b_rows, paired_b_times, rejected_pair_times_b),
        ):
            for row in rows:
                if row.timestamp_utc in paired_times or row.timestamp_utc in rejected_times:
                    continue
                fused.append(
                    HistoryRow(
                        f"site:single:{serial}",
                        row.timestamp_utc,
                        int(row.cpm),
                        row.temperature_c,
                        row.voltage_v,
                        None,
                        None,
                        None,
                        "normal",
                        pressure_hpa=row.pressure_hpa,
                    )
                )
                single_count += 1

    fused.sort(key=lambda row: row.timestamp_utc)
    return FusedSeriesResult(fused, len(valid_pairs), single_count, rejected, serials)
