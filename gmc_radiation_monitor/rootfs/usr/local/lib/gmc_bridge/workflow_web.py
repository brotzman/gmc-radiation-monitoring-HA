from __future__ import annotations

import html
import json
import statistics
from collections.abc import Mapping
from datetime import UTC, datetime, timedelta
from typing import Any, Protocol
from urllib.parse import quote_plus

from .backup_manager import ManagedBackup
from .number_format import format_number, localize_numeric_text, translator_language
from .workflow import CheckResult, PeriodComparison, WorkflowSettings


class TranslatorLike(Protocol):
    language: str

    def __call__(self, text: str, **values: object) -> str: ...


def _checked(value: bool) -> str:
    return " checked" if value else ""


def _format_time(timestamp: int | None, timezone, language: str = "en") -> str:
    if not timestamp:
        return "—"
    return datetime.fromtimestamp(int(timestamp), UTC).astimezone(timezone).strftime("%d.%m.%Y %H:%M %Z" if language == "de" else "%Y-%m-%d %H:%M %Z")


def _metric(title: str, value: str, detail: str = "") -> str:
    return (
        '<div class="metric"><strong>' + html.escape(title) + '</strong>'
        '<div class="value">' + html.escape(value) + '</div>'
        + (f'<small>{html.escape(detail)}</small>' if detail else '') + '</div>'
    )


def _comparison_html(comparison: PeriodComparison, t: TranslatorLike) -> str:
    first = comparison.first
    second = comparison.second
    language = translator_language(t)

    def shown(value: float | int | None, suffix: str = "") -> str:
        if value is None:
            return "—"
        return f"{format_number(value, language, decimals=2) if isinstance(value, float) else format_number(value, language, grouping=True)}{suffix}"
    interpretation = {
        "insufficient_data": t("Not enough data for a comparison"),
        "low_coverage": t("The comparison is only indicative because data coverage is low"),
        "no_clear_difference": t("No clear statistical difference is visible"),
        "possible_difference": t("A possible difference is visible and should be observed longer"),
        "clear_statistical_difference": t("A clear statistical difference is visible; this does not identify the physical cause"),
    }.get(comparison.interpretation, comparison.interpretation)
    return (
        '<div class="metrics comparison-results">'
        + _metric(t("First period mean"), shown(first.mean_cpm, " CPM"), t("{count} samples · {coverage:.1f}% coverage", count=first.samples, coverage=first.coverage_percent))
        + _metric(t("Second period mean"), shown(second.mean_cpm, " CPM"), t("{count} samples · {coverage:.1f}% coverage", count=second.samples, coverage=second.coverage_percent))
        + _metric(t("Mean difference"), shown(comparison.mean_difference_cpm, " CPM"), shown(comparison.mean_difference_percent, " %"))
        + _metric(t("Median difference"), shown(comparison.median_difference_cpm, " CPM"))
        + _metric(t("Statistical indication"), shown(comparison.z_indication), t("Difference divided by the combined standard error"))
        + '</div><div class="note">' + html.escape(interpretation) + '</div>'
    )


def _history_chart(
    points: list[dict[str, Any]],
    raw_points: list[dict[str, Any]],
    annotations: list[dict[str, Any]],
    timezone,
    t: TranslatorLike,
    *,
    data_mode: str = "raw",
) -> str:
    if len(points) < 2:
        return f'<div class="empty-state"><strong>{html.escape(t("No history data in this period"))}</strong></div>'
    raw_values = [float(point.get("raw_cpm", point.get("cpm")) or 0.0) for point in points]
    corrected_values = [float(point.get("corrected_cpm", point.get("cpm")) or 0.0) for point in points]
    values = corrected_values if data_mode == "corrected" else raw_values
    range_values = raw_values + corrected_values if data_mode == "comparison" else values
    minimum = min(range_values)
    maximum = max(range_values)
    span = maximum - minimum
    padding = max(1.0, span * 0.08)
    y_min = max(0.0, minimum - padding)
    y_max = maximum + padding
    y_span = max(1.0, y_max - y_min)
    start = int(points[0]["timestamp_utc"])
    end = int(points[-1]["timestamp_utc"])
    duration = max(1, end - start)

    def x_for(timestamp: int) -> float:
        return 13.0 + 101.0 * max(0.0, min(1.0, (timestamp - start) / duration))

    def y_for(value: float) -> float:
        return 42.0 - 35.0 * max(0.0, min(1.0, (value - y_min) / y_span))

    timestamps = [int(point["timestamp_utc"]) for point in points]
    intervals = [right - left for left, right in zip(timestamps, timestamps[1:]) if right > left]
    nominal_interval = statistics.median(intervals) if intervals else 60.0
    gap_threshold = max(300.0, nominal_interval * 3.0)
    segment_ranges: list[tuple[int, int]] = []
    gap_bands: list[str] = []
    segment_start = 0
    for index in range(1, len(points)):
        gap = timestamps[index] - timestamps[index - 1]
        if gap <= gap_threshold:
            continue
        segment_ranges.append((segment_start, index))
        left_x = x_for(timestamps[index - 1])
        right_x = x_for(timestamps[index])
        start_label = datetime.fromtimestamp(timestamps[index - 1], UTC).astimezone(timezone).strftime("%d.%m.%Y %H:%M")
        end_label = datetime.fromtimestamp(timestamps[index], UTC).astimezone(timezone).strftime("%d.%m.%Y %H:%M")
        gap_bands.append(
            f'<rect x="{left_x:.2f}" y="7" width="{max(0.35, right_x-left_x):.2f}" height="35" class="history-gap-band">'
            f'<title>{html.escape(t("No measurement data between {start} and {end}", start=start_label, end=end_label))}</title></rect>'
        )
        segment_start = index
    segment_ranges.append((segment_start, len(points)))

    def segmented_polylines(series: list[float], css_class: str) -> str:
        fragments: list[str] = []
        for first, last in segment_ranges:
            if last - first < 2:
                continue
            coords = [
                f"{x_for(timestamps[index]):.2f},{y_for(series[index]):.2f}"
                for index in range(first, last)
            ]
            fragments.append(
                '<polyline points="' + ' '.join(coords) + f'" class="{css_class}" vector-effect="non-scaling-stroke"/>'
            )
        return ''.join(fragments)

    smooth_window = max(3, min(21, len(values) // 24 or 3))
    smooth_values = list(values)
    for first, last in segment_ranges:
        for index in range(first, last):
            window_start = max(first, index - smooth_window + 1)
            window = values[window_start : index + 1]
            smooth_values[index] = sum(window) / len(window)
    accepted_lines = segmented_polylines(values, "chart-line history-accepted-line")
    corrected_lines = segmented_polylines(corrected_values, "history-corrected-line") if data_mode == "comparison" else ""
    trend_lines = segmented_polylines(smooth_values, "history-trend-line")

    y_grid: list[str] = []
    for index in range(5):
        value = y_min + (y_max - y_min) * index / 4
        y = y_for(value)
        y_grid.append(
            f'<line x1="13" y1="{y:.2f}" x2="114" y2="{y:.2f}" class="history-grid-line"/>'
            f'<text x="11.2" y="{y + 0.9:.2f}" text-anchor="end" class="history-axis-label">{format_number(value, translator_language(t), decimals=1)}</text>'
        )
    x_grid: list[str] = []
    for fraction in (0.0, 0.5, 1.0):
        timestamp = start + round(duration * fraction)
        x = x_for(timestamp)
        label = datetime.fromtimestamp(timestamp, UTC).astimezone(timezone).strftime("%d.%m.%Y %H:%M")
        anchor = "start" if fraction == 0 else "end" if fraction == 1 else "middle"
        x_grid.append(
            f'<line x1="{x:.2f}" y1="7" x2="{x:.2f}" y2="42" class="history-grid-line"/>'
            f'<text x="{x:.2f}" y="46.3" text-anchor="{anchor}" class="history-axis-label">{html.escape(label)}</text>'
        )

    raw_markers: list[str] = []
    for item in raw_points:
        timestamp = int(item.get("timestamp_utc") or start)
        value = float(item.get("cpm") or 0.0)
        raw_markers.append(
            f'<circle cx="{x_for(timestamp):.2f}" cy="{y_for(value):.2f}" r="0.72" class="raw-rejected-marker">'
            f'<title>{format_number(value, translator_language(t), decimals=0)} CPM · {html.escape(str(item.get("gate_state") or ""))}</title></circle>'
        )
    markers: list[str] = []
    for item in annotations:
        timestamp = int(item.get("start_timestamp_utc") or start)
        markers.append(
            f'<line x1="{x_for(timestamp):.2f}" y1="7" x2="{x_for(timestamp):.2f}" y2="42" class="event-marker">'
            f'<title>{html.escape(str(item.get("note") or ""))}</title></line>'
        )
    mean = sum(values) / len(values)
    return (
        '<figure class="workflow-history-chart">'
        + '<div class="chart-actions"><span>' + html.escape(t("Chart controls")) + '</span>'
        + '<button type="button" class="button" data-chart-reset>' + html.escape(t("Reset view")) + '</button>'
        + '<button type="button" class="button" data-chart-download>' + html.escape(t("Download SVG")) + '</button></div>'
        + '<svg viewBox="0 0 120 54" role="img" aria-label="'
        + html.escape(t("CPM history explorer"), quote=True)
        + '">'
        + ''.join(y_grid)
        + ''.join(x_grid)
        + '<line x1="13" y1="42" x2="114" y2="42" class="chart-axis"/>'
        + '<line x1="13" y1="7" x2="13" y2="42" class="chart-axis"/>'
        + ''.join(gap_bands)
        + ''.join(markers)
        + ''.join(raw_markers)
        + accepted_lines
        + corrected_lines
        + trend_lines
        + f'<text x="63.5" y="52.2" text-anchor="middle" class="history-axis-title">{html.escape(t("Local date and time"))}</text>'
        + f'<text x="2.2" y="24.5" text-anchor="middle" transform="rotate(-90 2.2 24.5)" class="history-axis-title">{html.escape(t("Count rate [CPM]"))}</text>'
        + '</svg><figcaption>'
        + f'<span>{html.escape(t("Minimum"))}: {format_number(minimum, translator_language(t), decimals=1)} CPM</span>'
        + f'<span>{html.escape(t("Mean"))}: {format_number(mean, translator_language(t), decimals=1)} CPM</span>'
        + f'<span>{html.escape(t("Maximum"))}: {format_number(maximum, translator_language(t), decimals=1)} CPM</span>'
        + (f'<span>{html.escape(t("Rejected raw values"))}: {format_number(len(raw_points), translator_language(t), grouping=True)}</span>' if raw_points else '')
        + '</figcaption></figure>'
    )


def render_scheduled_reports(
    *,
    t: TranslatorLike,
    timezone,
    reports: list[dict[str, Any]],
    csrf_token: str,
) -> str:
    """Render scheduled report files beside the manual report downloads."""
    delete_confirmation = html.escape(json.dumps(t("Delete this generated report?"), ensure_ascii=False), quote=True)
    rows = ''.join(
        '<div class="managed-backup-row"><div><strong>' + html.escape(str(item.get("name") or "")) + '</strong><small>'
        + html.escape(_format_time(int(item.get("created_utc") or 0), timezone, t.language))
        + f' · {format_number(int(item.get("size_bytes") or 0) / (1024 * 1024), t.language, decimals=2)} MiB</small></div><div class="annotation-actions">'
        + f'<a class="button" href="?action=scheduled-report-download&amp;name={quote_plus(str(item.get("name") or ""))}">{html.escape(t("Download"))}</a>'
        + f'<form method="post" action="?action=scheduled-report-delete" onsubmit="return confirm({delete_confirmation});">'
        + f'<input type="hidden" name="csrf_token" value="{html.escape(csrf_token, quote=True)}">'
        + f'<input type="hidden" name="name" value="{html.escape(str(item.get("name") or ""), quote=True)}">'
        + f'<button type="submit" class="danger">{html.escape(t("Delete"))}</button></form>'
        + '</div></div>'
        for item in reports
    ) or f'<div class="note">{html.escape(t("No generated report files are available."))}</div>'
    return (
        '<div class="generated-reports" id="generated-reports">'
        f'<h3>{html.escape(t("Generated reports"))}</h3>'
        f'<div class="managed-backup-list">{rows}</div></div>'
    )


def render_managed_backups(
    *,
    t: TranslatorLike,
    timezone,
    backups: list[ManagedBackup],
    comparison: dict[str, Any] | None,
    csrf_token: str,
) -> str:
    """Render all SQLite snapshot actions in the maintenance area."""
    rows = ''.join(
        '<div class="managed-backup-row"><div><strong>' + html.escape(item.name) + '</strong><small>'
        + html.escape(_format_time(item.created_utc, timezone, t.language)) + f' · {format_number(item.size_bytes / (1024 * 1024), t.language, decimals=2)} MiB · {format_number(int(item.summary.get("measurements", 0)), t.language, grouping=True)} '
        + html.escape(t("measurements")) + '</small></div><div class="annotation-actions">'
        f'<a class="button" href="?action=managed-backup-download&amp;name={quote_plus(item.name)}">{html.escape(t("Download"))}</a>'
        f'<form method="post" action="?action=managed-backup-delete"><input type="hidden" name="csrf_token" value="{html.escape(csrf_token, quote=True)}"><input type="hidden" name="name" value="{html.escape(item.name, quote=True)}"><button type="submit" class="danger">{html.escape(t("Delete"))}</button></form>'
        '</div></div>'
        for item in backups
    ) or f'<div class="note">{html.escape(t("No managed backups are available."))}</div>'
    comparison_html = ""
    if comparison:
        first_name = str((comparison.get("first") or {}).get("name") or "")
        second_name = str((comparison.get("second") or {}).get("name") or "")
        comparison_html = (
            '<div class="note"><strong>' + html.escape(t("Latest backup comparison")) + '</strong><br>'
            + html.escape(t(
                "{first} compared with {second}: {measurements:+d} measurements, {raw:+d} raw measurements",
                first=first_name,
                second=second_name,
                measurements=int(comparison.get("measurement_difference") or 0),
                raw=int(comparison.get("raw_measurement_difference") or 0),
            ))
            + '</div>'
        )
    return (
        '<div class="maintenance-subsection" id="managed-backups">'
        f'<h3>{html.escape(t("Managed backups"))}</h3>'
        f'<p>{html.escape(t("Create, inspect, compare, download and prune local SQLite snapshots"))}</p>'
        f'<form method="post" action="?action=managed-backup-create"><input type="hidden" name="csrf_token" value="{html.escape(csrf_token, quote=True)}"><button class="primary" type="submit">{html.escape(t("Create managed backup"))}</button></form>'
        f'{comparison_html}<div class="managed-backup-list">{rows}</div></div>'
    )


def _render_annotation_rows(
    *,
    t: TranslatorLike,
    timezone,
    annotations: list[dict[str, Any]],
    annotation_csrf: str,
) -> str:
    category_labels = {
        "window": "Window opened",
        "ventilation": "Ventilation",
        "device_moved": "Device moved",
        "maintenance": "Maintenance",
        "unknown": "Unknown cause",
        "other": "Other",
    }
    status_labels = {"note": "Note", "confirmed": "Confirmed", "dismissed": "Dismissed"}
    return "".join(
        '<div class="annotation-row"><div><strong>'
        + html.escape(t(category_labels.get(str(item.get("category") or "other"), "Other")))
        + "</strong><small>"
        + html.escape(_format_time(int(item.get("start_timestamp_utc") or 0), timezone, t.language))
        + " · "
        + html.escape(t(status_labels.get(str(item.get("status") or "note"), "Note")))
        + "</small><p>"
        + html.escape(str(item.get("note") or ""))
        + '</p></div><div class="annotation-actions">'
        + f'<form method="post" action="?action=annotation-status"><input type="hidden" name="csrf_token" value="{html.escape(annotation_csrf, quote=True)}"><input type="hidden" name="annotation_id" value="{int(item.get("id") or 0)}"><input type="hidden" name="status" value="confirmed"><button type="submit">{html.escape(t("Confirm"))}</button></form>'
        + f'<form method="post" action="?action=annotation-status"><input type="hidden" name="csrf_token" value="{html.escape(annotation_csrf, quote=True)}"><input type="hidden" name="annotation_id" value="{int(item.get("id") or 0)}"><input type="hidden" name="status" value="dismissed"><button type="submit">{html.escape(t("Dismiss"))}</button></form>'
        + f'<form method="post" action="?action=annotation-delete" onsubmit="return confirm(\'{html.escape(t("Delete this annotation?"), quote=True)}\');"><input type="hidden" name="csrf_token" value="{html.escape(annotation_csrf, quote=True)}"><input type="hidden" name="annotation_id" value="{int(item.get("id") or 0)}"><button type="submit" class="danger">{html.escape(t("Delete"))}</button></form>'
        + "</div></div>"
        for item in annotations
    ) or f'<div class="note">{html.escape(t("No annotations have been added yet."))}</div>'


def render_history_section(
    *,
    t: TranslatorLike,
    timezone,
    selected_serial: str,
    annotation_csrf: str,
    annotations: list[dict[str, Any]],
    history_points: list[dict[str, Any]],
    raw_history_points: list[dict[str, Any]],
    show_raw_history: bool,
    history_dates: dict[str, str],
    history_start_utc: int,
    history_end_utc: int,
    history_summary: dict[str, Any],
    data_mode: str = "raw",
) -> str:
    annotation_rows = _render_annotation_rows(
        t=t,
        timezone=timezone,
        annotations=annotations,
        annotation_csrf=annotation_csrf,
    )
    end_date = datetime.fromisoformat(history_dates["end"]).date()
    range_links: list[str] = []
    for days, label in ((1, "24 h"), (7, "7 days"), (30, "30 days"), (90, "90 days")):
        start_date = end_date - timedelta(days=max(1, days) - 1)
        href = (
            f"?device={quote_plus(selected_serial)}&lang={quote_plus(t.language)}&mode=advanced"
            f"&history_start={start_date.isoformat()}&history_end={end_date.isoformat()}"
            + ("&history_raw=1" if show_raw_history else "")
            + f"&data_mode={quote_plus(data_mode)}#history-explorer"
        )
        range_links.append(f'<a class="history-range-button" href="{html.escape(href, quote=True)}">{html.escape(t(label))}</a>')

    def shown(value: Any, *, decimals: int = 1, suffix: str = "") -> str:
        if value is None:
            return "—"
        return f"{format_number(float(value), t.language, decimals=decimals)}{suffix}"

    summary_metrics = (
        _metric(t("Accepted measurements"), format_number(int(history_summary.get('samples') or 0), t.language, grouping=True), t("Selected period"))
        + _metric(t("Data coverage"), shown(history_summary.get("coverage_percent"), decimals=1, suffix="%"), t("Expected from the configured scan interval"))
        + _metric(t("Mean count rate"), shown(history_summary.get("mean_cpm"), decimals=1, suffix=" CPM"), t("Accepted values only"))
        + _metric(t("Median count rate"), shown(history_summary.get("median_cpm"), decimals=1, suffix=" CPM"), t("Robust center of the selected period"))
        + _metric(t("Minimum / maximum"), f"{shown(history_summary.get('minimum_cpm'), decimals=1)} / {shown(history_summary.get('maximum_cpm'), decimals=1)} CPM", t("Accepted values only"))
        + _metric(t("Rejected raw values"), (format_number(int(history_summary['rejected_raw_count']), t.language, grouping=True) if history_summary.get('rejected_raw_count') is not None else "—"), t("Visible only when the raw-value layer is enabled"))
    )
    return f"""
<section class="advanced-only history-section" id="history">
<div class="history-section-heading"><div><h2>{html.escape(t("History"))}</h2><p>{html.escape(t("Explore, compare and document accepted measurements for the selected GMC device."))}</p></div><div class="history-period-label"><strong>{html.escape(history_dates['start'])}</strong><span>→</span><strong>{html.escape(history_dates['end'])}</strong></div></div>

<details class="analysis-group" id="history-explorer" open><summary><span class="summary-copy">{html.escape(t("History explorer"))}<small>{html.escape(t("Accepted count rates, smoothed trend, rejected raw values and event markers"))}</small></span></summary><div class="group-body">
<form method="get" class="history-filter-form"><input type="hidden" name="device" value="{html.escape(selected_serial, quote=True)}"><input type="hidden" name="lang" value="{html.escape(t.language, quote=True)}"><input type="hidden" name="mode" value="advanced"><div class="history-filter-grid"><label>{html.escape(t("History from"))}<input type="date" name="history_start" value="{html.escape(history_dates['start'], quote=True)}"></label><label>{html.escape(t("History to"))}<input type="date" name="history_end" value="{html.escape(history_dates['end'], quote=True)}"></label><label>{html.escape(t("Data mode"))}<select name="data_mode"><option value="raw"{" selected" if data_mode == "raw" else ""}>{html.escape(t("Raw data"))}</option><option value="corrected"{" selected" if data_mode == "corrected" else ""}>{html.escape(t("Dead-time corrected"))}</option><option value="comparison"{" selected" if data_mode == "comparison" else ""}>{html.escape(t("Raw and corrected comparison"))}</option></select></label><label class="toggle-row history-raw-toggle"><input type="checkbox" name="history_raw" value="1"{_checked(show_raw_history)}><span>{html.escape(t("Show rejected raw values"))}</span></label><button class="primary" type="submit">{html.escape(t("Show period"))}</button></div><div class="history-quick-ranges"><span>{html.escape(t("Quick ranges"))}</span>{''.join(range_links)}</div></form>
<div class="metrics history-summary-metrics">{summary_metrics}</div>
{_history_chart(history_points, raw_history_points, annotations, timezone, t, data_mode=data_mode)}
<div class="history-chart-help"><span class="history-key accepted"></span>{html.escape(t("Raw CPM") if data_mode != "corrected" else t("Corrected CPM"))}{'<span class="history-key corrected"></span>' + html.escape(t("Corrected CPM")) if data_mode == "comparison" else ''}<span class="history-key trend"></span>{html.escape(t("Smoothed trend"))}<span class="history-key event"></span>{html.escape(t("Event note"))}<span class="history-key rejected"></span>{html.escape(t("Rejected raw value"))}</div>
<div class="actions"><a class="button" href="./api/v1/history?device={quote_plus(selected_serial)}&amp;start_utc={history_start_utc}&amp;end_utc={history_end_utc}{'&amp;raw=1' if show_raw_history else ''}">{html.escape(t("Open history JSON"))}</a><a class="button" href="./api/v1/events?device={quote_plus(selected_serial)}&amp;start_utc={history_start_utc}&amp;end_utc={history_end_utc}">{html.escape(t("Open events JSON"))}</a></div></div></details>

<details class="analysis-group" id="history-event-notes"><summary><span class="summary-copy">{html.escape(t("Event notes"))}<small>{html.escape(t("Document movement, maintenance, shielding changes or an unknown cause"))}</small></span></summary><div class="group-body">
<form method="post" action="?action=annotation-add" class="annotation-form"><input type="hidden" name="csrf_token" value="{html.escape(annotation_csrf, quote=True)}"><input type="hidden" name="device_serial" value="{html.escape(selected_serial, quote=True)}"><div class="annotation-form-grid">
<label>{html.escape(t("Start"))}<input type="datetime-local" name="start_local" required></label><label>{html.escape(t("End"))}<input type="datetime-local" name="end_local"></label>
<label>{html.escape(t("Category"))}<select name="category"><option value="window">{html.escape(t("Window opened"))}</option><option value="ventilation">{html.escape(t("Ventilation"))}</option><option value="device_moved">{html.escape(t("Device moved"))}</option><option value="maintenance">{html.escape(t("Maintenance"))}</option><option value="unknown">{html.escape(t("Unknown cause"))}</option><option value="other">{html.escape(t("Other"))}</option></select></label>
<label>{html.escape(t("Status"))}<select name="status"><option value="note">{html.escape(t("Note"))}</option><option value="confirmed">{html.escape(t("Confirmed"))}</option><option value="dismissed">{html.escape(t("Dismissed"))}</option></select></label>
<label class="annotation-note-field">{html.escape(t("Note"))}<textarea name="note" maxlength="2000" required></textarea></label></div><button class="primary" type="submit">{html.escape(t("Add event note"))}</button></form>
<div class="annotation-list">{annotation_rows}</div></div></details>
</section>
"""


def render_workflow_section(
    *,
    t: TranslatorLike,
    timezone,
    selected_serial: str,
    device_options: list[tuple[str, str]],
    settings: WorkflowSettings,
    settings_csrf: str,
    comparison: PeriodComparison,
    comparison_dates: dict[str, str],
    self_tests: list[CheckResult],
    automation_status: dict[str, Any],
) -> str:
    device_select = "".join(
        f'<option value="{html.escape(serial, quote=True)}"{" selected" if serial == selected_serial else ""}>{html.escape(label)}</option>'
        for serial, label in device_options
    )
    status_overview_checks = {"database", "devices", "connections", "freshness"}
    check_cards: list[str] = []
    for check in self_tests:
        if check.key in status_overview_checks:
            continue
        problem_values = check.values.get("problems") if isinstance(check.values, Mapping) else None
        problem_rows = ""
        if isinstance(problem_values, list) and problem_values:
            problem_rows = '<ul class="self-test-problems">' + "".join(
                f'<li>{html.escape(str(problem))}</li>' for problem in problem_values
            ) + "</ul>"
        check_cards.append(
            '<div class="self-test-item '
            + html.escape(check.status, quote=True)
            + '"><span class="status-dot"></span><span><strong>'
            + html.escape(t(check.title_key))
            + "</strong><small>"
            + html.escape(t(check.detail_key, **dict(check.values)))
            + "</small>"
            + problem_rows
            + "</span></div>"
        )
    checks_html = "".join(check_cards)
    scheduler = automation_status.get("scheduler") if isinstance(automation_status.get("scheduler"), dict) else {}
    notifications = automation_status.get("notifications") if isinstance(automation_status.get("notifications"), dict) else {}
    schedule_detail = t("No scheduled report has run yet")
    latest_schedule = max(
        (int(scheduler.get(key) or 0) for key in ("last_daily_utc", "last_weekly_utc", "last_monthly_utc")),
        default=0,
    )
    if latest_schedule:
        schedule_detail = t("Last scheduled report: {time}", time=_format_time(latest_schedule, timezone, t.language))
    notification_detail = t("No notification has been sent yet")
    if notifications.get("last_notification_success_utc"):
        notification_detail = t(
            "Last notification: {time}",
            time=_format_time(int(notifications["last_notification_success_utc"]), timezone, t.language),
        )
    return f"""
<section class="advanced-only workflow-section" id="workflow">
<h2>{html.escape(t("Workflows and operations"))}</h2>
<p>{html.escape(t("Notifications, comparisons, self-tests and JSON APIs work with the existing measurements and require no additional hardware."))}</p>

<details class="analysis-group" id="workflow-notifications"><summary><span class="summary-copy">{html.escape(t("Notifications and scheduled reports"))}<small>{html.escape(notification_detail)} · {html.escape(schedule_detail)}</small></span></summary><div class="group-body">
<form method="post" action="?action=workflow-settings" class="workflow-settings-form">
<input type="hidden" name="csrf_token" value="{html.escape(settings_csrf, quote=True)}">
<div class="workflow-settings-grid">
<label class="toggle-row"><input type="checkbox" name="notifications_enabled" value="true"{_checked(settings.notifications_enabled)}><span>{html.escape(t("Enable Home Assistant notifications"))}</span></label>
<label class="toggle-row"><input type="checkbox" name="notify_device_offline" value="true"{_checked(settings.notify_device_offline)}><span>{html.escape(t("Notify when a device stays offline"))}</span></label>
<label class="toggle-row"><input type="checkbox" name="notify_data_stale" value="true"{_checked(settings.notify_data_stale)}><span>{html.escape(t("Notify when accepted measurements become stale"))}</span></label>
<label class="toggle-row"><input type="checkbox" name="notify_confirmed_event" value="true"{_checked(settings.notify_confirmed_event)}><span>{html.escape(t("Notify about confirmed warning events"))}</span></label>
<label class="toggle-row"><input type="checkbox" name="notify_database_problem" value="true"{_checked(settings.notify_database_problem)}><span>{html.escape(t("Notify about database integrity problems"))}</span></label>
<label>{html.escape(t("Offline threshold in minutes"))}<input type="number" name="offline_minutes" min="2" max="1440" value="{settings.offline_minutes}"></label>
<label>{html.escape(t("Stale-data threshold in minutes"))}<input type="number" name="stale_minutes" min="2" max="1440" value="{settings.stale_minutes}"></label>
<label>{html.escape(t("Notification cooldown in minutes"))}<input type="number" name="cooldown_minutes" min="15" max="10080" value="{settings.cooldown_minutes}"></label>
<label class="toggle-row"><input type="checkbox" name="scheduled_reports_enabled" value="true"{_checked(settings.scheduled_reports_enabled)}><span>{html.escape(t("Enable scheduled reports"))}</span></label>
<label class="toggle-row"><input type="checkbox" name="daily_report" value="true"{_checked(settings.daily_report)}><span>{html.escape(t("Daily ZIP reports"))}</span></label>
<label class="toggle-row"><input type="checkbox" name="weekly_report" value="true"{_checked(settings.weekly_report)}><span>{html.escape(t("Weekly ZIP reports"))}</span></label>
<label class="toggle-row"><input type="checkbox" name="monthly_summary" value="true"{_checked(settings.monthly_summary)}><span>{html.escape(t("Monthly JSON summaries"))}</span></label>
<label>{html.escape(t("Report hour"))}<input type="number" name="report_hour" min="0" max="23" value="{settings.report_hour}"></label>
<label>{html.escape(t("Managed backups to retain"))}<input type="number" name="managed_backup_retention" min="1" max="50" value="{settings.managed_backup_retention}"></label>
</div><button class="primary" type="submit">{html.escape(t("Save workflow settings"))}</button></form></div></details>

<details class="analysis-group" id="workflow-comparison"><summary><span class="summary-copy">{html.escape(t("Compare periods"))}<small>{html.escape(t("Compare two freely selected date ranges"))}</small></span></summary><div class="group-body">
<form method="get" class="comparison-form"><input type="hidden" name="device" value="{html.escape(selected_serial, quote=True)}"><input type="hidden" name="lang" value="{html.escape(t.language, quote=True)}"><input type="hidden" name="mode" value="advanced"><div class="comparison-form-grid">
<label>{html.escape(t("Device"))}<select name="compare_device">{device_select}</select></label>
<label>{html.escape(t("First period from"))}<input type="date" name="first_start" value="{html.escape(comparison_dates['first_start'], quote=True)}"></label>
<label>{html.escape(t("First period to"))}<input type="date" name="first_end" value="{html.escape(comparison_dates['first_end'], quote=True)}"></label>
<label>{html.escape(t("Second period from"))}<input type="date" name="second_start" value="{html.escape(comparison_dates['second_start'], quote=True)}"></label>
<label>{html.escape(t("Second period to"))}<input type="date" name="second_end" value="{html.escape(comparison_dates['second_end'], quote=True)}"></label>
<button class="primary" type="submit">{html.escape(t("Compare"))}</button></div></form>{_comparison_html(comparison, t)}</div></details>

<details class="analysis-group" id="workflow-self-test"><summary><span class="summary-copy">{html.escape(t("System self-test"))}<small>{html.escape(t("Additional diagnostics not shown in the status overview"))}</small></span></summary><div class="group-body"><div class="self-test-grid">{checks_html}</div><a class="button" href="./api/v1/self-test">{html.escape(t("Open self-test JSON"))}</a></div></details>

<details class="analysis-group" id="workflow-apis"><summary><span class="summary-copy">{html.escape(t("Machine-readable APIs"))}<small>{html.escape(t("Use the same structured results in Home Assistant automations or external dashboards"))}</small></span></summary><div class="group-body"><div class="actions"><a class="button" href="./api/v1/status">{html.escape(t("Status API"))}</a><a class="button" href="./api/v1/analysis?device={quote_plus(selected_serial)}">{html.escape(t("Analysis API"))}</a><a class="button" href="./api/v1/comparison?device={quote_plus(selected_serial)}">{html.escape(t("Comparison API"))}</a><a class="button" href="./api/v1/backups">{html.escape(t("Backups API"))}</a></div></div></details>
</section>
"""
