from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CalibrationPreset:
    """Transparent application defaults for one supported detector model.

    A preset makes the configured assumptions visible and reproducible. It is
    not a substitute for an individual, traceable calibration certificate.
    """

    profile_id: str
    display_name: str
    model_patterns: tuple[str, ...]
    dual_tube_mode: str
    tube_model: str
    cpm_per_usvh: float
    dead_time_us: float | None
    reliable_max_cpm: int | None
    dead_time_model: str
    conversion_factor_uncertainty_percent: float | None
    calibration_reference: str
    calibration_source: str = "application_profile"
    warning_load_percent: float = 5.0
    critical_load_percent: float = 10.0
    invalid_load_percent: float = 25.0
    dual_tube_switch_cpm: int | None = None
    high_dose_tube_model: str = ""
    high_dose_dead_time_us: float | None = None
    high_dose_reliable_max_cpm: int | None = None

    def matches_model(self, value: str) -> bool:
        return any(re.search(pattern, value, flags=re.IGNORECASE) for pattern in self.model_patterns)


GMC_300 = CalibrationPreset(
    profile_id="gmc_300",
    display_name="GMC-300 family (single glass GM tube)",
    model_patterns=(r"GMC[- ]?300", r"GMC300"),
    dual_tube_mode="single",
    tube_model="M4011-compatible glass GM tube",
    cpm_per_usvh=161.54,
    dead_time_us=120.0,
    reliable_max_cpm=50_000,
    dead_time_model="nonparalyzable",
    conversion_factor_uncertainty_percent=20.0,
    calibration_reference=(
        "Automatic GMC-300 application profile; model-dependent working values. "
        "Confirm the tube and device calibration for the individual counter."
    ),
)

GMC_320_PLUS_V4 = CalibrationPreset(
    profile_id="gmc_320_plus_v4",
    display_name="GMC-320 Plus V4 (M4011, single tube)",
    model_patterns=(r"GMC[- ]?320", r"GMC320"),
    dual_tube_mode="single",
    tube_model="M4011",
    cpm_per_usvh=154.0,
    dead_time_us=120.0,
    reliable_max_cpm=50_000,
    dead_time_model="nonparalyzable",
    conversion_factor_uncertainty_percent=20.0,
    calibration_reference=(
        "Automatic GMC-320 Plus V4 application profile; documented working values, "
        "not a traceable calibration certificate."
    ),
)

GMC_500_PLUS = CalibrationPreset(
    profile_id="gmc_500_plus",
    display_name="GMC-500+ (M4011 + SI-3BG, dual tube)",
    model_patterns=(r"GMC[- ]?500\+", r"GMC500\+"),
    dual_tube_mode="separate",
    tube_model="M4011",
    cpm_per_usvh=154.0,
    dead_time_us=120.0,
    reliable_max_cpm=30_000,
    dead_time_model="nonparalyzable",
    conversion_factor_uncertainty_percent=20.0,
    calibration_reference=(
        "Automatic GMC-500+ application profile. The SI-3BG dose conversion remains "
        "uncalibrated until a verified device-specific factor is supplied."
    ),
    dual_tube_switch_cpm=30_000,
    high_dose_tube_model="SI-3BG",
    high_dose_dead_time_us=30.0,
)

GMC_600_PLUS = CalibrationPreset(
    profile_id="gmc_600_plus",
    display_name="GMC-600/600+ (LND 7317 pancake tube)",
    model_patterns=(r"GMC[- ]?600", r"GMC600"),
    dual_tube_mode="single",
    tube_model="LND 7317",
    cpm_per_usvh=348.0,
    dead_time_us=40.0,
    reliable_max_cpm=500_000,
    dead_time_model="nonparalyzable",
    conversion_factor_uncertainty_percent=20.0,
    calibration_reference=(
        "Automatic GMC-600/600+ application profile using the LND 7317 tube working "
        "factor. Confirm the device calibration points for the individual firmware."
    ),
)

PRESETS: dict[str, CalibrationPreset] = {
    preset.profile_id: preset
    for preset in (GMC_300, GMC_320_PLUS_V4, GMC_500_PLUS, GMC_600_PLUS)
}

SUPPORTED_PROFILE_IDS = {"auto", *PRESETS, "custom_single", "custom_dual"}


def detect_profile_id(model_or_version: str) -> str | None:
    text = str(model_or_version or "").strip()
    # Order matters: exact 500+ before broad family matches.
    for profile_id in ("gmc_500_plus", "gmc_600_plus", "gmc_320_plus_v4", "gmc_300"):
        if PRESETS[profile_id].matches_model(text):
            return profile_id
    return None


def infer_profile_id(name: str, tube_model: str = "", dual_tube_mode: str = "single") -> str:
    detected = detect_profile_id(f"{name} {tube_model}")
    if detected:
        return detected
    return "custom_dual" if dual_tube_mode in {"separate", "curve"} else "custom_single"


def resolve_preset(
    profile_id: str, *, name: str, tube_model: str, dual_tube_mode: str
) -> tuple[str, CalibrationPreset | None]:
    normalized = str(profile_id or "auto").strip().lower()
    if normalized not in SUPPORTED_PROFILE_IDS:
        supported = ", ".join(sorted(SUPPORTED_PROFILE_IDS))
        raise ValueError(f"detector_profile must be one of: {supported}")
    if normalized == "auto":
        normalized = infer_profile_id(name, tube_model, dual_tube_mode)
    return normalized, PRESETS.get(normalized)
