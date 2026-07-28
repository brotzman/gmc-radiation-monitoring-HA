from __future__ import annotations

import html
from typing import Protocol

from .explanations import translate_action, translate_explanation
from .number_format import format_number, localize_numeric_text, translator_language
from .presentation_models import AnalysisLevel, AnalysisMetric, AnalysisResult, AnalysisStatus


class TranslatorLike(Protocol):
    def __call__(self, text: str, **values: object) -> str: ...


_STATUS_TONE = {
    AnalysisStatus.GOOD: "good",
    AnalysisStatus.NOTICE: "notice",
    AnalysisStatus.LEARNING: "notice",
    AnalysisStatus.WARNING: "alert",
    AnalysisStatus.ERROR: "alert",
    AnalysisStatus.UNAVAILABLE: "neutral",
    AnalysisStatus.NEUTRAL: "neutral",
}


_TRANSLATABLE_TEMPLATE_VALUES = {
    "confidence",
    "daily_label",
    "days_label",
    "from_value",
    "note",
    "to_value",
    "weekday",
}


def translated_template_values(values: dict[str, object], translator: TranslatorLike) -> dict[str, object]:
    """Translate nested semantic values before formatting a localized template."""
    result = dict(values)
    for key in _TRANSLATABLE_TEMPLATE_VALUES:
        value = result.get(key)
        if isinstance(value, str) and value:
            result[key] = translator(value)
    return result


def render_metric_card(metric: AnalysisMetric, translator: TranslatorLike) -> str:
    priority_class = " priority" if metric.priority else ""
    if metric.note_parts:
        note = " · ".join(
            translator(part.text_key, **translated_template_values(dict(part.values), translator)) for part in metric.note_parts
        )
    else:
        note = translator(metric.note_key, **translated_template_values(dict(metric.note_values), translator)) if metric.note_key else ""
    interpretation = (
        translator(metric.interpretation_key, **translated_template_values(dict(metric.interpretation_values), translator))
        if metric.interpretation_key
        else ""
    )
    interpretation_html = (
        f'<div class="interpretation {_STATUS_TONE[metric.status]}">{html.escape(interpretation)}</div>'
        if interpretation
        else ""
    )
    shown_value = (
        translator(metric.value_key, **translated_template_values(dict(metric.value_values), translator))
        if metric.value_key
        else localize_numeric_text(metric.value, translator_language(translator), group_plain_integers=True)
    )
    return (
        f'<div class="metric{priority_class}" data-metric-key="{html.escape(metric.key, quote=True)}" '
        f'data-analysis-tier="{metric.level.value}">'
        f'<strong>{html.escape(translator(metric.label_key, **translated_template_values(dict(metric.label_values), translator)))}</strong>'
        f'<div class="value">{html.escape(shown_value)}</div>'
        f'<small>{html.escape(note)}</small>'
        f'{interpretation_html}'
        '</div>'
    )


def render_collapsible_card(
    *,
    card_id: str,
    title: str,
    body: str,
    attributes: str = "",
    open_by_default: bool = True,
    help_text: str = "",
    explanation_code: str | None = None,
    translator: TranslatorLike | None = None,
    pin_label: str = "Pin card",
    help_label: str = "Show help",
) -> str:
    open_attribute = " open" if open_by_default else ""
    extra_attributes = f" {attributes.strip()}" if attributes.strip() else ""
    explanation = (
        translate_explanation(explanation_code, translator)
        if explanation_code and translator is not None
        else None
    )
    if explanation:
        explanation_title, explanation_body, explanation_action = explanation
        parts = [explanation_title, explanation_body]
        if explanation_action:
            parts.append(explanation_action)
        help_text = "\n\n".join(parts)
        help_label = explanation_title
    help_button = (
        f'<button type="button" class="card-help" aria-label="{html.escape(help_label, quote=True)}" '
        f'title="{html.escape(help_label, quote=True)}" data-help="{html.escape(help_text, quote=True)}">ⓘ</button>'
        if help_text
        else ""
    )
    return (
        f'<details class="card collapsible-card" id="{html.escape(card_id, quote=True)}"'
        f' data-card-title="{html.escape(title, quote=True)}"{extra_attributes}{open_attribute}>'
        f'<summary><h2>{html.escape(title)}</h2><span class="card-summary-actions">{help_button}'
        f'<button type="button" class="card-pin" aria-label="{html.escape(pin_label, quote=True)}" '
        f'title="{html.escape(pin_label, quote=True)}" aria-pressed="false">☆</button></span></summary>'
        f'<div class="collapsible-card-body">{body}</div></details>'
    )


def render_analysis_level_controls(*, default_level: str, translator: TranslatorLike) -> str:
    """The analysis-level chooser now lives in the compact header toolbar."""
    _ = AnalysisLevel.normalize(default_level)
    _translator = translator
    return ""


def render_analysis_result_summary(result: AnalysisResult, translator: TranslatorLike) -> str:
    tone = {
        AnalysisStatus.GOOD: "green",
        AnalysisStatus.NOTICE: "yellow",
        AnalysisStatus.LEARNING: "blue",
        AnalysisStatus.WARNING: "orange",
        AnalysisStatus.ERROR: "red",
        AnalysisStatus.UNAVAILABLE: "blue",
        AnalysisStatus.NEUTRAL: "blue",
    }[result.status]
    confidence = ""
    if result.confidence is not None:
        confidence = (
            f'<small>{html.escape(translator("Confidence"))}: '
            f'{format_number(float(result.confidence) * 100.0, translator_language(translator), decimals=0)}%</small>'
        )
    action = translate_action(result.action_code, translator)
    action_html = (
        f'<div class="analysis-action"><strong>{html.escape(translator("What should I do?"))}</strong> '
        f'{html.escape(action)}</div>'
        if action
        else ""
    )
    return (
        f'<div class="analysis-result-summary" data-analysis-result="{html.escape(result.key, quote=True)}">'
        f'<div class="orientation-state {tone}"><div class="orientation-state-copy">'
        f'<strong>{html.escape(translator(result.headline_key, **translated_template_values(dict(result.values), translator)))}</strong>'
        f'<span>{html.escape(translator(result.summary_key, **translated_template_values(dict(result.values), translator)))}</span>'
        f'{confidence}</div></div>{action_html}</div>'
    )


def render_inline_explanation(code: str, translator: TranslatorLike) -> str:
    explanation = translate_explanation(code, translator)
    if not explanation:
        return ""
    title, body, action = explanation
    action_html = (
        f'<p><strong>{html.escape(translator("What should I do?"))}</strong> {html.escape(action)}</p>'
        if action
        else ""
    )
    return (
        f'<details class="inline-help explanation"><summary>{html.escape(title)}</summary>'
        f'<div class="group-body"><p>{html.escape(body)}</p>{action_html}</div></details>'
    )


def format_geographic_coordinate(value: float, axis: str, language: str) -> str:
    """Format one geographic coordinate with degrees and a cardinal direction."""
    normalized_axis = axis.lower().strip()
    if normalized_axis == "latitude":
        direction = "N" if value >= 0 else "S"
    elif normalized_axis == "longitude":
        direction = "E" if value >= 0 else "W"
    else:
        raise ValueError(f"Unsupported coordinate axis: {axis}")
    return f"{format_number(abs(float(value)), language, decimals=5)}° {direction}"


def render_home_assistant_location(
    home_location: dict[str, object], *, timezone_text: str, language: str, translator: TranslatorLike
) -> str:
    """Render the collapsible Home Assistant location summary in one reusable component."""
    t = translator
    timezone_name = html.escape(timezone_text)
    if home_location.get("available"):
        location_name = str(home_location.get("location_name") or t("Configured location"))
        latitude = home_location.get("latitude")
        longitude = home_location.get("longitude")
        elevation = home_location.get("elevation")
        country = str(home_location.get("country") or "")
        parts: list[str] = []
        if latitude is not None and longitude is not None:
            parts.append(
                f"{t('Coordinates')}: "
                f"{format_geographic_coordinate(float(latitude), 'latitude', language)}, "
                f"{format_geographic_coordinate(float(longitude), 'longitude', language)}"
            )
        if elevation is not None:
            parts.append(f"{t('Elevation')}: {format_number(float(elevation), language, trim=True)} m")
        if country:
            parts.append(f"{t('Country')}: {country}")
        parts.append(f"{t('Timezone')}: {timezone_text}")
        details = " · ".join(parts)
        return (
            '<details class="location-details">'
            f'<summary><span class="details-summary-icon">📍</span><span><strong>{html.escape(t("Home Assistant location"))}</strong>'
            f"<small>{html.escape(location_name)}</small></span></summary>"
            '<div class="location-details-body">'
            f'<div class="location-details-values"><strong>{html.escape(location_name)}</strong>'
            f"<span>{html.escape(details)}</span></div>"
            f"<p>{html.escape(t('Location data comes from the Home Assistant general settings and is not sent to an external geocoding service.'))}</p>"
            "</div></details>"
        )
    return (
        '<details class="location-details">'
        f'<summary><span class="details-summary-icon">📍</span><span><strong>{html.escape(t("Home Assistant location"))}</strong>'
        f"<small>{html.escape(t('Location unavailable'))}</small></span></summary>"
        '<div class="location-details-body">'
        f'<div class="location-details-values"><span>{html.escape(t("Timezone"))}: {timezone_name}</span></div>'
        f"<p>{html.escape(t('Check the Home Assistant general settings and restart the add-on.'))}</p>"
        "</div></details>"
    )
