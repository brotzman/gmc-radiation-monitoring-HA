from __future__ import annotations

import html
import math
from collections.abc import Callable
from typing import Any

TranslatorLike = Callable[..., str]


def format_live_dose(value: object, language: str) -> tuple[str, str]:
    """Return a compact magnitude-aware value and unit for the live device card."""
    if value in (None, ""):
        return "—", "µSv/h"
    try:
        dose_usvh = float(value)
    except (TypeError, ValueError):
        return "—", "µSv/h"
    if not math.isfinite(dose_usvh):
        return "—", "µSv/h"

    absolute = abs(dose_usvh)
    unit = "µSv/h"
    display_value = dose_usvh
    if absolute >= 1000.0:
        display_value = dose_usvh / 1000.0
        unit = "mSv/h"
        decimals = 2
    elif absolute >= 10.0:
        decimals = 1
    elif absolute >= 1.0:
        decimals = 2
    elif absolute >= 0.1:
        decimals = 3
    else:
        decimals = 4

    formatted = f"{display_value:.{decimals}f}".rstrip("0").rstrip(".")
    if language != "en":
        formatted = formatted.replace(".", ",")
    return formatted, unit


def measurement_freshness(
    *,
    online: bool,
    age_seconds: int | None,
    scan_interval_seconds: int,
    runtime_reason: str = "",
    t: TranslatorLike,
) -> dict[str, Any]:
    """Classify measurement freshness independently from the serial connection.

    A connected counter can still have delayed accepted data (for example while a
    suspicious value is being confirmed).  Keeping the two states separate avoids
    presenting an old but plausible value as current.
    """
    interval = max(5, int(scan_interval_seconds or 60))
    reason = str(runtime_reason or "").strip().lower()
    reconnecting = not online and reason in {
        "reconnect_required",
        "serial_error",
        "read_failed",
        "initialization_failed",
        "hard_recovery",
    }
    if reconnecting:
        return {"state": "reconnecting", "label": t("Reconnecting"), "severity": "warning"}
    if not online:
        return {"state": "disconnected", "label": t("Device disconnected"), "severity": "offline"}
    if age_seconds is None:
        return {"state": "no-data", "label": t("No accepted measurement yet"), "severity": "warning"}

    current_limit = max(30, interval * 2)
    delayed_limit = max(120, interval * 5)
    if age_seconds <= current_limit:
        return {
            "state": "current",
            "label": t("Current · {seconds} s old", seconds=max(0, int(age_seconds))),
            "severity": "online",
        }
    if age_seconds <= delayed_limit:
        return {
            "state": "delayed",
            "label": t("Delayed · {seconds} s old", seconds=max(0, int(age_seconds))),
            "severity": "warning",
        }
    return {
        "state": "stale",
        "label": t("No new accepted data for {minutes} min", minutes=max(1, round(age_seconds / 60))),
        "severity": "error",
    }


def render_device_card_header(
    *,
    display_title: str,
    model_subtitle: str,
    serial_value: str,
    device_icon: str,
    status_class: str,
    status_label: str,
    freshness_display: str,
    last_update: str,
    freshness_state: str = "current",
    freshness_severity: str = "online",
) -> str:
    subtitle = (
        f'<span class="device-model-line">{html.escape(model_subtitle)}</span>'
        if model_subtitle
        else ""
    )
    return (
        '<div class="device-card-header">'
        f'<div class="device-card-title"><div class="assessment-icon device-card-icon">{html.escape(device_icon)}</div>'
        f'<div class="device-card-title-copy"><h3>{html.escape(display_title)}</h3>{subtitle}'
        f'<small class="device-id">ID: {html.escape(serial_value)}</small></div></div>'
        f'<div class="device-status-stack"><span class="device-status {status_class}">{html.escape(status_label)}</span>'
        f'<small class="device-freshness freshness-{html.escape(freshness_severity, quote=True)}" '
        f'data-live="freshness" data-freshness-state="{html.escape(freshness_state, quote=True)}" '
        f'title="{html.escape(last_update, quote=True)}">{html.escape(freshness_display)}</small></div></div>'
    )


def render_live_measurement(
    *,
    t: TranslatorLike,
    dose_number: str,
    dose_unit: str,
    quality_stars: str,
    latest_value: str,
    detector_name: str,
    cpm_per_usvh: float | None = None,
) -> str:
    factor = ""
    if cpm_per_usvh is not None:
        try:
            factor_value = float(cpm_per_usvh)
            if math.isfinite(factor_value) and factor_value > 0:
                factor = f'<span class="measurement-chip factor-chip">{html.escape(t("Factor"))}: {factor_value:g} CPM/(µSv/h)</span>'
        except (TypeError, ValueError):
            pass
    return (
        f'<div class="device-live measurement-hero"><strong>{html.escape(t("Estimated dose rate"))}</strong>'
        f'<span class="dose-reading"><span class="dose-number" data-live="dose-number">{html.escape(dose_number)}</span>'
        f'<span class="dose-unit" data-live="dose-unit">{html.escape(dose_unit)}</span></span>'
        f'<small class="primary-measurement-note">{html.escape(t("Derived from CPM; not independent dosimetry."))}</small>'
        f'<small class="quality-stars" data-live="quality-stars" title="{html.escape(t("Measurement quality explanation"), quote=True)}">{html.escape(quality_stars)}</small>'
        f'<div class="measurement-context"><span class="measurement-chip cpm-chip" data-live="cpm">{html.escape(latest_value)}</span>'
        f'<span class="measurement-chip detector-chip">{html.escape(detector_name)}</span>{factor}</div></div>'
    )


def render_measurement_display_settings(*, t: TranslatorLike, custom_px: int) -> str:
    options = "".join(
        f'<label><input type="radio" name="main-value-size" value="{value}"><span>{html.escape(t(label))}</span></label>'
        for value, label in (("small", "Small"), ("medium", "Medium"), ("large", "Large"), ("custom", "Custom"))
    )
    return (
        '<details class="measurement-display-settings">'
        f'<summary><span><strong>{html.escape(t("Measurement display"))}</strong>'
        f'<small>{html.escape(t("Main measurement font size"))}</small></span></summary>'
        f'<div class="measurement-size-options" role="radiogroup" aria-label="{html.escape(t("Main measurement font size"), quote=True)}">'
        f'{options}<label class="custom-font-size"><span>{html.escape(t("Custom font size"))}</span>'
        f'<input type="number" id="custom-value-font-size" min="20" max="64" step="1" value="{custom_px}"><span>px</span></label>'
        '</div>'
        f'<div class="measurement-override-row" id="measurement-override-status" hidden aria-live="polite">'
        f'<span>{html.escape(t("Local browser setting active"))}</span>'
        f'<button type="button" id="reset-main-value-size" class="button secondary">{html.escape(t("Reset to app default"))}</button>'
        '</div></details>'
    )


def render_connection_details(
    *,
    t: TranslatorLike,
    serial_value: str,
    port: object,
    baudrate: object,
    interval_seconds: object,
    last_response: str,
    next_scan: str,
    status_updated: str,
    runtime_reason: str,
    reconnects: int,
    serial_errors: int,
    profile: str,
    capabilities: str,
    stored_samples: int,
    health_summary: str,
    tube_values: str = "",
    diagnostics_values: str = "",
) -> str:
    rows = (
        ("Serial", serial_value, ""),
        ("Serial port", str(port), "technical-value"),
        ("Baud rate", str(baudrate), ""),
        ("Measurement interval", f"{interval_seconds} s", ""),
        ("Last successful response", last_response, ""),
        ("Next automatic scan", next_scan, ""),
        ("Connection state updated", status_updated, ""),
        ("Connection reason", runtime_reason, ""),
        ("Reconnects since app start", str(reconnects), ""),
        ("Serial errors since app start", str(serial_errors), ""),
        ("Profile", profile, ""),
        ("Device capabilities", capabilities, ""),
        ("Stored samples for this device", f"{stored_samples:,}", ""),
    )
    fields = "".join(
        f'<div class="device-field"><strong>{html.escape(t(label))}</strong>'
        f'<span class="{css_class}">{html.escape(value)}</span></div>'
        for label, value, css_class in rows
    )
    return (
        '<details class="device-connection-details" data-analysis-tier="expert">'
        f'<summary><span><strong>{html.escape(t("Connection details"))}</strong>'
        f'<small data-live="health">{html.escape(health_summary)}</small></span></summary>'
        f'<div class="device-fields">{fields}{tube_values}{diagnostics_values}</div></details>'
    )
