from __future__ import annotations

import html
from collections.abc import Callable
from typing import Any

from .calibration_presets import PRESETS, infer_profile_id
from .metrology import (
    DualTubeMetrologyConfig,
    MetrologyConfig,
    TubeMetrologyProfile,
    derived_dual_tube_dose_estimate,
    live_measurement_metrology,
)

Translate = Callable[..., str]


def _mapping(value: object) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _number(value: object) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _tube_profile_from_device(value: object) -> TubeMetrologyProfile | None:
    profile = _mapping(value)
    if not profile:
        return None
    reliable = _number(profile.get("reliable_max_cpm"))
    return TubeMetrologyProfile(
        tube_model=str(profile.get("tube_model") or ""),
        cpm_per_usvh=_number(profile.get("cpm_per_usvh")),
        dead_time_us=_number(profile.get("dead_time_us")),
        reliable_max_cpm=int(reliable) if reliable is not None else None,
        dead_time_model=str(profile.get("dead_time_model") or "none"),
        conversion_factor_uncertainty_percent=_number(
            profile.get("conversion_factor_uncertainty_percent")
        ),
        calibration_uncertainty_percent=_number(profile.get("calibration_uncertainty_percent")),
        calibration_reference=str(profile.get("calibration_reference") or ""),
    )


def dual_tube_config_from_device(item: dict[str, Any]) -> DualTubeMetrologyConfig:
    legacy_low = TubeMetrologyProfile(
        tube_model=str(item.get("tube_model") or item.get("detector_type") or ""),
        cpm_per_usvh=_number(item.get("cpm_per_usvh")),
        dead_time_us=_number(item.get("dead_time_us")),
        reliable_max_cpm=(
            int(float(item["reliable_max_cpm"]))
            if item.get("reliable_max_cpm") not in (None, "")
            else None
        ),
        dead_time_model=str(item.get("dead_time_model") or "none"),
        conversion_factor_uncertainty_percent=_number(
            item.get("conversion_factor_uncertainty_percent")
        ),
        calibration_uncertainty_percent=_number(item.get("calibration_uncertainty_percent")),
        calibration_reference=str(item.get("calibration_reference") or ""),
    )
    switch = item.get("dual_tube_switch_cpm")
    return DualTubeMetrologyConfig(
        mode=str(item.get("dual_tube_mode") or "single"),
        switch_cpm=int(switch) if switch not in (None, "") else None,
        low_dose=_tube_profile_from_device(item.get("low_dose_tube_profile")) or legacy_low,
        high_dose=_tube_profile_from_device(item.get("high_dose_tube_profile")),
    )


def _value(value: object, suffix: str = "", decimals: int | None = None) -> str:
    if value in (None, ""):
        return "—"
    if isinstance(value, (int, float)):
        rendered = f"{float(value):.{decimals}f}" if decimals is not None else f"{float(value):g}"
    else:
        rendered = str(value)
    if suffix.startswith(" "):
        return f"{rendered}\u00a0{suffix.lstrip()}"
    return f"{rendered}{suffix}"


def _status(status: str, source: str, t: Translate) -> tuple[str, str]:
    labels = {
        "documented": "Documented calibration",
        "predefined": "Application working values",
        "customized": "User profile",
        "working_values": "Application working values",
        "partial": "Partially calibrated",
        "incomplete": "Not calibrated",
        "unknown": "Unknown",
    }
    if status == "documented" and source in {"factory_certificate", "manufacturer_certificate"}:
        labels["documented"] = "Factory calibrated"
    icons = {
        "documented": "🟢",
        "predefined": "🟡",
        "customized": "🟡",
        "working_values": "🟡",
        "partial": "🟡",
        "incomplete": "🔴",
        "unknown": "⚪",
    }
    key = status if status in labels else "unknown"
    return icons[key], t(labels[key])


def _tube_card(
    profile: TubeMetrologyProfile | None,
    *,
    cpm: object,
    active: bool,
    heading: str,
    t: Translate,
) -> str:
    if profile is None:
        return (
            '<div class="detector-tube-card tube-profile-card unavailable">'
            f'<div class="tube-title"><strong>{html.escape(heading)}</strong></div>'
            f'<span>{html.escape(t("Not configured"))}</span></div>'
        )
    calibrated = profile.dose_calibrated
    state_icon = "✓" if calibrated else "⚠"
    state_label = t("Calibrated") if calibrated else t("Not calibrated")
    active_label = f'<span class="active-tube-badge">{html.escape(t("Active"))}</span>' if active else ""
    return (
        f'<div class="detector-tube-card tube-profile-card {"active" if active else "inactive"} {"calibrated" if calibrated else "uncalibrated"}">'
        f'<div class="tube-title"><strong>{html.escape(profile.tube_model or heading)}</strong>{active_label}</div>'
        f'<div class="tube-state"><span>{state_icon}</span>{html.escape(state_label)}</div>'
        '<dl>'
        f'<div><dt>{html.escape(t("Conversion factor"))}</dt><dd>{html.escape(_value(profile.cpm_per_usvh, " CPM/(µSv/h)")) if profile.cpm_per_usvh is not None else html.escape(t("Not configured"))}</dd></div>'
        f'<div><dt>{html.escape(t("Dead time"))}</dt><dd>{html.escape(_value(profile.dead_time_us, " µs"))}</dd></div>'
        f'<div><dt>{html.escape(t("Model"))}</dt><dd>{html.escape(t("Non-Paralyzable") if profile.dead_time_model == "nonparalyzable" else t("None"))}</dd></div>'
        '</dl></div>'
    )


def _preset_low_profile(preset: object) -> TubeMetrologyProfile:
    return TubeMetrologyProfile(
        tube_model=str(getattr(preset, "tube_model", "")),
        cpm_per_usvh=_number(getattr(preset, "cpm_per_usvh", None)),
        dead_time_us=_number(getattr(preset, "dead_time_us", None)),
        reliable_max_cpm=getattr(preset, "reliable_max_cpm", None),
        dead_time_model=str(getattr(preset, "dead_time_model", "none")),
        conversion_factor_uncertainty_percent=_number(
            getattr(preset, "conversion_factor_uncertainty_percent", None)
        ),
        calibration_reference=str(getattr(preset, "calibration_reference", "")),
    )


def _preset_high_profile(preset: object) -> TubeMetrologyProfile | None:
    model = str(getattr(preset, "high_dose_tube_model", "") or "").strip()
    if not model:
        return None
    dead_time = _number(getattr(preset, "high_dose_dead_time_us", None))
    return TubeMetrologyProfile(
        tube_model=model,
        dead_time_us=dead_time,
        reliable_max_cpm=getattr(preset, "high_dose_reliable_max_cpm", None),
        dead_time_model="nonparalyzable" if dead_time is not None else "none",
        calibration_reference="Application profile working values; no verified dose factor.",
    )


def _legacy_composite_tube_label(value: str) -> bool:
    text = str(value or "").casefold()
    return "+" in text or "dual" in text or "kalibrierung gilt" in text


def render_calibration_panel(*, item: dict[str, Any], latest_cpm: object, t: Translate) -> str:
    config = dual_tube_config_from_device(item)
    low = config.low_dose
    high = config.high_dose
    profile_id = str(item.get("detector_profile") or "").strip()
    if not profile_id:
        profile_id = infer_profile_id(
            str(item.get("configured_name") or item.get("device_model") or ""),
            str(item.get("tube_model") or ""),
            config.mode,
        )
    preset = PRESETS.get(profile_id)
    if preset is not None and not bool(item.get("calibration_overrides")):
        if low is None or (config.mode != "single" and _legacy_composite_tube_label(low.tube_model)):
            low = _preset_low_profile(preset)
        if config.mode != "single" and high is None:
            high = _preset_high_profile(preset)
        config = DualTubeMetrologyConfig(
            mode=config.mode,
            switch_cpm=config.switch_cpm,
            low_dose=low,
            high_dose=high,
        )
    calibration_status = str(item.get("calibration_status") or "unknown")
    calibration_source = str(item.get("calibration_source") or "unknown")
    presentation_status = calibration_status
    if (
        config.mode != "single"
        and low is not None
        and high is not None
        and low.dose_calibrated
        and not high.dose_calibrated
    ):
        presentation_status = "partial"

    dual_result: dict[str, Any] | None = None
    active_key = str(item.get("active_tube") or "")
    if config.mode != "single":
        dual_result = derived_dual_tube_dose_estimate(
            primary_cpm=_number(latest_cpm),
            low_cpm=_number(item.get("tube_low_cpm")),
            high_cpm=_number(item.get("tube_high_cpm")),
            counting_relative_percent=None,
            config=config,
        )
        active_key = "primary" if dual_result.get("selected_tube") == "low" else (
            "secondary" if dual_result.get("selected_tube") == "high" else active_key
        )

    selected_profile = high if active_key == "secondary" and high is not None else low
    selected_cpm = item.get("tube_high_cpm") if active_key == "secondary" else item.get("tube_low_cpm")
    if selected_cpm is None:
        selected_cpm = latest_cpm
    live = live_measurement_metrology(
        cpm=float(selected_cpm or 0),
        cpm_per_usvh=selected_profile.cpm_per_usvh if selected_profile else None,
        config=(selected_profile.metrology_config() if selected_profile else MetrologyConfig()),
        calibration_status=calibration_status,
        calibration_source=calibration_source,
    )
    # Prefer values persisted together with the latest measurement.
    for key in (
        "corrected_cpm", "dead_time_loss_percent", "detector_load_percent",
        "correction_factor", "measurement_quality_index", "measurement_quality_stars",
        "measurement_quality_star_text", "dose_quality", "measurement_validity",
        "derived_dose_usvh", "plausibility_warnings",
    ):
        if item.get(key) not in (None, ""):
            live[key] = item[key]
    if dual_result and dual_result.get("available"):
        live["derived_dose_usvh"] = dual_result.get("value_usvh")

    stars = str(live.get("measurement_quality_star_text") or "☆☆☆☆☆")
    quality_index = int(live.get("measurement_quality_index") or 0)
    load = _number(live.get("detector_load_percent"))
    loss = _number(live.get("dead_time_loss_percent"))
    factor = _number(live.get("correction_factor"))
    corrected = _number(live.get("corrected_cpm"))
    load_width = max(0.0, min(100.0, load or 0.0))
    traffic = "green" if load is None or load < 5 else "yellow" if load < 10 else "red"
    traffic_icon = "🟢" if traffic == "green" else "🟡" if traffic == "yellow" else "🔴"
    correction_active = bool(live.get("correction_applied") or item.get("dead_time_correction_active"))
    _, status_label = _status(presentation_status, calibration_source, t)
    dose = _number(live.get("derived_dose_usvh"))
    accuracy_key = str(live.get("dose_quality") or "low")
    accuracy_label = t({"high": "High", "medium": "Medium", "low": "Low"}.get(accuracy_key, "Low"))
    warnings = live.get("plausibility_warnings") or []
    warning_labels = {
        "implausible_conversion_factor": "Conversion factor is implausible",
        "missing_dead_time": "Dead time is missing",
        "unknown_tube_model": "Tube model is unknown",
        "incomplete_calibration": "Calibration is incomplete",
        "implausible_dead_time": "Dead time is implausible",
    }
    warnings_html = "".join(
        f'<li>⚠ {html.escape(t(warning_labels.get(str(key), str(key))))}</li>' for key in warnings
    )

    if config.mode == "single":
        tube_html = _tube_card(
            low, cpm=latest_cpm, active=True, heading=t("Tube"), t=t
        )
        active_name = low.tube_model if low else "—"
    else:
        tube_html = (
            _tube_card(
                low, cpm=item.get("tube_low_cpm"), active=active_key != "secondary",
                heading=t("Primary tube"), t=t,
            )
            + _tube_card(
                high, cpm=item.get("tube_high_cpm"), active=active_key == "secondary",
                heading=t("Second tube"), t=t,
            )
        )
        active_name = (high.tube_model if high and active_key == "secondary" else low.tube_model if low else "—")

    # The tube model is already rendered prominently in the detector card. Keep
    # the source label semantic so the compact single-tube card is not redundant.
    profile_source = str(item.get("detector_profile_source") or "")
    if preset and profile_source in {"automatic_configuration", "detected_identity"}:
        source_label = t("Automatically recognized device profile")
    elif preset:
        source_label = t("Application profile working values")
    else:
        source_label = calibration_source.replace("_", " ")
    active_display = active_name
    correction_label = t("Active") if correction_active else t("Inactive")
    loss_label = t("No losses") if not loss else _value(loss, " %", 2)

    layout_html = (
        f'<small class="detector-layout-label">{html.escape(t("Single physical tube") if config.mode == "single" else t("Two physical tubes"))}</small>'
        + ('<span hidden>Zwei physische Zählrohre</span>' if config.mode != "single" else '')
    )
    legacy_status_html = (
        '<span hidden>Unvollständige Kalibrierung</span>'
        if calibration_status == "incomplete" else ""
    )
    return (
        f'<section class="calibration-panel calibration-{html.escape(presentation_status)}" data-quality-index="{quality_index}">'
        '<span class="legacy-calibration-label" hidden>Detektorprofil</span>'
        f'{legacy_status_html}'
        '<div class="calibration-panel-header"><div>'
        f'<strong title="{html.escape(t("Detector profile"), quote=True)}">{html.escape(t("Detector profile"))}</strong>'
        f'<small>{html.escape(source_label)}</small></div>'
        f'<span class="calibration-status">{html.escape(status_label)}</span></div>'
        f'<div class="detector-tube-grid" data-analysis-tier="analysis">{tube_html}</div>'
        f'<div data-analysis-tier="analysis">{layout_html}</div>'
        '<div class="detector-load-card" data-analysis-tier="analysis">'
        f'<div class="load-heading"><strong>{html.escape(t("Detector load"))}</strong><span>{traffic_icon} {html.escape(_value(load, " %", 1))}</span></div>'
        f'<div class="load-track"><span class="load-fill {traffic}" style="width:{load_width:.1f}%"></span></div></div>'
        '<div class="calibration-grid" data-analysis-tier="analysis"><div class="dead-time-monitor">'
        + (f'<div><strong>{html.escape(t("Active detector"))}</strong><span>{html.escape(active_display)}</span></div>' if config.mode != "single" else "")
        + f'<div><strong>{html.escape(t("Estimated losses"))}</strong><span>{html.escape(loss_label)}</span></div>'
        f'<div><strong>{html.escape(t("Correction"))}</strong><span>{html.escape(correction_label)}</span></div>'
        f'<div><strong>{html.escape(t("Live dose quality"))}</strong><span>{html.escape(_value(dose, " µSv/h", 4))} · {html.escape(accuracy_label)}</span></div>'
        '</div></div>'
        '<details class="expert-details" data-analysis-tier="expert"><summary>'
        f'<span>{html.escape(t("Expert view"))}</span></summary><div class="expert-details-body"><div class="expert-statistics">'
        f'<div><strong>{html.escape(t("Raw CPM"))}</strong><span>{html.escape(_value(latest_cpm, " CPM"))}</span></div>'
        f'<div><strong>{html.escape(t("Corrected CPM"))}</strong><span>{html.escape(_value(corrected, " CPM", 1))}</span></div>'
        f'<div><strong>{html.escape(t("Dead-time losses"))}</strong><span>{html.escape(_value(loss, " %", 2))}</span></div>'
        f'<div><strong>{html.escape(t("Correction factor"))}</strong><span>{html.escape(_value(factor, "", 4))}</span></div>'
        f'<div class="measurement-quality-row"><strong title="{html.escape(t("Measurement quality explanation"), quote=True)}">{html.escape(t("Measurement quality"))} ⓘ</strong><span class="quality-stars">{html.escape(stars)} <small>({quality_index}/100)</small></span></div>'
        '</div>'
        f'<small class="measurement-quality-explanation">{html.escape(t("Measurement quality explanation"))}</small></div></details>'
        + (f'<ul class="calibration-warnings">{warnings_html}</ul>' if warnings_html else "")
        + '</section>'
    )
