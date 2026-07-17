from __future__ import annotations

import html
import json
from datetime import UTC, datetime
from typing import Any, Protocol
from urllib.parse import quote_plus

from .backup_manager import ManagedBackup
from .workflow import CheckResult, PeriodComparison, WorkflowSettings


class TranslatorLike(Protocol):
    language: str

    def __call__(self, text: str, **values: object) -> str: ...


def _checked(value: bool) -> str:
    return " checked" if value else ""


def _format_time(timestamp: int | None, timezone) -> str:
    if not timestamp:
        return "—"
    return datetime.fromtimestamp(int(timestamp), UTC).astimezone(timezone).strftime("%Y-%m-%d %H:%M %Z")


def _metric(title: str, value: str, detail: str = "") -> str:
    return (
        '<div class="metric"><strong>' + html.escape(title) + '</strong>'
        '<div class="value">' + html.escape(value) + '</div>'
        + (f'<small>{html.escape(detail)}</small>' if detail else '') + '</div>'
    )


def _comparison_html(comparison: PeriodComparison, t: TranslatorLike) -> str:
    first = comparison.first
    second = comparison.second
    def shown(value: float | int | None, suffix: str = "") -> str:
        return "—" if value is None else f"{value:.2f}{suffix}" if isinstance(value, float) else f"{value}{suffix}"
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


def _history_chart(points: list[dict[str, Any]], raw_points: list[dict[str, Any]], annotations: list[dict[str, Any]], t: TranslatorLike) -> str:
    if len(points) < 2:
        return f'<div class="empty-state"><strong>{html.escape(t("No history data in this period"))}</strong></div>'
    values = [float(point.get("cpm") or 0.0) for point in points]
    minimum = min(values)
    maximum = max(values)
    span = maximum - minimum or 1.0
    coords: list[str] = []
    for index, value in enumerate(values):
        x = 3.0 + 94.0 * index / max(1, len(values) - 1)
        y = 35.0 - 29.0 * (value - minimum) / span
        coords.append(f"{x:.2f},{y:.2f}")
    start = int(points[0]["timestamp_utc"])
    end = int(points[-1]["timestamp_utc"])
    duration = max(1, end - start)
    raw_markers: list[str] = []
    for item in raw_points:
        timestamp = int(item.get("timestamp_utc") or start)
        value = float(item.get("cpm") or 0.0)
        x = 3.0 + 94.0 * max(0.0, min(1.0, (timestamp - start) / duration))
        y = 35.0 - 29.0 * max(0.0, min(1.0, (value - minimum) / span))
        raw_markers.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="0.8" class="raw-rejected-marker"><title>{value:.0f} CPM · {html.escape(str(item.get("gate_state") or ""))}</title></circle>')
    markers = []
    for item in annotations:
        timestamp = int(item.get("start_timestamp_utc") or start)
        x = 3.0 + 94.0 * max(0.0, min(1.0, (timestamp - start) / duration))
        markers.append(f'<line x1="{x:.2f}" y1="5" x2="{x:.2f}" y2="36" class="event-marker"><title>{html.escape(str(item.get("note") or ""))}</title></line>')
    return (
        '<figure class="workflow-history-chart"><svg viewBox="0 0 100 40" role="img" aria-label="'
        + html.escape(t("CPM history explorer"), quote=True) + '">'
        '<line x1="3" y1="36" x2="97" y2="36" class="chart-axis"/>'
        + ''.join(markers)
        + ''.join(raw_markers)
        + '<polyline points="' + ' '.join(coords) + '" class="chart-line" vector-effect="non-scaling-stroke"/>'
        '</svg><figcaption><span>' + html.escape(t("Minimum")) + f': {minimum:.1f} CPM</span>'
        '<span>' + html.escape(t("Maximum")) + f': {maximum:.1f} CPM</span>'
        + (f'<span>{html.escape(t("Rejected raw values"))}: {len(raw_points)}</span>' if raw_points else '')
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
        + html.escape(_format_time(int(item.get("created_utc") or 0), timezone))
        + f' · {int(item.get("size_bytes") or 0) / (1024 * 1024):.2f} MiB</small></div><div class="annotation-actions">'
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
        + html.escape(_format_time(item.created_utc, timezone)) + f' · {item.size_bytes / (1024 * 1024):.2f} MiB · {int(item.summary.get("measurements", 0)):,} '
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
        + html.escape(_format_time(int(item.get("start_timestamp_utc") or 0), timezone))
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
) -> str:
    annotation_rows = _render_annotation_rows(
        t=t,
        timezone=timezone,
        annotations=annotations,
        annotation_csrf=annotation_csrf,
    )
    return f"""
<section class="advanced-only history-section" id="history">
<h2>{html.escape(t("History"))}</h2>
<p>{html.escape(t("Explore accepted measurements and document events for the selected GMC device."))}</p>

<details class="analysis-group" id="history-event-notes"><summary><span class="summary-copy">{html.escape(t("Event notes"))}<small>{html.escape(t("Document ventilation, movement, maintenance or an unknown cause"))}</small></span></summary><div class="group-body">
<form method="post" action="?action=annotation-add" class="annotation-form"><input type="hidden" name="csrf_token" value="{html.escape(annotation_csrf, quote=True)}"><input type="hidden" name="device_serial" value="{html.escape(selected_serial, quote=True)}"><div class="annotation-form-grid">
<label>{html.escape(t("Start"))}<input type="datetime-local" name="start_local" required></label><label>{html.escape(t("End"))}<input type="datetime-local" name="end_local"></label>
<label>{html.escape(t("Category"))}<select name="category"><option value="window">{html.escape(t("Window opened"))}</option><option value="ventilation">{html.escape(t("Ventilation"))}</option><option value="device_moved">{html.escape(t("Device moved"))}</option><option value="maintenance">{html.escape(t("Maintenance"))}</option><option value="unknown">{html.escape(t("Unknown cause"))}</option><option value="other">{html.escape(t("Other"))}</option></select></label>
<label>{html.escape(t("Status"))}<select name="status"><option value="note">{html.escape(t("Note"))}</option><option value="confirmed">{html.escape(t("Confirmed"))}</option><option value="dismissed">{html.escape(t("Dismissed"))}</option></select></label>
<label class="annotation-note-field">{html.escape(t("Note"))}<textarea name="note" maxlength="2000" required></textarea></label></div><button class="primary" type="submit">{html.escape(t("Add event note"))}</button></form>
<div class="annotation-list">{annotation_rows}</div></div></details>

<details class="analysis-group" id="history-explorer" open><summary><span class="summary-copy">{html.escape(t("History explorer"))}<small>{html.escape(t("Accepted CPM values with event markers in a freely selected period"))}</small></span></summary><div class="group-body">
<form method="get" class="history-filter-form"><input type="hidden" name="device" value="{html.escape(selected_serial, quote=True)}"><input type="hidden" name="lang" value="{html.escape(t.language, quote=True)}"><input type="hidden" name="mode" value="advanced"><div class="comparison-form-grid"><label>{html.escape(t("History from"))}<input type="date" name="history_start" value="{html.escape(history_dates['start'], quote=True)}"></label><label>{html.escape(t("History to"))}<input type="date" name="history_end" value="{html.escape(history_dates['end'], quote=True)}"></label><label class="toggle-row"><input type="checkbox" name="history_raw" value="1"{_checked(show_raw_history)}><span>{html.escape(t("Show rejected raw values"))}</span></label><button class="primary" type="submit">{html.escape(t("Show period"))}</button></div></form>
{_history_chart(history_points, raw_history_points, annotations, t)}<div class="actions"><a class="button" href="./api/v1/history?device={quote_plus(selected_serial)}&amp;start_utc={history_start_utc}&amp;end_utc={history_end_utc}{'&amp;raw=1' if show_raw_history else ''}">{html.escape(t("Open history JSON"))}</a><a class="button" href="./api/v1/events?device={quote_plus(selected_serial)}&amp;start_utc={history_start_utc}&amp;end_utc={history_end_utc}">{html.escape(t("Open events JSON"))}</a></div></div></details>
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
    checks_html = "".join(
        '<div class="self-test-item '
        + html.escape(check.status, quote=True)
        + '"><span class="status-dot"></span><span><strong>'
        + html.escape(t(check.title_key))
        + "</strong><small>"
        + html.escape(t(check.detail_key, **dict(check.values)))
        + "</small></span></div>"
        for check in self_tests
        if check.key not in status_overview_checks
    )
    scheduler = automation_status.get("scheduler") if isinstance(automation_status.get("scheduler"), dict) else {}
    notifications = automation_status.get("notifications") if isinstance(automation_status.get("notifications"), dict) else {}
    schedule_detail = t("No scheduled report has run yet")
    latest_schedule = max(
        (int(scheduler.get(key) or 0) for key in ("last_daily_utc", "last_weekly_utc", "last_monthly_utc")),
        default=0,
    )
    if latest_schedule:
        schedule_detail = t("Last scheduled report: {time}", time=_format_time(latest_schedule, timezone))
    notification_detail = t("No notification has been sent yet")
    if notifications.get("last_notification_success_utc"):
        notification_detail = t(
            "Last notification: {time}",
            time=_format_time(int(notifications["last_notification_success_utc"]), timezone),
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
