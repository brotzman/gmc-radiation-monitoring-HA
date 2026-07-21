from __future__ import annotations

import html
from collections.abc import Callable
from typing import Any

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


def _profile_html(
    profile: TubeMetrologyProfile | None,
    *,
    heading: str,
    profile_class: str,
    t: Translate,
) -> str:
    if profile is None:
        return (
            f'<div class="tube-profile-card {profile_class} unconfigured">'
            f'<strong>{html.escape(t(heading))}</strong>'
            f'<span>{html.escape(t("Not configured"))}</span></div>'
        )
    factor = _calibration_value(profile.cpm_per_usvh, " CPM/(µSv/h)")
    dead_time = _calibration_value(profile.dead_time_us, " µs")
    reliable = _calibration_value(profile.reliable_max_cpm, " CPM")
    correction = (
        t("Active")
        if profile.dead_time_model != "none" and profile.dead_time_us is not None
        else t("Inactive")
    )
    reference = profile.calibration_reference or t("No calibration reference stored")
    card_state = "calibrated" if profile.dose_calibrated else "uncalibrated"
    return (
        f'<div class="tube-profile-card {profile_class} {card_state}">'
        f'<div class="tube-profile-heading"><strong>{html.escape(t(heading))}</strong>'
        f'<span>{html.escape(profile.tube_model or t("Unknown tube"))}</span></div>'
        f'<dl><div><dt>{html.escape(t("Conversion factor"))}</dt><dd>{html.escape(factor)}</dd></div>'
        f'<div><dt>{html.escape(t("Detector dead time"))}</dt><dd>{html.escape(dead_time)}</dd></div>'
        f'<div><dt>{html.escape(t("Maximum reliable CPM"))}</dt><dd>{html.escape(reliable)}</dd></div>'
        f'<div><dt>{html.escape(t("Dead-time correction"))}</dt><dd>{html.escape(correction)}</dd></div>'
        f'<div><dt>{html.escape(t("Conversion-factor uncertainty"))}</dt>'
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
        "incomplete": "Incomplete calibration",
    }
    mode_labels = {
        "single": "Single-tube profile",
        "separate": "Separate tube profiles",
        "curve": "Dual-tube calibration curve",
    }

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
            active_tube = t("Low-dose tube")
        elif active_key == "high":
            active_tube = t("High-dose tube")
        if live_dual.get("available") and live_dual.get("value_usvh") is not None:
            live_dose = f"{float(live_dual['value_usvh']):.4g} µSv/h"
        elif active_key:
            live_dose = t("Not available: selected tube is not calibrated")

    low_profile = dual_config.low_dose
    high_profile = dual_config.high_dose
    if dual_config.mode == "single":
        summary_tubes = (
            low_profile.tube_model
            if low_profile
            else str(item.get("tube_model") or "—")
        )
        summary_factor = _calibration_value(item.get("cpm_per_usvh"), " CPM/(µSv/h)")
    else:
        low_name = (
            low_profile.tube_model
            if low_profile and low_profile.tube_model
            else t("Low-dose tube")
        )
        high_name = (
            high_profile.tube_model
            if high_profile and high_profile.tube_model
            else t("High-dose tube")
        )
        summary_tubes = f"{low_name} + {high_name}"
        low_factor = _calibration_value(
            low_profile.cpm_per_usvh if low_profile else None
        )
        high_factor = _calibration_value(
            high_profile.cpm_per_usvh if high_profile else None
        )
        summary_factor = f"{low_factor} / {high_factor} CPM/(µSv/h)"

    legacy_dead_time = _calibration_value(item.get("dead_time_us"), " µs")
    legacy_reliable = _calibration_value(item.get("reliable_max_cpm"), " CPM")
    legacy_correction = (
        t("Active")
        if str(item.get("dead_time_model") or "none") != "none"
        and item.get("dead_time_us") not in (None, "")
        else t("Inactive")
    )
    mode_label = t(mode_labels.get(dual_config.mode, "Single-tube profile"))
    status_label_text = t(status_labels.get(calibration_status, "Working values"))
    switch_value = _calibration_value(dual_config.switch_cpm, " CPM")
    live_fields = ""
    if dual_config.mode != "single":
        live_fields = (
            f'<div><strong>{html.escape(t("Active tube profile"))}</strong><span>{html.escape(active_tube)}</span></div>'
            f'<div><strong>{html.escape(t("Derived dose rate"))}</strong><span>{html.escape(live_dose)}</span></div>'
        )
    calibration_profiles = (
        _profile_html(
            low_profile,
            heading="Detector profile",
            profile_class="single-profile",
            t=t,
        )
        if dual_config.mode == "single"
        else (
            _profile_html(
                low_profile,
                heading="Low-dose tube profile",
                profile_class="low-profile",
                t=t,
            )
            + _profile_html(
                high_profile,
                heading="High-dose tube profile",
                profile_class="high-profile",
                t=t,
            )
        )
    )
    return (
        f'<section class="calibration-panel calibration-{html.escape(calibration_status)}">'
        f'<div class="calibration-panel-header"><div><strong>{html.escape(t("Detector and calibration"))}</strong>'
        f'<small>{html.escape(summary_tubes)} · {html.escape(summary_factor)}</small></div>'
        f'<span class="calibration-status">{html.escape(status_label_text)}</span></div>'
        f'<div class="calibration-summary"><span>{html.escape(mode_label)}</span>'
        f'<span>{html.escape(t("Dead-time correction"))}: {html.escape(legacy_correction)}</span></div>'
        f'<div class="calibration-grid" data-analysis-tier="analysis">'
        f'<div><strong>{html.escape(t("Calibration mode"))}</strong><span>{html.escape(mode_label)}</span></div>'
        f'<div><strong>{html.escape(t("Tube model"))}</strong><span>{html.escape(summary_tubes)}</span></div>'
        f'<div><strong>{html.escape(t("Detector dead time"))}</strong><span>{html.escape(legacy_dead_time)}</span></div>'
        f'<div><strong>{html.escape(t("Maximum reliable CPM"))}</strong><span>{html.escape(legacy_reliable)}</span></div>'
        f'<div><strong>{html.escape(t("Dual-tube switch"))}</strong><span>{html.escape(switch_value)}</span></div>'
        f'{live_fields}</div>'
        f'<div class="tube-profile-grid" data-analysis-tier="expert">{calibration_profiles}</div>'
        f'</section>'
    )
