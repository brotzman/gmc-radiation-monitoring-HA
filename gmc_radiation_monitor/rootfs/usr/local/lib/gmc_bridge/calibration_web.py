from __future__ import annotations

import html
from collections.abc import Callable
from typing import Any

from .calibration_presets import infer_profile_id
from .metrology import (
    DualTubeMetrologyConfig,
    TubeMetrologyProfile,
    derived_dual_tube_dose_estimate,
)

Translate = Callable[..., str]


def _calibration_mapping(value: object) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    return {}


def _tube_profile_from_device(value: object) -> TubeMetrologyProfile | None:
    profile = _calibration_mapping(value)
    if not profile:
        return None

    def number(key: str) -> float | None:
        raw = profile.get(key)
        if raw in (None, ""):
            return None
        try:
            return float(raw)
        except (TypeError, ValueError):
            return None

    reliable = number("reliable_max_cpm")
    return TubeMetrologyProfile(
        tube_model=str(profile.get("tube_model") or ""),
        cpm_per_usvh=number("cpm_per_usvh"),
        dead_time_us=number("dead_time_us"),
        reliable_max_cpm=int(reliable) if reliable is not None else None,
        dead_time_model=str(profile.get("dead_time_model") or "none"),
        conversion_factor_uncertainty_percent=number(
            "conversion_factor_uncertainty_percent"
        ),
        calibration_uncertainty_percent=number("calibration_uncertainty_percent"),
        calibration_reference=str(profile.get("calibration_reference") or ""),
    )


def dual_tube_config_from_device(item: dict[str, Any]) -> DualTubeMetrologyConfig:
    legacy_low = TubeMetrologyProfile(
        tube_model=str(item.get("tube_model") or ""),
        cpm_per_usvh=float(item.get("cpm_per_usvh") or 154.0),
        dead_time_us=(
            float(item["dead_time_us"])
            if item.get("dead_time_us") not in (None, "")
            else None
        ),
        reliable_max_cpm=(
            int(item["reliable_max_cpm"])
            if item.get("reliable_max_cpm") not in (None, "")
            else None
        ),
        dead_time_model=str(item.get("dead_time_model") or "none"),
        conversion_factor_uncertainty_percent=(
            float(item["conversion_factor_uncertainty_percent"])
            if item.get("conversion_factor_uncertainty_percent") not in (None, "")
            else None
        ),
        calibration_uncertainty_percent=(
            float(item["calibration_uncertainty_percent"])
            if item.get("calibration_uncertainty_percent") not in (None, "")
            else None
        ),
        calibration_reference=str(item.get("calibration_reference") or ""),
    )
    switch = item.get("dual_tube_switch_cpm")
    return DualTubeMetrologyConfig(
        mode=str(item.get("dual_tube_mode") or "single"),
        switch_cpm=int(switch) if switch not in (None, "") else None,
        low_dose=_tube_profile_from_device(item.get("low_dose_tube_profile"))
        or legacy_low,
        high_dose=_tube_profile_from_device(item.get("high_dose_tube_profile")),
    )


def _calibration_value(value: object, suffix: str = "") -> str:
    if value in (None, ""):
        return "—"
    rendered = f"{value:g}" if isinstance(value, float) else str(value)
    return f"{rendered}{suffix}"


def _profile_analysis_fields(
    profile: TubeMetrologyProfile | None,
    *,
    prefix: str,
    t: Translate,
) -> str:
    """Render operational values once in the analysis tier."""

    label = t(prefix)
    if profile is None:
        return (
            f'<div><strong>{html.escape(label)}</strong>'
            f'<span>{html.escape(t("Not configured"))}</span></div>'
        )
    correction = (
        t("Active")
        if profile.dead_time_model != "none" and profile.dead_time_us is not None
        else t("Inactive")
    )
    fields = (
        (
            f'{label} · {t("Conversion factor")}',
            _calibration_value(profile.cpm_per_usvh, " CPM/(µSv/h)"),
        ),
        (
            f'{label} · {t("Detector dead time")}',
            _calibration_value(profile.dead_time_us, " µs"),
        ),
        (
            f'{label} · {t("Maximum reliable CPM")}',
            _calibration_value(profile.reliable_max_cpm, " CPM"),
        ),
        (f'{label} · {t("Dead-time correction")}', correction),
    )
    return "".join(
        f'<div><strong>{html.escape(title)}</strong>'
        f'<span>{html.escape(value)}</span></div>'
        for title, value in fields
    )


def _profile_html(
    profile: TubeMetrologyProfile | None,
    *,
    heading: str,
    profile_class: str,
    t: Translate,
) -> str:
    """Render provenance details without repeating operational values."""

    if profile is None:
        return (
            f'<div class="tube-profile-card {profile_class} unconfigured">'
            f'<strong>{html.escape(t(heading))}</strong>'
            f'<span>{html.escape(t("Not configured"))}</span></div>'
        )
    reference = profile.calibration_reference or t("No calibration reference stored")
    card_state = "calibrated" if profile.dose_calibrated else "uncalibrated"
    return (
        f'<div class="tube-profile-card {profile_class} {card_state}">'
        f'<div class="tube-profile-heading"><strong>{html.escape(t(heading))}</strong></div>'
        f'<dl><div><dt>{html.escape(t("Conversion-factor uncertainty"))}</dt>'
        f'<dd>{html.escape(_calibration_value(profile.conversion_factor_uncertainty_percent, " %"))}</dd></div>'
        f'<div><dt>{html.escape(t("Calibration uncertainty"))}</dt>'
        f'<dd>{html.escape(_calibration_value(profile.calibration_uncertainty_percent, " %"))}</dd></div></dl>'
        f'<p><strong>{html.escape(t("Calibration reference"))}:</strong> {html.escape(reference)}</p>'
        f'</div>'
    )


def render_calibration_panel(
    *,
    item: dict[str, Any],
    latest_cpm: object,
    t: Translate,
) -> str:
    dual_config = dual_tube_config_from_device(item)
    calibration_status = str(item.get("calibration_status") or "working_values")
    status_labels = {
        "documented": "Documented calibration",
        "working_values": "Working values",
        "predefined": "Predefined profile",
        "customized": "Customized profile",
        "incomplete": "Incomplete calibration",
    }
    mode_labels = {
        "single": "Single physical tube",
        "separate": "Two physical tubes",
        "curve": "Dual-tube calibration curve",
    }
    detector_profile_labels = {
        "gmc_320_plus_v4": "GMC-320 Plus V4 · M4011",
        "gmc_500_plus": "GMC-500+ · M4011 + SI-3BG",
        "custom_single": "Custom single-tube profile",
        "custom_dual": "Custom dual-tube profile",
    }
    detector_profile = str(item.get("detector_profile") or "").strip()
    if not detector_profile:
        detector_profile = infer_profile_id(
            str(
                item.get("configured_name")
                or item.get("device_model")
                or item.get("hardware_model")
                or ""
            ),
            str(item.get("tube_model") or ""),
            dual_config.mode,
        )
    detector_profile_label = detector_profile_labels.get(
        detector_profile, detector_profile.replace("_", " ")
    )

    active_tube = "—"
    live_dose = "—"
    if dual_config.mode != "single":
        live_dual = derived_dual_tube_dose_estimate(
            primary_cpm=float(latest_cpm) if latest_cpm is not None else None,
            low_cpm=(
                float(item["tube_low_cpm"])
                if item.get("tube_low_cpm") is not None
                else None
            ),
            high_cpm=(
                float(item["tube_high_cpm"])
                if item.get("tube_high_cpm") is not None
                else None
            ),
            counting_relative_percent=None,
            config=dual_config,
        )
        active_key = live_dual.get("selected_tube")
        if active_key == "low":
            active_tube = t("Primary tube")
        elif active_key == "high":
            active_tube = t("Second tube")
        if live_dual.get("available") and live_dual.get("value_usvh") is not None:
            live_dose = f"{float(live_dual['value_usvh']):.4g} µSv/h"
        elif active_key:
            live_dose = t("Not available: selected tube is not calibrated")

    low_profile = dual_config.low_dose
    high_profile = dual_config.high_dose
    if dual_config.mode == "single":
        overview_fields = _profile_analysis_fields(
            low_profile, prefix="Tube profile", t=t
        )
        calibration_profiles = _profile_html(
            low_profile,
            heading="Tube profile",
            profile_class="single-profile",
            t=t,
        )
    else:
        switch_value = _calibration_value(dual_config.switch_cpm, " CPM")
        overview_fields = (
            f'<div><strong>{html.escape(t("Dual-tube switch"))}</strong>'
            f'<span>{html.escape(switch_value)}</span></div>'
            f'<div><strong>{html.escape(t("Active tube profile"))}</strong>'
            f'<span>{html.escape(active_tube)}</span></div>'
            f'<div><strong>{html.escape(t("Derived dose rate"))}</strong>'
            f'<span>{html.escape(live_dose)}</span></div>'
            + _profile_analysis_fields(
                low_profile, prefix="Primary tube", t=t
            )
            + _profile_analysis_fields(
                high_profile, prefix="Second tube", t=t
            )
        )
        calibration_profiles = (
            _profile_html(
                low_profile,
                heading="Primary tube profile",
                profile_class="low-profile",
                t=t,
            )
            + _profile_html(
                high_profile,
                heading="Second tube profile",
                profile_class="high-profile",
                t=t,
            )
        )

    status_label_text = t(status_labels.get(calibration_status, "Working values"))
    return (
        f'<section class="calibration-panel calibration-{html.escape(calibration_status)}">'
        f'<div class="calibration-panel-header"><strong>{html.escape(t("Detector and calibration"))}</strong>'
        f'<span class="calibration-status">{html.escape(status_label_text)}</span></div>'
        f'<div class="calibration-summary"><span>{html.escape(detector_profile_label)}</span>'
        f'<span>{html.escape(t(mode_labels.get(dual_config.mode, "Single physical tube")))}</span></div>'
        f'<div class="calibration-grid" data-analysis-tier="analysis">{overview_fields}</div>'
        f'<div class="tube-profile-grid" data-analysis-tier="expert">{calibration_profiles}</div>'
        f'</section>'
    )
