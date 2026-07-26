from __future__ import annotations

import html
import math
from datetime import UTC, datetime
from typing import Any, Protocol
from urllib.parse import quote_plus

from .field_test_protocol import build_field_test_protocol
from .long_term_analysis import build_long_term_analysis
from .number_format import format_number


class TranslatorLike(Protocol):
    language: str

    def __call__(self, text: str, **values: object) -> str: ...


def _num(value: Any, language: str, *, decimals: int = 1, suffix: str = "") -> str:
    if value is None:
        return "—"
    try:
        shown = format_number(float(value), language, decimals=decimals, grouping=True, trim=True)
    except (TypeError, ValueError):
        return "—"
    return f"{shown}{suffix}"


def _date_time(value: Any, timezone, language: str) -> str:
    try:
        dt = datetime.fromtimestamp(int(value), UTC).astimezone(timezone)
    except (TypeError, ValueError, OSError):
        return "—"
    return dt.strftime("%d.%m.%Y %H:%M" if language == "de" else "%Y-%m-%d %H:%M")


def _window_card(key: str, item: dict[str, Any], t: TranslatorLike) -> str:
    label = {
        "24h": t("24 hours"),
        "7d": t("7 days"),
        "30d": t("30 days"),
        "90d": t("90 days"),
        "365d": t("365 days"),
    }[key]
    ready = bool(item.get("ready"))
    if ready:
        value = _num(item.get("mean_cpm"), t.language, decimals=2, suffix=" CPM")
        note = t(
            "Median {median} CPM · coverage {coverage}%",
            median=_num(item.get("median_cpm"), t.language, decimals=2),
            coverage=_num(item.get("coverage_percent"), t.language, decimals=1),
        )
        status_class = "good"
    else:
        value = t("Not yet meaningful")
        reason = str(item.get("reason") or "insufficient_duration")
        if reason == "insufficient_coverage":
            note = t(
                "Coverage {coverage}% · at least {required}% required",
                coverage=_num(item.get("coverage_percent"), t.language, decimals=1),
                required=_num(item.get("minimum_coverage_percent", 80.0), t.language, decimals=0),
            )
        else:
            note = t(
                "Only {covered} of {required} days covered",
                covered=_num(item.get("covered_days"), t.language, decimals=1),
                required=item.get("days", 0),
            )
        status_class = "pending"
    dose = item.get("dose_usv")
    dose_note = (
        t("Derived cumulative dose: {dose} µSv", dose=_num(dose, t.language, decimals=3))
        if dose is not None
        else t("No supported dose conversion for this period")
    )
    return (
        f'<article class="long-term-card window-card {status_class}">'
        f'<div class="long-term-card-head"><strong>{html.escape(label)}</strong>'
        f'<span class="long-term-state">{html.escape(t("Ready") if ready else t("Preliminary"))}</span></div>'
        f'<div class="long-term-value">{html.escape(value)}</div>'
        f'<small>{html.escape(note)}</small><small>{html.escape(dose_note)}</small></article>'
    )


def _trend_chart(days: list[dict[str, Any]], t: TranslatorLike) -> str:
    points = days[-365:]
    if len(points) < 2:
        return f'<div class="empty-state"><strong>{html.escape(t("Not enough daily values for a long-term chart"))}</strong></div>'
    values = [float(item["median_cpm"]) for item in points]
    minimum = min(values)
    maximum = max(values)
    span = max(1.0, maximum - minimum)
    width, height, pad = 900.0, 260.0, 24.0

    def coordinates(series: list[float]) -> str:
        result: list[str] = []
        denominator = max(1, len(series) - 1)
        for index, value in enumerate(series):
            x = pad + (width - 2 * pad) * index / denominator
            y = pad + (height - 2 * pad) * (maximum - value) / span
            result.append(f"{x:.1f},{y:.1f}")
        return " ".join(result)

    rolling: list[float] = []
    for index in range(len(values)):
        start = max(0, index - 6)
        rolling.append(float(sorted(values[start : index + 1])[len(values[start : index + 1]) // 2]))
    raw_points = coordinates(values)
    rolling_points = coordinates(rolling)
    first_label = str(points[0]["date"])
    last_label = str(points[-1]["date"])
    return f'''
<div class="long-term-chart-wrap" role="img" aria-label="{html.escape(t('Daily median and 7-day rolling median'), quote=True)}">
<svg class="long-term-chart" viewBox="0 0 900 260" preserveAspectRatio="none" aria-hidden="true">
<line x1="24" y1="236" x2="876" y2="236" class="chart-axis"/>
<polyline points="{raw_points}" class="chart-series raw"/>
<polyline points="{rolling_points}" class="chart-series smooth"/>
</svg>
<div class="long-term-chart-legend"><span><i class="legend-line raw"></i>{html.escape(t('Daily median'))}</span><span><i class="legend-line smooth"></i>{html.escape(t('7-day rolling median'))}</span></div>
<div class="long-term-chart-dates"><span>{html.escape(first_label)}</span><span>{html.escape(last_label)}</span></div>
</div>'''


def _calendar_heatmap(days: list[dict[str, Any]], background: dict[str, Any], t: TranslatorLike) -> str:
    median = background.get("median_cpm")
    p95 = background.get("p95_cpm")
    if not days:
        return f'<div class="empty-state"><strong>{html.escape(t("No calendar data available"))}</strong></div>'
    cells: list[str] = []
    for item in days[-366:]:
        value = float(item["median_cpm"])
        coverage = float(item.get("coverage_percent") or 0.0)
        if coverage < 25.0:
            level = "missing"
        elif median is None or float(median) <= 0:
            level = "level-2"
        else:
            ratio = value / float(median)
            if ratio < 0.8:
                level = "level-0"
            elif ratio < 1.05:
                level = "level-1"
            elif ratio < 1.25:
                level = "level-2"
            elif p95 is not None and value < float(p95):
                level = "level-3"
            else:
                level = "level-4"
        title = t(
            "{date}: median {median} CPM, coverage {coverage}%",
            date=item["date"],
            median=_num(value, t.language, decimals=1),
            coverage=_num(coverage, t.language, decimals=0),
        )
        cells.append(
            f'<span class="calendar-cell {level}" title="{html.escape(title, quote=True)}" '
            f'aria-label="{html.escape(title, quote=True)}"></span>'
        )
    return (
        '<div class="calendar-scroll" tabindex="0"><div class="calendar-grid" role="img" '
        f'aria-label="{html.escape(t("Calendar heat map of daily median CPM"), quote=True)}">'
        + "".join(cells)
        + '</div></div><div class="calendar-legend"><span>'
        + html.escape(t("Lower"))
        + '</span><i class="level-0"></i><i class="level-1"></i><i class="level-2"></i><i class="level-3"></i><i class="level-4"></i><span>'
        + html.escape(t("Higher"))
        + "</span></div>"
    )


def _monthly_table(months: list[dict[str, Any]], t: TranslatorLike) -> str:
    if not months:
        return f'<div class="empty-state"><strong>{html.escape(t("No monthly aggregates available"))}</strong></div>'
    rows = []
    for item in reversed(months[-18:]):
        rows.append(
            "<tr>"
            f'<td>{html.escape(str(item["month"]))}</td>'
            f'<td>{html.escape(_num(item.get("mean_cpm"), t.language, decimals=2))}</td>'
            f'<td>{html.escape(_num(item.get("median_cpm"), t.language, decimals=2))}</td>'
            f'<td>{html.escape(_num(item.get("covered_hours"), t.language, decimals=1))}</td>'
            f'<td>{html.escape(_num(item.get("dose_usv"), t.language, decimals=3))}</td>'
            "</tr>"
        )
    return f'''
<div class="table-scroll long-term-table-wrap" tabindex="0"><table class="long-term-table">
<thead><tr><th>{html.escape(t('Month'))}</th><th>{html.escape(t('Mean CPM'))}</th><th>{html.escape(t('Median CPM'))}</th><th>{html.escape(t('Covered hours'))}</th><th>{html.escape(t('Derived dose (µSv)'))}</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>'''


def _seasonal_table(items: list[dict[str, Any]], t: TranslatorLike) -> str:
    if len(items) < 6:
        return f'<div class="seasonal-table empty-state"><strong>{html.escape(t("Not enough months for a seasonal profile"))}</strong><small>{html.escape(t("At least six represented calendar months are required."))}</small></div>'
    rows = []
    for item in items:
        rows.append(
            "<tr>"
            f'<td>{html.escape(str(int(item.get("month") or 0)))}</td>'
            f'<td>{html.escape(_num(item.get("median_cpm"), t.language, decimals=2))}</td>'
            f'<td>{html.escape(str(int(item.get("days") or 0)))}</td>'
            "</tr>"
        )
    return f'''
<div class="table-scroll long-term-table-wrap" tabindex="0"><table class="long-term-table seasonal-table">
<thead><tr><th>{html.escape(t('Calendar month'))}</th><th>{html.escape(t('Median CPM'))}</th><th>{html.escape(t('Days represented'))}</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>
<div class="note">{html.escape(t('Exploratory seasonal summary; it does not separate weather, location, detector or calibration changes.'))}</div>'''


def _episodes_table(episodes: dict[str, Any], timezone, t: TranslatorLike) -> str:
    items = list(episodes.get("items") or [])
    if not items:
        return f'<div class="empty-state"><strong>{html.escape(t("No persistent relative elevation episodes detected"))}</strong><small>{html.escape(t("The detector uses the robust long-term local background and does not replace radiation-safety alarms."))}</small></div>'
    rows = []
    for item in items[:10]:
        rows.append(
            "<tr>"
            f'<td>{html.escape(_date_time(item.get("start_utc"), timezone, t.language))}</td>'
            f'<td>{html.escape(_num(item.get("duration_hours"), t.language, decimals=1))}</td>'
            f'<td>{html.escape(_num(item.get("mean_cpm"), t.language, decimals=1))}</td>'
            f'<td>{html.escape(_num(item.get("maximum_cpm"), t.language, decimals=0))}</td>'
            f'<td>{html.escape(_num(item.get("area_above_threshold_cpm_h"), t.language, decimals=1))}</td>'
            "</tr>"
        )
    return f'''
<div class="table-scroll long-term-table-wrap" tabindex="0"><table class="long-term-table">
<thead><tr><th>{html.escape(t('Start'))}</th><th>{html.escape(t('Duration (h)'))}</th><th>{html.escape(t('Mean CPM'))}</th><th>{html.escape(t('Maximum CPM'))}</th><th>{html.escape(t('Excess area (CPM·h)'))}</th></tr></thead>
<tbody>{''.join(rows)}</tbody></table></div>'''


def _evidence_label(level: str, t: TranslatorLike) -> str:
    return t({
        "not_evaluable": "Not evaluable",
        "exploratory": "Exploratory",
        "preliminary": "Preliminary",
        "supported": "Supported",
        "well_supported": "Well supported",
    }.get(level, "Not evaluable"))


def _evidence_badge(evidence: dict[str, Any], t: TranslatorLike) -> str:
    level = str(evidence.get("level") or "not_evaluable")
    return f'<span class="evidence-badge evidence-{html.escape(level, quote=True)}">{html.escape(_evidence_label(level, t))}</span>'


def _effect_label(level: str, t: TranslatorLike) -> str:
    return t({
        "very_small": "Very small practical magnitude",
        "small": "Small practical magnitude",
        "moderate": "Moderate practical magnitude",
        "large": "Large practical magnitude",
        "unknown": "Practical magnitude not available",
    }.get(level, "Practical magnitude not available"))


def _plain_trend_text(trend: dict[str, Any], t: TranslatorLike) -> tuple[str, str]:
    evidence = trend.get("evidence") or {}
    if evidence.get("level") == "not_evaluable" or not trend.get("available"):
        return t("No reliable long-term trend can be assessed yet"), t("At least 30 sufficiently complete days and an adequate effective sample size are required.")
    direction = str(trend.get("direction") or "stable")
    effect = trend.get("effect") or {}
    percent = effect.get("percent_per_month")
    if direction == "increasing":
        headline = t("A rising long-term tendency is visible")
    elif direction == "decreasing":
        headline = t("A falling long-term tendency is visible")
    else:
        headline = t("No statistically clear long-term trend is visible")
    detail = t(
        "Estimated change {value}% per month · {magnitude}",
        value=_num(percent, t.language, decimals=1),
        magnitude=_effect_label(str(effect.get("level") or "unknown"), t),
    )
    return headline, detail


def _field_test_cards(protocol: dict[str, Any], t: TranslatorLike) -> str:
    runtime = protocol.get("runtime") or {}
    history = protocol.get("history") or {}
    gmcmap = protocol.get("gmcmap") or {}
    uptime_seconds = runtime.get("uptime_seconds")
    uptime_days = float(uptime_seconds) / 86400.0 if uptime_seconds is not None else None
    longest_gap_hours = float(history.get("longest_gap_seconds") or 0) / 3600.0
    export_url = './api/v1/field-test-protocol?device=' + quote_plus(str((protocol.get("device") or {}).get("serial") or ""))
    return f'''<div class="long-term-grid field-test-grid">
<article class="long-term-card"><strong>{html.escape(t('Runtime since service start'))}</strong><div class="long-term-value">{html.escape(_num(uptime_days, t.language, decimals=1, suffix=' d'))}</div><small>{html.escape(t('Cumulative counters reset when the service restarts.'))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('USB / serial recovery'))}</strong><div class="long-term-value">{html.escape(_num(runtime.get('serial_reconnect_count'), t.language, decimals=0))}</div><small>{html.escape(t('{errors} serial errors · {reconnects} reconnects', errors=int(runtime.get('serial_error_count') or 0), reconnects=int(runtime.get('serial_reconnect_count') or 0)))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('Longest data gap'))}</strong><div class="long-term-value">{html.escape(_num(longest_gap_hours, t.language, decimals=1, suffix=' h'))}</div><small>{html.escape(t('{count} detected gaps above the expected interval', count=int(history.get('gap_count') or 0)))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('Database write errors'))}</strong><div class="long-term-value">{html.escape(_num(runtime.get('history_write_error_count'), t.language, decimals=0))}</div><small>{html.escape(t('Stored samples: {count}', count=int(history.get('stored_samples') or 0)))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('GMCMap transmission'))}</strong><div class="long-term-value compact">{html.escape(t(str(gmcmap.get('status') or 'not configured')))}</div><small>{html.escape(t('{success} successful · {errors} failed uploads', success=int(gmcmap.get('successful_uploads') or 0), errors=int(gmcmap.get('upload_errors') or 0)))}</small></article>
</div>
<div class="field-test-actions"><a class="button" href="{html.escape(export_url, quote=True)}" download>{html.escape(t('Export field-test protocol (JSON)'))}</a></div>
<div class="note"><strong>{html.escape(t('Field-test interpretation'))}</strong><br>{html.escape(t('These operational counters help assess long-term reliability. They do not certify detector calibration or measurement accuracy.'))}</div>'''


def _environment_card(item: dict[str, Any], title: str, t: TranslatorLike) -> str:
    evidence = item.get("evidence") or {}
    if not item.get("available"):
        maximum_pairs = int(item.get("maximum_pairs") or 0)
        minimum_pairs = int(item.get("minimum_pairs") or 100)
        return (
            f'<article class="long-term-card pending"><div class="long-term-card-head"><strong>{html.escape(title)}</strong>{_evidence_badge(evidence, t)}</div>'
            f'<div class="long-term-value compact">{html.escape(t("Not enough paired data"))}</div>'
            f'<small>{html.escape(t("{available} of {required} required hourly pairs are available.", available=maximum_pairs, required=minimum_pairs))}</small></article>'
        )
    best = item.get("best") or {}
    correlation = float(best.get("correlation") or 0.0)
    strength = t("weak")
    if abs(correlation) >= 0.6:
        strength = t("strong")
    elif abs(correlation) >= 0.3:
        strength = t("moderate")
    fdr = best.get("p_value_fdr")
    fdr_text = t("FDR-adjusted p={value}", value=_num(fdr, t.language, decimals=3)) if fdr is not None else t("FDR-adjusted significance not available")
    return (
        f'<article class="long-term-card"><div class="long-term-card-head"><strong>{html.escape(title)}</strong>{_evidence_badge(evidence, t)}</div>'
        f'<div class="long-term-value">ρ = {html.escape(_num(correlation, t.language, decimals=2))}</div>'
        f'<small>{html.escape(t("Strongest at {lag} h lag · {pairs} pairs · {strength} association", lag=int(best.get("lag_hours") or 0), pairs=int(best.get("pairs") or 0), strength=strength))}</small>'
        f'<small>{html.escape(fdr_text)} · {html.escape(t("Correlation does not prove causation."))}</small></article>'
    )


def render_long_term_analysis(result: dict[str, Any], *, timezone, t: TranslatorLike, device_label: str) -> str:
    heading = t("Long-term analysis") if not device_label else t("Long-term analysis for {device}", device=device_label)
    if not result.get("available"):
        return (
            f'<section id="long-term-analysis" class="analysis-section long-term-analysis"><div class="analysis-heading">'
            f'<span class="analysis-device-badge device-generic">LT</span><h2>{html.escape(heading)}</h2></div>'
            f'<div class="note"><strong>{html.escape(t("No long-term analysis available yet"))}</strong><br>'
            f'{html.escape(t("Stored measurements are required before long-term statistics can be calculated."))}</div></section>'
        )

    windows = result.get("windows") or {}
    window_cards = "".join(_window_card(key, windows.get(key, {}), t) for key in ("24h", "7d", "30d", "90d", "365d"))
    background = result.get("background") or {}
    trend = result.get("trend") or {}
    dose = result.get("dose") or {}
    effective = result.get("effective_sample_size") or {}
    bootstrap = result.get("bootstrap") or {}
    control = result.get("control_chart") or {}
    overdispersion = result.get("overdispersion") or {}
    episodes = result.get("episodes") or {}
    threshold_time = result.get("threshold_time") or {}
    environment = result.get("environment") or {}
    field_test = result.get("field_test") or {}
    seasonal_evidence = result.get("seasonal_evidence") or {}

    trend_headline, trend_detail = _plain_trend_text(trend, t)
    trend_text = t("Not yet meaningful")
    if trend.get("available"):
        direction = t(str(trend.get("direction") or "stable"))
        trend_text = t(
            "{direction} · {slope} CPM/day · p={p}",
            direction=direction,
            slope=_num(trend.get("sen_slope_cpm_per_day"), t.language, decimals=3),
            p=_num(trend.get("p_value"), t.language, decimals=3),
        )
    bootstrap_mean = "—"
    bootstrap_median = "—"
    if bootstrap.get("available"):
        mean_ci = bootstrap.get("mean_ci95") or [None, None]
        median_ci = bootstrap.get("median_ci95") or [None, None]
        bootstrap_mean = f'{_num(mean_ci[0], t.language, decimals=2)}–{_num(mean_ci[1], t.language, decimals=2)} CPM'
        bootstrap_median = f'{_num(median_ci[0], t.language, decimals=2)}–{_num(median_ci[1], t.language, decimals=2)} CPM'

    projection = dose.get("annual_projection_usv")
    projection_text = (
        t("Annual projection from the last 90 days: {value} µSv", value=_num(projection, t.language, decimals=1))
        if projection is not None
        else t("Annual projection is not shown until a sufficiently complete 90-day period exists.")
    )
    threshold_total = sum(
        float(threshold_time.get(key) or 0.0)
        for key in ("below_warning_hours", "warning_hours", "danger_hours")
    )
    if threshold_total > 0:
        warning_share = 100.0 * float(threshold_time.get("warning_hours") or 0.0) / threshold_total
        danger_share = 100.0 * float(threshold_time.get("danger_hours") or 0.0) / threshold_total
    else:
        warning_share = danger_share = 0.0

    return f'''
<section id="long-term-analysis" class="analysis-section long-term-analysis">
<div class="analysis-heading"><span class="analysis-device-badge device-generic">LT</span><div><h2>{html.escape(heading)}</h2><p>{html.escape(t('Long-term background, cumulative dose, trend, recurring patterns and statistical process diagnostics'))}</p></div></div>
<div data-analysis-tier="summary">
<div class="plain-assessment" aria-label="{html.escape(t('Plain-language assessment'), quote=True)}">
<div class="plain-assessment-head"><div><strong>{html.escape(t('Plain-language assessment'))}</strong><small>{html.escape(t('The main result first; method details remain available below.'))}</small></div>{_evidence_badge(trend.get('evidence') or {}, t)}</div>
<div class="plain-assessment-grid">
<article><strong>{html.escape(t('Long-term trend'))}</strong><span>{html.escape(trend_headline)}</span><small>{html.escape(trend_detail)}</small></article>
<article><strong>{html.escape(t('Current background context'))}</strong><span>{html.escape(_num(background.get('recent_deviation_percent'), t.language, decimals=1, suffix='%'))}</span><small>{html.escape(t('Recent 7-day median relative to the robust long-term background'))}</small></article>
<article><strong>{html.escape(t('Data basis'))}</strong><span>{html.escape(_num(result.get('coverage_percent'), t.language, decimals=1, suffix='%'))}</span><small>{html.escape(t('{days} covered days · {observed} daily observations', days=_num(result.get('covered_days'), t.language, decimals=1), observed=int(effective.get('observations') or 0)))}</small></article>
</div></div>
<details class="analysis-group long-term-group" open><summary><span class="summary-copy">{html.escape(t('Long-term overview'))}<small>{html.escape(t('Real time windows with duration and coverage checks'))}</small></span></summary><div class="group-body">
<div class="long-term-window-grid">{window_cards}</div>
<div class="long-term-grid">
<article class="long-term-card"><strong>{html.escape(t('Robust local background'))}</strong><div class="long-term-value">{html.escape(_num(background.get('median_cpm'), t.language, decimals=2, suffix=' CPM'))}</div><small>{html.escape(t('Typical range P05–P95: {low}–{high} CPM', low=_num(background.get('p05_cpm'), t.language, decimals=1), high=_num(background.get('p95_cpm'), t.language, decimals=1)))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('Integrated derived dose in the measured period'))}</strong><div class="long-term-value">{html.escape(_num(dose.get('total_usv'), t.language, decimals=3, suffix=' µSv'))}</div><small>{html.escape(t('Based on {hours} covered hours', hours=_num(dose.get('covered_hours'), t.language, decimals=1)))}</small><small>{html.escape(projection_text)}</small></article>
<article class="long-term-card"><div class="long-term-card-head"><strong>{html.escape(t('Long-term trend'))}</strong>{_evidence_badge(trend.get('evidence') or {}, t)}</div><div class="long-term-value compact">{html.escape(trend_headline)}</div><small>{html.escape(trend_detail)}</small></article>
<article class="long-term-card"><strong>{html.escape(t('Seasonal assessment'))}</strong><div class="long-term-value compact">{html.escape(_evidence_label(str(seasonal_evidence.get('level') or 'not_evaluable'), t))}</div><small>{html.escape(t('{months} represented calendar months', months=int(seasonal_evidence.get('represented_months') or 0)))}</small></article>
</div></div></details>
</div>
<div data-analysis-tier="analysis">
<details class="analysis-group long-term-group"><summary><span class="summary-copy">{html.escape(t('Daily and monthly development'))}<small>{html.escape(t('Daily medians, rolling median and calendar view'))}</small></span></summary><div class="group-body">
{_trend_chart(result.get('daily') or [], t)}
<div><h3>{html.escape(t('Calendar heat map'))}</h3>{_calendar_heatmap(result.get('calendar') or [], background, t)}</div>
<div><h3>{html.escape(t('Monthly aggregates'))}</h3>{_monthly_table(result.get('monthly') or [], t)}</div>
<details class="analysis-group long-term-subgroup"><summary><span class="summary-copy">{html.escape(t('Seasonal month-of-year profile'))}<small>{html.escape(t('Median CPM by calendar month across available years'))}</small></span></summary><div class="group-body">{_seasonal_table(result.get('seasonal') or [], t)}</div></details>
</div></details>
<details class="analysis-group long-term-group"><summary><span class="summary-copy">{html.escape(t('Persistent elevation episodes'))}<small>{html.escape(t('Connected periods above the robust local long-term threshold'))}</small></span></summary><div class="group-body">
<div class="long-term-grid">
<article class="long-term-card"><strong>{html.escape(t('Relative event threshold'))}</strong><div class="long-term-value">{html.escape(_num(episodes.get('threshold_cpm'), t.language, decimals=1, suffix=' CPM'))}</div><small>{html.escape(t('Derived from the robust local background; not an official alarm threshold'))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('Persistent episodes'))}</strong><div class="long-term-value">{html.escape(_num(episodes.get('event_count'), t.language, decimals=0))}</div><small>{html.escape(t('{hours} total elevated hours · longest {longest} h', hours=_num(episodes.get('total_hours'), t.language, decimals=1), longest=_num(episodes.get('maximum_duration_hours'), t.language, decimals=1)))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('Time in configured warning range'))}</strong><div class="long-term-value">{html.escape(_num(warning_share, t.language, decimals=2, suffix='%'))}</div><small>{html.escape(t('{hours} covered hours', hours=_num(threshold_time.get('warning_hours'), t.language, decimals=1)))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('Time at or above configured danger threshold'))}</strong><div class="long-term-value">{html.escape(_num(danger_share, t.language, decimals=2, suffix='%'))}</div><small>{html.escape(t('{hours} covered hours', hours=_num(threshold_time.get('danger_hours'), t.language, decimals=1)))}</small></article>
</div>
{_episodes_table(episodes, timezone, t)}
</div></details>
</div>
<div data-analysis-tier="expert">
<details class="analysis-group long-term-group"><summary><span class="summary-copy">{html.escape(t('Extended statistical methods'))}<small>{html.escape(t('Confidence intervals, effective sample size, test statistics and practical effect size'))}</small></span></summary><div class="group-body">
<div class="long-term-grid">
<article class="long-term-card"><strong>{html.escape(t('Effective sample size'))}</strong><div class="long-term-value">{html.escape(_num(effective.get('effective'), t.language, decimals=1))}</div><small>{html.escape(t('{observed} daily observations · correlation duration {duration} days', observed=int(effective.get('observations') or 0), duration=_num(effective.get('correlation_days'), t.language, decimals=1)))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('Trend method details'))}</strong><div class="long-term-value compact">{html.escape(trend_text)}</div><small>{html.escape(t('Mann-Kendall test with Sen slope on sufficiently covered daily medians'))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('95% block-bootstrap interval for mean'))}</strong><div class="long-term-value compact">{html.escape(bootstrap_mean)}</div><small>{html.escape(t('Moving blocks preserve short-range time dependence'))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('95% block-bootstrap interval for median'))}</strong><div class="long-term-value compact">{html.escape(bootstrap_median)}</div><small>{html.escape(t('{replicates} replicates · block length {block} days', replicates=int(bootstrap.get('replicates') or 0), block=int(bootstrap.get('block_length') or 0)))}</small></article>
</div></div></details>
<details class="analysis-group long-term-group"><summary><span class="summary-copy">{html.escape(t('Statistical process diagnostics'))}<small>{html.escape(t('EWMA, CUSUM and dispersion diagnostics; statistical context only'))}</small></span></summary><div class="group-body">
<div class="long-term-grid">
<article class="long-term-card {'notice' if control.get('ewma_signal') else ''}"><strong>EWMA</strong><div class="long-term-value">{html.escape(_num(control.get('ewma_cpm'), t.language, decimals=2, suffix=' CPM'))}</div><small>{html.escape(t('Statistical signal detected') if control.get('ewma_signal') else t('No persistent EWMA signal detected'))}</small></article>
<article class="long-term-card {'notice' if control.get('cusum_signal') else ''}"><strong>CUSUM</strong><div class="long-term-value">{html.escape(_num(control.get('cusum_positive'), t.language, decimals=2))}</div><small>{html.escape(t('Statistical signal detected') if control.get('cusum_signal') else t('No persistent CUSUM signal detected'))}</small></article>
<article class="long-term-card"><strong>{html.escape(t('Hourly dispersion ratio'))}</strong><div class="long-term-value">{html.escape(_num(overdispersion.get('fano_like_ratio'), t.language, decimals=2))}</div><small>{html.escape(t('Contextual Fano-like ratio; rolling CPM values are not independent Poisson counts'))}</small></article>
</div>
<div class="note"><strong>{html.escape(t('Scientific interpretation'))}</strong><br>{html.escape(t('EWMA, CUSUM, trend tests and relative event detection provide statistical context only. They do not identify a radiation source and do not replace calibrated radiation-protection measurements.'))}</div>
</div></details>
<details class="analysis-group long-term-group"><summary><span class="summary-copy">{html.escape(t('Lagged environmental associations'))}<small>{html.escape(t('Exploratory Spearman correlations with false-discovery-rate correction'))}</small></span></summary><div class="group-body"><div class="long-term-grid">
{_environment_card(environment.get('temperature') or {}, t('Temperature association'), t)}
{_environment_card(environment.get('pressure') or {}, t('Air-pressure association'), t)}
</div><div class="note">{html.escape(t('Environmental correlations are exploratory. Benjamini-Hochberg correction reduces false discoveries across tested lags, but no causal conclusion is justified.'))}</div></div></details>
<details class="analysis-group long-term-group"><summary><span class="summary-copy">{html.escape(t('Long-term reliability field test'))}<small>{html.escape(t('Operational counters for USB, database continuity and GMCMap transmission'))}</small></span></summary><div class="group-body">{_field_test_cards(field_test, t)}</div></details>
</div>
</section>'''



def render_cached_long_term_analysis(
    application: Any,
    *,
    device_serial: str,
    scan_interval_seconds: int,
    cpm_per_usvh: float,
    device_label: str,
    translator: Any,
) -> str:
    """Build and render the cached long-term section for the dashboard.

    Keeping cache assembly here prevents the main report web module from
    growing another view-specific service implementation.
    """
    if not device_serial:
        return render_long_term_analysis(
            {"available": False, "device_serial": "", "windows": {}},
            timezone=application.timezone,
            t=translator,
            device_label=device_label,
        )
    thresholds = application._effective_safety_thresholds(cpm_per_usvh)
    key = (
        "long-term-analysis", application._data_revision()[:2], device_serial,
        scan_interval_seconds, cpm_per_usvh, application.timezone_name,
        float(thresholds["warning_cpm"]), float(thresholds["danger_cpm"]),
        int(application.store.retention_days),
    )
    result = application.analysis_cache.get_or_build(
        key,
        lambda: build_long_term_analysis(
            application.store,
            device_serial=device_serial,
            scan_interval_seconds=scan_interval_seconds,
            cpm_per_usvh=cpm_per_usvh,
            timezone_name=application.timezone_name,
            warning_cpm=float(thresholds["warning_cpm"]),
            danger_cpm=float(thresholds["danger_cpm"]),
            maximum_days=min(3650, max(365, int(application.store.retention_days))),
        ),
    )
    rendered_result = dict(result)
    rendered_result["field_test"] = build_field_test_protocol(
        application.store, device_serial=device_serial, timezone_name=application.timezone_name
    )
    return render_long_term_analysis(
        rendered_result, timezone=application.timezone, t=translator, device_label=device_label
    )


__all__ = ["render_cached_long_term_analysis", "render_long_term_analysis"]
