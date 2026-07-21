from __future__ import annotations

import math
from dataclasses import asdict, dataclass
from itertools import pairwise
from typing import Any

ALGORITHM_VERSION = "8.3-metrology-2"


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


@dataclass(frozen=True)
class TubeMetrologyProfile:
    """Calibration and count-rate model for one physical GM tube."""

    tube_model: str = ""
    cpm_per_usvh: float | None = None
    dead_time_us: float | None = None
    reliable_max_cpm: int | None = None
    dead_time_model: str = "none"
    conversion_factor_uncertainty_percent: float | None = None
    calibration_uncertainty_percent: float | None = None
    calibration_reference: str = ""

    def metrology_config(self) -> MetrologyConfig:
        return MetrologyConfig(
            dead_time_us=self.dead_time_us,
            reliable_max_cpm=self.reliable_max_cpm,
            dead_time_model=self.dead_time_model,
            conversion_factor_uncertainty_percent=self.conversion_factor_uncertainty_percent,
            calibration_uncertainty_percent=self.calibration_uncertainty_percent,
            calibration_reference=self.calibration_reference,
            tube_model=self.tube_model,
        )

    @property
    def dose_calibrated(self) -> bool:
        return self.cpm_per_usvh is not None and self.cpm_per_usvh > 0

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DualTubeMetrologyConfig:
    """Piecewise or channel-specific calibration for dual-tube counters.

    ``separate`` uses the device's low- and high-dose tube CPM channels.
    ``curve`` applies a piecewise profile to the primary CPM channel.
    ``single`` retains the legacy single-profile behaviour.
    """

    mode: str = "single"  # single | separate | curve
    switch_cpm: int | None = None
    low_dose: TubeMetrologyProfile | None = None
    high_dose: TubeMetrologyProfile | None = None

    def as_dict(self) -> dict[str, Any]:
        return {
            "mode": self.mode,
            "switch_cpm": self.switch_cpm,
            "low_dose": self.low_dose.as_dict() if self.low_dose else None,
            "high_dose": self.high_dose.as_dict() if self.high_dose else None,
        }


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
        return {
            "available": False,
            "label": "Derived dose estimate",
            "value_usvh": None,
            "reason": "missing count rate or conversion factor",
        }
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
        "reason": None if value is not None else rate["correction_reason"],
    }


def _profile_estimate(
    *,
    cpm: float | None,
    profile: TubeMetrologyProfile | None,
    counting_relative_percent: float | None,
) -> dict[str, Any]:
    if profile is None:
        return {
            "available": False,
            "value_usvh": None,
            "reason": "tube profile is not configured",
            "profile": None,
        }
    if not profile.dose_calibrated:
        return {
            "available": False,
            "value_usvh": None,
            "reason": "tube conversion factor is not configured",
            "profile": profile.as_dict(),
            "primary_measurement_cpm": cpm,
        }
    result = derived_dose_estimate(
        cpm=cpm,
        cpm_per_usvh=float(profile.cpm_per_usvh),
        counting_relative_percent=counting_relative_percent,
        config=profile.metrology_config(),
    )
    result["profile"] = profile.as_dict()
    return result


def derived_dual_tube_dose_estimate(
    *,
    primary_cpm: float | None,
    low_cpm: float | None,
    high_cpm: float | None,
    counting_relative_percent: float | None,
    config: DualTubeMetrologyConfig,
) -> dict[str, Any]:
    """Return one qualified dose estimate without double-counting both tubes."""

    low_result = _profile_estimate(
        cpm=low_cpm,
        profile=config.low_dose,
        counting_relative_percent=counting_relative_percent,
    )
    high_result = _profile_estimate(
        cpm=high_cpm,
        profile=config.high_dose,
        counting_relative_percent=counting_relative_percent,
    )
    selected_tube: str | None = None
    selection_reason = "dual-tube mode is not configured"

    if config.mode == "curve":
        if primary_cpm is None:
            selection_reason = "primary CPM is unavailable"
        elif config.switch_cpm is None:
            selection_reason = "dual-tube curve switch is not configured"
        else:
            selected_tube = "high" if primary_cpm > config.switch_cpm else "low"
            selection_reason = "piecewise primary-CPM calibration curve"
            selected_profile = config.high_dose if selected_tube == "high" else config.low_dose
            selected_result = _profile_estimate(
                cpm=primary_cpm,
                profile=selected_profile,
                counting_relative_percent=counting_relative_percent,
            )
            if selected_tube == "low":
                low_result = selected_result
            else:
                high_result = selected_result
    elif config.mode == "separate":
        low_reliable_max = config.low_dose.reliable_max_cpm if config.low_dose else None
        threshold = low_reliable_max or config.switch_cpm
        if low_cpm is None and high_cpm is not None:
            selected_tube = "high"
            selection_reason = "only the high-dose tube channel is available"
        elif low_cpm is not None:
            if threshold is not None and low_cpm > threshold:
                selected_tube = "high"
                selection_reason = "low-dose tube exceeded its configured reliable range"
            else:
                selected_tube = "low"
                selection_reason = "low-dose tube is within its configured reliable range"
        elif high_cpm is not None:
            selected_tube = "high"
            selection_reason = "only the high-dose tube channel is available"
        else:
            selection_reason = "no dual-tube CPM channels are available"
    elif config.mode == "single":
        selection_reason = "single-tube mode uses the legacy primary calibration"
    else:
        selection_reason = "unsupported dual-tube mode"

    selected_result = low_result if selected_tube == "low" else high_result if selected_tube == "high" else None
    available = bool(selected_result and selected_result.get("available"))
    reason = None if available else (
        str(selected_result.get("reason")) if selected_result else selection_reason
    )
    return {
        "available": available,
        "label": "Derived dual-tube dose estimate",
        "value_usvh": selected_result.get("value_usvh") if available and selected_result else None,
        "selected_tube": selected_tube,
        "selection_reason": selection_reason,
        "reason": reason,
        "mode": config.mode,
        "switch_cpm": config.switch_cpm,
        "primary_measurement_cpm": primary_cpm,
        "tube_measurements_cpm": {"low": low_cpm, "high": high_cpm},
        "tube_results": {"low": low_result, "high": high_result},
        "calibration_traceable": bool(
            selected_result and selected_result.get("calibration_traceable")
        ),
        "qualification": "derived estimate from a selected dual-tube calibration profile",
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
    for (ts0, cpm0), (ts1, cpm1) in pairwise(ordered):
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


def integrated_dual_tube_dose_estimate(
    *,
    samples: list[tuple[int, float | None, float | None, float | None]],
    config: DualTubeMetrologyConfig,
    expected_interval_seconds: int,
) -> dict[str, Any]:
    """Integrate a dual-tube estimate while preserving gaps and invalid ranges."""

    ordered = sorted((int(ts), primary, low, high) for ts, primary, low, high in samples)
    dose_usv = 0.0
    covered_seconds = 0
    gap_seconds = 0
    gap_count = 0
    excluded_intervals = 0
    profile_switches = 0
    max_interval = max(1, int(expected_interval_seconds * 1.5))
    previous_tube: str | None = None

    for first, second in pairwise(ordered):
        ts0, primary0, low0, high0 = first
        ts1, primary1, low1, high1 = second
        dt = ts1 - ts0
        if dt <= 0:
            continue
        if dt > max_interval:
            gap_count += 1
            gap_seconds += dt
            continue
        result0 = derived_dual_tube_dose_estimate(
            primary_cpm=primary0,
            low_cpm=low0,
            high_cpm=high0,
            counting_relative_percent=None,
            config=config,
        )
        result1 = derived_dual_tube_dose_estimate(
            primary_cpm=primary1,
            low_cpm=low1,
            high_cpm=high1,
            counting_relative_percent=None,
            config=config,
        )
        if not result0["available"] or not result1["available"]:
            excluded_intervals += 1
            continue
        tube0 = result0.get("selected_tube")
        tube1 = result1.get("selected_tube")
        if previous_tube is not None and tube0 != previous_tube:
            profile_switches += 1
        if tube0 != tube1:
            profile_switches += 1
        previous_tube = tube1
        mean_usvh = (float(result0["value_usvh"]) + float(result1["value_usvh"])) / 2.0
        dose_usv += mean_usvh * (dt / 3600.0)
        covered_seconds += dt

    total_span = ordered[-1][0] - ordered[0][0] if len(ordered) >= 2 else 0
    coverage = (covered_seconds / total_span * 100.0) if total_span > 0 else None
    return {
        "available": covered_seconds > 0,
        "label": "Derived integrated dual-tube dose estimate",
        "value_usv": dose_usv if covered_seconds > 0 else None,
        "qualification": "derived estimate from selected dual-tube calibration profiles",
        "covered_seconds": covered_seconds,
        "total_span_seconds": total_span,
        "coverage_percent": coverage,
        "gap_count": gap_count,
        "gap_seconds": gap_seconds,
        "excluded_invalid_intervals": excluded_intervals,
        "profile_switches": profile_switches,
    }
