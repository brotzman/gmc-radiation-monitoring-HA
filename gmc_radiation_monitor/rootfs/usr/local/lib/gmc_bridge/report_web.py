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
from .fleet_analytics import build_fleet_snapshot
from .historical_presentation import trend_symbol
from .history import DEFAULT_DB_PATH, HistoryStore
from .home_assistant import HomeAssistantConfigClient, HomeAssistantPressureClient
from .intelligence import build_radiation_intelligence
from .orientation import calculate_orientation, orientation_status
from .report_web_http import (
    ReportRequestHandler,
)
from .report_web_http import (
    _localized_exception_message as _localized_exception_message,
)
from .report_web_support import (
    MAX_DOWNLOAD_BYTES as MAX_DOWNLOAD_BYTES,
)
from .report_web_support import (
    MAX_RESTORE_BYTES as MAX_RESTORE_BYTES,
)
from .report_web_support import (
    REPORT_TARGET_COMBINED as REPORT_TARGET_COMBINED,
)
from .report_web_support import (
    STREAM_CHUNK_BYTES as STREAM_CHUNK_BYTES,
)
from .report_web_support import (
    USER_MANUAL_DIRECTORY as USER_MANUAL_DIRECTORY,
)
from .report_web_support import (
    USER_MANUAL_FILENAME as USER_MANUAL_FILENAME,
)
from .report_web_support import (
    USER_MANUAL_FILENAMES as USER_MANUAL_FILENAMES,
)
from .report_web_support import (
    USER_MANUAL_LANGUAGE_NAMES,
    _encode_report_target,
)
from .report_web_support import (
    USER_MANUAL_PATH as USER_MANUAL_PATH,
)
from .report_web_support import (
    _decode_report_target as _decode_report_target,
)
from .report_web_support import (
    _one as _one,
)
from .report_web_support import (
    _optional_one as _optional_one,
)
from .report_web_support import (
    _parse_multipart_form as _parse_multipart_form,
)
from .report_web_support import (
    _resolve_user_manual as _resolve_user_manual,
)
from .report_web_support import (
    _stream_restore_upload_to_temp as _stream_restore_upload_to_temp,
)
from .report_web_support import (
    _temporary_path as _temporary_path,
)
from .reports import build_live_analysis, load_timezone
from .revision_cache import RevisionCache
from .scientific_web import render_calibration_management
from .security_logging import configure_secure_logging
from .translations import SUPPORTED_UI_LANGUAGES, Translator, resolve_language
from .utils import slugify
from .version import APP_VERSION
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
from .web_assets import DASHBOARD_CSS, render_dashboard_script
from .web_components import render_analysis_level_controls, render_collapsible_card
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
from .workflow_controller import WorkflowApplicationMixin
from .workflow_web import (
    render_history_section,
    render_managed_backups,
    render_scheduled_reports,
    render_workflow_section,
)

LOG = logging.getLogger("gmc_reports")
class ReportApplication(WorkflowApplicationMixin):
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
    ) -> None:
        self.store = store
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
    def _device_is_connected(self, item: dict[str, Any]) -> bool:
        """Return the bridge-owned live state, with a legacy freshness fallback."""
        runtime_online = item.get("runtime_online")
        if isinstance(runtime_online, str):
            runtime_online = runtime_online.strip().lower() in {"1", "true", "yes", "on", "online"}
        if runtime_online is not None:
            return bool(runtime_online)
        if not item.get("runtime_status") and not item.get("runtime_status_updated_utc"):
            # Legacy/history-only databases have no live-state field. The bridge
            # resets every known device to explicit offline at startup, so this
            # compatibility path is only used before that first runtime write.
            return True
        latest_timestamp = int(item.get("timestamp_utc") or item.get("last_timestamp_utc") or 0)
        last_seen_text = str(item.get("last_seen_utc", ""))
        last_seen_epoch = latest_timestamp
        if last_seen_text:
            with contextlib.suppress(ValueError):
                last_seen_epoch = max(
                    last_seen_epoch,
                    int(datetime.fromisoformat(last_seen_text.replace("Z", "+00:00")).timestamp()),
                )
        online_window = max(180, int(item.get("scan_interval_seconds") or self.scan_interval_seconds) * 3)
        return last_seen_epoch > 0 and int(datetime.now(UTC).timestamp()) - last_seen_epoch <= online_window
    def _connected_devices(self, devices: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Hide historical/offline counters from the live analysis views."""
        return [item for item in devices if self._device_is_connected(item)]
    def _data_revision(self) -> tuple[int, int | None, int]:
        count = self.store.count(all_devices=True)
        _first, last = self.store.bounds()
        # A minute bucket lets cached environmental context refresh even when no
        # new radiation sample has arrived.
        return count, last, int(time.time() // 60)

    def _live_analysis_cached(
        self, *, device_serial: str, scan_interval_seconds: int, cpm_per_usvh: float
    ) -> dict[str, Any]:
        key = (
            "live-analysis",
            self._data_revision()[:2],
            device_serial,
            scan_interval_seconds,
            self.traffic_light_yellow_percent,
            self.traffic_light_red_percent,
        )

        def build() -> dict[str, Any]:
            result = build_live_analysis(
                self.store,
                scan_interval_seconds=scan_interval_seconds,
                traffic_light_yellow_percent=self.traffic_light_yellow_percent,
                traffic_light_red_percent=self.traffic_light_red_percent,
                device_serial=device_serial,
            )
            result["_scan_interval_seconds"] = scan_interval_seconds
            result["_cpm_per_usvh"] = cpm_per_usvh
            return result

        return self.analysis_cache.get_or_build(key, build)

    def _fleet_context_cached(self, *, selected_serial: str, devices: list[dict[str, Any]]) -> dict[str, Any]:
        revision = self._data_revision()
        device_signature = tuple(
            sorted(
                (
                    str(item.get("serial") or ""),
                    int(float(item.get("scan_interval_seconds") or self.scan_interval_seconds)),
                )
                for item in devices
                if item.get("serial")
            )
        )
        key = ("fleet-context", revision, selected_serial, device_signature)

        def build() -> dict[str, Any]:
            fleet_snapshot = build_fleet_snapshot(self.store)
            selected_rows = self.store.query_all(device_serial=selected_serial) if selected_serial else []
            device_profile = (
                build_adaptive_background(selected_rows, timezone_name=self.timezone_name)
                if selected_serial
                else {"available": False}
            )
            rows_by_serial = {
                str(item.get("serial")): self.store.query_all(device_serial=str(item.get("serial")))
                for item in devices
                if item.get("serial")
            }
            tolerance = max(
                [
                    int(float(item.get("scan_interval_seconds") or self.scan_interval_seconds))
                    for item in devices
                ]
                or [self.scan_interval_seconds]
            )
            site_profile = build_site_adaptive_background(
                rows_by_serial,
                timezone_name=self.timezone_name,
                device_weights=fleet_snapshot.get("device_weights", {}),
                tolerance_seconds=tolerance,
            )
            pressure_snapshot = (
                self.pressure_client.get_pressure().as_dict()
                if self.pressure_client is not None
                else {"available": False, "error": "Pressure client is not configured"}
            )
            barometric_hint = build_barometric_cosmic_hint(
                rows_by_serial,
                timezone_name=self.timezone_name,
                device_weights=fleet_snapshot.get("device_weights", {}),
                tolerance_seconds=tolerance,
                pressure_snapshot=pressure_snapshot,
                enabled=self.cosmic_hint_enabled,
            )
            return {
                "fleet_snapshot": fleet_snapshot,
                "device_profile": device_profile,
                "site_profile": site_profile,
                "barometric_hint": barometric_hint,
            }

        return self.analysis_cache.get_or_build(key, build)

    def status(self) -> dict[str, Any]:
        count = self.store.count(all_devices=True)
        first, last = self.store.bounds()
        metadata = self.store.get_metadata()
        database = self.store.database_stats()
        capabilities = self.store.get_device_capabilities()
        devices = self.store.list_devices()
        ingest = self.store.get_ingest_diagnostics()
        home_location = (
            self.home_assistant_client.get_location().as_dict()
            if self.home_assistant_client is not None
            else {"available": False, "error": "Home Assistant API client is not configured"}
        )
        return {
            "status": "ok",
            "measurements": count,
            "first_timestamp_utc": first,
            "last_timestamp_utc": last,
            "timezone": self.timezone_name,
            "scan_interval_seconds": self.scan_interval_seconds,
            "history_retention_days": self.store.retention_days,
            "cpm_per_usvh": self.cpm_per_usvh,
            "traffic_light_yellow_percent": self.traffic_light_yellow_percent,
            "traffic_light_red_percent": self.traffic_light_red_percent,
            "safety_profile": self.safety_profile,
            "safety_threshold_basis": self.safety_threshold_basis,
            "safety_warning_cpm": self.safety_warning_cpm,
            "safety_danger_cpm": self.safety_danger_cpm,
            "safety_warning_usvh": self.safety_warning_usvh,
            "safety_danger_usvh": self.safety_danger_usvh,
            "restore_enabled": self.restore_enabled,
            "device_model": metadata.get("device_model", "Not detected yet"),
            "serial": metadata.get("serial", "Not detected yet"),
            "device_profile": metadata.get(
                "device_profile_name", metadata.get("device_profile", "Not detected yet")
            ),
            "capabilities": capabilities,
            "database": database,
            "ingest_diagnostics": ingest,
            "devices": devices,
            "home_assistant_location": home_location,
        }

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
        selected_device_label = (
            f"{selected_device.get('configured_name') or normalize_device_version_display(str(selected_device.get('device_model', 'GMC')))} · {selected_serial}"
            if selected_device
            else ""
        )
        timezone_text = str(self.timezone_name)
        timezone_name = html.escape(timezone_text)
        count = int(status["measurements"])
        home_location = status.get("home_assistant_location") or {}
        if home_location.get("available"):
            location_name = str(home_location.get("location_name") or t("Configured location"))
            latitude = home_location.get("latitude")
            longitude = home_location.get("longitude")
            elevation = home_location.get("elevation")
            country = str(home_location.get("country") or "")
            location_parts: list[str] = []
            if latitude is not None and longitude is not None:
                location_parts.append(f"{t('Coordinates')}: {float(latitude):.5f}, {float(longitude):.5f}")
            if elevation is not None:
                location_parts.append(f"{t('Elevation')}: {float(elevation):g} m")
            if country:
                location_parts.append(f"{t('Country')}: {country}")
            location_parts.append(f"{t('Timezone')}: {timezone_text}")
            location_details = " · ".join(location_parts)
            location_details_html = (
                '<details class="location-details">'
                f'<summary><span class="details-summary-icon">📍</span><span><strong>{html.escape(t("Home Assistant location"))}</strong>'
                f"<small>{html.escape(location_name)}</small></span></summary>"
                '<div class="location-details-body">'
                f'<div class="location-details-values"><strong>{html.escape(location_name)}</strong>'
                f"<span>{html.escape(location_details)}</span></div>"
                f"<p>{html.escape(t('Location data comes from the Home Assistant general settings and is not sent to an external geocoding service.'))}</p>"
                "</div></details>"
            )
        else:
            location_name = t("Location unavailable")
            location_details_html = (
                '<details class="location-details">'
                f'<summary><span class="details-summary-icon">📍</span><span><strong>{html.escape(t("Home Assistant location"))}</strong>'
                f"<small>{html.escape(t('Location unavailable'))}</small></span></summary>"
                '<div class="location-details-body">'
                f'<div class="location-details-values"><span>{html.escape(t("Timezone"))}: {timezone_name}</span></div>'
                f"<p>{html.escape(t('Check the Home Assistant general settings and restart the add-on.'))}</p>"
                "</div></details>"
            )
        today = datetime.now(self.timezone).date().isoformat()
        iso = datetime.now(self.timezone).isocalendar()
        current_week = f"{iso.year}-W{iso.week:02d}"
        gyro_note = (
            t("Gyro data will be included when available.")
            if self.read_gyro
            else t("Gyro recording is disabled.")
        )
        database = status["database"]
        db_size_bytes = int(database.get("size_bytes", 0))
        db_size = f"{db_size_bytes / (1024 * 1024):.2f} MiB"
        now_epoch = int(datetime.now(UTC).timestamp())

        def _dashboard_timestamp(value: object, fallback: str | None = None) -> str:
            if value in (None, "", 0):
                return fallback or t("No data")
            try:
                return (
                    datetime.fromtimestamp(int(value), UTC)
                    .astimezone(self.timezone)
                    .strftime("%Y-%m-%d %H:%M:%S %Z")
                )
            except (TypeError, ValueError, OSError):
                return str(value)

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
        selected_latest_timestamp = int((selected_device or {}).get("timestamp_utc") or 0)
        selected_latest_cpm = (selected_device or {}).get("cpm")
        selected_latest_value = (
            f"{int(selected_latest_cpm)} CPM" if selected_latest_cpm is not None else t("No measurement yet")
        )
        selected_latest_age = (
            max(0, now_epoch - selected_latest_timestamp) if selected_latest_timestamp else None
        )
        selected_latest_meta = (
            t("{seconds} seconds ago", seconds=selected_latest_age)
            if selected_latest_age is not None and selected_latest_age < 120
            else _dashboard_timestamp(selected_latest_timestamp)
        )
        global_last_timestamp = int(status.get("last_timestamp_utc") or 0)
        discarded_peak_samples = sum(
            int(item.get("cpm_discarded_peak_samples") or 0) for item in all_sorted_devices
        )
        db_integrity = str(database.get("integrity") or "unknown")
        db_state_class = "ok" if db_integrity == "ok" else "error"
        status_strip_html = f"""
<section class="status-strip" id="live-status" aria-label="{html.escape(t("Live system status"), quote=True)}">
<a class="status-strip-item {connection_state_class}" href="#devices"><span class="status-dot"></span><span><strong>{html.escape(t("Devices"))}</strong><small>{html.escape(connection_summary)}</small></span></a>
<a class="status-strip-item {"ok" if selected_latest_timestamp else "waiting"}" href="#analysis"><span class="status-dot"></span><span><strong>{html.escape(t("Latest accepted value"))}: {html.escape(selected_latest_value)}</strong><small>{html.escape(selected_latest_meta)}</small></span></a>
<a class="status-strip-item {"ok" if global_last_timestamp else "waiting"}" href="#maintenance"><span class="status-dot"></span><span><strong>{html.escape(t("Last successful storage"))}</strong><small>{html.escape(_dashboard_timestamp(global_last_timestamp))}</small></span></a>
<a class="status-strip-item {"warning" if discarded_peak_samples else "ok"}" href="#devices"><span class="status-dot"></span><span><strong>{html.escape(t("Discarded CPM peaks"))}: {discarded_peak_samples:,}</strong><small>{html.escape(t("Unconfirmed values since bridge start"))}</small></span></a>
<a class="status-strip-item ok" href="#maintenance"><span class="status-dot"></span><span><strong>{html.escape(t("Stored samples"))}: {count:,}</strong><small>{html.escape(t("Stored samples across all devices"))}</small></span></a>
<a class="status-strip-item {db_state_class}" href="#maintenance"><span class="status-dot"></span><span><strong>{html.escape(t("Database"))}: {html.escape(db_integrity)}</strong><small>{html.escape(db_size)}</small></span></a>
</section>
"""
        dashboard_controls_html = f"""
<nav class="dashboard-controls" id="dashboard-controls" aria-label="{html.escape(t("Dashboard navigation"), quote=True)}">
<div class="jump-links">
<a href="#devices">{html.escape(t("Devices"))}</a>
<a href="#radiation-intelligence">{html.escape(t("Intelligence"))}</a>
<a href="#analysis">{html.escape(t("Analysis"))}</a>
<a href="#history">{html.escape(t("History"))}</a>
<a href="#workflow">{html.escape(t("Workflows"))}</a>
<a href="#calibration-management">{html.escape(t("Calibration profiles"))}</a>
<a href="#reports">{html.escape(t("Reports"))}</a>
</div>
<div class="dashboard-actions">
<button type="button" class="compact-action" id="toggle-all-cards" aria-expanded="false">{html.escape(t("Expand all"))}</button>
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
                return (
                    datetime.fromtimestamp(int(value), UTC)
                    .astimezone(self.timezone)
                    .strftime("%Y-%m-%d %H:%M:%S %Z")
                )

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
<div class="metric"><strong>{html.escape(t("Measurements to delete"))}</strong><div class="value">{int(purge_preview.get("measurements", 0)):,}</div><small>{html.escape(purge_period)}</small></div>
<div class="metric"><strong>{html.escape(t("Raw-data archive"))}</strong><div class="value">{int(purge_preview.get("raw_measurements", 0)):,}</div><small>{html.escape(t("Raw device values are stored separately before quality filtering"))}</small></div>
<div class="metric"><strong>{html.escape(t("Events, annotations and diagnostics"))}</strong><div class="value">{int(purge_preview.get("events", 0)) + int(purge_preview.get("annotations", 0)) + int(purge_preview.get("diagnostics", 0)):,}</div><small>{html.escape(t("{events} events · {annotations} annotations · {diagnostics} diagnostics", events=int(purge_preview.get("events", 0)), annotations=int(purge_preview.get("annotations", 0)), diagnostics=int(purge_preview.get("diagnostics", 0))))}</small></div>
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
        analysis_level_controls_html = self._render_analysis_level_controls(
            default_level="summary" if mode == "simple" else "analysis",
            t=t,
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
        history_summary = {
            "samples": len(explorer_rows),
            "coverage_percent": min(100.0, 100.0 * len(explorer_rows) / expected_history_samples),
            "mean_cpm": statistics.fmean(history_values) if history_values else None,
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
        language_links = []
        for language_code, language_name in language_options:
            current = ' aria-current="page"' if language_code == language_preference else ""
            language_attribute = (
                f' lang="{html.escape(language_code, quote=True)}"'
                if language_code != "auto"
                else ""
            )
            title = (
                f' title="{html.escape(t("Use the browser or system language"), quote=True)}"'
                if language_code == "auto"
                else ""
            )
            language_links.append(
                f'<a href="?lang={quote_plus(language_code)}{language_query_suffix}"'
                f"{language_attribute}{title}{current}>{html.escape(language_name)}</a>"
            )
        language_switcher_html = (
            f'<nav class="language-switcher" aria-label="{html.escape(t("Language"), quote=True)}">'
            + "".join(language_links)
            + "</nav>"
        )
        page = f"""<!doctype html>
<html lang="{language}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(t("GMC Radiation Monitoring"))}</title>
<style>{DASHBOARD_CSS}</style>
</head>
<body class="mode-{mode}" data-analysis-level="{"summary" if mode == "simple" else "analysis"}"><div class="page-scroll" id="page-scroll"><main>
<header class="report-header">
<div class="header-intro">
<h1>{html.escape(t("GMC Radiation Monitoring"))}</h1>
<p>{html.escape(t("Local monitoring for GQ GMC Geiger counters"))}</p>
{language_switcher_html}
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
{analysis_level_controls_html}
{status_strip_html}
{dashboard_controls_html}
<div id="primary-dashboard" class="primary-dashboard">
{multi_device_html}
{radiation_intelligence_html}
{adaptive_background_html}
{cosmic_influence_html}
{fleet_intelligence_html}
</div>
{analysis_html}
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

<div class="advanced-only"><h3>{html.escape(t("Custom period"))}</h3>
<div class="custom-periods">
<form class="custom-form report-preset-source" action="" method="get" data-preset-kind="daily">
<input type="hidden" name="action" value="download">
<input type="hidden" name="period" value="daily">
<input type="hidden" name="selection" value="specific">
<div class="form-grid">
<label>{html.escape(t("Specific date"))}<input type="date" name="date" value="{today}" required></label>
<label>{html.escape(t("Format"))}<select name="format">{format_options}</select></label>
<div class="form-actions"><button type="submit" class="primary">{html.escape(t("Download"))}</button></div>
</div>
</form>
<form class="custom-form report-preset-source" action="" method="get" data-preset-kind="weekly">
<input type="hidden" name="action" value="download">
<input type="hidden" name="period" value="weekly">
<input type="hidden" name="selection" value="specific">
<div class="form-grid">
<label>{html.escape(t("Specific ISO week"))}<input type="week" name="week" value="{current_week}" required></label>
<label>{html.escape(t("Format"))}<select name="format">{format_options}</select></label>
<div class="form-actions"><button type="submit" class="primary">{html.escape(t("Download"))}</button></div>
</div>
</form>
</div></div>

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
</div>
{managed_backups_html}
<details class="analysis-group history-management-tool" id="history-restore"><summary><span class="summary-copy">{html.escape(t("Restore history"))}<small>{html.escape(t("Preview and merge a compatible SQLite backup"))}</small></span></summary><div class="group-body">{restore_controls}</div></details>
<details class="analysis-group history-management-tool" id="history-delete"><summary><span class="summary-copy">{html.escape(t("Delete history"))}<small>{html.escape(t("Permanently remove app and Recorder history after explicit confirmation"))}</small></span></summary><div class="group-body">{purge_controls}</div></details>
</section>
</main></div>
<script nonce="{html.escape(script_nonce, quote=True)}">{render_dashboard_script(selected_serial=selected_serial, language=language, translator=t)}</script></body></html>"""
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

    @staticmethod
    def _render_collapsible_card(
        *,
        card_id: str,
        title: str,
        body: str,
        attributes: str = "",
        open_by_default: bool = True,
        help_text: str = "",
        explanation_code: str | None = None,
        t: Translator | None = None,
        pin_label: str = "Pin card",
        help_label: str = "Show help",
    ) -> str:
        return render_collapsible_card(
            card_id=card_id,
            title=title,
            body=body,
            attributes=attributes,
            open_by_default=open_by_default,
            help_text=help_text,
            explanation_code=explanation_code,
            translator=t,
            pin_label=pin_label,
            help_label=help_label,
        )

    @staticmethod
    def _render_analysis_level_controls(*, default_level: str, t) -> str:
        return render_analysis_level_controls(default_level=default_level, translator=t)

    @staticmethod
    def _trend_symbol(value: float | None) -> str:
        return trend_symbol(value)

    @staticmethod
    def _background_profile_block(profile: dict[str, Any], *, title: str, t: Translator) -> str:
        """Compatibility wrapper for callers predating the shared model migration."""
        entity = build_background_profile_entity(
            profile, key=slugify(title) or "background-profile", title=title
        )
        return render_background_profile_entity(entity, t)

    @staticmethod
    def _fleet_stability_display_key(item: Any) -> tuple[int, str, str]:
        """Compatibility wrapper for the shared fleet-card ordering rule."""
        return fleet_stability_display_key(item)

    def _render_radiation_intelligence(
        self,
        *,
        analysis: dict[str, Any],
        selected_serial: str,
        snapshot: dict[str, Any],
        t,
        device_profile: dict[str, Any],
        site_profile: dict[str, Any],
    ) -> str:
        recent_move = any(
            str(event.get("serial")) == selected_serial
            and int(snapshot.get("generated_at_utc", 0)) - int(event.get("timestamp_utc", 0)) <= 1800
            for event in snapshot.get("orientation_events", [])
        )
        raw_result = build_radiation_intelligence(
            analysis,
            comparison=snapshot.get("comparison"),
            shared_event=snapshot.get("shared_event"),
            recent_orientation_change=recent_move,
            device_profile=device_profile,
            site_profile=site_profile,
        )
        collected = int(analysis.get("samples_24h") or analysis.get("samples_1h") or 0)
        needed = max(
            0,
            int(analysis.get("baseline_minimum_samples") or 6) - int(analysis.get("samples_7d") or 0),
        )
        result = build_radiation_intelligence_result(raw_result, collected=collected, needed=needed)
        return render_radiation_intelligence(result, t)

    def _render_adaptive_background(
        self, *, device_profile: dict[str, Any], site_profile: dict[str, Any], t
    ) -> str:
        result = build_adaptive_background_result(device_profile, site_profile)
        return render_adaptive_background(result, t)

    def _render_cosmic_influence(self, model: dict[str, Any], *, t) -> str:
        result = build_cosmic_influence_result(model)
        return render_cosmic_influence(result, t)

    def _render_fleet_intelligence(self, *, t, snapshot: dict[str, Any] | None = None) -> str:
        result = build_fleet_intelligence_result(snapshot or build_fleet_snapshot(self.store))
        return render_fleet_intelligence(result, t)

    def _render_devices_section(
        self,
        *,
        devices: list[dict[str, Any]],
        selected_serial: str,
        mode: str,
        language: str,
        t: Translator,
    ) -> str:
        capability_labels = {
            "cpm": "CPM",
            "temperature": t("Temperature"),
            "voltage": t("Voltage"),
            "gyro": t("Gyroscope"),
            "dual_tube": t("Dual-tube measurement"),
            "device_time": t("Device time"),
            "tube_low_cpm": t("Low-dose tube"),
            "tube_high_cpm": t("High-dose tube"),
        }

        def render_device_card(item: dict[str, Any]) -> str:
            serial_value = str(item.get("serial", "unknown"))
            selected = serial_value == selected_serial
            capabilities_map = item.get("capabilities_map") or {}
            if capabilities_map:
                enabled = [
                    capability_labels.get(name, name.replace("_", " "))
                    for name, supported in capabilities_map.items()
                    if supported
                ]
            else:
                enabled = [
                    capability_labels.get(name.strip(), name.strip().replace("_", " "))
                    for name in str(item.get("capabilities", "")).split(",")
                    if name.strip()
                ]
            capabilities_value = ", ".join(enabled) or t("Not detected yet")
            latest_timestamp = int(item.get("timestamp_utc") or item.get("last_timestamp_utc") or 0)
            last_seen_text = str(item.get("last_seen_utc", ""))
            last_seen_epoch = latest_timestamp
            if last_seen_text:
                with contextlib.suppress(ValueError):
                    last_seen_epoch = max(
                        last_seen_epoch,
                        int(datetime.fromisoformat(last_seen_text.replace("Z", "+00:00")).timestamp()),
                    )
            online_window = max(180, int(item.get("scan_interval_seconds") or self.scan_interval_seconds) * 3)
            runtime_online = item.get("runtime_online")
            if isinstance(runtime_online, str):
                runtime_online = runtime_online.strip().lower() in {"1", "true", "yes", "on", "online"}
            if runtime_online is None:
                online = (
                    last_seen_epoch > 0
                    and int(datetime.now(UTC).timestamp()) - last_seen_epoch <= online_window
                )
            else:
                # The bridge owns the authoritative per-device connection state.
                # Analysis selection is a read-only view and must never affect it.
                online = bool(runtime_online)
            status_class = "online" if online else "offline"
            status_label = t("Online") if online else t("Offline")

            def format_external_timestamp(value: object, fallback: str) -> str:
                if value in (None, ""):
                    return fallback
                try:
                    parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
                    return parsed.astimezone(self.timezone).strftime("%Y-%m-%d %H:%M:%S %Z")
                except (TypeError, ValueError):
                    return str(value)

            if latest_timestamp:
                last_update = (
                    datetime.fromtimestamp(latest_timestamp, UTC)
                    .astimezone(self.timezone)
                    .strftime("%Y-%m-%d %H:%M:%S %Z")
                )
            else:
                last_update = t("Not detected yet")
            profile = t(str(item.get("device_profile_name", item.get("device_profile", "unknown"))))
            model_display = normalize_device_version_display(str(item.get("device_model", "GMC")))
            normalized_model = model_display.casefold().replace(" ", "")
            if "320" in normalized_model:
                device_visual_class, device_icon = "device-320", "320"
            elif "500" in normalized_model:
                device_visual_class, device_icon = "device-500", "500+"
            else:
                device_visual_class, device_icon = "device-generic", "GMC"
            latest_cpm = item.get("cpm")
            latest_value = "—" if latest_cpm is None else f"{int(latest_cpm)} CPM"
            tube_values = ""
            if item.get("tube_low_cpm") is not None or item.get("tube_high_cpm") is not None:
                tube_values = (
                    f'<div class="device-field"><strong>{html.escape(t("Low-dose tube"))}</strong>'
                    f"<span>{html.escape(str(item.get('tube_low_cpm', '—')))} CPM</span></div>"
                    f'<div class="device-field"><strong>{html.escape(t("High-dose tube"))}</strong>'
                    f"<span>{html.escape(str(item.get('tube_high_cpm', '—')))} CPM</span></div>"
                )
            diagnostics_values: list[str] = []
            for label, key in (
                ("Hardware model", "hardware_model"),
                ("Firmware version", "firmware_version"),
            ):
                value = item.get(key)
                if value not in (None, "", "unknown"):
                    diagnostics_values.append(
                        f'<div class="device-field"><strong>{html.escape(t(label))}</strong>'
                        f"<span>{html.escape(str(value))}</span></div>"
                    )
            if item.get("voltage_v") is not None:
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Battery voltage"))}</strong>'
                    f"<span>{float(item['voltage_v']):.2f} V</span></div>"
                )
            if item.get("device_time"):
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Device clock"))}</strong>'
                    f"<span>{html.escape(str(item['device_time']))}</span></div>"
                )
            if item.get("device_clock_offset_seconds") is not None:
                offset = int(item["device_clock_offset_seconds"])
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Device clock offset"))}</strong>'
                    f"<span>{offset:+d} s</span></div>"
                )
            clock_status = str(item.get("device_clock_status", ""))
            clock_status_labels = {
                "ok": "Clock synchronized",
                "warning": "Clock offset exceeds warning threshold",
                "unavailable": "Device clock unavailable",
                "invalid": "Invalid device clock response",
            }
            if clock_status in clock_status_labels:
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Device clock status"))}</strong>'
                    f"<span>{html.escape(t(clock_status_labels[clock_status]))}</span></div>"
                )
            if item.get("heartbeat_enabled"):
                cps_value = item.get("heartbeat_cps", "—")
                rolling_value = item.get("heartbeat_cpm_60s", "—")
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Live radiation CPS"))}</strong>'
                    f"<span>{html.escape(str(cps_value))} CPS</span></div>"
                )
                diagnostics_values.append(
                    f'<div class="device-field"><strong>{html.escape(t("Heartbeat rolling 60 s CPM"))}</strong>'
                    f"<span>{html.escape(str(rolling_value))} CPM</span></div>"
                )
            gyro_values = (item.get("gyro_x"), item.get("gyro_y"), item.get("gyro_z"))
            if all(value is not None for value in gyro_values):
                raw_x, raw_y, raw_z = (int(value) for value in gyro_values)
                orientation = calculate_orientation(serial_value, raw_x, raw_y, raw_z)
                if orientation is not None:
                    status_key, status_color = orientation_status(orientation)
                    diagnostics_values.extend(
                        [
                            f'<div class="orientation-state {status_color}">'
                            f'<div class="orientation-state-copy"><strong>{html.escape(t("Device position"))} · {html.escape(t(status_key))}</strong>'
                            f"<span>{html.escape(t(orientation.position_key))}</span>"
                            f"<small>{html.escape(t('Inclination'))}: {orientation.inclination_degrees:.1f}°</small></div></div>",
                            f'<div class="device-field"><strong>{html.escape(t("Roll angle"))}</strong>'
                            f"<span>{orientation.roll_degrees:+.1f}°</span></div>",
                            f'<div class="device-field"><strong>{html.escape(t("Pitch angle"))}</strong>'
                            f"<span>{orientation.pitch_degrees:+.1f}°</span></div>",
                            f'<div class="device-field"><strong>{html.escape(t("Inclination"))}</strong>'
                            f"<span>{orientation.inclination_degrees:.1f}°</span></div>",
                        ]
                    )
            device_diagnostics_values = "".join(diagnostics_values)

            calibration_html = render_calibration_panel(
                item=item,
                latest_cpm=latest_cpm,
                t=t,
            )
            gmcmap_html = ""
            if item.get("gmcmap_enabled"):
                raw_map_status = str(item.get("gmcmap_upload_status", "not_configured"))
                map_status_labels = {
                    "disabled": "Disabled",
                    "not_configured": "Not configured",
                    "waiting": "Waiting for first upload",
                    "uploading": "Uploading",
                    "success": "Upload successful",
                    "error": "Upload failed",
                }
                map_status_label = t(map_status_labels.get(raw_map_status, raw_map_status))
                map_status_class = {
                    "success": "online",
                    "uploading": "online",
                    "error": "error",
                    "not_configured": "offline",
                    "waiting": "waiting",
                }.get(raw_map_status, "offline")
                last_map_upload = format_external_timestamp(item.get("gmcmap_last_upload_utc"), t("Never"))
                counter_id_masked = item.get("gmcmap_counter_id_masked") or "—"
                map_error = ""
                if not item.get("gmcmap_configured"):
                    map_error = (
                        f'<div class="gmcmap-error">'
                        f"{html.escape(t('GMCMap is enabled, but this device has no counter ID mapping.'))}"
                        f"</div>"
                    )
                gmcmap_html = (
                    f'<div class="gmcmap-panel">'
                    f'<div class="gmcmap-header"><div><strong>{html.escape(t("Public GMCMap upload"))}</strong>'
                    f"<small>{html.escape(t('Measurements are sent to the public GMCMap service.'))}</small></div>"
                    f'<span class="device-status {map_status_class}">{html.escape(map_status_label)}</span></div>'
                    f'<div class="gmcmap-grid">'
                    f"<div><strong>{html.escape(t('Counter ID'))}</strong><span>{html.escape(str(counter_id_masked))}</span></div>"
                    f"<div><strong>{html.escape(t('Last upload'))}</strong><span>{html.escape(str(last_map_upload))}</span></div>"
                    f"<div><strong>{html.escape(t('Last uploaded CPM'))}</strong><span>{html.escape(str(item.get('gmcmap_last_cpm') if item.get('gmcmap_last_cpm') is not None else '—'))} CPM</span></div>"
                    f"<div><strong>{html.escape(t('Last uploaded ACPM'))}</strong><span>{html.escape(str(item.get('gmcmap_last_average_cpm') if item.get('gmcmap_last_average_cpm') is not None else '—'))} ACPM</span></div>"
                    f'</div><small class="gmcmap-acpm-help">{html.escape(t("ACPM is the average of all accepted CPM readings since the current app measurement session began."))}</small>'
                    f"{map_error}</div>"
                )
            alerts: list[str] = []
            health_status = str(item.get("device_health_status") or "ok")
            health_reason = str(item.get("device_health_reason") or "normal_variation")
            health_reason_labels = {
                "prolonged_zero_cpm": "Unusually long sequence of zero CPM values",
                "unchanged_cpm_sequence": "CPM has remained exactly unchanged for an unusually long time",
                "dual_tube_imbalance": "Dual-tube values are persistently implausible",
                "normal_variation": "Device values vary normally",
                "initializing": "Device health monitoring is still initializing",
            }
            if health_status != "ok":
                alerts.append(
                    f'<div class="device-alert warning"><strong>{html.escape(t("Device health warning"))}</strong>'
                    f"<span>{html.escape(t(health_reason_labels.get(health_reason, health_reason)))}</span></div>"
                )
            pending_confirmations = int(item.get("cpm_gate_pending_confirmations") or 0)
            required_confirmations = int(item.get("cpm_gate_required_confirmations") or 3)
            if pending_confirmations:
                alerts.append(
                    f'<div class="device-alert warning"><strong>{html.escape(t("Suspicious CPM value is being verified"))}</strong>'
                    f"<span>{pending_confirmations}/{required_confirmations} {html.escape(t('confirmations'))}</span></div>"
                )
            discarded_peaks = int(item.get("cpm_discarded_peak_samples") or 0)
            if discarded_peaks:
                alerts.append(
                    f'<div class="device-alert info"><strong>{html.escape(t("Discarded unconfirmed CPM peaks"))}</strong>'
                    f"<span>{discarded_peaks:,} {html.escape(t('since the current bridge start'))}</span></div>"
                )
            serial_errors = int(item.get("serial_error_count") or 0)
            reconnects = int(item.get("serial_reconnect_count") or 0)
            if serial_errors or reconnects:
                alerts.append(
                    f'<div class="device-alert info"><strong>{html.escape(t("Serial connection recovered"))}</strong>'
                    f"<span>{serial_errors} {html.escape(t('errors'))} · {reconnects} {html.escape(t('reconnects'))}</span></div>"
                )
            history_errors = int(item.get("history_write_error_count") or 0)
            if history_errors:
                alerts.append(
                    f'<div class="device-alert error"><strong>{html.escape(t("History storage warning"))}</strong>'
                    f"<span>{history_errors} {html.escape(t('write errors since app start'))}</span></div>"
                )
            if clock_status == "warning":
                alerts.append(
                    f'<div class="device-alert warning"><strong>{html.escape(t("Device clock warning"))}</strong>'
                    f"<span>{html.escape(t('The device clock differs from Home Assistant time.'))}</span></div>"
                )
            alert_html = (
                f'<div class="device-alerts">{"".join(alerts)}</div>'
                if alerts
                else f'<div class="device-ok"><span>✓</span>{html.escape(t("No active device warnings"))}</div>'
            )
            action_label = t("Analysis shown") if selected else t("Show analysis")
            href = f"?mode={mode}&amp;lang={language}&amp;device={quote_plus(serial_value)}"
            selected_class = " selected" if selected else ""
            primary_class = " primary" if selected else ""
            return (
                f'<article class="device-card {device_visual_class}{selected_class}" data-device-serial="{html.escape(serial_value, quote=True)}" data-device-model="{html.escape(model_display, quote=True)}">'
                f'<div class="device-card-header">'
                f'<div class="device-card-title"><div class="assessment-icon device-card-icon">{html.escape(device_icon)}</div>'
                f'<div class="device-card-title-copy"><h3>{html.escape(model_display)}</h3>'
                f"<small>{html.escape(serial_value)}</small></div></div>"
                f'<span class="device-status {status_class}">{html.escape(status_label)}</span></div>'
                f'<div class="device-live"><strong>{html.escape(t("Latest measurement"))}</strong>'
                f"<span>{html.escape(latest_value)}</span></div>"
                f"{alert_html}"
                '<div class="device-fields">'
                f'<div class="device-field"><strong>{html.escape(t("Serial"))}</strong><span>{html.escape(serial_value)}</span></div>'
                f'<div class="device-field"><strong>{html.escape(t("Serial port"))}</strong><span class="technical-value">{html.escape(str(item.get("port", "—")))}</span></div>'
                f'<div class="device-field"><strong>{html.escape(t("Baud rate"))}</strong><span>{html.escape(str(item.get("baudrate", "—")))}</span></div>'
                f'<div class="device-field"><strong>{html.escape(t("Measurement interval"))}</strong><span>{html.escape(str(item.get("scan_interval_seconds", "—")))} s</span></div>'
                f'<div class="device-field"><strong>{html.escape(t("Profile"))}</strong><span>{html.escape(profile)}</span></div>'
                f'<div class="device-field"><strong>{html.escape(t("Device capabilities"))}</strong><span>{html.escape(capabilities_value)}</span></div>'
                f'<div class="device-field"><strong>{html.escape(t("Stored samples for this device"))}</strong><span>{int(item.get("stored_samples") or 0):,}</span></div>'
                f'<div class="device-field"><strong>{html.escape(t("Last update"))}</strong><span>{html.escape(last_update)}</span></div>'
                f"{tube_values}{device_diagnostics_values}</div>"
                f"{calibration_html}"
                f"{gmcmap_html}"
                f'<a class="button device-select{primary_class}" href="{href}">{html.escape(action_label)}</a>'
                "</article>"
            )

        device_cards = "".join(render_device_card(item) for item in devices) or (
            f'<div class="empty-state scanning"><span class="empty-state-icon">⌁</span>'
            f"<strong>{html.escape(t('GMC devices are being detected automatically'))}</strong>"
            f"<span>{html.escape(t('No connected counter is available yet. The next serial scan runs automatically.'))}</span></div>"
        )
        connected_count = sum(1 for item in devices if self._device_is_connected(item))
        return self._render_collapsible_card(
            card_id="devices",
            title=t("Connected GMC devices"),
            body=f'<div class="device-grid">{device_cards}</div>',
            attributes=(
                f'data-connected-count="{connected_count}" '
                f'data-selected-serial="{html.escape(selected_serial, quote=True)}"'
            ),
            help_text=t(
                "Shows live connection state, the latest accepted measurement and warnings for each automatically detected GMC counter."
            ),
            pin_label=t("Pin card"),
            help_label=t("Show help"),
        )

    def render_devices_fragment(
        self,
        *,
        mode_override: str | None = None,
        language_override: str | None = None,
        device_override: str | None = None,
        report_device_override: str | None = None,
        accept_language: str = "",
    ) -> bytes:
        mode = mode_override if mode_override in {"simple", "advanced"} else self.ui_mode
        language = resolve_language(
            self.ui_language, accept_language=accept_language, override=language_override
        )
        t = Translator(language)
        all_sorted_devices = sorted(
            self.store.list_devices(),
            key=lambda item: (str(item.get("device_model", "")), str(item.get("serial", ""))),
        )
        devices = self._connected_devices(all_sorted_devices)
        card_devices = self._connected_devices(all_sorted_devices)
        device_serials = {str(item.get("serial")) for item in devices if item.get("serial")}
        primary_serial = str(self.store.get_metadata().get("serial", ""))
        if primary_serial not in device_serials:
            primary_serial = next(iter(sorted(device_serials)), "")
        selected_serial = device_override if device_override in device_serials else primary_serial
        _encode_report_target(selected_serial) if selected_serial else ""
        return self._render_devices_section(
            devices=card_devices,
            selected_serial=selected_serial,
            mode=mode,
            language=language,
            t=t,
        ).encode("utf-8")

    def _analysis_scan_interval(self, analysis: dict[str, Any]) -> int:
        return max(5, int(analysis.get("_scan_interval_seconds") or self.scan_interval_seconds))

    def _analysis_cpm_per_usvh(self, analysis: dict[str, Any]) -> float:
        value = float(analysis.get("_cpm_per_usvh") or self.cpm_per_usvh)
        return value if value > 0 else self.cpm_per_usvh

    def _device_report_settings(self, device_serial: str | None) -> tuple[int, float]:
        if device_serial:
            for item in self.store.list_devices():
                if str(item.get("serial")) == device_serial:
                    return (
                        max(5, int(item.get("scan_interval_seconds") or self.scan_interval_seconds)),
                        float(item.get("cpm_per_usvh") or self.cpm_per_usvh),
                    )
        return self.scan_interval_seconds, self.cpm_per_usvh

    def _presentation_config(self) -> AnalysisPresentationConfig:
        return AnalysisPresentationConfig(
            scan_interval_seconds=self.scan_interval_seconds,
            cpm_per_usvh=self.cpm_per_usvh,
            traffic_light_yellow_percent=self.traffic_light_yellow_percent,
            traffic_light_red_percent=self.traffic_light_red_percent,
            safety_profile=self.safety_profile,
            safety_threshold_basis=self.safety_threshold_basis,
            safety_warning_cpm=self.safety_warning_cpm,
            safety_danger_cpm=self.safety_danger_cpm,
            safety_warning_usvh=self.safety_warning_usvh,
            safety_danger_usvh=self.safety_danger_usvh,
        )

    def _render_analysis(
        self,
        analysis: dict[str, Any],
        *,
        advanced: bool = True,
        t: Translator | None = None,
        device_label: str = "",
        device_model: str = "",
    ) -> str:
        t = t or Translator("en")
        latest_local = None
        if analysis.get("available") and analysis.get("latest_timestamp_utc") is not None:
            latest_local = datetime.fromtimestamp(int(analysis["latest_timestamp_utc"]), UTC).astimezone(
                self.timezone
            )
        config = self._presentation_config()
        result = build_detailed_analysis_result(analysis, config=config, latest_local=latest_local)
        safety = build_absolute_safety_result(analysis, config=config)
        background = build_local_background_result(analysis, config=config)
        interpretation = build_combined_interpretation_result(analysis, config=config)
        return render_device_analysis(
            result,
            safety=safety,
            background=background,
            interpretation=interpretation,
            t=t,
            advanced=advanced,
            device_label=device_label,
            device_model=device_model,
        )

    def _effective_safety_thresholds(self, cpm_per_usvh: float | None = None) -> dict[str, Any]:
        return effective_safety_thresholds(self._presentation_config(), cpm_per_usvh=cpm_per_usvh)

    def _safety_state(self, analysis: dict[str, Any]) -> tuple[str, dict[str, Any], float, float]:
        return safety_state(analysis, config=self._presentation_config())

    def _render_safety_status(self, analysis: dict[str, Any], *, t: Translator | None = None) -> str:
        translator = t or Translator("en")
        return render_absolute_safety(
            build_absolute_safety_result(analysis, config=self._presentation_config()),
            translator,
        )

    def _baseline_state(self, analysis: dict[str, Any]) -> tuple[str, float | None, float]:
        return baseline_state(analysis, config=self._presentation_config())

    def _render_traffic_light(self, analysis: dict[str, Any], *, t: Translator | None = None) -> str:
        translator = t or Translator("en")
        return render_local_background(
            build_local_background_result(analysis, config=self._presentation_config()),
            translator,
        )

    def _render_combined_interpretation(
        self, analysis: dict[str, Any], *, t: Translator | None = None
    ) -> str:
        translator = t or Translator("en")
        return render_combined_interpretation(
            build_combined_interpretation_result(analysis, config=self._presentation_config()),
            translator,
        )

    def _render_recommendation(self, analysis: dict[str, Any], *, t: Translator | None = None) -> str:
        translator = t or Translator("en")
        return render_recommendation(
            build_recommendation_result(analysis, config=self._presentation_config()),
            translator,
        )
    def _render_assessment_legend(self, *, t: Translator | None = None) -> str:
        return render_assessment_legend(t or Translator("en"))
def run_report_server() -> None:
    level_name = os.environ.get("LOG_LEVEL", "info").upper()
    configure_secure_logging(
        level=getattr(logging, level_name, logging.INFO),
        format_string="%(asctime)s %(levelname)s %(message)s",
    )
    timezone_name = os.environ.get("REPORT_TIMEZONE", "UTC")
    scan_interval = int(os.environ.get("SCAN_INTERVAL", "60"))
    retention_days = int(os.environ.get("HISTORY_RETENTION_DAYS", "90"))
    read_gyro = os.environ.get("READ_GYRO", "false").strip().lower() == "true"
    history_management_enabled = (
        os.environ.get(
            "HISTORY_MANAGEMENT_ENABLED",
            os.environ.get("ENABLE_RESTORE", os.environ.get("ENABLE_PURGE_ALL_HISTORY", "false")),
        )
        .strip()
        .lower()
        == "true"
    )
    cpm_per_usvh = float(os.environ.get("CPM_PER_USVH", "154.0"))
    traffic_light_yellow_percent = float(os.environ.get("TRAFFIC_LIGHT_YELLOW_PERCENT", "125.0"))
    traffic_light_red_percent = float(os.environ.get("TRAFFIC_LIGHT_RED_PERCENT", "175.0"))
    safety_profile = os.environ.get("SAFETY_PROFILE", "gq").strip().lower()
    safety_threshold_basis = os.environ.get("SAFETY_THRESHOLD_BASIS", "either").strip().lower()
    safety_warning_cpm = int(os.environ.get("SAFETY_WARNING_CPM", "51"))
    safety_danger_cpm = int(os.environ.get("SAFETY_DANGER_CPM", "100"))
    safety_warning_usvh = float(os.environ.get("SAFETY_WARNING_USVH", "0.326"))
    safety_danger_usvh = float(os.environ.get("SAFETY_DANGER_USVH", "0.651"))
    ui_mode = os.environ.get("UI_MODE", "simple").strip().lower()
    ui_language = os.environ.get("UI_LANGUAGE", "auto").strip().lower()
    cosmic_hint_enabled = os.environ.get("COSMIC_HINT_ENABLED", "true").strip().lower() == "true"
    pressure_weather_entity_primary = os.environ.get(
        "PRESSURE_WEATHER_ENTITY_PRIMARY", "weather.forecast_home"
    ).strip()
    pressure_weather_entity_secondary = os.environ.get(
        "PRESSURE_WEATHER_ENTITY_SECONDARY", "weather.forecast_balkon"
    ).strip()
    pressure_weather_source_name = os.environ.get(
        "PRESSURE_WEATHER_SOURCE_NAME", "Meteorologisk institutt (Met.no)"
    ).strip()
    pressure_weather_max_age_seconds = int(os.environ.get("PRESSURE_WEATHER_MAX_AGE_SECONDS", "7200"))
    pressure_weather_max_difference_hpa = float(os.environ.get("PRESSURE_WEATHER_MAX_DIFFERENCE_HPA", "5.0"))
    load_timezone(timezone_name)
    if scan_interval < 5:
        raise ValueError("SCAN_INTERVAL must be at least 5 seconds")
    if not 7 <= retention_days <= 3650:
        raise ValueError("HISTORY_RETENTION_DAYS must be between 7 and 3650")
    if cpm_per_usvh <= 0:
        raise ValueError("CPM_PER_USVH must be greater than 0")
    if traffic_light_yellow_percent < 100:
        raise ValueError("TRAFFIC_LIGHT_YELLOW_PERCENT must be at least 100")
    if traffic_light_red_percent <= traffic_light_yellow_percent:
        raise ValueError("TRAFFIC_LIGHT_RED_PERCENT must be greater than TRAFFIC_LIGHT_YELLOW_PERCENT")
    if safety_profile not in {"gq", "bfs_reference", "icrp_reference", "custom"}:
        raise ValueError("SAFETY_PROFILE must be gq, bfs_reference, icrp_reference, or custom")
    if safety_threshold_basis not in {"cpm", "dose_rate", "either"}:
        raise ValueError("SAFETY_THRESHOLD_BASIS must be cpm, dose_rate, or either")
    if safety_warning_cpm < 0 or safety_danger_cpm <= safety_warning_cpm:
        raise ValueError("CPM safety danger threshold must be greater than warning threshold")
    if safety_warning_usvh < 0 or safety_danger_usvh <= safety_warning_usvh:
        raise ValueError("Dose-rate safety danger threshold must be greater than warning threshold")
    if ui_mode not in {"simple", "advanced"}:
        raise ValueError("UI_MODE must be simple or advanced")
    if ui_language not in {"auto", *SUPPORTED_UI_LANGUAGES}:
        raise ValueError("UI_LANGUAGE is unsupported")
    store = HistoryStore(DEFAULT_DB_PATH, retention_days=retention_days)
    home_assistant_client = HomeAssistantConfigClient()
    pressure_client = (
        HomeAssistantPressureClient(
            entity_ids=(pressure_weather_entity_primary, pressure_weather_entity_secondary),
            provider_name=pressure_weather_source_name,
            max_age_seconds=pressure_weather_max_age_seconds,
            max_difference_hpa=pressure_weather_max_difference_hpa,
        )
        if cosmic_hint_enabled
        else None
    )
    app = ReportApplication(
        store=store,
        timezone_name=timezone_name,
        scan_interval_seconds=scan_interval,
        read_gyro=read_gyro,
        cpm_per_usvh=cpm_per_usvh,
        traffic_light_yellow_percent=traffic_light_yellow_percent,
        traffic_light_red_percent=traffic_light_red_percent,
        safety_profile=safety_profile,
        safety_threshold_basis=safety_threshold_basis,
        safety_warning_cpm=safety_warning_cpm,
        safety_danger_cpm=safety_danger_cpm,
        safety_warning_usvh=safety_warning_usvh,
        safety_danger_usvh=safety_danger_usvh,
        ui_mode=ui_mode,
        ui_language=ui_language,
        history_management_enabled=history_management_enabled,
        home_assistant_client=home_assistant_client,
        pressure_client=pressure_client,
        cosmic_hint_enabled=cosmic_hint_enabled,
    )
    automation_service = WorkflowAutomationService(
        store=store,
        timezone=app.timezone,
        timezone_name=timezone_name,
        scan_interval_seconds=scan_interval,
        cpm_per_usvh=cpm_per_usvh,
        traffic_light_yellow_percent=traffic_light_yellow_percent,
        traffic_light_red_percent=traffic_light_red_percent,
        home_assistant_client=home_assistant_client,
        ui_language=ui_language,
        report_slot=app.report_slot,
        backup_manager=app.backup_manager,
    )
    automation_service.start()
    max_http_workers = int(os.environ.get("HTTP_MAX_WORKERS", "12"))
    socket_timeout_seconds = float(os.environ.get("HTTP_SOCKET_TIMEOUT_SECONDS", "30"))
    if not 2 <= max_http_workers <= 64:
        raise ValueError("HTTP_MAX_WORKERS must be between 2 and 64")
    if not 5.0 <= socket_timeout_seconds <= 300.0:
        raise ValueError("HTTP_SOCKET_TIMEOUT_SECONDS must be between 5 and 300")
    server = BoundedThreadingHTTPServer(
        # Binding on all interfaces is required for Home Assistant add-on ingress.
        ("0.0.0.0", 8099),  # nosec B104
        ReportRequestHandler,
        max_workers=max_http_workers,
        socket_timeout_seconds=socket_timeout_seconds,
    )
    server.app = app  # type: ignore[attr-defined]
    LOG.info(
        "GMC report server ready on port 8099 (%s, %d stored measurements)",
        timezone_name,
        store.count(),
    )
    try:
        server.serve_forever(poll_interval=0.5)
    finally:
        automation_service.stop()
        server.server_close()
