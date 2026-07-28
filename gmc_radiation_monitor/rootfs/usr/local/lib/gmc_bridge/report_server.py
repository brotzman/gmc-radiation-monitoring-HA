from __future__ import annotations

import logging
import os

from .automation import WorkflowAutomationService
from .history import DEFAULT_DB_PATH, HistoryStore
from .home_assistant import HomeAssistantConfigClient, HomeAssistantPressureClient
from .report_web_http import ReportRequestHandler
from .reports import load_timezone
from .security_logging import configure_secure_logging
from .translations import SUPPORTED_UI_LANGUAGES
from .web_server import BoundedThreadingHTTPServer

LOG = logging.getLogger("gmc_reports")


def run_report_server() -> None:
    # Imported lazily to keep the application renderer independent from server startup.
    from .report_web import ReportApplication
    level_name = os.environ.get("LOG_LEVEL", "info").upper()
    configure_secure_logging(
        level=getattr(logging, level_name, logging.INFO),
        format_string="%(asctime)s %(levelname)s %(message)s",
    )
    timezone_name = os.environ.get("REPORT_TIMEZONE", "UTC")
    scan_interval = int(os.environ.get("SCAN_INTERVAL", "60"))
    retention_days = int(os.environ.get("HISTORY_RETENTION_DAYS", "730"))
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
    cosmic_hint_enabled = os.environ.get("COSMIC_HINT_ENABLED", "false").strip().lower() == "true"
    bridge_heartbeat_path = os.environ.get("BRIDGE_HEARTBEAT_PATH", "/data/gmc_bridge_heartbeat.json").strip()
    pressure_weather_entity_primary = os.environ.get(
        "PRESSURE_WEATHER_ENTITY_PRIMARY", ""
    ).strip()
    pressure_weather_entity_secondary = os.environ.get(
        "PRESSURE_WEATHER_ENTITY_SECONDARY", ""
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
        bridge_heartbeat_path=bridge_heartbeat_path,
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
