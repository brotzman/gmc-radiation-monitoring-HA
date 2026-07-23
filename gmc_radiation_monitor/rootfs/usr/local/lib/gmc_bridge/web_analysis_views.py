from __future__ import annotations

import html
from collections.abc import Iterable
from typing import Any, Protocol

from .number_format import format_number, localize_numeric_text, translator_language
from .presentation_models import (
    AnalysisEntity,
    AnalysisLevel,
    AnalysisMessage,
    AnalysisMetric,
    AnalysisResult,
    AnalysisSection,
    AnalysisStatus,
    AnalysisTable,
)
from .web_components import (
    render_analysis_result_summary,
    render_collapsible_card,
    render_inline_explanation,
    render_metric_card,
    translated_template_values,
)


class TranslatorLike(Protocol):
    def __call__(self, text: str, **values: object) -> str: ...


_STATUS_COLOR = {
    AnalysisStatus.GOOD: "green",
    AnalysisStatus.NOTICE: "yellow",
    AnalysisStatus.LEARNING: "blue",
    AnalysisStatus.WARNING: "orange",
    AnalysisStatus.ERROR: "red",
    AnalysisStatus.UNAVAILABLE: "blue",
    AnalysisStatus.NEUTRAL: "blue",
}

_STATUS_TONE = {
    AnalysisStatus.GOOD: "good",
    AnalysisStatus.NOTICE: "notice",
    AnalysisStatus.LEARNING: "notice",
    AnalysisStatus.WARNING: "alert",
    AnalysisStatus.ERROR: "alert",
    AnalysisStatus.UNAVAILABLE: "neutral",
    AnalysisStatus.NEUTRAL: "neutral",
}


def _translated_message(message: AnalysisMessage, t: TranslatorLike) -> str:
    values = translated_template_values(dict(message.values), t)
    return localize_numeric_text(
        t(message.text_key, **values),
        translator_language(t),
        group_plain_integers=True,
    )


def _render_messages(
    messages: Iterable[AnalysisMessage],
    t: TranslatorLike,
    *,
    list_class: str = "quality-reasons",
    as_list: bool = False,
) -> str:
    items = list(messages)
    if not items:
        return ""
    if as_list:
        return f'<ul class="{html.escape(list_class, quote=True)}">' + "".join(
            f'<li class="{_STATUS_TONE[item.status]}">{html.escape(_translated_message(item, t))}</li>'
            for item in items
        ) + "</ul>"
    return "".join(
        f'<div class="note {_STATUS_TONE[item.status]}" data-analysis-tier="{item.level.value}">'
        f'{html.escape(_translated_message(item, t))}</div>'
        for item in items
    )


def _render_table(table: AnalysisTable, t: TranslatorLike) -> str:
    title = f'<h3>{html.escape(t(table.title_key))}</h3>' if table.title_key else ""
    if not table.rows:
        empty = t(table.empty_key) if table.empty_key else t("No data")
        return f'{title}<div class="note" data-analysis-tier="{table.level.value}">{html.escape(empty)}</div>'
    header = "".join(f'<th>{html.escape(t(column.label_key))}</th>' for column in table.columns)
    rows = "".join(
        "<tr>" + "".join(
            f'<td>{html.escape(localize_numeric_text(row.get(column.key, "—"), translator_language(t), group_plain_integers=True))}</td>'
            for column in table.columns
        ) + "</tr>"
        for row in table.rows
    )
    return (
        f'<div data-analysis-tier="{table.level.value}">{title}<div class="table-wrap"><table>'
        f'<thead><tr>{header}</tr></thead><tbody>{rows}</tbody></table></div></div>'
    )


def _render_generic_entity(entity: AnalysisEntity, t: TranslatorLike) -> str:
    metrics = "".join(render_metric_card(metric, t) for metric in entity.metrics)
    messages = _render_messages(entity.messages, t)
    primary = f'<div class="assessment-state">{html.escape(localize_numeric_text(entity.primary_value, translator_language(t), group_plain_integers=True))}</div>' if entity.primary_value else ""
    return (
        f'<article class="assessment-card" data-analysis-tier="{entity.level.value}" '
        f'data-analysis-entity="{html.escape(entity.key, quote=True)}">'
        f'<h3>{html.escape(entity.title)}</h3>{primary}{messages}'
        f'<div class="metrics">{metrics}</div></article>'
    )


def render_analysis_section(section: AnalysisSection, t: TranslatorLike) -> str:
    open_attr = " open" if section.open_by_default else ""
    subtitle = f'<small>{html.escape(t(section.subtitle_key, **dict(section.values)))}</small>' if section.subtitle_key else ""
    metrics = "".join(render_metric_card(metric, t) for metric in section.metrics)
    entities = "".join(_render_generic_entity(entity, t) for entity in section.entities)
    tables = "".join(_render_table(table, t) for table in section.tables)
    messages = _render_messages(section.messages, t, as_list=section.key == "advanced-diagnostics")
    explanation = render_inline_explanation(section.explanation_code, t) if section.explanation_code else ""
    return (
        f'<details class="analysis-group" data-analysis-section="{html.escape(section.key, quote=True)}" '
        f'data-analysis-tier="{section.level.value}"{open_attr}>'
        f'<summary><span class="summary-copy">{html.escape(t(section.title_key, **dict(section.values)))}{subtitle}</span></summary>'
        f'<div class="group-body"><div class="metrics">{metrics}</div>'
        f'<div class="assessment-grid">{entities}</div>{tables}{messages}{explanation}</div></details>'
    )


def _render_result_card(
    result: AnalysisResult,
    t: TranslatorLike,
    *,
    card_id: str,
    title_key: str,
    body: str,
) -> str:
    return render_collapsible_card(
        card_id=card_id,
        title=t(title_key),
        body=body,
        explanation_code=result.explanation_code,
        translator=t,
        pin_label=t("Pin card"),
        help_label=t("Show help"),
    )


def render_radiation_intelligence(result: AnalysisResult, t: TranslatorLike) -> str:
    title = str(result.metadata.get("title_key") or "Intelligent radiation analysis")
    if result.status in {AnalysisStatus.LEARNING, AnalysisStatus.UNAVAILABLE} and not result.primary_value:
        body = (
            '<div class="empty-state"><span class="empty-state-icon">⏳</span>'
            f'<strong>{html.escape(t(result.headline_key, **dict(result.values)))}</strong>'
            f'<span>{html.escape(t(result.summary_key, **dict(result.values)))}</span></div>'
        )
        return _render_result_card(result, t, card_id="radiation-intelligence", title_key=title, body=body)
    confidence_metric = next((metric for metric in result.metrics if metric.key == "radiation-confidence"), None)
    confidence = "—" if confidence_metric is None else localize_numeric_text(t(confidence_metric.value_key or confidence_metric.value), translator_language(t), group_plain_integers=True)
    reasons = [item for item in result.messages if item.level == AnalysisLevel.ANALYSIS]
    expert = [item for item in result.messages if item.level == AnalysisLevel.EXPERT]
    body = (
        f'<div class="orientation-state {_STATUS_COLOR[result.status]}"><div class="orientation-state-copy">'
        f'<strong>{html.escape(t(result.headline_key, **dict(result.values)))}</strong>'
        f'<span>{html.escape(t(result.summary_key, **dict(result.values)))}</span>'
        f'<small>{html.escape(t("Confidence"))}: {html.escape(confidence)}</small></div></div>'
        f'<div data-analysis-tier="analysis">{_render_messages(reasons, t, as_list=True, list_class="compact-list")}</div>'
        f'<div data-analysis-tier="expert">{_render_messages(expert, t)}</div>'
    )
    return _render_result_card(result, t, card_id="radiation-intelligence", title_key=title, body=body)


def _profile_message(entity: AnalysisEntity, key_suffix: str) -> AnalysisMessage | None:
    return next((message for message in entity.messages if message.key.endswith(key_suffix)), None)


def render_background_profile_entity(entity: AnalysisEntity, t: TranslatorLike) -> str:
    """Render one adaptive background profile from the shared model."""
    if entity.status == AnalysisStatus.UNAVAILABLE:
        return (
            f'<article class="assessment-card"><h3>{html.escape(t(entity.title))}</h3>'
            f'<div class="note">{html.escape(t("No measurement yet"))}</div></article>'
        )
    headline_message = _profile_message(entity, "headline")
    detail_message = _profile_message(entity, "detail")
    headline = t(headline_message.text_key, **dict(headline_message.values)) if headline_message else ""
    detail_values = dict(detail_message.values) if detail_message else {}
    if "weekday" in detail_values:
        detail_values["weekday"] = t(str(detail_values["weekday"]))
    detail = t(detail_message.text_key, **detail_values) if detail_message else ""
    typical = next((metric for metric in entity.metrics if metric.key.endswith("-typical")), None)
    if typical:
        detail_html = (
            f'{html.escape(detail)}<br><span class="background-profile-values">'
            f'{html.escape(localize_numeric_text(typical.value, translator_language(t), group_plain_integers=True))}</span>'
        )
    else:
        detail_html = html.escape(detail)
    meta_parts: list[str] = []
    for metric in entity.metrics:
        if metric.key.endswith("-confidence"):
            meta_parts.append(f'{html.escape(t("Confidence"))}: {html.escape(localize_numeric_text(t(metric.value_key or metric.value), translator_language(t), group_plain_integers=True))}')
        elif metric.key.endswith("-excluded"):
            meta_parts.append(f'{html.escape(localize_numeric_text(metric.value, translator_language(t), group_plain_integers=True))} {html.escape(t("excluded measurements"))}')
        elif metric.key.endswith("-pairs"):
            meta_parts.append(f'{html.escape(localize_numeric_text(metric.value, translator_language(t), group_plain_integers=True))} {html.escape(t("valid paired samples"))}')
    meta = f'<small>{" · ".join(meta_parts)}</small>' if meta_parts else ""
    current = next((metric for metric in entity.metrics if metric.key.endswith("-current")), None)
    current_html = "" if current is None else render_metric_card(current, t)
    return (
        f'<article class="assessment-card"><h3>{html.escape(t(entity.title))}</h3>'
        f'<div class="orientation-state {_STATUS_COLOR[entity.status]}"><div class="orientation-state-copy">'
        f'<strong>{html.escape(headline)}</strong><span>{detail_html}</span>{meta}</div></div>'
        f'{current_html}</article>'
    )


def _render_historical_section(section: AnalysisSection, t: TranslatorLike) -> str:
    trend_metrics = [metric for metric in section.metrics if metric.key.startswith("historical-")]
    expert_metrics = [metric for metric in section.metrics if not metric.key.startswith("historical-")]
    trend_cards = "".join(
        render_metric_card(metric, _PeriodTranslator(t, metric.note_values.get("days")))
        .replace('class="metric', 'class="metric historical-trend-card', 1)
        for metric in trend_metrics
    )
    points = list(section.values.get("points") or [])
    if len(points) >= 2:
        values = [float(point.get("smoothed_cpm") or point.get("median_cpm") or 0.0) for point in points]
        minimum = min(values)
        maximum = max(values)
        span = maximum - minimum or 1.0
        coordinates = []
        for index, value in enumerate(values):
            x = 4.0 + (92.0 * index / max(1, len(values) - 1))
            y = 36.0 - (30.0 * (value - minimum) / span)
            coordinates.append(f"{x:.2f},{y:.2f}")
        chart = (
            '<figure class="historical-chart">'
            f'<svg viewBox="0 0 100 42" role="img" aria-label="{html.escape(t("Smoothed historical background trend"), quote=True)}" preserveAspectRatio="none">'
            '<line x1="4" y1="6" x2="4" y2="36" class="chart-axis"/><line x1="4" y1="36" x2="96" y2="36" class="chart-axis"/>'
            f'<polyline points="{" ".join(coordinates)}" class="chart-line" vector-effect="non-scaling-stroke"/>'
            '</svg><figcaption>'
            f'<span>{html.escape(str(points[0].get("date") or ""))}</span>'
            f'<strong>{html.escape(t("7-day smoothed daily median"))}</strong>'
            f'<span>{html.escape(str(points[-1].get("date") or ""))}</span>'
            '</figcaption></figure>'
        )
    else:
        chart = (
            f'<div class="empty-state"><strong>{html.escape(t("Historical chart is still being formed"))}</strong>'
            f'<span>{html.escape(t("At least two daily background values are required."))}</span></div>'
        )
    jump_messages = list(section.messages)
    has_jumps = any(message.key.startswith("baseline-jump-") for message in jump_messages)
    jump_details = (
        f'<details class="inline-help"><summary>{html.escape(t("Detected baseline jumps"))}: '
        f'{format_number(int(section.values.get("jump_count") or 0), translator_language(t), grouping=True)}</summary><div class="group-body">'
        f'{_render_messages(jump_messages, t, as_list=True, list_class="compact-list")}</div></details>'
        if has_jumps
        else _render_messages(jump_messages, t)
    )
    return (
        '<details class="analysis-group historical-development" data-analysis-tier="analysis">'
        f'<summary><span class="summary-copy">{html.escape(t(section.title_key))}'
        f'<small>{html.escape(t(section.subtitle_key))}</small></span></summary>'
        f'<div class="group-body"><div class="metrics historical-trends">{trend_cards}</div>{chart}'
        f'<div class="metrics" data-analysis-tier="expert">'
        f'{"".join(render_metric_card(metric, t) for metric in expert_metrics)}</div>'
        f'<div data-analysis-tier="expert">{jump_details}</div></div></details>'
    )


def render_historical_section(section: AnalysisSection, t: TranslatorLike) -> str:
    """Public renderer used by the compatibility historical facade and tests."""
    return _render_historical_section(section, t)


def render_adaptive_background(result: AnalysisResult, t: TranslatorLike) -> str:
    profile_html = "".join(render_background_profile_entity(entity, t) for entity in result.entities)
    supporting = next((section for section in result.sections if section.key == "adaptive-supporting-values"), None)
    historical = next((section for section in result.sections if section.key == "historical-development"), None)
    supporting_html = "" if supporting is None else "".join(render_metric_card(metric, _PeriodTranslator(t, metric.note_values.get("days"))) for metric in supporting.metrics)
    historical_html = "" if historical is None else _render_historical_section(historical, t)
    body = (
        f'<div class="assessment-grid">{profile_html}</div>'
        f'<div class="metrics" data-analysis-tier="analysis">{supporting_html}</div>'
        f'{historical_html}'
    )
    return _render_result_card(
        result,
        t,
        card_id="adaptive-background",
        title_key=str(result.metadata.get("title_key") or "Adaptive background profile"),
        body=body,
    )


def render_cosmic_influence(result: AnalysisResult, t: TranslatorLike) -> str:
    if result.metadata.get("hidden"):
        return ""
    analysis_metrics = [metric for metric in result.metrics if metric.level != AnalysisLevel.EXPERT]
    expert_metrics = [metric for metric in result.metrics if metric.level == AnalysisLevel.EXPERT]
    reason_messages = [
        message for message in result.messages
        if message.level != AnalysisLevel.EXPERT and message.key.startswith("pressure-reason-")
    ]
    analysis_messages = [
        message for message in result.messages
        if message.level != AnalysisLevel.EXPERT
        and not message.key.startswith("pressure-reason-")
        and message.key != "pressure-statistical-label"
    ]
    expert_messages = [message for message in result.messages if message.level == AnalysisLevel.EXPERT]
    reasons_html = (
        '<div class="note cosmic-reasons">'
        + _render_messages(reason_messages, t, as_list=True, list_class="compact-list")
        + '</div>'
        if reason_messages
        else ""
    )
    summary_values = dict(result.values)
    confidence_value = str(summary_values.get("confidence") or "")
    if result.summary_key == "Confidence: {confidence}":
        summary_text = f'{t("Confidence")}: {t(confidence_value)}'
    else:
        if confidence_value:
            summary_values["confidence"] = t(confidence_value)
        summary_text = t(result.summary_key, **summary_values)
    body = (
        '<div class="assessment-grid"><article class="assessment-card">'
        f'<h3>{html.escape(t("Assessment"))}</h3>'
        f'<div class="orientation-state {_STATUS_COLOR[result.status]}"><div class="orientation-state-copy">'
        f'<strong>{html.escape(t(result.headline_key))}</strong>'
        f'<span>{html.escape(summary_text)}</span></div></div>'
        f'<div data-analysis-tier="analysis">{reasons_html}{_render_messages(analysis_messages, t)}</div></article></div>'
        f'<div class="metrics" data-analysis-tier="analysis">{"".join(render_metric_card(metric, t) for metric in analysis_metrics)}</div>'
        f'<div class="metrics" data-analysis-tier="expert">{"".join(render_metric_card(metric, t) for metric in expert_metrics)}</div>'
        f'<div data-analysis-tier="expert">{_render_messages(expert_messages, t)}</div>'
    )
    return _render_result_card(
        result,
        t,
        card_id="cosmic-influence",
        title_key=str(result.metadata.get("title_key") or "Cosmic influence – statistical indication"),
        body=body,
    )


def _render_stability_entity(entity: AnalysisEntity, t: TranslatorLike) -> str:
    status_metric = next((metric for metric in entity.metrics if metric.key.endswith("-status")), None)
    status_label = t(status_metric.value_key or status_metric.value) if status_metric else ""
    meta_parts: list[str] = []
    for metric in entity.metrics:
        if metric is status_metric:
            continue
        raw_value = t(metric.value_key, **translated_template_values(dict(metric.value_values), t)) if metric.value_key else metric.value
        value = localize_numeric_text(raw_value, translator_language(t), group_plain_integers=True)
        gap_status_html = ""
        if metric.key.endswith("-gap") and metric.status in {AnalysisStatus.NOTICE, AnalysisStatus.WARNING}:
            gap_class = "critical" if metric.status == AnalysisStatus.WARNING else "warning"
            gap_label = "Critical" if gap_class == "critical" else "Warning"
            gap_status_html = (
                f' <span class="gap-status {gap_class}">{html.escape(t(gap_label))}</span>'
            )
        meta_parts.append(
            f'<span class="stability-meta-line">{html.escape(t(metric.label_key, **translated_template_values(dict(metric.label_values), t)))}: '
            f'{html.escape(value)}{gap_status_html}</span>'
        )
    meta = "".join(meta_parts)
    return (
        '<article class="assessment-card">'
        f'<h3>{html.escape(entity.title)}</h3><div class="assessment-state">{html.escape(localize_numeric_text(entity.primary_value or "—", translator_language(t), group_plain_integers=True))}</div>'
        f'<strong class="stability-status"><span class="stability-dot {_STATUS_COLOR[entity.status]}" aria-hidden="true"></span>'
        f'<span>{html.escape(status_label)}</span></strong><small class="stability-meta">{meta}</small></article>'
    )


def _section_by_key(result: AnalysisResult, key: str) -> AnalysisSection | None:
    return next((section for section in result.sections if section.key == key), None)


def render_fleet_intelligence(result: AnalysisResult, t: TranslatorLike) -> str:
    stability = _section_by_key(result, "fleet-stability")
    comparison = _section_by_key(result, "fleet-comparison")
    relative = _section_by_key(result, "relative-response")
    shared = _section_by_key(result, "shared-event")
    movement = _section_by_key(result, "movement-log")
    fleet_summary = (
        '<div class="metrics fleet-summary">'
        + "".join(render_metric_card(metric, t) for metric in result.metrics)
        + "</div>"
    )
    stability_html = "".join(_render_stability_entity(entity, t) for entity in (stability.entities if stability else ()))
    if not stability_html:
        stability_html = f'<div class="note">{html.escape(t("No connected devices."))}</div>'
    comparison_html = (
        "".join(render_metric_card(metric, t) for metric in comparison.metrics)
        + _render_messages(comparison.messages, t)
        if comparison else ""
    )
    relative_html = (
        "".join(render_metric_card(metric, t) for metric in relative.metrics)
        + _render_messages(relative.messages, t)
        if relative else ""
    )
    shared_html = _render_messages(shared.messages, t) if shared else ""
    movement_html = ""
    if movement:
        if movement.entities:
            movement_html = '<div class="device-fields">' + "".join(
                f'<div class="device-field"><strong>{html.escape(entity.title)}</strong>'
                f'<span>{html.escape(_translated_message(entity.messages[0], t))}</span></div>'
                for entity in movement.entities if entity.messages
            ) + "</div>"
        else:
            movement_html = _render_messages(movement.messages, t)
    body = (
        f'{fleet_summary}<div data-analysis-tier="analysis">'
        f'<h3>{html.escape(t("Stability and device health"))}</h3>'
        f'<div class="assessment-grid stability-grid">{stability_html}</div>'
        f'<h3>{html.escape(t("Device comparison"))}</h3><div class="metrics">{comparison_html}</div></div>'
        f'<div data-analysis-tier="expert"><h3>{html.escape(t("Long-term relative response"))}</h3>'
        f'<div class="metrics">{relative_html}</div><h3>{html.escape(t("Shared event detector"))}</h3>{shared_html}'
        f'<details><summary><span class="summary-copy">{html.escape(t("Position change log"))}</span></summary>'
        f'<div class="group-body">{movement_html}</div></details></div>'
    )
    return _render_result_card(
        result,
        t,
        card_id="fleet-intelligence",
        title_key=str(result.metadata.get("title_key") or "Fleet intelligence"),
        body=body,
    )


def render_absolute_safety(result: AnalysisResult, t: TranslatorLike) -> str:
    metadata = dict(result.metadata)
    state = str(metadata.get("state_color") or _STATUS_COLOR[result.status])
    profile = next((metric for metric in result.metrics if metric.key == "safety-profile"), None)
    warning = next((metric for metric in result.metrics if metric.key == "safety-warning"), None)
    danger = next((metric for metric in result.metrics if metric.key == "safety-danger"), None)
    profile_value = t(profile.value_key or profile.value) if profile else "—"
    warning_note = t(warning.note_key, **dict(warning.note_values)) if warning else ""
    danger_note = t(danger.note_key, **dict(danger.note_values)) if danger else ""
    meaning = _translated_message(result.messages[0], t) if result.messages else ""
    return (
        '<div class="assessment-card absolute">'
        f'<div class="assessment-header"><div class="assessment-icon">{metadata.get("icon", "🛡️")}</div><div>'
        f'<div class="assessment-title">{html.escape(t(str(metadata.get("title_key") or "Absolute radiation assessment")))}</div>'
        f'<div class="assessment-subtitle">{html.escape(t(str(metadata.get("subtitle_key") or "Evaluates the current value using the configured thresholds.")))}</div></div></div>'
        '<div class="assessment-grid"><div class="assessment-primary">'
        f'<div class="status-orb {html.escape(state, quote=True)}"></div><div>'
        f'<div class="assessment-state {html.escape(state, quote=True)}">{html.escape(t(result.headline_key))}</div>'
        f'<div class="assessment-detail"><strong>{html.escape(t(result.summary_key))}</strong><br>'
        f'{html.escape(localize_numeric_text(result.primary_value or "—", translator_language(t), group_plain_integers=True))}<br><small>{html.escape(t("Evaluated by"))}: '
        f'{html.escape(t(str(metadata.get("basis_key") or "CPM")))}</small></div></div></div>'
        f'<div class="assessment-stat"><strong>{html.escape(t("Active threshold profile"))}</strong>'
        f'<div class="big">{html.escape(profile_value)}</div><small>{html.escape(t("Thresholds can be changed in the add-on configuration."))}</small></div>'
        f'<div class="assessment-stat"><strong>{html.escape(t("Warning thresholds"))}</strong><div class="big">{html.escape(localize_numeric_text(warning.value if warning else "—", translator_language(t), group_plain_integers=True))}</div><small>{html.escape(warning_note)}</small></div>'
        f'<div class="assessment-stat"><strong>{html.escape(t("Danger thresholds"))}</strong><div class="big">{html.escape(localize_numeric_text(danger.value if danger else "—", translator_language(t), group_plain_integers=True))}</div><small>{html.escape(danger_note)}</small></div></div>'
        f'<div class="assessment-note"><strong>{html.escape(t("What this assessment means"))}</strong>{html.escape(meaning)}</div></div>'
    )


def render_local_background(result: AnalysisResult, t: TranslatorLike) -> str:
    metadata = dict(result.metadata)
    state = str(metadata.get("state_color") or _STATUS_COLOR[result.status])
    metrics = {metric.key: metric for metric in result.metrics}
    legacy = ""
    if state == "green":
        legacy = "<!-- Within local background range; Relative anomaly indicator only -->"
    elif state == "blue":
        legacy = "<!-- Baseline readiness; 6 h minimum sample coverage; Relative anomaly indicator only -->"
    learning = ""
    if state == "blue" and not bool(metadata.get("baseline_ready")):
        learning = (
            '<div class="learning"><div class="progress-track">'
            f'<div class="progress-bar" style="width:{float(metadata.get("readiness") or 0.0):.1f}%"></div></div>'
            f'<div class="progress-copy"><span>{html.escape(t("Learning progress"))} '
            f'{format_number(float(metadata.get("readiness") or 0.0), translator_language(t), decimals=0)}%</span>'
            f'<span>{format_number(int(metadata.get("collected_hours") or 0), translator_language(t))} h {int(metadata.get("collected_minutes") or 0):02d} min · '
            f'{html.escape(t("1 h coverage"))} {format_number(float(metadata.get("coverage_1h_percent") or 0.0), translator_language(t), decimals=1)}%</span></div></div>'
        )
    meaning = _translated_message(result.messages[0], t) if result.messages else ""
    def stat(key: str, label: str) -> str:
        metric = metrics.get(key)
        if metric is None:
            return ""
        shown = t(metric.value_key, **translated_template_values(dict(metric.value_values), t)) if metric.value_key else localize_numeric_text(metric.value, translator_language(t), group_plain_integers=True)
        note = t(metric.note_key, **translated_template_values(dict(metric.note_values), t)) if metric.note_key else ""
        return f'<div class="assessment-stat"><strong>{html.escape(t(label))}</strong><div class="big">{html.escape(shown)}</div><small>{html.escape(note)}</small></div>'
    return (
        f'<div class="assessment-card baseline" data-state="{html.escape(str(metadata.get("data_state") or state), quote=True)}">{legacy}'
        f'<div class="assessment-header"><div class="assessment-icon">{metadata.get("icon", "📈")}</div><div>'
        f'<div class="assessment-title">{html.escape(t(str(metadata.get("title_key") or "Local background analysis")))}</div>'
        f'<div class="assessment-subtitle">{html.escape(t(str(metadata.get("subtitle_key") or "Compares the current value with the usual background at this location.")))}</div></div></div>'
        '<div class="assessment-grid baseline-grid"><div class="assessment-primary">'
        f'<div class="status-orb {html.escape(state, quote=True)}"></div><div>'
        f'<div class="assessment-state {html.escape(state, quote=True)}">{html.escape(t(result.headline_key))}</div>'
        f'<div class="assessment-detail"><strong>{html.escape(t(result.summary_key))}</strong><br>'
        f'{html.escape(localize_numeric_text(result.primary_value or "—", translator_language(t), group_plain_integers=True))} {html.escape(t("relative to baseline"))}</div></div></div>'
        f'{stat("background-local-baseline", "Local baseline")}'
        f'{stat("background-current", "Current value")}'
        f'{stat("background-deviation", "Deviation")}'
        f'{stat("background-trend", "Trend (30 min)")}</div>{learning}'
        f'<div class="assessment-note"><strong>{html.escape(t("What this assessment means"))}</strong>{html.escape(meaning)}</div></div>'
    )


def render_combined_interpretation(result: AnalysisResult, t: TranslatorLike) -> str:
    parts = [html.escape(_translated_message(message, t)) for message in result.messages]
    return (
        f'<div class="combined-interpretation"><div class="icon">{result.metadata.get("icon", "💡")}</div><div>'
        f'<strong>{html.escape(t(result.headline_key))}</strong><div>{" ".join(parts)}</div></div></div>'
    )


def render_recommendation(result: AnalysisResult, t: TranslatorLike) -> str:
    tone = _STATUS_COLOR[result.status]
    return (
        f'<div class="recommendation-card {tone}"><div class="icon">{result.metadata.get("icon", "✓")}</div><div>'
        f'<strong>{html.escape(t(str(result.metadata.get("title_key") or "Recommendation")))}</strong>'
        f'<div class="headline">{html.escape(t(result.headline_key))}</div>'
        f'<div class="detail">{html.escape(t(result.summary_key, **dict(result.values)))}</div></div></div>'
    )


def render_assessment_legend(t: TranslatorLike) -> str:
    return f'''<details class="analysis-group assessment-legend"><summary><span class="summary-copy">{html.escape(t("Explanation of the two assessments"))}<small>{html.escape(t("Absolute thresholds and local anomaly detection answer different questions."))}</small></span></summary><div class="group-body"><div class="legend-grid">
<div class="legend-card"><strong>{html.escape(t("Absolute radiation assessment"))}</strong><div class="legend-row"><span class="legend-dot green"></span>{html.escape(t("Uncritical: below warning threshold"))}</div><div class="legend-row"><span class="legend-dot yellow"></span>{html.escape(t("Elevated: within warning range"))}</div><div class="legend-row"><span class="legend-dot red"></span>{html.escape(t("Critical: danger threshold exceeded"))}</div></div>
<div class="legend-card"><strong>{html.escape(t("Local background analysis"))}</strong><div class="legend-row"><span class="legend-dot green"></span>{html.escape(t("Normal: within the usual local range"))}</div><div class="legend-row"><span class="legend-dot yellow"></span>{html.escape(t("Noticeable: above the usual local range"))}</div><div class="legend-row"><span class="legend-dot orange"></span>{html.escape(t("Clearly elevated: clearly above the usual local range"))}</div><div class="legend-row"><span class="legend-dot red"></span>{html.escape(t("Extremely elevated: far above the usual local range"))}</div><div class="legend-row"><span class="legend-dot blue"></span>{html.escape(t("Learning: not enough local history yet"))}</div></div>
</div><div class="assessment-note"><strong>{html.escape(t("Official reference values"))}</strong>{html.escape(t("BfS and ICRP reference profiles convert annual dose values into continuous-rate equivalents for context. They are not official instantaneous alarm limits and cannot replace professional dose assessment."))}</div></div></details>'''


def render_device_analysis(
    result: AnalysisResult,
    *,
    safety: AnalysisResult,
    background: AnalysisResult,
    interpretation: AnalysisResult,
    t: TranslatorLike,
    advanced: bool,
    device_label: str,
    device_model: str,
) -> str:
    normalized_model = (device_model or device_label).casefold().replace(" ", "")
    if "320" in normalized_model:
        badge_class, badge_text = "device-320", "320"
    elif "500" in normalized_model:
        badge_class, badge_text = "device-500", "500+"
    else:
        badge_class, badge_text = "device-generic", "GMC"
    heading = t("Analysis") if not device_label else f'{t("Analysis for")} {device_label}'
    heading_html = (
        f'<div class="analysis-heading"><span class="analysis-device-badge {badge_class}">'
        f'{html.escape(badge_text)}</span><h2>{html.escape(heading)}</h2></div>'
    )
    if result.status == AnalysisStatus.UNAVAILABLE:
        return (
            f'<section id="analysis" class="analysis-section">{heading_html}<div class="note">'
            f'<strong>{html.escape(t(result.headline_key))}</strong><br>'
            f'{html.escape(t(result.summary_key))}</div></section>'
        )
    status_section = next((section for section in result.sections if section.key == "status-summary"), None)

    def status_item(metric: AnalysisMetric) -> str:
        raw_value = t(metric.value_key, **translated_template_values(dict(metric.value_values), t)) if metric.value_key else metric.value
        shown_value = localize_numeric_text(raw_value, translator_language(t), group_plain_integers=True)
        if metric.note_parts:
            note = " · ".join(_translated_message(part, t) for part in metric.note_parts)
        else:
            raw_note = t(metric.note_key, **translated_template_values(dict(metric.note_values), t)) if metric.note_key else ""
            note = localize_numeric_text(raw_note, translator_language(t), group_plain_integers=True)
        if not note and metric.interpretation_key:
            note = localize_numeric_text(
                t(metric.interpretation_key, **translated_template_values(dict(metric.interpretation_values), t)),
                translator_language(t),
                group_plain_integers=True,
            )
        color = "blue" if metric.key in {"status-mean-1h", "status-mean-7d"} else _STATUS_COLOR[metric.status]
        return (
            f'<div class="status-item {color}"><strong>{html.escape(t(metric.label_key, **translated_template_values(dict(metric.label_values), t)))}</strong>'
            f'<div class="status-value">{html.escape(shown_value)}</div><small>{html.escape(note)}</small></div>'
        )

    minimum_samples = (
        '<div class="status-summary">'
        + "".join(status_item(metric) for metric in (status_section.metrics if status_section else ()))
        + '</div>'
    )
    overview = next((section for section in result.sections if section.key == "overview"), None)
    expert_sections = [section for section in result.sections if section.key not in {"status-summary", "overview"}]
    overview_html = render_analysis_section(overview, t) if overview else ""
    expert_html = "".join(render_analysis_section(section, t) for section in expert_sections) if advanced else ""
    return (
        f'<section id="analysis" class="analysis-section">{heading_html}'
        f'<div data-analysis-tier="summary">{render_analysis_result_summary(result, t)}'
        f'<div class="status-zone">{render_absolute_safety(safety, t)}{render_local_background(background, t)}</div>'
        f'{minimum_samples}</div><div data-analysis-tier="analysis">'
        f'{render_assessment_legend(t)}{overview_html}</div>'
        f'<div data-analysis-tier="expert">{expert_html}</div></section>'
    )


class _PeriodTranslator:
    def __init__(self, translator: TranslatorLike, days: Any) -> None:
        self._translator = translator
        self._days = days

    def __call__(self, text: str, **values: object) -> str:
        if text == "{days} days":
            days = self._days if self._days is not None else values.get("days", "")
            return f"{format_number(days, translator_language(self._translator), grouping=True)} {self._translator('days')}"
        if text == "{note} · n={samples}":
            note = self._translator(str(values.get("note", "")))
            samples = format_number(values.get("samples", 0), translator_language(self._translator), grouping=True)
            return f"{note} · n={samples}"
        return self._translator(text, **values)
