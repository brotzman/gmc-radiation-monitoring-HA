from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from typing import Any

ALGORITHM_VERSION = "8.3-metrology-1"


@dataclass(frozen=True)
class MetrologyConfig:
    dead_time_us: float | None = None
    reliable_max_cpm: int | None = None
    dead_time_model: str = "none"  # none | nonparalyzable
    conversion_factor_uncertainty_percent: float | None = None
    calibration_uncertainty_percent: float | None = None
    calibration_reference: str = ""
    tube_model: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def assess_count_rate(cpm: float, config: MetrologyConfig) -> dict[str, Any]:
    measured = max(0.0, float(cpm))
    reliable = config.reliable_max_cpm
    saturation = reliable is not None and measured > reliable
    corrected: float | None = None
    correction_applied = False
    correction_reason = "not configured"

    if config.dead_time_model == "nonparalyzable" and config.dead_time_us is not None:
        tau = config.dead_time_us / 1_000_000.0
        measured_hz = measured / 60.0
        denominator = 1.0 - measured_hz * tau
        if denominator > 0 and not saturation:
            corrected = measured / denominator
            correction_applied = True
            correction_reason = "nonparalyzable dead-time correction"
        elif denominator <= 0:
            saturation = True
            correction_reason = "dead-time model singularity"
        else:
            correction_reason = "outside reliable range"

    return {
        "measured_cpm": measured,
        "reliable_max_cpm": reliable,
        "dead_time_us": config.dead_time_us,
        "dead_time_model": config.dead_time_model,
        "possible_saturation_or_count_loss": saturation,
        "dose_rate_display_allowed": not saturation,
        "corrected_cpm": corrected,
        "correction_applied": correction_applied,
        "correction_reason": correction_reason,
    }


def uncertainty_budget(
    *,
    counting_relative_percent: float | None,
    config: MetrologyConfig,
) -> dict[str, Any]:
    components = {
        "counting_statistics_percent": counting_relative_percent,
        "conversion_factor_percent": config.conversion_factor_uncertainty_percent,
        "calibration_percent": config.calibration_uncertainty_percent,
    }
    known = [float(v) for v in components.values() if v is not None]
    complete = all(value is not None for value in components.values())
    combined = math.sqrt(sum(value * value for value in known)) if complete else None
    return {
        "components": components,
        "complete": complete,
        "combined_standard_uncertainty_percent": combined,
        "statement": (
            f"Combined standard uncertainty: {combined:.2f}%"
            if combined is not None
            else "Total uncertainty cannot be determined because one or more components are unknown"
        ),
    }


def derived_dose_estimate(
    *,
    cpm: float | None,
    cpm_per_usvh: float,
    counting_relative_percent: float | None,
    config: MetrologyConfig,
    coverage_percent: float | None = None,
    gap_count: int | None = None,
) -> dict[str, Any]:
    if cpm is None or cpm_per_usvh <= 0:
        return {"available": False, "label": "Derived dose estimate", "value_usvh": None}
    rate = assess_count_rate(cpm, config)
    budget = uncertainty_budget(counting_relative_percent=counting_relative_percent, config=config)
    effective_cpm = rate["corrected_cpm"] if rate["correction_applied"] else float(cpm)
    value = None if not rate["dose_rate_display_allowed"] else effective_cpm / float(cpm_per_usvh)
    return {
        "available": value is not None,
        "label": "Derived dose estimate",
        "value_usvh": value,
        "primary_measurement_cpm": float(cpm),
        "effective_cpm_for_conversion": effective_cpm if value is not None else None,
        "metrology": rate,
        "uncertainty_budget": budget,
        "coverage_percent": coverage_percent,
        "gap_count": gap_count,
        "calibration_traceable": bool(config.calibration_reference.strip()),
        "qualification": "derived estimate; not a traceably calibrated dose measurement",
    }


def integrated_dose_estimate(
    *,
    samples: list[tuple[int, float]],
    cpm_per_usvh: float,
    config: MetrologyConfig,
    expected_interval_seconds: int,
) -> dict[str, Any]:
    """Integrate qualified dose-rate estimates over covered intervals only.

    Intervals longer than 1.5 times the expected cadence are reported as gaps and
    are not silently bridged. Saturated endpoints invalidate the respective interval.
    """
    ordered = sorted((int(ts), float(cpm)) for ts, cpm in samples)
    dose_usv = 0.0
    covered_seconds = 0
    gap_seconds = 0
    gap_count = 0
    saturated_intervals = 0
    max_interval = max(1, int(expected_interval_seconds * 1.5))
    for (ts0, cpm0), (ts1, cpm1) in zip(ordered, ordered[1:]):
        dt = ts1 - ts0
        if dt <= 0:
            continue
        if dt > max_interval:
            gap_count += 1
            gap_seconds += dt
            continue
        r0 = assess_count_rate(cpm0, config)
        r1 = assess_count_rate(cpm1, config)
        if not r0["dose_rate_display_allowed"] or not r1["dose_rate_display_allowed"]:
            saturated_intervals += 1
            continue
        e0 = r0["corrected_cpm"] if r0["correction_applied"] else cpm0
        e1 = r1["corrected_cpm"] if r1["correction_applied"] else cpm1
        mean_usvh = ((e0 + e1) / 2.0) / cpm_per_usvh
        dose_usv += mean_usvh * (dt / 3600.0)
        covered_seconds += dt
    total_span = ordered[-1][0] - ordered[0][0] if len(ordered) >= 2 else 0
    coverage = (covered_seconds / total_span * 100.0) if total_span > 0 else None
    return {
        "available": covered_seconds > 0,
        "label": "Derived integrated dose estimate",
        "value_usv": dose_usv if covered_seconds > 0 else None,
        "qualification": "derived estimate; not a traceably calibrated dose measurement",
        "covered_seconds": covered_seconds,
        "total_span_seconds": total_span,
        "coverage_percent": coverage,
        "gap_count": gap_count,
        "gap_seconds": gap_seconds,
        "excluded_saturated_intervals": saturated_intervals,
        "calibration_traceable": bool(config.calibration_reference.strip()),
    }
