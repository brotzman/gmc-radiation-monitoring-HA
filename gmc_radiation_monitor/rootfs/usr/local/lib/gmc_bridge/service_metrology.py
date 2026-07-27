from __future__ import annotations

from typing import Any

from .config import DeviceConfig
from .metrology import (
    DualTubeMetrologyConfig,
    MetrologyConfig,
    TubeMetrologyProfile,
    derived_dual_tube_dose_estimate,
    live_measurement_metrology,
)

def _tube_metrology_profile(profile: Any) -> TubeMetrologyProfile | None:
    if profile is None:
        return None
    return TubeMetrologyProfile(
        tube_model=profile.tube_model,
        cpm_per_usvh=profile.cpm_per_usvh,
        dead_time_us=profile.dead_time_us,
        reliable_max_cpm=profile.reliable_max_cpm,
        dead_time_model=profile.dead_time_model,
        conversion_factor_uncertainty_percent=profile.conversion_factor_uncertainty_percent,
        calibration_uncertainty_percent=profile.calibration_uncertainty_percent,
        calibration_reference=profile.calibration_reference,
    )


def enrich_metrology_state(state: dict[str, Any], config: DeviceConfig) -> None:
    if state.get("cpm") is None:
        return
    registry = config.calibration_registry_values()
    status = str(registry.get("calibration_status") or "unknown")
    source = str(registry.get("calibration_source") or "unknown")
    active_tube = "primary"
    selected_profile = config.effective_low_dose_tube()
    derived_dose = None

    if config.dual_tube_mode != "single":
        dual = DualTubeMetrologyConfig(
            mode=config.dual_tube_mode,
            switch_cpm=config.dual_tube_switch_cpm,
            low_dose=_tube_metrology_profile(config.effective_low_dose_tube()),
            high_dose=_tube_metrology_profile(config.high_dose_tube),
        )
        dual_result = derived_dual_tube_dose_estimate(
            primary_cpm=float(state["cpm"]),
            low_cpm=float(state["tube_low_cpm"]) if state.get("tube_low_cpm") is not None else None,
            high_cpm=float(state["tube_high_cpm"]) if state.get("tube_high_cpm") is not None else None,
            counting_relative_percent=None,
            config=dual,
        )
        if dual_result.get("selected_tube") == "high":
            active_tube = "secondary"
            if config.high_dose_tube is not None:
                selected_profile = config.high_dose_tube
        elif dual_result.get("selected_tube") == "low":
            active_tube = "primary"
        derived_dose = dual_result.get("value_usvh") if dual_result.get("available") else None
        state["dual_tube_selection_reason"] = dual_result.get("selection_reason")

    selected_cpm = float(state["cpm"])
    if active_tube == "primary" and state.get("tube_low_cpm") is not None:
        selected_cpm = float(state["tube_low_cpm"])
    elif active_tube == "secondary" and state.get("tube_high_cpm") is not None:
        selected_cpm = float(state["tube_high_cpm"])

    result = live_measurement_metrology(
        cpm=selected_cpm,
        cpm_per_usvh=selected_profile.cpm_per_usvh,
        config=MetrologyConfig(
            dead_time_us=selected_profile.dead_time_us,
            reliable_max_cpm=selected_profile.reliable_max_cpm,
            dead_time_model=selected_profile.dead_time_model,
            conversion_factor_uncertainty_percent=selected_profile.conversion_factor_uncertainty_percent,
            calibration_uncertainty_percent=selected_profile.calibration_uncertainty_percent,
            calibration_reference=selected_profile.calibration_reference,
            tube_model=selected_profile.tube_model,
        ),
        calibration_status=status,
        calibration_source=source,
    )
    if derived_dose is not None:
        result["derived_dose_usvh"] = derived_dose
    state.update(
        {
            "raw_cpm": float(state["cpm"]),
            "corrected_cpm": result.get("corrected_cpm"),
            "detector_type": selected_profile.tube_model,
            "dual_tube_mode": config.dual_tube_mode,
            "active_tube": active_tube,
            "dead_time_model": selected_profile.dead_time_model,
            "dead_time_us": selected_profile.dead_time_us,
            "dead_time_loss_percent": result.get("dead_time_loss_percent"),
            "detector_load_percent": result.get("detector_load_percent"),
            "correction_factor": result.get("correction_factor"),
            "calibration_status": status,
            "calibration_source": source,
            "measurement_quality_index": result.get("measurement_quality_index"),
            "measurement_quality_stars": result.get("measurement_quality_stars"),
            "measurement_quality_star_text": result.get("measurement_quality_star_text"),
            "measurement_validity": result.get("measurement_validity"),
            "dose_quality": result.get("dose_quality"),
            "derived_dose_usvh": result.get("derived_dose_usvh"),
            "plausibility_warnings": result.get("plausibility_warnings", []),
            "dead_time_correction_active": bool(result.get("correction_applied")),
        }
    )
