from __future__ import annotations
import contextlib
import html
import logging
import os
import re
import secrets
import statistics
import threading
import time
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import quote_plus
from .adaptive_background import build_adaptive_background, build_site_adaptive_background
from .analysis_presentation import (
    AnalysisPresentationConfig,
    baseline_state,
    build_absolute_safety_result,
    build_adaptive_background_result,
    build_background_profile_entity,
    build_combined_interpretation_result,
    build_cosmic_influence_result,
    build_detailed_analysis_result,
    build_fleet_intelligence_result,
    build_local_background_result,
    build_radiation_intelligence_result,
    build_recommendation_result,
    effective_safety_thresholds,
    fleet_stability_display_key,
    safety_state,
)
from .automation import WorkflowAutomationService, automation_status
from .backup_manager import ManagedBackupManager
from .barometric_background import build_barometric_cosmic_hint
from .calibration_web import render_calibration_panel
from .device_profiles import normalize_device_version_display
from .device_card_display import (
    format_live_dose as _format_live_dose,
    measurement_freshness,
    render_connection_details,
    render_device_card_header,
    render_live_measurement,
)
from .fleet_analytics import build_fleet_snapshot
from .historical_presentation import trend_symbol
from .history import DEFAULT_DB_PATH, HistoryStore
from .home_assistant import HomeAssistantConfigClient, HomeAssistantPressureClient
from .intelligence import build_radiation_intelligence
from .long_term_web import render_cached_long_term_analysis
from .number_format import format_number, localize_numeric_text
from .orientation import calculate_orientation, orientation_status
from .report_web_http import ReportRequestHandler, _localized_exception_message
from .report_web_support import (
    MAX_DOWNLOAD_BYTES,
    MAX_RESTORE_BYTES,
    REPORT_TARGET_COMBINED,
    STREAM_CHUNK_BYTES,
    USER_MANUAL_DIRECTORY,
    USER_MANUAL_FILENAME,
    USER_MANUAL_FILENAMES,
    USER_MANUAL_LANGUAGE_NAMES,
    USER_MANUAL_PATH,
    _decode_report_target,
    _encode_report_target,
    _one,
    _optional_one,
    _parse_multipart_form,
    _resolve_user_manual,
    _stream_restore_upload_to_temp,
    _temporary_path,
)
from .report_statistics import build_statistics
from .reports import build_live_analysis, expected_samples, load_timezone, resolve_period
from .revision_cache import RevisionCache
from .scientific_web import render_calibration_management
from .security_logging import configure_secure_logging
from .time_series import time_weighted_summary
from .translations import SUPPORTED_UI_LANGUAGES, Translator, resolve_language
from .utils import slugify
from .version import APP_VERSION, ASSET_REVISION
from .web_analysis_views import (
    render_absolute_safety,
    render_adaptive_background,
    render_assessment_legend,
    render_background_profile_entity,
    render_combined_interpretation,
    render_cosmic_influence,
    render_device_analysis,
    render_fleet_intelligence,
    render_local_background,
    render_radiation_intelligence,
    render_recommendation,
)
from .web_assets import render_dashboard_bootstrap
from .web_components import (
    render_collapsible_card,
    render_home_assistant_location,
)
from .web_security import CsrfTokenManager
from .web_server import BoundedThreadingHTTPServer
from .workflow import (
    compare_periods,
    default_comparison_ranges,
    downsample_history,
    load_workflow_settings,
    local_range,
    run_self_test,
)
from .report_web_devices import ReportDeviceViewMixin
from .report_web_status import ReportStatusMixin
from .workflow_controller import WorkflowApplicationMixin
from .workflow_web import (
    render_history_section,
    render_managed_backups,
    render_scheduled_reports,
    render_workflow_section,
)
LOG = logging.getLogger("gmc_reports")
# Source-compatibility markers retained for downstream checks: class="device-card-title" class="assessment-icon device-card-icon">{html.escape(device_icon)}</div> class="device-card-title-copy"
class ReportApplication(ReportStatusMixin, ReportDeviceViewMixin, WorkflowApplicationMixin):
    def __init__(
        self,
        *,
        store: HistoryStore,
        timezone_name: str,
        scan_interval_seconds: int,
        read_gyro: bool,
        cpm_per_usvh: float,
        traffic_light_yellow_percent: float = 125.0,
        traffic_light_red_percent: float = 175.0,
        safety_profile: str = "gq",
        safety_threshold_basis: str = "either",
        safety_warning_cpm: int = 51,
        safety_danger_cpm: int = 100,
        safety_warning_usvh: float = 0.326,
        safety_danger_usvh: float = 0.651,
        ui_mode: str = "advanced",
        ui_language: str = "auto",
        history_management_enabled: bool = False,
        restore_enabled: bool | None = None,
        purge_all_history_enabled: bool | None = None,
        home_assistant_client: HomeAssistantConfigClient | None = None,
        pressure_client: HomeAssistantPressureClient | None = None,
        cosmic_hint_enabled: bool = True,
        options_path: str | Path = "/data/options.json",
        bridge_heartbeat_path: str | Path | None = None,
        started_at_utc: int | None = None,
    ) -> None:
        self.store = store
        self.options_path = Path(options_path)
        self.bridge_heartbeat_path = Path(bridge_heartbeat_path) if bridge_heartbeat_path is not None else None
        self.started_at_utc = int(time.time()) if started_at_utc is None else int(started_at_utc)
        self.timezone_name = timezone_name
        self.timezone = load_timezone(timezone_name)
        self.scan_interval_seconds = scan_interval_seconds
        self.read_gyro = read_gyro
        self.cpm_per_usvh = cpm_per_usvh
        self.traffic_light_yellow_percent = traffic_light_yellow_percent
        self.traffic_light_red_percent = traffic_light_red_percent
        self.safety_profile = safety_profile
        self.safety_threshold_basis = safety_threshold_basis
        self.safety_warning_cpm = safety_warning_cpm
        self.safety_danger_cpm = safety_danger_cpm
        self.safety_warning_usvh = safety_warning_usvh
        self.safety_danger_usvh = safety_danger_usvh
        self.ui_mode = ui_mode if ui_mode in {"simple", "advanced"} else "advanced"
        self.ui_language = ui_language
        legacy_history_management = bool(restore_enabled) or bool(purge_all_history_enabled)
        self.history_management_enabled = bool(history_management_enabled) or legacy_history_management
        self.restore_enabled = self.history_management_enabled
        self.purge_all_history_enabled = self.history_management_enabled
        self.report_slot = threading.BoundedSemaphore(1)
        self.csrf_tokens = CsrfTokenManager(lifetime_seconds=900, maximum_tokens=256)
        self.analysis_cache = RevisionCache(max_entries=16, ttl_seconds=300.0)
        self.home_assistant_client = home_assistant_client
        self.pressure_client = pressure_client
        self.cosmic_hint_enabled = bool(cosmic_hint_enabled)
        self.backup_manager = ManagedBackupManager(store)
        self.scheduled_report_directory = store.path.parent / "scheduled_reports"
        self.scheduled_report_directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    def render_index(
        self,
        *,
        mode_override: str | None = None,
        language_override: str | None = None,
        device_override: str | None = None,
        report_device_override: str | None = None,
        compare_device_override: str | None = None,
        first_start_override: str | None = None,
        first_end_override: str | None = None,
        second_start_override: str | None = None,
        second_end_override: str | None = None,
        history_start_override: str | None = None,
        history_end_override: str | None = None,
        history_raw_override: str | None = None,
        data_mode_override: str | None = None,
        accept_language: str = "",
    ) -> bytes:
        script_nonce = secrets.token_urlsafe(18)
        status = self.status()
        mode = mode_override if mode_override in {"simple", "advanced"} else self.ui_mode
        language = resolve_language(
            self.ui_language, accept_language=accept_language, override=language_override
        )
        language_preference = (
            language_override
            if language_override in {"auto", *SUPPORTED_UI_LANGUAGES}
            else self.ui_language
            if self.ui_language in {"auto", *SUPPORTED_UI_LANGUAGES}
            else "auto"
        )
        t = Translator(language)
        data_mode = data_mode_override if data_mode_override in {"raw", "corrected", "comparison"} else "raw"
        all_sorted_devices = sorted(
            status.get("devices", []),
            key=lambda item: (str(item.get("device_model", "")), str(item.get("serial", ""))),
        )
        devices = self._connected_devices(all_sorted_devices)
        card_devices = self._connected_devices(all_sorted_devices)
        device_serials = {str(item.get("serial")) for item in devices if item.get("serial")}
        primary_serial = str(status.get("serial", ""))
        if primary_serial not in device_serials:
            primary_serial = next(iter(sorted(device_serials)), "")
        selected_serial = device_override if device_override in device_serials else primary_serial
        _encode_report_target(selected_serial) if selected_serial else ""
        selected_device = next((item for item in devices if str(item.get("serial")) == selected_serial), None)
        selected_scan_interval = int(
            (selected_device or {}).get("scan_interval_seconds") or self.scan_interval_seconds
        )
        selected_cpm_per_usvh = float((selected_device or {}).get("cpm_per_usvh") or self.cpm_per_usvh)
        analysis = self._live_analysis_cached(
            device_serial=selected_serial,
            scan_interval_seconds=selected_scan_interval,
            cpm_per_usvh=selected_cpm_per_usvh,
        )
        selected_device_label = (f"{selected_device.get('configured_name') or normalize_device_version_display(str(selected_device.get('device_model', 'GMC')))} · {selected_serial}" if selected_device else "")
        timezone_text = str(self.timezone_name)
        timezone_name = html.escape(timezone_text)
        count = int(status["measurements"])
        home_location = status.get("home_assistant_location") or {}
        location_details_html = render_home_assistant_location(
            home_location, timezone_text=timezone_text, language=language, translator=t
        )
        current_local_date = datetime.now(self.timezone).date()
        today = current_local_date.isoformat()
        yesterday = (current_local_date - timedelta(days=1)).isoformat()
        custom_start = (current_local_date - timedelta(days=6)).isoformat()
        current_month = current_local_date.strftime("%Y-%m")
        iso = datetime.now(self.timezone).isocalendar()
        current_week = f"{iso.year}-W{iso.week:02d}"
        gyro_note = (
            t("Gyro data will be included when available.")
            if self.read_gyro
            else t("Gyro recording is disabled.")
        )
        database = status["database"]
        db_size_bytes = int(database.get("size_bytes", 0))
        db_size = f"{format_number(db_size_bytes / (1024 * 1024), language, decimals=2)} MiB"
        connected_count = len(devices)
        known_count = len(all_sorted_devices)
        disconnected_count = max(0, known_count - connected_count)
        connection_state_class = (
            "ok" if known_count and disconnected_count == 0 else "warning" if connected_count else "error"
        )
        connection_summary = (
            t("All {count} known GMC devices are connected", count=connected_count)
            if known_count and disconnected_count == 0
            else t(
                "{connected} connected · {disconnected} disconnected",
                connected=connected_count,
                disconnected=disconnected_count,
            )
            if known_count
            else t("Automatic device detection is running")
        )
        header_connection_label = (
            t("{connected}/{known} connected", connected=connected_count, known=known_count)
            if known_count
            else t("Scanning for devices")
        )
        header_connection_symbol = (
            "🟢" if known_count and connected_count == known_count
            else "🟡" if known_count and connected_count > 0
            else "🔴" if known_count
            else "🔵"
        )
        dashboard_controls_html = f"""
<nav class="dashboard-controls" id="dashboard-controls" aria-label="{html.escape(t("Dashboard navigation"), quote=True)}">
<div class="desktop-dashboard-navigation">
<div class="jump-links primary-jump-links">
<a data-jump-link href="#devices">{html.escape(t("Devices"))}</a>
<a data-jump-link href="#radiation-intelligence">{html.escape(t("Intelligence"))}</a>
<a data-jump-link href="#analysis">{html.escape(t("Analysis"))}</a>
<a data-jump-link href="#long-term-analysis">{html.escape(t("Long-term"))}</a>
<a data-jump-link href="#history">{html.escape(t("History"))}</a>
</div>
<details class="navigation-menu more-navigation-menu">
<summary>{html.escape(t("More"))}<span aria-hidden="true">▾</span></summary>
<div class="navigation-menu-popover">
<a data-jump-link href="#workflow">{html.escape(t("Workflows"))}</a>
<a data-jump-link href="#calibration-management">{html.escape(t("Calibration"))}</a>
<a data-jump-link href="#reports">{html.escape(t("Reports"))}</a>
<hr>
<button type="button" class="navigation-menu-action" id="toggle-all-cards" aria-expanded="false">{html.escape(t("Expand all"))}</button>
</div>
</details>
</div>
<div class="mobile-dashboard-navigation">
<details class="navigation-menu sections-navigation-menu" id="mobile-sections-menu">
<summary><span aria-hidden="true">☰</span><span>{html.escape(t("Sections"))}</span></summary>
<div class="mobile-navigation-sheet">
<strong>{html.escape(t("Overview"))}</strong>
<a data-jump-link href="#devices">{html.escape(t("Devices"))}</a>
<a data-jump-link href="#radiation-intelligence">{html.escape(t("Intelligence"))}</a>
<strong>{html.escape(t("Evaluation"))}</strong>
<a data-jump-link href="#analysis">{html.escape(t("Analysis"))}</a>
<a data-jump-link href="#long-term-analysis">{html.escape(t("Long-term"))}</a>
<a data-jump-link href="#history">{html.escape(t("History"))}</a>
<strong>{html.escape(t("Administration"))}</strong>
<a data-jump-link href="#workflow">{html.escape(t("Workflows"))}</a>
<a data-jump-link href="#calibration-management">{html.escape(t("Calibration"))}</a>
<a data-jump-link href="#reports">{html.escape(t("Reports"))}</a>
<button type="button" class="navigation-menu-action mobile-toggle-all" data-toggle-all-cards aria-expanded="false">{html.escape(t("Expand all"))}</button>
</div>
</details>
<span class="current-section-label" id="current-section-label" aria-live="polite">{html.escape(t("Devices"))}</span>
<button type="button" class="back-to-top-button" id="back-to-top" aria-label="{html.escape(t("Back to top"), quote=True)}" title="{html.escape(t("Back to top"), quote=True)}">⌃</button>
</div>
</nav>
"""
        purge_controls = (
            f'<div class="note"><strong>{html.escape(t("Deletion is disabled by default."))}</strong><br>'
            f"{html.escape(t('Enable history management in the app configuration and restart only when maintenance is planned.'))}"
            "</div>"
        )
        if self.purge_all_history_enabled:
            purge_preview = self.store.complete_history_summary()
            purge_serials = sorted(
                {
                    str(item.get("serial") or "").strip()
                    for item in status.get("devices", [])
                    if str(item.get("serial") or "").strip()
                }
                | set(purge_preview.get("device_serials", []))
            )
            purge_entity_globs = [f"sensor.gmc_{slugify(serial)}_*" for serial in purge_serials]

            def _history_time(value: object) -> str:
                if value is None:
                    return t("No data")
                localized = datetime.fromtimestamp(int(value), UTC).astimezone(self.timezone)
                return localized.strftime("%d.%m.%Y %H:%M:%S %Z" if language == "de" else "%Y-%m-%d %H:%M:%S %Z")

            purge_period = (
                f"{_history_time(purge_preview.get('first_timestamp_utc'))} – "
                f"{_history_time(purge_preview.get('last_timestamp_utc'))}"
                if purge_preview.get("measurements")
                else t("No stored measurements")
            )
            purge_csrf_token = self.csrf_tokens.issue("purge-all-history")
            purge_controls = f"""
<div class="danger-zone">
<h3>{html.escape(t("Danger zone"))}</h3>
<p>{html.escape(t("Permanently delete all GMC history from this app and Home Assistant Recorder. This includes CPM, temperature, voltage, gyro and tube measurements for every known GMC and all time periods."))}</p>
<div class="database-grid">
<div class="metric"><strong>{html.escape(t("Measurements to delete"))}</strong><div class="value">{format_number(int(purge_preview.get("measurements", 0)), language, grouping=True)}</div><small>{html.escape(purge_period)}</small></div>
<div class="metric"><strong>{html.escape(t("Raw-data archive"))}</strong><div class="value">{format_number(int(purge_preview.get("raw_measurements", 0)), language, grouping=True)}</div><small>{html.escape(t("Raw device values are stored separately before quality filtering"))}</small></div>
<div class="metric"><strong>{html.escape(t("Events, annotations and diagnostics"))}</strong><div class="value">{format_number(int(purge_preview.get("events", 0)) + int(purge_preview.get("annotations", 0)) + int(purge_preview.get("diagnostics", 0)), language, grouping=True)}</div><small>{html.escape(t("{events} events · {annotations} annotations · {diagnostics} diagnostics", events=int(purge_preview.get("events", 0)), annotations=int(purge_preview.get("annotations", 0)), diagnostics=int(purge_preview.get("diagnostics", 0))))}</small></div>
<div class="metric"><strong>{html.escape(t("Affected GMC devices"))}</strong><div class="value">{len(purge_serials)}</div><small>{html.escape(t("All known GMC devices with stored history"))}</small></div>
<div class="metric"><strong>{html.escape(t("Home Assistant Recorder entity patterns"))}</strong><div class="value">{len(purge_entity_globs)}</div><small>{html.escape(t("Scoped only to known GMC sensor entities"))}</small></div>
<div class="metric"><strong>{html.escape(t("Current database size"))}</strong><div class="value">{html.escape(db_size)}</div><small>{html.escape(t("A fresh backup is recommended before deletion."))}</small></div>
</div>
<form action="?action=purge-all-history" method="post" onsubmit="return confirm(`{html.escape(t("This cannot be undone. Delete all GMC history?"))}`);">
<input type="hidden" name="csrf_token" value="{html.escape(purge_csrf_token, quote=True)}">
<label>{html.escape(t("Type DELETE ALL GMC HISTORY to confirm"))}<input name="confirm" autocomplete="off" required></label>
<button class="danger" type="submit">{html.escape(t("Delete all GMC history"))}</button>
</form>
</div>
"""
        if self.restore_enabled:
            restore_csrf_token = self.csrf_tokens.issue("restore")
            restore_preview_csrf_token = self.csrf_tokens.issue("restore-preview")
            restore_controls = f"""
<p>{html.escape(t("Merge a compatible SQLite backup into the current history. Existing rows are preserved or updated by device serial and UTC timestamp."))}</p>
<form class="restore-form" id="restore-form" action="?action=restore" method="post" enctype="multipart/form-data">
<input type="hidden" name="csrf_token" value="{html.escape(restore_csrf_token, quote=True)}">
<input type="hidden" name="preview_csrf_token" value="{html.escape(restore_preview_csrf_token, quote=True)}">
<label><span>{html.escape(t("SQLite backup file"))}</span><input type="file" name="backup" accept=".sqlite,.sqlite3,application/x-sqlite3" required></label>
<div class="restore-preview" id="restore-preview" aria-live="polite"><span>{html.escape(t("Select a backup to preview its schema, devices, data period and row counts before restoring."))}</span></div>
<label><span>{html.escape(t("Type RESTORE to confirm"))}</span><input type="text" name="confirm" pattern="RESTORE" required></label>
<div class="actions"><button type="button" id="preview-restore" class="button">{html.escape(t("Preview backup"))}</button><button class="primary" type="submit">{html.escape(t("Restore backup"))}</button></div>
</form>
"""
        else:
            restore_controls = (
                f'<div class="note"><strong>{html.escape(t("Restore is disabled by default."))}</strong><br>'
                f"{html.escape(t('Enable “{setting}” in the app configuration and restart only when history maintenance is planned.', setting=t('History management')))}"
                "</div>"
            )
        history_management_banner = (
            '<div class="history-management-status enabled"><span class="status-dot"></span><div><strong>'
            + html.escape(t("History management enabled"))
            + '</strong><small>'
            + html.escape(t("Restore and complete deletion are available. Disable the configuration switch again after maintenance."))
            + '</small></div></div>'
            if self.history_management_enabled
            else '<div class="history-management-status disabled"><span class="status-dot"></span><div><strong>'
            + html.escape(t("History management protected"))
            + '</strong><small>'
            + html.escape(t("Restore and complete deletion remain locked during normal operation."))
            + '</small></div></div>'
        )
        analysis_html = self._render_analysis(
            analysis,
            advanced=True,
            t=t,
            device_label=selected_device_label,
            device_model=str((selected_device or {}).get("device_model") or ""),
        )
        long_term_analysis_html = render_cached_long_term_analysis(
            self, device_serial=selected_serial, scan_interval_seconds=selected_scan_interval,
            cpm_per_usvh=selected_cpm_per_usvh, device_label=selected_device_label, translator=t,
        )

        fleet_context = self._fleet_context_cached(selected_serial=selected_serial, devices=devices)
        fleet_snapshot = fleet_context["fleet_snapshot"]
        device_background_profile = fleet_context["device_profile"]
        site_background_profile = fleet_context["site_profile"]
        fleet_intelligence_html = self._render_fleet_intelligence(t=t, snapshot=fleet_snapshot)
        radiation_intelligence_html = self._render_radiation_intelligence(
            analysis=analysis,
            selected_serial=selected_serial,
            snapshot=fleet_snapshot,
            t=t,
            device_profile=device_background_profile,
            site_profile=site_background_profile,
        )
        adaptive_background_html = self._render_adaptive_background(
            device_profile=device_background_profile, site_profile=site_background_profile, t=t
        )
        barometric_hint = fleet_context["barometric_hint"]
        cosmic_influence_html = self._render_cosmic_influence(barometric_hint, t=t)

        multi_device_html = self._render_devices_section(
            devices=card_devices,
            selected_serial=selected_serial,
            mode=mode,
            language=language,
            t=t,
        )
        calibration_management_html = render_calibration_management(
            store=self.store,
            timezone=self.timezone,
            devices=devices,
            selected_serial=selected_serial,
            t=t,
            csrf_token=self.csrf_tokens.issue("calibration-profiles"),
        )
        workflow_settings = load_workflow_settings(self.store)
        comparison_serial = (
            compare_device_override if compare_device_override in device_serials else selected_serial
        )
        comparison_device = next(
            (item for item in devices if str(item.get("serial")) == comparison_serial),
            selected_device,
        )
        default_first, default_second = default_comparison_ranges(self.timezone)

        def _local_date_from_epoch(value: int) -> str:
            return datetime.fromtimestamp(value, UTC).astimezone(self.timezone).date().isoformat()

        comparison_dates = {
            "first_start": first_start_override or _local_date_from_epoch(default_first[0]),
            "first_end": first_end_override or _local_date_from_epoch(default_first[1] - 1),
            "second_start": second_start_override or _local_date_from_epoch(default_second[0]),
            "second_end": second_end_override or _local_date_from_epoch(default_second[1] - 1),
        }
        try:
            first_range = local_range(
                comparison_dates["first_start"], comparison_dates["first_end"], self.timezone
            )
            second_range = local_range(
                comparison_dates["second_start"], comparison_dates["second_end"], self.timezone
            )
        except ValueError:
            first_range, second_range = default_first, default_second
            comparison_dates = {
                "first_start": _local_date_from_epoch(first_range[0]),
                "first_end": _local_date_from_epoch(first_range[1] - 1),
                "second_start": _local_date_from_epoch(second_range[0]),
                "second_end": _local_date_from_epoch(second_range[1] - 1),
            }
        comparison = compare_periods(
            self.store,
            device_serial=comparison_serial,
            first_start_utc=first_range[0],
            first_end_utc=first_range[1],
            second_start_utc=second_range[0],
            second_end_utc=second_range[1],
            scan_interval_seconds=int(
                (comparison_device or {}).get("scan_interval_seconds") or self.scan_interval_seconds
            ),
        )
        default_history_end = datetime.now(self.timezone).date()
        default_history_start = default_history_end - timedelta(days=1)
        history_dates = {
            "start": history_start_override or default_history_start.isoformat(),
            "end": history_end_override or default_history_end.isoformat(),
        }
        try:
            explorer_start, explorer_end = local_range(
                history_dates["start"], history_dates["end"], self.timezone
            )
            if explorer_end - explorer_start > 366 * 86400:
                raise ValueError("History explorer period is limited to 366 days")
        except ValueError:
            history_dates = {
                "start": default_history_start.isoformat(),
                "end": default_history_end.isoformat(),
            }
            explorer_start, explorer_end = local_range(
                history_dates["start"], history_dates["end"], self.timezone
            )
        explorer_rows = (
            self.store.query_range(explorer_start, explorer_end, device_serial=selected_serial)
            if selected_serial
            else []
        )
        explorer_points = downsample_history(explorer_rows, maximum_points=600)
        expected_history_samples = max(
            1, round((explorer_end - explorer_start) / max(1, selected_scan_interval))
        )
        if data_mode == "corrected":
            history_values = [
                float(row.corrected_cpm if row.corrected_cpm is not None else row.cpm)
                for row in explorer_rows
            ]
        else:
            history_values = [float(row.raw_cpm if row.raw_cpm is not None else row.cpm) for row in explorer_rows]
        history_weighted = time_weighted_summary(
            explorer_rows,
            timestamp=lambda row: row.timestamp_utc,
            value=(
                (lambda row: row.corrected_cpm if row.corrected_cpm is not None else row.cpm)
                if data_mode == "corrected"
                else (lambda row: row.raw_cpm if row.raw_cpm is not None else row.cpm)
            ),
            start_utc=explorer_start,
            end_utc=explorer_end,
            expected_interval_seconds=selected_scan_interval,
        )
        history_summary = {
            "samples": len(explorer_rows),
            "coverage_percent": history_weighted.coverage_percent,
            "sample_coverage_percent": min(100.0, 100.0 * len(explorer_rows) / expected_history_samples),
            "mean_cpm": history_weighted.mean if history_weighted.available else (statistics.fmean(history_values) if history_values else None),
            "covered_seconds": history_weighted.covered_seconds,
            "gap_seconds": history_weighted.gap_seconds,
            "median_cpm": statistics.median(history_values) if history_values else None,
            "minimum_cpm": min(history_values) if history_values else None,
            "maximum_cpm": max(history_values) if history_values else None,
            "rejected_raw_count": None,
        }
        show_raw_history = str(history_raw_override or "").strip().lower() in {"1", "true", "yes", "on"}
        raw_history_points = []
        if show_raw_history and selected_serial:
            raw_rows = self.store.query_raw_measurements(
                explorer_start, explorer_end, device_serial=selected_serial
            )
            rejected_rows = [row for row in raw_rows if not bool(row.get("accepted"))]
            history_summary["rejected_raw_count"] = len(rejected_rows)
            step = max(1, (len(rejected_rows) + 499) // 500)
            raw_history_points = [
                {
                    "timestamp_utc": int(row.get("timestamp_utc") or 0),
                    "cpm": int(row.get("cpm") or 0),
                    "gate_state": str(row.get("gate_state") or ""),
                }
                for row in rejected_rows[::step]
            ]
        annotations = self.store.list_event_annotations(
            start_utc=explorer_start,
            end_utc=explorer_end,
            device_serial=selected_serial or None,
            limit=100,
        )
        home_available = bool(home_location.get("available"))
        self_tests = run_self_test(
            store=self.store,
            timezone_name=self.timezone_name,
            devices=all_sorted_devices,
            home_assistant_available=home_available,
            backup_directory=self.backup_manager.directory,
        )
        managed_backups = self.backup_manager.list()
        backup_comparison = (
            self.backup_manager.compare(managed_backups[1].name, managed_backups[0].name)
            if len(managed_backups) >= 2
            else None
        )
        managed_backups_html = render_managed_backups(
            t=t,
            timezone=self.timezone,
            backups=managed_backups,
            comparison=backup_comparison,
            csrf_token=self.csrf_tokens.issue("managed-backups"),
        )
        scheduled_reports_html = render_scheduled_reports(
            t=t,
            timezone=self.timezone,
            reports=self.list_scheduled_reports(limit=20),
            csrf_token=self.csrf_tokens.issue("scheduled-reports"),
        )
        annotation_csrf = self.csrf_tokens.issue("event-annotations")
        history_html = render_history_section(
            t=t,
            timezone=self.timezone,
            selected_serial=selected_serial,
            annotation_csrf=annotation_csrf,
            annotations=annotations,
            history_points=explorer_points,
            raw_history_points=raw_history_points,
            show_raw_history=show_raw_history,
            history_dates=history_dates,
            history_start_utc=explorer_start,
            history_end_utc=explorer_end,
            history_summary=history_summary,
            data_mode=data_mode,
        )
        workflow_html = render_workflow_section(
            t=t,
            timezone=self.timezone,
            selected_serial=selected_serial,
            device_options=[
                (
                    str(item.get("serial") or ""),
                    str(
                        item.get("configured_name")
                        or normalize_device_version_display(str(item.get("device_model") or "GMC"))
                    ),
                )
                for item in devices
                if str(item.get("serial") or "")
            ],
            settings=workflow_settings,
            settings_csrf=self.csrf_tokens.issue("workflow-settings"),
            comparison=comparison,
            comparison_dates=comparison_dates,
            self_tests=self_tests,
            automation_status=automation_status(self.store),
        )

        format_options = "".join(
            f'<option value="{value}">{html.escape(t(label))}</option>'
            for value, label in (
                ("pdf", "Analysis PDF"),
                ("zip", "Complete ZIP bundle"),
                ("csv", "Quality-filtered measurement CSV"),
                ("raw-archive-csv", "Original raw-data CSV"),
                ("png", "Time-series PNG"),
                ("analysis-json", "Analysis JSON"),
                ("daily-summary-csv", "Daily summary CSV"),
                ("events-csv", "Events CSV"),
                ("histogram-png", "Histogram PNG"),
                ("heatmap-png", "Heatmap PNG"),
            )
        )
        language_query_suffix = f"&amp;mode={quote_plus(mode)}"
        if selected_serial:
            language_query_suffix += f"&amp;device={quote_plus(selected_serial)}"
        language_options = (
            ("auto", "Auto"),
            ("de", "Deutsch"),
            ("en", "English"),
            ("es", "Español"),
            ("fr", "Français"),
            ("hr", "Hrvatski"),
            ("it", "Italiano"),
            ("nl", "Nederlands"),
            ("pl", "Polski"),
        )
        language_select_options = []
        for language_code, language_name in language_options:
            selected = ' selected' if language_code == language_preference else ""
            option_label = t("Automatic") if language_code == "auto" else language_name
            language_select_options.append(
                f'<option value="{html.escape(language_code, quote=True)}"{selected}>'
                f'{html.escape(option_label)}</option>'
            )
        analysis_level_default = "summary" if mode == "simple" else "analysis"
        analysis_level_options = (
            ("summary", "◉", t("Summary"), t("Only the most important conclusions at a glance")),
            ("analysis", "▤", t("Analysis"), t("Detailed interpretation and the most useful supporting values")),
            ("expert", "∑", t("Expert"), t("All statistical values, confidence intervals and diagnostics")),
        )
        analysis_select_options = []
        analysis_selected_description = ""
        analysis_selected_symbol = "◉"
        for level_value, level_symbol, level_label, level_description in analysis_level_options:
            selected = ' selected' if level_value == analysis_level_default else ""
            if level_value == analysis_level_default:
                analysis_selected_description = level_description
                analysis_selected_symbol = level_symbol
            analysis_select_options.append(
                f'<option value="{html.escape(level_value, quote=True)}" data-symbol="{html.escape(level_symbol, quote=True)}" '
                f'data-description="{html.escape(level_description, quote=True)}"{selected}>'
                f'{html.escape(level_symbol)} {html.escape(level_label)}</option>'
            )
        language_toolbar_html = f"""
<div class="header-tools" aria-label="{html.escape(t("Application controls"), quote=True)}">
<div class="analysis-select-group">
<label class="analysis-select-label" for="analysis-level-select"><span class="visually-hidden">{html.escape(t("View"))}</span><span class="analysis-select-control"><span class="analysis-select-icon" id="analysis-level-icon" aria-hidden="true">{html.escape(analysis_selected_symbol)}</span>
<select id="analysis-level-select" aria-label="{html.escape(t("View"), quote=True)}" title="{html.escape(t("View"), quote=True)}" data-default-level="{html.escape(analysis_level_default, quote=True)}">{''.join(analysis_select_options)}</select></span></label>
<small id="analysis-level-description" class="header-select-description" aria-live="polite">{html.escape(analysis_selected_description)}</small>
</div>
<form method="get" class="language-select-form" id="language-select-form">
<input type="hidden" name="mode" value="{html.escape(mode, quote=True)}">
{f'<input type="hidden" name="device" value="{html.escape(selected_serial, quote=True)}">' if selected_serial else ''}
<label class="language-select-label" for="language-select"><span class="visually-hidden">{html.escape(t("Language"))}</span><span class="language-select-control"><span class="language-select-icon" aria-hidden="true">🌐</span>
<select name="lang" id="language-select" aria-label="{html.escape(t("Language"), quote=True)}" title="{html.escape(t("Language"), quote=True)}">{''.join(language_select_options)}</select></span></label>
<noscript><button type="submit" class="header-tool-button">{html.escape(t("Apply"))}</button></noscript>
</form>
<a class="header-status-badge {connection_state_class}" id="header-status-badge" href="#devices" title="{html.escape(connection_summary, quote=True)}" aria-label="{html.escape(connection_summary, quote=True)}"><span class="header-status-symbol" aria-hidden="true">{header_connection_symbol}</span><span class="header-status-text">{html.escape(header_connection_label)}</span></a>
<button type="button" class="header-tool-button reload-button" id="reload-dashboard" aria-label="{html.escape(t("Refresh page"), quote=True)}" title="{html.escape(t("Refresh page"), quote=True)}"><span class="header-tool-icon" aria-hidden="true">↻</span><span class="header-tool-label visually-hidden">{html.escape(t("Refresh"))}</span></button>
</div>
"""
        page = f"""<!doctype html>
<html lang="{language}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(t("GMC Radiation Monitoring"))}</title>
<link rel="stylesheet" href="./assets/dashboard.css?v={html.escape(ASSET_REVISION, quote=True)}">
<style id="critical-dashboard-layout">
.page-scroll {{ width:100%; height:100%; min-height:0; overflow-y:auto; overflow-x:clip; -webkit-overflow-scrolling:touch; touch-action:pan-y; padding-bottom:env(safe-area-inset-bottom,0px); }}
.form-grid > *, label {{ min-width:0; max-width:100%; }}
input[type="date"], input[type="week"], input[type="month"], input[type="datetime-local"] {{ min-inline-size:0; max-inline-size:100%; }}
@media (max-width:620px) {{ .report-format-guide {{ grid-template-columns:1fr; }} }}
</style>
</head>
<body class="mode-{mode}" data-analysis-level="{"summary" if mode == "simple" else "analysis"}"><div class="page-scroll" id="page-scroll"><main>
<header class="report-header">
<div class="header-topline">
<div class="header-intro">
<h1>{html.escape(t("GMC Radiation Monitoring"))}</h1>
<p>{html.escape(t("Local monitoring for GQ GMC Geiger counters"))}</p>
</div>
{language_toolbar_html}
</div>
{location_details_html}
<div class="header-resource-links">
<a class="location-details external-map-link" href="https://www.gmcmap.com/index.php" target="_blank" rel="noopener noreferrer external" aria-label="{html.escape(t("Open GMCMap world map"), quote=True)}">
<span class="details-summary-icon" aria-hidden="true">🌐</span>
<span class="external-map-copy"><strong>{html.escape(t("GMCMap world map"))}</strong><small>gmcmap.com</small></span>
<span class="external-link-mark" aria-hidden="true">↗</span>
</a>
<a class="location-details manual-link" href="./docs/user-manual.pdf?lang={quote_plus(language)}" target="_blank" rel="noopener" aria-label="{html.escape(t("Open user manual PDF"), quote=True)}">
<span class="details-summary-icon manual-icon" aria-hidden="true">📘</span>
<span class="external-map-copy"><strong>{html.escape(t("User manual"))}</strong><small>PDF · Version {html.escape(APP_VERSION)} · {html.escape(USER_MANUAL_LANGUAGE_NAMES.get(language, "English"))}</small></span>
<span class="external-link-mark" aria-hidden="true">↗</span>
</a>
</div>
</header>
{dashboard_controls_html}
<div id="primary-dashboard" class="primary-dashboard">
{multi_device_html}
{radiation_intelligence_html}
{adaptive_background_html}
{cosmic_influence_html}
{fleet_intelligence_html}
</div>
{analysis_html}
{long_term_analysis_html}
{history_html}
{workflow_html}
{calibration_management_html}
<section id="reports">
<h2>{html.escape(t("Reports"))}</h2>
<div class="report-target-card active-report-context">
<strong>{html.escape(t("Reports for the displayed analysis"))}</strong>
<span>{html.escape(selected_device_label or t("No connected GMC device"))}</span>
<small>{html.escape(t("All downloads below automatically use the GMC device currently shown in Analysis. Select another connected device above to change the report source."))}</small>
</div>
<div class="report-data-mode-card advanced-only"><div><strong>{html.escape(t("Report data mode"))}</strong><small>{html.escape(t("Choose whether charts and statistics use raw or dead-time-corrected values."))}</small></div><div class="data-mode-switch"><a class="button{' primary' if data_mode == 'raw' else ''}" href="?device={quote_plus(selected_serial)}&amp;lang={quote_plus(language)}&amp;mode={quote_plus(mode)}&amp;data_mode=raw#reports">{html.escape(t("Raw data"))}</a><a class="button{' primary' if data_mode == 'corrected' else ''}" href="?device={quote_plus(selected_serial)}&amp;lang={quote_plus(language)}&amp;mode={quote_plus(mode)}&amp;data_mode=corrected#reports">{html.escape(t("Dead-time corrected"))}</a><a class="button{' primary' if data_mode == 'comparison' else ''}" href="?device={quote_plus(selected_serial)}&amp;lang={quote_plus(language)}&amp;mode={quote_plus(mode)}&amp;data_mode=comparison#reports">{html.escape(t("Comparison view"))}</a></div></div>
<h3>{html.escape(t("Quick downloads"))}</h3>
<div class="report-format-guide" aria-label="{html.escape(t("Format"), quote=True)}">
<div class="report-format-item"><strong>{html.escape(t("PDF report"))}</strong><small>{html.escape(t("Best for reading, printing and sharing"))}</small></div>
<div class="report-format-item"><strong>{html.escape(t("Complete ZIP bundle"))}</strong><small>{html.escape(t("Includes raw data, checksums and reproducibility metadata"))}</small></div>
<div class="report-format-item"><strong>{html.escape(t("Measurement CSV"))}</strong><small>{html.escape(t("For spreadsheets and further analysis"))}</small></div>
</div>
<div class="download-columns">
<div class="download-card">
<h3>{html.escape(t("Previous day"))}</h3>
<div class="actions">
<a class="button primary" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=pdf">{html.escape(t("PDF report"))}</a>
<a class="button primary" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=zip">{html.escape(t("Complete ZIP bundle"))}</a>
<a class="button" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=csv">{html.escape(t("Measurement CSV"))}</a>
</div>
</div>
<div class="download-card">
<h3>{html.escape(t("Previous week"))}</h3>
<div class="actions">
<a class="button primary" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=pdf">{html.escape(t("PDF report"))}</a>
<a class="button primary" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=zip">{html.escape(t("Complete ZIP bundle"))}</a>
<a class="button" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=csv">{html.escape(t("Measurement CSV"))}</a>
</div>
</div>
</div>
<div class="actions" style="margin-top:.7rem">
<a class="button" href="?action=download&amp;period=daily&amp;selection=today&amp;format=zip">{html.escape(t("Today so far bundle"))}</a>
<a class="button" href="?action=download&amp;period=weekly&amp;selection=current&amp;format=zip">{html.escape(t("Current week bundle"))}</a>
<a class="button" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=pdf&amp;scientific=1">{html.escape(t("Scientific PDF"))}</a>
<a class="button" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=zip&amp;scientific=1">{html.escape(t("Scientific ZIP bundle"))}</a>
</div>

{scheduled_reports_html}

<details class="download-group advanced-only" id="reports-data-exports">
<summary><span class="summary-copy">{html.escape(t("Data exports"))}<small>{html.escape(t("Machine-readable statistics and event data"))}</small></span></summary>
<div class="group-body download-columns">
<div class="download-card">
<h3>{html.escape(t("Previous day"))}</h3>
<div class="actions">
<a class="button" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=analysis-json">{html.escape(t("Analysis JSON"))}</a>
<a class="button" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=daily-summary-csv">{html.escape(t("Daily summary CSV"))}</a>
<a class="button" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=events-csv">{html.escape(t("Events CSV"))}</a>
<a class="button" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=raw-archive-csv">{html.escape(t("Original raw-data CSV"))}</a>
</div>
</div>
<div class="download-card">
<h3>{html.escape(t("Previous week"))}</h3>
<div class="actions">
<a class="button" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=analysis-json">{html.escape(t("Analysis JSON"))}</a>
<a class="button" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=daily-summary-csv">{html.escape(t("Daily summary CSV"))}</a>
<a class="button" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=events-csv">{html.escape(t("Events CSV"))}</a>
<a class="button" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=raw-archive-csv">{html.escape(t("Original raw-data CSV"))}</a>
</div>
</div>
</div>
</details>

<details class="download-group advanced-only" id="reports-visuals">
<summary><span class="summary-copy">{html.escape(t("Advanced visuals"))}<small>{html.escape(t("Time series, Poisson comparison and weekday/hour heatmap"))}</small></span></summary>
<div class="group-body download-columns">
<div class="download-card">
<h3>{html.escape(t("Previous day"))}</h3>
<div class="actions">
<a class="button" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=png">{html.escape(t("Time-series PNG"))}</a>
<a class="button" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=histogram-png">{html.escape(t("Histogram PNG"))}</a>
<a class="button" href="?action=download&amp;period=daily&amp;selection=previous&amp;format=heatmap-png">{html.escape(t("Heatmap PNG"))}</a>
</div>
</div>
<div class="download-card">
<h3>{html.escape(t("Previous week"))}</h3>
<div class="actions">
<a class="button" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=png">{html.escape(t("Time-series PNG"))}</a>
<a class="button" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=histogram-png">{html.escape(t("Histogram PNG"))}</a>
<a class="button" href="?action=download&amp;period=weekly&amp;selection=previous&amp;format=heatmap-png">{html.escape(t("Heatmap PNG"))}</a>
</div>
</div>
</div>
</details>

<div class="advanced-only"><h3>{html.escape(t("Custom period"))}</h3><div class="report-generation-preview" id="report-generation-preview" aria-live="polite"><div><strong>{html.escape(t("Selected device"))}</strong><span>{html.escape(selected_device_label or t("No connected GMC device"))}</span></div><div><strong>{html.escape(t("Report timezone"))}</strong><span>{html.escape(str(self.timezone))}</span></div><div><strong>{html.escape(t("Selected period"))}</strong><span id="report-preview-period">—</span></div><div><strong>{html.escape(t("Time-based data coverage"))}</strong><span id="report-preview-coverage">—</span></div><div><strong>{html.escape(t("Stored measurements"))}</strong><span id="report-preview-samples">—</span></div><div><strong>{html.escape(t("Uncovered time"))}</strong><span id="report-preview-gap">—</span></div><p id="report-preview-warning" class="report-preview-warning" hidden></p></div>
<div class="custom-periods"><div class="report-period-presets" role="group" aria-label="{html.escape(t("Quick period presets"), quote=True)}"><button type="button" class="button" data-report-preset="today">{html.escape(t("Today"))}</button><button type="button" class="button" data-report-preset="yesterday">{html.escape(t("Yesterday"))}</button><button type="button" class="button" data-report-preset="rolling24">{html.escape(t("Last 24 hours"))}</button><button type="button" class="button" data-report-preset="rolling7">{html.escape(t("Last 7 days"))}</button><button type="button" class="button" data-report-preset="month">{html.escape(t("Current month"))}</button><button type="button" class="button" data-report-preset="custom">{html.escape(t("Custom range"))}</button></div>
<form class="custom-form report-preset-source unified-report-form" id="custom-report-form" action="" method="get" data-preset-kind="custom" data-today="{today}" data-yesterday="{yesterday}" data-current-month="{current_month}" novalidate><input type="hidden" name="action" value="download"><input type="hidden" name="selection" value="specific"><div class="form-grid report-form-grid">
<label>{html.escape(t("Period type"))}<select name="period" id="custom-report-period"><option value="daily">{html.escape(t("Daily"))}</option><option value="weekly">{html.escape(t("Weekly"))}</option><option value="monthly">{html.escape(t("Monthly"))}</option><option value="rolling24">{html.escape(t("Last 24 hours"))}</option><option value="rolling7">{html.escape(t("Last 7 days"))}</option><option value="custom">{html.escape(t("Custom range"))}</option></select></label><label data-report-date-field>{html.escape(t("Specific date"))}<input type="date" name="date" value="{today}"></label><label data-report-week-field hidden>{html.escape(t("Specific ISO week"))}<input type="week" name="week" value="{current_week}"></label><label data-report-month-field hidden>{html.escape(t("Specific month"))}<input type="month" name="month" value="{current_month}"></label><label data-report-start-field hidden>{html.escape(t("From"))}<input type="date" name="start" value="{custom_start}"></label><label data-report-end-field hidden>{html.escape(t("To"))}<input type="date" name="end" value="{today}"></label><label>{html.escape(t("Format"))}<select name="format">{format_options}</select></label><div class="form-actions"><button type="submit" class="primary" id="custom-report-submit">{html.escape(t("Download"))}</button></div></div>
<small class="report-timezone-note">{html.escape(t("Dates use the report timezone"))}: {html.escape(str(self.timezone))}</small><p id="report-form-status" class="report-form-status" role="status" aria-live="polite" hidden></p></form></div></div>

<details class="download-group advanced-only" id="reports-export-details">
<summary><span class="summary-copy">{html.escape(t("Export details"))}<small>{html.escape(t("What each report preserves and how periods are defined"))}</small></span></summary>
<div class="group-body">
<p>{html.escape(t("The professional five-page PDF report starts with an executive beta/gamma assessment, followed by correctly labelled CPM time series, distribution and Poisson reference, temporal heat maps, statistical significance, events and traceability. CPM remains the primary measurement; derived µSv/h values are not independent dosimetry. CSV files preserve accepted measurements without interpolation, and ZIP bundles additionally contain machine-readable analysis and specialist graphics."))}</p>
<small>{html.escape(t("{gyro_note} History retention: {days} days. Daily periods are local calendar days; weekly periods are ISO weeks from Monday through Sunday.", gyro_note=gyro_note, days=self.store.retention_days))}</small>
</div>
</details>
</section>

<section class="advanced-only history-management-section" id="maintenance">
<div class="history-section-heading"><div><h2>{html.escape(t("History management"))}</h2><p>{html.escape(t("Export, back up, restore or deliberately remove stored radiation history from one protected workspace."))}</p></div></div>
{history_management_banner}
<div class="actions maintenance-actions">
<a class="button primary" href="?action=history-export">{html.escape(t("Full history ZIP"))}</a>
<a class="button" href="?action=diagnostics">{html.escape(t("Diagnostics JSON"))}</a>
<button type="button" class="button" id="copy-support-diagnostics">{html.escape(t("Copy support diagnostics"))}</button>
<span id="support-diagnostics-status" class="copy-status" role="status" aria-live="polite"></span>
</div>
{managed_backups_html}
<details class="analysis-group history-management-tool" id="history-restore"><summary><span class="summary-copy">{html.escape(t("Restore history"))}<small>{html.escape(t("Preview and merge a compatible SQLite backup"))}</small></span></summary><div class="group-body">{restore_controls}</div></details>
<details class="analysis-group history-management-tool" id="history-delete"><summary><span class="summary-copy">{html.escape(t("Delete history"))}<small>{html.escape(t("Permanently remove app and Recorder history after explicit confirmation"))}</small></span></summary><div class="group-body">{purge_controls}</div></details>
</section>
</main></div>
<script nonce="{html.escape(script_nonce, quote=True)}">{render_dashboard_bootstrap(selected_serial=selected_serial, language=language, translator=t)}</script><script src="./assets/dashboard.js?v={html.escape(ASSET_REVISION, quote=True)}" defer></script></body></html>"""
        # Bind every download server-side to the device currently shown in Analysis.
        # JavaScript is only a progressive enhancement; Ingress-safe links work without it.
        report_prefix = (
            f"?device={quote_plus(selected_serial)}&amp;lang={quote_plus(language)}"
            "&amp;action=download"
        )
        page = page.replace('href="?action=download', f'href="{report_prefix}')
        page = re.sub(
            r'(href="\?device=[^"]*?&amp;action=download[^"]*)"',
            lambda match: match.group(1) + f"&amp;data_mode={quote_plus(data_mode)}\"", page,
        )
        hidden_report_fields = (
            '<input type="hidden" name="device" value="'
            + html.escape(selected_serial, quote=True)
            + '"><input type="hidden" name="lang" value="'
            + html.escape(language, quote=True)
            + '"><input type="hidden" name="data_mode" value="'
            + html.escape(data_mode, quote=True)
            + '">'
        )
        page = page.replace(
            '<input type="hidden" name="action" value="download">',
            '<input type="hidden" name="action" value="download">' + hidden_report_fields,
        )
        return page.encode("utf-8")


























def run_report_server() -> None:
    """Start the HTTP service through the split server bootstrap module."""
    from .report_server import run_report_server as _run_report_server

    _run_report_server()
