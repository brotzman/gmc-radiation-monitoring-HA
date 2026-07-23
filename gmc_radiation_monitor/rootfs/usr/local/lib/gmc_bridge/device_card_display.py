from __future__ import annotations

import html
import math
from collections.abc import Callable

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
        f'<small class="device-freshness" data-live="freshness" title="{html.escape(last_update, quote=True)}">{html.escape(freshness_display)}</small></div></div>'
    )


def render_live_measurement(
    *,
    t: TranslatorLike,
    dose_number: str,
    dose_unit: str,
    quality_stars: str,
    latest_value: str,
    detector_name: str,
) -> str:
    return (
        f'<div class="device-live measurement-hero"><strong>{html.escape(t("Latest measurement"))}</strong>'
        f'<span class="dose-reading"><span class="dose-number" data-live="dose-number">{html.escape(dose_number)}</span>'
        f'<span class="dose-unit" data-live="dose-unit">{html.escape(dose_unit)}</span></span>'
        f'<small class="quality-stars" data-live="quality-stars" title="{html.escape(t("Measurement quality explanation"), quote=True)}">{html.escape(quality_stars)}</small>'
        f'<div class="measurement-context"><span class="measurement-chip cpm-chip" data-live="cpm">{html.escape(latest_value)}</span>'
        f'<span class="measurement-chip detector-chip">{html.escape(detector_name)}</span></div></div>'
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
