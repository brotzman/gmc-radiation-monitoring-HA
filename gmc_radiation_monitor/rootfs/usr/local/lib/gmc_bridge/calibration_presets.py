from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CalibrationPreset:
    """Predefined metrology working values for one supported detector model.

    These are transparent application defaults, not traceable calibration
    certificates. Explicit user values always override a preset.
    """

    profile_id: str
    display_name: str
    dual_tube_mode: str
    tube_model: str
    cpm_per_usvh: float
    dead_time_us: float | None
    reliable_max_cpm: int | None
    dead_time_model: str
    conversion_factor_uncertainty_percent: float | None
    calibration_reference: str
    dual_tube_switch_cpm: int | None = None
    high_dose_tube_model: str = ""


GMC_320_PLUS_V4 = CalibrationPreset(
    profile_id="gmc_320_plus_v4",
    display_name="GMC-320 Plus V4 (M4011, single tube)",
    dual_tube_mode="single",
    tube_model="M4011",
    cpm_per_usvh=154.0,
    dead_time_us=120.0,
    reliable_max_cpm=50_000,
    dead_time_model="nonparalyzable",
    conversion_factor_uncertainty_percent=20.0,
    calibration_reference=(
        "Application preset gmc_320_plus_v4; documented working values, "
        "not a traceable calibration certificate."
    ),
)

GMC_500_PLUS = CalibrationPreset(
    profile_id="gmc_500_plus",
    display_name="GMC-500+ (M4011 + SI-3BG, dual tube)",
    dual_tube_mode="separate",
    tube_model="M4011",
    cpm_per_usvh=154.0,
    dead_time_us=120.0,
    reliable_max_cpm=30_000,
    dead_time_model="nonparalyzable",
    conversion_factor_uncertainty_percent=20.0,
    calibration_reference=(
        "Application preset gmc_500_plus; the second-tube dose conversion remains "
        "uncalibrated until a verified factor is supplied."
    ),
    dual_tube_switch_cpm=30_000,
    high_dose_tube_model="SI-3BG",
)

PRESETS: dict[str, CalibrationPreset] = {
    GMC_320_PLUS_V4.profile_id: GMC_320_PLUS_V4,
    GMC_500_PLUS.profile_id: GMC_500_PLUS,
}

SUPPORTED_PROFILE_IDS = {
    "auto",
    *PRESETS,
    "custom_single",
    "custom_dual",
}


def infer_profile_id(name: str, tube_model: str = "", dual_tube_mode: str = "single") -> str:
    """Infer a conservative preset from the configured model/name.

    Explicit ``detector_profile`` is preferred. This inference only keeps older
    configurations working and does not attempt to identify arbitrary hardware.
    """

    text = f"{name} {tube_model}".strip()
    if re.search(r"GMC[- ]?320(?:\s*PLUS)?(?:\s*V?4)?", text, flags=re.IGNORECASE):
        return GMC_320_PLUS_V4.profile_id
    if re.search(r"GMC[- ]?500\+", text, flags=re.IGNORECASE):
        return GMC_500_PLUS.profile_id
    return "custom_dual" if dual_tube_mode in {"separate", "curve"} else "custom_single"


def resolve_preset(profile_id: str, *, name: str, tube_model: str, dual_tube_mode: str) -> tuple[str, CalibrationPreset | None]:
    normalized = str(profile_id or "auto").strip().lower()
    if normalized not in SUPPORTED_PROFILE_IDS:
        raise ValueError(
            "detector_profile must be auto, gmc_320_plus_v4, gmc_500_plus, "
            "custom_single or custom_dual"
        )
    if normalized == "auto":
        normalized = infer_profile_id(name, tube_model, dual_tube_mode)
    return normalized, PRESETS.get(normalized)
