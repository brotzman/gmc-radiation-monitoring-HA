from __future__ import annotations

import contextlib
import logging
import os
import signal
import sqlite3
import threading
import time
from collections import deque
from dataclasses import replace
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .baseline_cache import RollingBaselineCache
from .config import (
    DeviceConfig,
    Settings,
    TubeCalibrationConfig,
    apply_detected_detector_profile,
)
from .device_health import DeviceHealthMonitor
from .device_profiles import (
    DeviceCapabilities,
    normalize_device_version_display,
    resolve_device_profile,
    split_device_version,
)
from .errors import DeviceIdentityChanged, GmcError, GmcProtocolError, GmcTimeout
from .filtering import HighCpmGate
from .gmcmap import (
    AcpmAccumulator,
    GmcMapConfig,
    GmcMapReading,
    GmcMapUploadCoordinator,
    GmcMapUploader,
    effective_upload_interval,
    resolve_counter_id,
    staggered_startup_delay,
)
from .history import DEFAULT_DB_PATH, HistoryStore
from .home_assistant import HomeAssistantPressureClient, HomeAssistantTemperatureClient
from .metrology import (
    DualTubeMetrologyConfig,
    MetrologyConfig,
    TubeMetrologyProfile,
    derived_dual_tube_dose_estimate,
    live_measurement_metrology,
)
from .monitoring import SmartMonitor
from .mqtt_pub import MqttPublisher
from .orientation import calculate_orientation, calibration_for_serial
from .runtime_diagnostics import RuntimeDiagnosticTracker
from .security_logging import configure_secure_logging
from .serial_autoconfig import effective_serial_startup_delays
from .serial_device import (
    SampleResult,
    SerialGmc,
    ensure_same_serial,
    probe_capabilities,
    read_identity,
    read_sample,
)
from .serial_scheduler import SerialScheduler
from .utils import interruptible_sleep, utc_timestamp
from .version import APP_VERSION

LOG = logging.getLogger("gmc_bridge")
STOP_EVENT = threading.Event()


def handle_signal(signum: int, frame: Any) -> None:
    STOP_EVENT.set()


def configure_logging() -> None:
    level_name = os.environ.get("LOG_LEVEL", "info").upper()
    configure_secure_logging(
        level=getattr(logging, level_name, logging.INFO),
        format_string="%(asctime)s %(levelname)s %(message)s",
    )


def format_published_sample(sample: dict[str, Any]) -> str:
    parts = [f"Published CPM={int(sample['cpm'])}"] if "cpm" in sample else ["Published partial sample"]
    if "tube_low_cpm" in sample and "tube_high_cpm" in sample:
        parts.append(f"tubes=(low:{int(sample['tube_low_cpm'])}, high:{int(sample['tube_high_cpm'])})")
    if "temperature_c" in sample:
        parts.append(f"temperature={float(sample['temperature_c']):.1f}°C")
    if "voltage_v" in sample:
        parts.append(f"voltage={float(sample['voltage_v']):.1f}V")
    if all(key in sample for key in ("gyro_x", "gyro_y", "gyro_z")):
        parts.append(f"gyro=({int(sample['gyro_x'])}, {int(sample['gyro_y'])}, {int(sample['gyro_z'])})")
    return " ".join(parts)


def _tube_metrology_profile(profile: Any) -> TubeMetrologyProfile | None:
    if profile is None:
        return None
    return TubeMetrologyProfile(
        tube_model=profile.tube_model,
        cpm_per_usvh=profile.cpm_per_usvh,
        dead_time_us=profile.dead_time_us,
        reliable_max_cpm=profile.reliable_max_cpm,
        dead_time_model=profile.dead_time_model,
        conversion_factor_uncertainty_percent=profile.conversion_factor_uncertainty_percent,
        calibration_uncertainty_percent=profile.calibration_uncertainty_percent,
        calibration_reference=profile.calibration_reference,
    )


def _enrich_metrology_state(state: dict[str, Any], config: DeviceConfig) -> None:
    if state.get("cpm") is None:
        return
    registry = config.calibration_registry_values()
    status = str(registry.get("calibration_status") or "unknown")
    source = str(registry.get("calibration_source") or "unknown")
    active_tube = "primary"
    selected_profile = config.effective_low_dose_tube()
    derived_dose = None

    if config.dual_tube_mode != "single":
        dual = DualTubeMetrologyConfig(
            mode=config.dual_tube_mode,
            switch_cpm=config.dual_tube_switch_cpm,
            low_dose=_tube_metrology_profile(config.effective_low_dose_tube()),
            high_dose=_tube_metrology_profile(config.high_dose_tube),
        )
        dual_result = derived_dual_tube_dose_estimate(
            primary_cpm=float(state["cpm"]),
            low_cpm=float(state["tube_low_cpm"]) if state.get("tube_low_cpm") is not None else None,
            high_cpm=float(state["tube_high_cpm"]) if state.get("tube_high_cpm") is not None else None,
            counting_relative_percent=None,
            config=dual,
        )
        if dual_result.get("selected_tube") == "high":
            active_tube = "secondary"
            if config.high_dose_tube is not None:
                selected_profile = config.high_dose_tube
        elif dual_result.get("selected_tube") == "low":
            active_tube = "primary"
        derived_dose = dual_result.get("value_usvh") if dual_result.get("available") else None
        state["dual_tube_selection_reason"] = dual_result.get("selection_reason")

    selected_cpm = float(state["cpm"])
    if active_tube == "primary" and state.get("tube_low_cpm") is not None:
        selected_cpm = float(state["tube_low_cpm"])
    elif active_tube == "secondary" and state.get("tube_high_cpm") is not None:
        selected_cpm = float(state["tube_high_cpm"])

    result = live_measurement_metrology(
        cpm=selected_cpm,
        cpm_per_usvh=selected_profile.cpm_per_usvh,
        config=MetrologyConfig(
            dead_time_us=selected_profile.dead_time_us,
            reliable_max_cpm=selected_profile.reliable_max_cpm,
            dead_time_model=selected_profile.dead_time_model,
            conversion_factor_uncertainty_percent=selected_profile.conversion_factor_uncertainty_percent,
            calibration_uncertainty_percent=selected_profile.calibration_uncertainty_percent,
            calibration_reference=selected_profile.calibration_reference,
            tube_model=selected_profile.tube_model,
        ),
        calibration_status=status,
        calibration_source=source,
    )
    if derived_dose is not None:
        result["derived_dose_usvh"] = derived_dose
    state.update(
        {
            "raw_cpm": float(state["cpm"]),
            "corrected_cpm": result.get("corrected_cpm"),
            "detector_type": selected_profile.tube_model,
            "dual_tube_mode": config.dual_tube_mode,
            "active_tube": active_tube,
            "dead_time_model": selected_profile.dead_time_model,
            "dead_time_us": selected_profile.dead_time_us,
            "dead_time_loss_percent": result.get("dead_time_loss_percent"),
            "detector_load_percent": result.get("detector_load_percent"),
            "correction_factor": result.get("correction_factor"),
            "calibration_status": status,
            "calibration_source": source,
            "measurement_quality_index": result.get("measurement_quality_index"),
            "measurement_quality_stars": result.get("measurement_quality_stars"),
            "measurement_quality_star_text": result.get("measurement_quality_star_text"),
            "measurement_validity": result.get("measurement_validity"),
            "dose_quality": result.get("dose_quality"),
            "derived_dose_usvh": result.get("derived_dose_usvh"),
            "plausibility_warnings": result.get("plausibility_warnings", []),
            "dead_time_correction_active": bool(result.get("correction_applied")),
        }
    )


def _diagnostics(
    *,
    app_started_at: str,
    serial_reconnect_count: int,
    serial_error_count: int,
    optional_error_counts: dict[str, int],
    history_write_error_count: int,
    capabilities: DeviceCapabilities,
    device_profile: str,
) -> dict[str, Any]:
    return {
        "last_successful_measurement": utc_timestamp(),
        "serial_reconnect_count": serial_reconnect_count,
        "serial_error_count": serial_error_count,
        "temperature_error_count": optional_error_counts["temperature"],
        "voltage_error_count": optional_error_counts["voltage"],
        "gyro_error_count": optional_error_counts["gyro"],
        "device_time_error_count": optional_error_counts.get("device_time", 0),
        "heartbeat_error_count": optional_error_counts.get("heartbeat", 0),
        "app_started_at": app_started_at,
        "history_write_error_count": history_write_error_count,
        "device_profile": device_profile,
        "capabilities": ",".join(capabilities.enabled_channels()),
    }


def _device_clock_diagnostics(
    device_time_local: str | None,
    settings: Settings | None = None,
    *,
    report_timezone: str | None = None,
    warning_seconds: int | None = None,
) -> dict[str, Any]:
    if settings is not None:
        report_timezone = settings.report_timezone
        warning_seconds = settings.device_clock_warning_seconds
    report_timezone = report_timezone or "UTC"
    warning_seconds = 120 if warning_seconds is None else int(warning_seconds)
    if not device_time_local:
        return {
            "device_time": None,
            "device_clock_offset_seconds": None,
            "device_clock_status": "unavailable",
        }
    try:
        timezone = ZoneInfo(report_timezone)
        device_time = datetime.fromisoformat(device_time_local).replace(tzinfo=timezone)
    except (ValueError, TypeError):
        return {
            "device_time": None,
            "device_clock_offset_seconds": None,
            "device_clock_status": "invalid",
        }
    offset_seconds = round((device_time - datetime.now(timezone)).total_seconds())
    return {
        "device_time": device_time.isoformat(timespec="seconds"),
        "device_clock_offset_seconds": offset_seconds,
        "device_clock_status": ("ok" if abs(offset_seconds) <= warning_seconds else "warning"),
    }


def _publish_heartbeat_until(
    *,
    device: SerialGmc,
    publisher: MqttPublisher,
    base_state: dict[str, Any],
    available: dict[str, bool],
    deadline_monotonic: float,
    rolling_cps: deque[int],
) -> int | None:
    """Publish RFC1801 heartbeat CPS once per second until the next regular sample."""
    last_cps: int | None = None
    device.start_heartbeat()
    try:
        while not STOP_EVENT.is_set() and time.monotonic() < deadline_monotonic:
            cps = device.read_heartbeat_cps()
            last_cps = cps
            rolling_cps.append(cps)
            live_state = dict(base_state)
            live_state.update(
                {
                    "cps": cps,
                    "heartbeat_cpm_60s": sum(rolling_cps),
                    "heartbeat_active": True,
                }
            )
            publisher.publish_sample(live_state, available)
    finally:
        device.stop_heartbeat()
    return last_cps


def _state_for_gate(result: SampleResult, accepted: bool) -> tuple[dict[str, Any], dict[str, bool]]:
    state = dict(result.state)
    available = dict(result.available)
    if not accepted:
        state.pop("cpm", None)
        available["cpm"] = False
    return state, available


def _persist_runtime_state(
    history_store: HistoryStore | None,
    *,
    serial: str,
    port: str,
    online: bool,
    reason: str,
) -> None:
    """Persist the live connection state for one physical counter.

    The report server runs in a separate process, so it must not infer device
    availability from the currently selected analysis or only from the latest
    accepted measurement. A valid serial read keeps the device online even when
    a suspicious CPM value is temporarily held back by the confirmation gate.
    """
    if history_store is None:
        return
    try:
        status_timestamp = utc_timestamp()
        values: dict[str, Any] = {
            "port": port,
            "runtime_online": bool(online),
            "runtime_status": "online" if online else "offline",
            "runtime_status_reason": reason,
            "runtime_status_updated_utc": status_timestamp,
        }
        if online:
            values["last_seen_utc"] = status_timestamp
        history_store.upsert_device_registry(serial, values)
    except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
        LOG.warning("[%s/%s] Could not persist runtime state: %s", port, serial, exc)


def _resolved_serial_target(port: str) -> str:
    """Resolve the current kernel device behind a stable serial symlink."""
    try:
        return os.path.realpath(port)
    except (OSError, ValueError):
        return port


def _hard_recovery_pause(port: str, stop_event: threading.Event, delay: float = 2.0) -> bool:
    """Allow the kernel/USB UART to settle before a completely fresh open."""
    LOG.warning(
        "[%s] Performing hard serial recovery; current target=%s; reopening in %.1fs",
        port,
        _resolved_serial_target(port),
        delay,
    )
    return interruptible_sleep(delay, stop_event)


def _apply_runtime_calibration_assignment(
    config: DeviceConfig, history_store: HistoryStore | None, device_serial: str
) -> DeviceConfig:
    """Apply an app-local custom calibration after the physical device is known."""
    if history_store is None:
        return config
    try:
        assignment = history_store.get_custom_calibration_assignment(device_serial)
    except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
        LOG.warning("[%s] Could not load custom calibration assignment: %s", device_serial, exc)
        return config
    if not assignment or not isinstance(assignment.get("values"), dict):
        return config
    values = assignment["values"]
    try:
        tube = TubeCalibrationConfig(
            tube_model=str(values.get("tube_model") or config.tube_model).strip(),
            cpm_per_usvh=(
                float(values["cpm_per_usvh"])
                if values.get("cpm_per_usvh") not in (None, "")
                else config.cpm_per_usvh
            ),
            dead_time_us=(
                float(values["dead_time_us"])
                if values.get("dead_time_us") not in (None, "")
                else None
            ),
            reliable_max_cpm=(
                int(float(values["reliable_max_cpm"]))
                if values.get("reliable_max_cpm") not in (None, "")
                else None
            ),
            dead_time_model=str(values.get("dead_time_model") or "none").strip().lower(),
            conversion_factor_uncertainty_percent=(
                float(values["conversion_factor_uncertainty_percent"])
                if values.get("conversion_factor_uncertainty_percent") not in (None, "")
                else None
            ),
            calibration_uncertainty_percent=(
                float(values["calibration_uncertainty_percent"])
                if values.get("calibration_uncertainty_percent") not in (None, "")
                else None
            ),
            calibration_reference=str(values.get("calibration_reference") or "").strip(),
        )
        tube.validate("custom calibration assignment")
    except (TypeError, ValueError) as exc:
        LOG.warning("[%s] Ignoring invalid custom calibration assignment: %s", device_serial, exc)
        return config
    updates: dict[str, Any] = {
        "detector_profile": str(assignment.get("profile_id") or "custom_single"),
        "detector_profile_source": "custom_assignment",
        "calibration_overrides": True,
        "tube_model": tube.tube_model,
        "cpm_per_usvh": float(tube.cpm_per_usvh or config.cpm_per_usvh),
        "dead_time_us": tube.dead_time_us,
        "reliable_max_cpm": tube.reliable_max_cpm,
        "dead_time_model": tube.dead_time_model,
        "conversion_factor_uncertainty_percent": tube.conversion_factor_uncertainty_percent,
        "calibration_uncertainty_percent": tube.calibration_uncertainty_percent,
        "calibration_reference": tube.calibration_reference,
    }
    if config.dual_tube_mode != "single":
        updates["low_dose_tube"] = tube
    return replace(config, **updates)


def _run_device(
    settings: Settings,
    device_config: DeviceConfig,
    device_index: int,
    configured_device_count: int,
    history_store: HistoryStore | None,
    app_started_at: str,
    gmcmap_coordinator: GmcMapUploadCoordinator,
    temperature_client: HomeAssistantTemperatureClient | None,
    pressure_client: HomeAssistantPressureClient | None,
    serial_scheduler: SerialScheduler,
    serial_startup_delay: float,
) -> None:
    port = device_config.port
    device = SerialGmc(
        port,
        device_config.baudrate,
        device_config.command_timeout,
        device_config.inter_command_delay_ms,
        stop_event=STOP_EVENT,
        debug_frames=device_config.serial_debug,
        debug_max_bytes=device_config.serial_debug_max_bytes,
    )
    gate = HighCpmGate(device_config.high_cpm_threshold, device_config.high_cpm_confirmations)
    pending_raw_samples: list[tuple[int, dict[str, Any]]] = []
    publisher: MqttPublisher | None = None
    gmcmap_uploader: GmcMapUploader | None = None
    gmcmap_static_status: dict[str, Any] = {
        "gmcmap_enabled": settings.gmcmap_enabled,
        "gmcmap_configured": False,
        "gmcmap_upload_status": "disabled" if not settings.gmcmap_enabled else "not_configured",
    }
    capabilities = DeviceCapabilities(cpm=True)
    profile = resolve_device_profile("")
    reconnect_delay = 1.0
    if serial_startup_delay > 0:
        LOG.info(
            "[%s] Delaying serial initialization by %.1fs to stagger %d configured devices",
            port,
            serial_startup_delay,
            configured_device_count,
        )
        if not interruptible_sleep(serial_startup_delay, STOP_EVENT):
            return

    while not STOP_EVENT.is_set() and publisher is None:
        try:
            with serial_scheduler.window(device_index, "INIT", STOP_EVENT):
                device.open()
                version, serial = read_identity(device)
                if (
                    device_config.expected_serial
                    and device_config.expected_serial.casefold() != serial.casefold()
                ):
                    LOG.error(
                        "[%s] Serial identity mismatch: dual-tube settings expect %s, connected counter is %s; device disabled",
                        port,
                        device_config.expected_serial,
                        serial,
                    )
                    device.close()
                    return
                device_config = apply_detected_detector_profile(device_config, version)
                device_config = _apply_runtime_calibration_assignment(device_config, history_store, serial)
                profile = resolve_device_profile(version)
                hardware_model, firmware_version = split_device_version(version)
                display_version = normalize_device_version_display(version)
                LOG.info(
                    "[%s] Detected %s with serial %s (profile=%s)", port, version, serial, profile.profile_id
                )
                if history_store is not None and gate.baseline_median is None:
                    try:
                        recent_rows = history_store.query_range(
                            int(time.time()) - 86400,
                            int(time.time()) + 1,
                            device_serial=serial,
                        )
                        seed_values = [int(row.cpm) for row in recent_rows if row.cpm_quality == "normal"][
                            -24:
                        ]
                        gate.seed(seed_values)
                        if gate.baseline_median is not None:
                            LOG.info(
                                "[%s/%s] Seeded adaptive CPM plausibility baseline: median=%.1f CPM, trigger=%d CPM",
                                port,
                                serial,
                                gate.baseline_median,
                                gate.adaptive_threshold,
                            )
                    except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
                        LOG.warning("[%s/%s] Could not seed CPM plausibility baseline: %s", port, serial, exc)
                capabilities = probe_capabilities(
                    device,
                    expected_serial=serial,
                    probe_gyro=device_config.read_gyro,
                    probe_dual_tube=profile.dual_tube_hint == "yes",
                    probe_device_time=device_config.read_device_time and profile.device_time_hint == "yes",
                    probe_heartbeat=device_config.heartbeat_enabled and profile.heartbeat_hint == "yes",
                )
            publisher = MqttPublisher(
                settings,
                serial,
                display_version,
                capabilities=capabilities,
                device_name=device_config.name,
                read_gyro=device_config.read_gyro,
            )
            counter_id = device_config.gmcmap_counter_id or resolve_counter_id(
                serial,
                settings.gmcmap_device_ids,
                configured_device_count=configured_device_count,
            )
            if settings.gmcmap_enabled and counter_id is not None:

                def update_gmcmap_status(values: dict[str, object], *, device_serial: str = serial) -> None:
                    if history_store is not None:
                        try:
                            history_store.upsert_device_registry(device_serial, values)
                        except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
                            LOG.warning("[%s] Could not persist GMCMap status: %s", port, exc)

                startup_delay = staggered_startup_delay(
                    device_index,
                    configured_device_count,
                    device_config.gmcmap_upload_interval,
                )
                gmcmap_uploader = GmcMapUploader(
                    GmcMapConfig(
                        account_id=settings.gmcmap_account_id,
                        counter_id=counter_id,
                        upload_interval_seconds=device_config.gmcmap_upload_interval,
                        timeout_seconds=device_config.gmcmap_timeout,
                        startup_delay_seconds=startup_delay,
                    ),
                    status_callback=update_gmcmap_status,
                    coordinator=gmcmap_coordinator,
                )
                gmcmap_static_status = gmcmap_uploader.snapshot()
                LOG.info(
                    "[%s/%s] GMCMap upload enabled for mapped counter %s; "
                    "first slot in %.1fs, cadence %.1fs, shared connection gap %.1fs",
                    port,
                    serial,
                    gmcmap_static_status.get("gmcmap_counter_id_masked"),
                    startup_delay,
                    effective_upload_interval(device_config.gmcmap_upload_interval),
                    gmcmap_coordinator.minimum_gap_seconds,
                )
            elif settings.gmcmap_enabled:
                gmcmap_static_status = {
                    "gmcmap_enabled": True,
                    "gmcmap_configured": False,
                    "gmcmap_upload_status": "not_configured",
                    "gmcmap_last_error": "No counter ID mapping for this device serial",
                }
                LOG.warning(
                    "[%s/%s] GMCMap enabled, but no counter ID mapping exists for this serial",
                    port,
                    serial,
                )
            if history_store is not None:
                history_store.upsert_device_registry(
                    serial,
                    {
                        "port": port,
                        "configured_name": device_config.name,
                        "baudrate": device_config.baudrate,
                        "scan_interval_seconds": device_config.scan_interval,
                        "cpm_per_usvh": device_config.cpm_per_usvh,
                        "dead_time_us": device_config.dead_time_us,
                        "reliable_max_cpm": device_config.reliable_max_cpm,
                        "dead_time_model": device_config.dead_time_model,
                        "conversion_factor_uncertainty_percent": device_config.conversion_factor_uncertainty_percent,
                        "calibration_uncertainty_percent": device_config.calibration_uncertainty_percent,
                        "calibration_reference": device_config.calibration_reference,
                        "tube_model": device_config.tube_model,
                        **device_config.calibration_registry_values(),
                        "command_timeout_seconds": device_config.command_timeout,
                        "serial_startup_delay_seconds": serial_startup_delay,
                        "auxiliary_read_interval_seconds": device_config.auxiliary_read_interval,
                        "read_gyro_configured": device_config.read_gyro,
                        "read_device_time_configured": device_config.read_device_time,
                        "heartbeat_configured": device_config.heartbeat_enabled,
                        "device_model": display_version,
                        "hardware_model": hardware_model,
                        "firmware_version": firmware_version,
                        "device_profile": profile.profile_id,
                        "device_profile_name": profile.display_name,
                        "capabilities": ",".join(capabilities.enabled_channels()),
                        "last_seen_utc": utc_timestamp(),
                        "runtime_online": True,
                        "runtime_status": "online",
                        "runtime_status_reason": "connected",
                        "runtime_status_updated_utc": utc_timestamp(),
                        "heartbeat_enabled": device_config.heartbeat_enabled and capabilities.heartbeat,
                        **gmcmap_static_status,
                    },
                )
                history_store.set_device_capabilities(serial, capabilities.as_dict(), source="runtime_probe")
                history_store.set_metadata(
                    {
                        "app_version": APP_VERSION,
                        "time_basis": "UTC",
                        "database_schema_version": history_store.schema_version(),
                        "scan_interval_seconds": device_config.scan_interval,
                        "report_timezone": settings.report_timezone,
                        "configured_ports": ",".join(item.port for item in settings.effective_devices()),
                    }
                )
            if not publisher.start(wait_timeout=15.0):
                LOG.warning("[%s] MQTT did not connect within 15 seconds", port)
            if gmcmap_uploader is not None:
                gmcmap_uploader.start()
            reconnect_delay = 1.0
        except (GmcError, OSError, ValueError, sqlite3.Error) as exc:
            device.close()
            if gmcmap_uploader is not None:
                gmcmap_uploader.stop()
                gmcmap_uploader = None
            if publisher is not None:
                with contextlib.suppress(OSError, RuntimeError, ValueError):
                    publisher.stop()
                publisher = None
            LOG.error("[%s] Device initialization failed: %s; retrying in %.0fs", port, exc, reconnect_delay)
            if not interruptible_sleep(reconnect_delay, STOP_EVENT):
                return
            reconnect_delay = min(reconnect_delay * 2.0, 60.0)

    if publisher is None:
        return

    serial_error_count = 0
    serial_reconnect_count = 0
    optional_error_counts = {
        "temperature": 0,
        "voltage": 0,
        "gyro": 0,
        "dual_tube": 0,
        "device_time": 0,
        "heartbeat": 0,
    }
    reconnect_pending = False
    consecutive_serial_failures = 0
    identity_mismatch_count = 0
    last_valid_measurement_monotonic = time.monotonic()
    watchdog_timeout_seconds = max(300.0, float(device_config.scan_interval) * 4.0)
    history_write_error_count = 0
    discarded_peak_sample_count = 0
    monitor = SmartMonitor(
        settings.rapid_rise_percent, settings.rapid_rise_window_minutes, settings.sustained_alert_minutes
    )
    device_health = DeviceHealthMonitor()
    latest_device_health = {"device_health_status": "ok", "device_health_reason": "initializing"}
    heartbeat_window: deque[int] = deque(maxlen=60)
    gmcmap_acpm = AcpmAccumulator(
        window_seconds=3600, expected_interval_seconds=device_config.scan_interval
    )
    baseline_cache = RollingBaselineCache(
        window_seconds=settings.baseline_learning_days * 86400
    )
    runtime_diagnostics = RuntimeDiagnosticTracker()
    if history_store is not None:
        try:
            baseline_seed_now = int(time.time())
            baseline_cache.seed(
                history_store.query_range(
                    baseline_seed_now - settings.baseline_learning_days * 86400,
                    baseline_seed_now + 1,
                    device_serial=publisher.serial,
                ),
                now_utc=baseline_seed_now,
            )
        except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
            issue, should_log = runtime_diagnostics.record("baseline_seed", exc)
            if should_log:
                LOG.warning("[%s] Could not seed rolling baseline cache: %s", port, exc)
            if history_store is not None:
                history_store.set_metadata({
                    f"runtime_diagnostic_{publisher.serial}_baseline_seed": issue
                })
    cached_optional_state: dict[str, Any] = {}
    last_orientation_position: str | None = None
    cached_optional_available = {
        "temperature": False,
        "voltage": False,
        "gyro": False,
        "dual_tube": False,
        "device_time": False,
    }
    next_auxiliary_read_monotonic = 0.0
    gyro_consecutive_failures = 0
    gyro_paused_until_monotonic = 0.0
    gyro_pause_seconds = 15.0 * 60.0
    gyro_failure_limit = 2
    cached_clock_diagnostics = _device_clock_diagnostics(
        None,
        report_timezone=settings.report_timezone,
        warning_seconds=device_config.device_clock_warning_seconds,
    )

    try:
        while not STOP_EVENT.is_set():
            cycle_started = time.monotonic()
            reconnect_after_cycle = False
            try:
                silent_for = cycle_started - last_valid_measurement_monotonic
                if silent_for >= watchdog_timeout_seconds:
                    publisher.set_device_online(False)
                    _persist_runtime_state(
                        history_store,
                        serial=publisher.serial,
                        port=port,
                        online=False,
                        reason="serial_watchdog_timeout",
                    )
                    device.close()
                    LOG.warning(
                        "[%s] Serial watchdog: no valid measurement for %.0fs (limit %.0fs)",
                        port,
                        silent_for,
                        watchdog_timeout_seconds,
                    )
                    if not _hard_recovery_pause(port, STOP_EVENT):
                        break
                    reconnect_pending = True
                    consecutive_serial_failures = 0
                    last_valid_measurement_monotonic = time.monotonic()

                if device.fd is None:
                    with serial_scheduler.window(device_index, "RECONNECT", STOP_EVENT):
                        LOG.info(
                            "[%s] Opening serial device (resolved target %s)",
                            port,
                            _resolved_serial_target(port),
                        )
                        device.open()
                        device.recover_protocol_stream()
                        version, serial = read_identity(device, expected_serial=publisher.serial)
                        ensure_same_serial(publisher.serial, serial)
                    if reconnect_pending:
                        serial_reconnect_count += 1
                        reconnect_pending = False
                        LOG.info("[%s] Serial connection restored", port)

                read_auxiliary = (
                    device_config.auxiliary_read_interval == 0
                    or cycle_started >= next_auxiliary_read_monotonic
                )
                gyro_runtime_enabled = (
                    device_config.read_gyro and cycle_started >= gyro_paused_until_monotonic
                )
                if (
                    device_config.read_gyro
                    and gyro_paused_until_monotonic > 0
                    and cycle_started >= gyro_paused_until_monotonic
                ):
                    LOG.info("[%s] Gyro pause expired; probing GETGYRO again", port)
                    gyro_paused_until_monotonic = 0.0
                try:
                    with serial_scheduler.window(device_index, "READ", STOP_EVENT):
                        result = read_sample(
                            device,
                            gyro_runtime_enabled,
                            capabilities,
                            read_device_time=device_config.read_device_time,
                            read_optional_channels=read_auxiliary,
                        )
                except (GmcProtocolError, GmcTimeout) as first_error:
                    LOG.warning(
                        "[%s] Serial state READ failed (%s); transitioning to SYNC and retrying once",
                        port,
                        first_error,
                    )
                    with serial_scheduler.window(device_index, "SYNC", STOP_EVENT):
                        device.recover_protocol_stream()
                        result = read_sample(
                            device,
                            gyro_runtime_enabled,
                            capabilities,
                            read_device_time=device_config.read_device_time,
                            read_optional_channels=read_auxiliary,
                        )
                consecutive_serial_failures = 0
                identity_mismatch_count = 0
                last_valid_measurement_monotonic = time.monotonic()
                if read_auxiliary:
                    next_auxiliary_read_monotonic = cycle_started + device_config.auxiliary_read_interval
                    optional_keys = {
                        "temperature": ("temperature_c",),
                        "voltage": ("voltage_v",),
                        "gyro": ("gyro_x", "gyro_y", "gyro_z"),
                        "dual_tube": ("tube_low_cpm", "tube_high_cpm"),
                        "device_time": (),
                    }
                    for channel, keys in optional_keys.items():
                        if result.available.get(channel, False):
                            for key in keys:
                                if key in result.state:
                                    cached_optional_state[key] = result.state[key]
                            cached_optional_available[channel] = True
                gyro_failed_this_cycle = any(error.sensor == "gyro" for error in result.optional_errors)
                if gyro_runtime_enabled and read_auxiliary:
                    if result.available.get("gyro", False):
                        if gyro_consecutive_failures:
                            LOG.info("[%s] Gyro communication recovered", port)
                        gyro_consecutive_failures = 0
                    elif gyro_failed_this_cycle:
                        gyro_consecutive_failures += 1
                        cached_optional_available["gyro"] = False
                        for key in ("gyro_x", "gyro_y", "gyro_z"):
                            cached_optional_state.pop(key, None)
                        if gyro_consecutive_failures >= gyro_failure_limit:
                            gyro_paused_until_monotonic = time.monotonic() + gyro_pause_seconds
                            LOG.warning(
                                "[%s] Gyro failed %d consecutive times; pausing GETGYRO for %.0f minutes while CPM and other channels continue",
                                port,
                                gyro_consecutive_failures,
                                gyro_pause_seconds / 60.0,
                            )
                            gyro_consecutive_failures = 0
                for optional_error in result.optional_errors:
                    optional_error_counts[optional_error.sensor] += 1
                    LOG.warning(
                        "[%s] optional channel issue code=%s sensor=%s affects_measurement=%s retryable=%s: %s",
                        port,
                        optional_error.code,
                        optional_error.sensor,
                        optional_error.affects_measurement,
                        optional_error.retryable,
                        optional_error.error,
                    )
                if result.reconnect_required:
                    serial_error_count += 1

                if result.state.get("device_time_local"):
                    cached_clock_diagnostics = _device_clock_diagnostics(
                        result.state.get("device_time_local"),
                        report_timezone=settings.report_timezone,
                        warning_seconds=device_config.device_clock_warning_seconds,
                    )
                clock_diagnostics = dict(cached_clock_diagnostics)
                cpm = int(result.state["cpm"])
                assessment = gate.assess(cpm)
                accepted = gate.accept(cpm, assessment=assessment)
                measurement_timestamp = int(time.time())
                current_raw_sample = (measurement_timestamp, dict(result.state))
                raw_samples_to_store: list[tuple[int, dict[str, Any]]] = []
                confirmed_history_backfill: list[tuple[int, dict[str, Any]]] = []

                if not accepted:
                    # A changed spike magnitude restarts the confirmation sequence.
                    # Drop the older in-memory candidates immediately; they never
                    # reach either raw or accepted history.
                    if gate.pending == 1 and pending_raw_samples:
                        LOG.warning(
                            "[%s/%s] Discarded %d unconfirmed CPM candidate(s) after confirmation sequence changed",
                            port,
                            publisher.serial,
                            len(pending_raw_samples),
                        )
                        discarded_peak_sample_count += len(pending_raw_samples)
                        pending_raw_samples.clear()
                    pending_raw_samples.append(current_raw_sample)
                elif assessment.suspicious and gate.just_confirmed:
                    pending_raw_samples.append(current_raw_sample)
                    raw_samples_to_store = list(pending_raw_samples)
                    confirmed_history_backfill = raw_samples_to_store[:-1]
                    pending_raw_samples.clear()
                else:
                    if pending_raw_samples:
                        LOG.warning(
                            "[%s/%s] Discarded %d unconfirmed CPM peak sample(s); normal reading resumed before 3 confirmations",
                            port,
                            publisher.serial,
                            len(pending_raw_samples),
                        )
                        discarded_peak_sample_count += len(pending_raw_samples)
                        pending_raw_samples.clear()
                    raw_samples_to_store = [current_raw_sample]

                if history_store is not None:
                    gate_state = (
                        f"accepted_confirmed_{assessment.trigger}"
                        if assessment.suspicious
                        else "accepted_normal"
                    )
                    for raw_timestamp, raw_sample in raw_samples_to_store:
                        try:
                            history_store.insert_raw_measurement(
                                raw_sample,
                                device_serial=publisher.serial,
                                timestamp_utc=raw_timestamp,
                                gate_state=gate_state,
                                accepted=True,
                            )
                        except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
                            history_write_error_count += 1
                            LOG.error("[%s] Could not store raw measurement: %s", port, exc)
                    for backfill_timestamp, backfill_sample in confirmed_history_backfill:
                        try:
                            history_store.insert_measurement(
                                backfill_sample,
                                device_serial=publisher.serial,
                                timestamp_utc=backfill_timestamp,
                                cpm_quality="confirmed_high",
                                expected_interval_seconds=device_config.scan_interval,
                            )
                        except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
                            history_write_error_count += 1
                            LOG.error("[%s] Could not backfill confirmed high measurement: %s", port, exc)
                if not accepted:
                    _persist_runtime_state(
                        history_store,
                        serial=publisher.serial,
                        port=port,
                        online=True,
                        reason="measurement_received_pending_confirmation",
                    )
                state, available = _state_for_gate(result, accepted)
                external_temperature = None
                pressure_reading = None
                if accepted:
                    for key, value in cached_optional_state.items():
                        state.setdefault(key, value)
                    for channel, is_available in cached_optional_available.items():
                        if is_available:
                            available[channel] = True
                    if not capabilities.temperature and temperature_client is not None:
                        external_temperature = temperature_client.get_temperature()
                        if external_temperature.available and external_temperature.temperature_c is not None:
                            state["temperature_c"] = external_temperature.temperature_c
                            state["temperature_source"] = "home_assistant"
                            state["temperature_source_entity"] = external_temperature.entity_id
                    if pressure_client is not None:
                        pressure_reading = pressure_client.get_pressure()
                        if pressure_reading.available and pressure_reading.pressure_hpa is not None:
                            state["pressure_hpa"] = pressure_reading.pressure_hpa
                if accepted:
                    _enrich_metrology_state(state, device_config)
                state.pop("device_time_local", None)
                if device_config.heartbeat_enabled and capabilities.heartbeat and heartbeat_window:
                    state["cps"] = heartbeat_window[-1]
                    state["heartbeat_cpm_60s"] = sum(heartbeat_window)
                    state["heartbeat_active"] = False
                if accepted and history_store is not None:
                    try:
                        history_store.insert_measurement(
                            state,
                            device_serial=publisher.serial,
                            timestamp_utc=measurement_timestamp,
                            cpm_quality="confirmed_high" if assessment.suspicious else "normal",
                            expected_interval_seconds=device_config.scan_interval,
                        )
                        history_store.upsert_device_registry(
                            publisher.serial,
                            {
                                "port": port,
                                "configured_name": device_config.name,
                                "baudrate": device_config.baudrate,
                                "scan_interval_seconds": device_config.scan_interval,
                                "cpm_per_usvh": device_config.cpm_per_usvh,
                        "dead_time_us": device_config.dead_time_us,
                        "reliable_max_cpm": device_config.reliable_max_cpm,
                        "dead_time_model": device_config.dead_time_model,
                        "conversion_factor_uncertainty_percent": device_config.conversion_factor_uncertainty_percent,
                        "calibration_uncertainty_percent": device_config.calibration_uncertainty_percent,
                        "calibration_reference": device_config.calibration_reference,
                        "tube_model": device_config.tube_model,
                        **device_config.calibration_registry_values(),
                                "command_timeout_seconds": device_config.command_timeout,
                                "serial_startup_delay_seconds": serial_startup_delay,
                                "auxiliary_read_interval_seconds": device_config.auxiliary_read_interval,
                                "read_gyro_configured": device_config.read_gyro,
                                "read_device_time_configured": device_config.read_device_time,
                                "heartbeat_configured": device_config.heartbeat_enabled,
                                "device_model": publisher.version,
                                "hardware_model": hardware_model,
                                "firmware_version": firmware_version,
                                "device_profile": profile.profile_id,
                                "device_profile_name": profile.display_name,
                                "capabilities": ",".join(capabilities.enabled_channels()),
                                "last_seen_utc": utc_timestamp(),
                                "runtime_online": True,
                                "runtime_status": "online",
                                "runtime_status_reason": "measurement_accepted",
                                "runtime_status_updated_utc": utc_timestamp(),
                                "device_time": clock_diagnostics.get("device_time"),
                                "device_clock_offset_seconds": clock_diagnostics.get(
                                    "device_clock_offset_seconds"
                                ),
                                "device_clock_status": clock_diagnostics.get("device_clock_status"),
                                "heartbeat_enabled": device_config.heartbeat_enabled
                                and capabilities.heartbeat,
                                "temperature_correlation_source": (
                                    "gmc"
                                    if capabilities.temperature
                                    else (
                                        "home_assistant"
                                        if external_temperature and external_temperature.available
                                        else "unavailable"
                                    )
                                ),
                                "temperature_fallback_entity": (
                                    external_temperature.entity_id
                                    if external_temperature and external_temperature.available
                                    else settings.external_temperature_entity
                                ),
                                "temperature_fallback_error": (
                                    external_temperature.error
                                    if external_temperature and not external_temperature.available
                                    else ""
                                ),
                                "pressure_hpa": (
                                    pressure_reading.pressure_hpa
                                    if pressure_reading and pressure_reading.available
                                    else None
                                ),
                                "pressure_source_mode": (
                                    pressure_reading.source_mode if pressure_reading else "disabled"
                                ),
                                "pressure_source_count": (
                                    pressure_reading.source_count if pressure_reading else 0
                                ),
                                "pressure_source_provider": settings.pressure_weather_source_name,
                                "pressure_source_entities": ",".join(
                                    source.entity_id for source in pressure_reading.sources
                                )
                                if pressure_reading
                                else "",
                                "pressure_source_error": (
                                    pressure_reading.error
                                    if pressure_reading and not pressure_reading.available
                                    else ""
                                ),
                                **(
                                    gmcmap_uploader.snapshot()
                                    if gmcmap_uploader is not None
                                    else gmcmap_static_status
                                ),
                            },
                        )
                    except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
                        history_write_error_count += 1
                        LOG.error("[%s] Could not store measurement: %s", port, exc)

                if accepted and gmcmap_uploader is not None:
                    average_cpm = gmcmap_acpm.add(cpm, timestamp_utc=measurement_timestamp)
                    gmcmap_uploader.offer(
                        GmcMapReading(
                            cpm=cpm,
                            average_cpm=average_cpm,
                            dose_rate_usvh=cpm / device_config.cpm_per_usvh,
                            captured_at_utc=int(time.time()),
                            average_sample_count=gmcmap_acpm.sample_count,
                        )
                    )

                if accepted:
                    health = device_health.update(state)
                    latest_device_health = {
                        "device_health_status": health.status,
                        "device_health_reason": health.reason,
                    }
                    if health.event is not None and history_store is not None:
                        try:
                            history_store.insert_operational_event(
                                {**health.event, "timestamp_utc": measurement_timestamp},
                                device_serial=publisher.serial,
                            )
                        except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
                            LOG.warning("[%s] Could not store device-health event: %s", port, exc)

                if accepted and settings.smart_alerts_enabled:
                    baseline_snapshot = baseline_cache.snapshot(now_utc=measurement_timestamp)
                    baseline = baseline_snapshot.value_cpm
                    derived, events = monitor.update(cpm, baseline_cpm=baseline)
                    baseline_cache.add(measurement_timestamp, cpm)
                    recovered = runtime_diagnostics.recover("baseline_seed")
                    if recovered is not None:
                        LOG.info("[%s] Rolling baseline cache is available again", port)
                    if settings.publish_advanced_sensors:
                        state.update({k: v for k, v in derived.items() if v is not None})
                    if history_store is not None:
                        for event in events:
                            try:
                                history_store.insert_operational_event(event, device_serial=publisher.serial)
                            except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
                                LOG.error("[%s] Could not store operational event: %s", port, exc)

                if not accepted:
                    publisher.mark_all_measurements_unavailable()
                diagnostics = _diagnostics(
                    app_started_at=app_started_at,
                    serial_reconnect_count=serial_reconnect_count,
                    serial_error_count=serial_error_count,
                    optional_error_counts=optional_error_counts,
                    history_write_error_count=history_write_error_count,
                    capabilities=capabilities,
                    device_profile=profile.profile_id,
                )
                diagnostics.update(clock_diagnostics)
                diagnostics.update(latest_device_health)
                diagnostics["recoverable_runtime_issues"] = runtime_diagnostics.snapshot()
                diagnostics["gmcmap_acpm_window_minutes"] = gmcmap_acpm.window_minutes
                diagnostics.update(
                    gmcmap_uploader.snapshot() if gmcmap_uploader is not None else gmcmap_static_status
                )
                diagnostics.update(
                    {
                        "serial_port": port,
                        "configured_name": device_config.name or publisher.version,
                        "configured_baudrate": device_config.baudrate,
                        "configured_scan_interval_seconds": device_config.scan_interval,
                        "configured_serial_startup_delay_seconds": serial_startup_delay,
                        "configured_auxiliary_read_interval_seconds": device_config.auxiliary_read_interval,
                        "configured_cpm_per_usvh": device_config.cpm_per_usvh,
                        "serial_watchdog_timeout_seconds": watchdog_timeout_seconds,
                        "serial_consecutive_failures": consecutive_serial_failures,
                        "serial_resolved_target": _resolved_serial_target(port),
                        "gyro_runtime_status": (
                            "disabled"
                            if not device_config.read_gyro
                            else ("paused" if time.monotonic() < gyro_paused_until_monotonic else "active")
                        ),
                        "gyro_pause_remaining_seconds": max(
                            0, round(gyro_paused_until_monotonic - time.monotonic())
                        ),
                        "gyro_consecutive_failures": gyro_consecutive_failures,
                        "cpm_gate_state": gate.state,
                        "cpm_gate_pending_confirmations": gate.pending,
                        "cpm_gate_required_confirmations": device_config.high_cpm_confirmations,
                        "cpm_gate_last_reason": gate.last_accept_reason,
                        "cpm_gate_last_trigger": assessment.trigger,
                        "cpm_adaptive_baseline_median": gate.baseline_median,
                        "cpm_adaptive_trigger": gate.adaptive_threshold,
                        "cpm_fixed_trigger": device_config.high_cpm_threshold,
                        "cpm_discarded_peak_samples": discarded_peak_sample_count,
                        "hardware_model": hardware_model,
                        "firmware_version": firmware_version,
                        "heartbeat_enabled": device_config.heartbeat_enabled and capabilities.heartbeat,
                        "temperature_correlation_source": (
                            "gmc"
                            if capabilities.temperature
                            else (
                                "home_assistant"
                                if external_temperature and external_temperature.available
                                else "unavailable"
                            )
                        ),
                        "temperature_fallback_entity": (
                            external_temperature.entity_id
                            if external_temperature and external_temperature.available
                            else settings.external_temperature_entity
                        ),
                        "temperature_fallback_error": (
                            external_temperature.error
                            if external_temperature and not external_temperature.available
                            else ""
                        ),
                        "pressure_hpa": (
                            pressure_reading.pressure_hpa
                            if pressure_reading and pressure_reading.available
                            else None
                        ),
                        "pressure_source_mode": pressure_reading.source_mode
                        if pressure_reading
                        else "disabled",
                        "pressure_source_count": pressure_reading.source_count if pressure_reading else 0,
                        "pressure_source_provider": settings.pressure_weather_source_name,
                        "pressure_source_error": (
                            pressure_reading.error
                            if pressure_reading and not pressure_reading.available
                            else ""
                        ),
                    }
                )
                if history_store is not None:
                    try:
                        history_store.upsert_device_registry(
                            publisher.serial,
                            {
                                "serial_error_count": serial_error_count,
                                "serial_reconnect_count": serial_reconnect_count,
                                "history_write_error_count": history_write_error_count,
                                "temperature_error_count": optional_error_counts["temperature"],
                                "voltage_error_count": optional_error_counts["voltage"],
                                "gyro_error_count": optional_error_counts["gyro"],
                                "cpm_gate_state": gate.state,
                                "cpm_gate_pending_confirmations": gate.pending,
                                "cpm_gate_required_confirmations": device_config.high_cpm_confirmations,
                                "cpm_discarded_peak_samples": discarded_peak_sample_count,
                                **latest_device_health,
                            },
                        )
                    except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
                        LOG.warning(
                            "[%s/%s] Could not persist diagnostics summary: %s", port, publisher.serial, exc
                        )
                if all(key in state for key in ("gyro_x", "gyro_y", "gyro_z")):
                    raw_x = int(state["gyro_x"])
                    raw_y = int(state["gyro_y"])
                    raw_z = int(state["gyro_z"])
                    diagnostics.update({"gyro_x": raw_x, "gyro_y": raw_y, "gyro_z": raw_z})
                    orientation = calculate_orientation(publisher.serial, raw_x, raw_y, raw_z)
                    calibration = calibration_for_serial(publisher.serial)
                    if orientation is not None:
                        if (
                            last_orientation_position is not None
                            and orientation.position_key != last_orientation_position
                            and history_store is not None
                        ):
                            with contextlib.suppress(OSError, sqlite3.Error, RuntimeError, ValueError):
                                history_store.insert_operational_event(
                                    {
                                        "timestamp_utc": int(time.time()),
                                        "event_type": "orientation_changed",
                                        "severity": "info",
                                        "details": {
                                            "from": last_orientation_position,
                                            "to": orientation.position_key,
                                            "roll": round(orientation.roll_degrees, 2),
                                            "pitch": round(orientation.pitch_degrees, 2),
                                        },
                                    },
                                    device_serial=publisher.serial,
                                )
                        last_orientation_position = orientation.position_key
                        diagnostics.update(
                            {
                                "gyro_calibrated_x": round(orientation.gx, 6),
                                "gyro_calibrated_y": round(orientation.gy, 6),
                                "gyro_calibrated_z": round(orientation.gz, 6),
                                "gyro_acceleration_magnitude": round(orientation.gravity_magnitude, 6),
                                "gyro_roll_degrees": round(orientation.roll_degrees, 3),
                                "gyro_pitch_degrees": round(orientation.pitch_degrees, 3),
                                "gyro_inclination_degrees": round(orientation.inclination_degrees, 3),
                                "gyro_position": orientation.position_key,
                                "gyro_calibration_profile": calibration.profile_name if calibration else "",
                            }
                        )
                publisher.publish_diagnostics(diagnostics)
                publisher.set_device_online(True)
                published = publisher.publish_sample(state, available)
                if accepted and published:
                    LOG.info("[%s/%s] %s", port, publisher.serial, format_published_sample(state))
                elif not accepted:
                    LOG.warning(
                        "[%s/%s] Suppressed suspicious CPM=%d (%s; baseline=%s, trigger=%s; %d/%d confirmations)",
                        port,
                        publisher.serial,
                        cpm,
                        assessment.trigger,
                        "n/a" if assessment.baseline_median is None else f"{assessment.baseline_median:.1f}",
                        "n/a"
                        if assessment.adaptive_threshold is None
                        else str(assessment.adaptive_threshold),
                        gate.pending,
                        device_config.high_cpm_confirmations,
                    )
                publisher.sync_mqtt_state()
                reconnect_delay = 1.0
                reconnect_after_cycle = result.reconnect_required
                if (
                    accepted
                    and not reconnect_after_cycle
                    and device_config.heartbeat_enabled
                    and capabilities.heartbeat
                ):
                    try:
                        last_heartbeat_cps = _publish_heartbeat_until(
                            device=device,
                            publisher=publisher,
                            base_state=state,
                            available=available,
                            deadline_monotonic=cycle_started + device_config.scan_interval,
                            rolling_cps=heartbeat_window,
                        )
                    except (GmcError, OSError):
                        optional_error_counts["heartbeat"] += 1
                        raise
                    if last_heartbeat_cps is not None and history_store is not None:
                        history_store.upsert_device_registry(
                            publisher.serial,
                            {
                                "heartbeat_cps": last_heartbeat_cps,
                                "heartbeat_cpm_60s": sum(heartbeat_window),
                                "heartbeat_last_seen_utc": utc_timestamp(),
                            },
                        )
            except DeviceIdentityChanged as exc:
                identity_mismatch_count += 1
                publisher.set_device_online(False)
                _persist_runtime_state(
                    history_store,
                    serial=publisher.serial,
                    port=port,
                    online=False,
                    reason="identity_check_failed",
                )
                device.close()
                if identity_mismatch_count < 3:
                    LOG.warning(
                        "[%s] Identity check failed (%d/3): %s; forcing a fresh reopen",
                        port,
                        identity_mismatch_count,
                        exc,
                    )
                    if not _hard_recovery_pause(port, STOP_EVENT):
                        break
                    reconnect_pending = True
                    continue
                LOG.critical(
                    "[%s] Physical GMC identity changed after 3 independent reads: %s",
                    port,
                    exc,
                )
                return
            except (GmcError, OSError) as exc:
                discarded_peak_sample_count += len(pending_raw_samples)
                gate.reset()
                pending_raw_samples.clear()
                serial_error_count += 1
                reconnect_pending = True
                consecutive_serial_failures += 1
                publisher.set_device_online(False)
                _persist_runtime_state(
                    history_store,
                    serial=publisher.serial,
                    port=port,
                    online=False,
                    reason="serial_error",
                )
                device.close()
                if consecutive_serial_failures >= 3:
                    LOG.warning(
                        "[%s] %d consecutive serial failures (%s); escalating to hard recovery",
                        port,
                        consecutive_serial_failures,
                        exc,
                    )
                    if not _hard_recovery_pause(port, STOP_EVENT):
                        break
                    consecutive_serial_failures = 0
                    reconnect_delay = 1.0
                else:
                    LOG.warning(
                        "[%s] Measurement failed: %s; reopening in %.0fs",
                        port,
                        exc,
                        reconnect_delay,
                    )
                    if not interruptible_sleep(reconnect_delay, STOP_EVENT):
                        break
                    reconnect_delay = min(reconnect_delay * 2.0, 60.0)
            else:
                if reconnect_after_cycle:
                    reconnect_pending = True
                    publisher.set_device_online(False)
                    _persist_runtime_state(
                        history_store,
                        serial=publisher.serial,
                        port=port,
                        online=False,
                        reason="reconnect_required",
                    )
                    device.close()
                    if not interruptible_sleep(reconnect_delay, STOP_EVENT):
                        break
                    reconnect_delay = min(reconnect_delay * 2.0, 60.0)
            elapsed = time.monotonic() - cycle_started
            if not interruptible_sleep(max(0.0, device_config.scan_interval - elapsed), STOP_EVENT):
                break
    finally:
        _persist_runtime_state(
            history_store,
            serial=publisher.serial,
            port=port,
            online=False,
            reason="service_stopped",
        )
        device.close()
        if gmcmap_uploader is not None:
            gmcmap_uploader.stop()
        publisher.stop()


def main() -> int:
    configure_logging()
    settings = Settings.from_env()
    signal.signal(signal.SIGTERM, handle_signal)
    signal.signal(signal.SIGINT, handle_signal)
    app_started_at = utc_timestamp()
    history_store: HistoryStore | None = None
    try:
        history_store = HistoryStore(DEFAULT_DB_PATH, retention_days=settings.history_retention_days)
        history_store.purge_unconfirmed_adaptive_spikes()
        history_store.prune()
        history_store.reset_device_runtime_states()
    except (OSError, sqlite3.Error, RuntimeError, ValueError) as exc:
        LOG.error("History storage unavailable; measurement and MQTT will continue: %s", exc)

    configured_devices = settings.effective_devices()
    serial_startup_delays = effective_serial_startup_delays(
        [device.serial_startup_delay for device in configured_devices]
    )
    LOG.info(
        "Configured GMC devices: %s",
        "; ".join(
            f"{device.name or os.path.basename(device.port)}={device.port}@{device.baudrate}"
            for device in configured_devices
        ),
    )
    gmcmap_coordinator = GmcMapUploadCoordinator()
    serial_scheduler = SerialScheduler(
        enabled=settings.serial_scheduler_enabled and len(configured_devices) > 1,
        minimum_gap_seconds=settings.serial_scheduler_gap_seconds,
    )
    LOG.info(
        "Serial scheduler %s (shared command gap %.1fs)",
        "enabled" if serial_scheduler.enabled else "disabled",
        serial_scheduler.minimum_gap_seconds,
    )
    temperature_client = (
        HomeAssistantTemperatureClient(
            entity_id=settings.external_temperature_entity,
            friendly_name=settings.external_temperature_name,
            max_age_seconds=settings.external_temperature_max_age_seconds,
        )
        if (settings.external_temperature_entity or settings.external_temperature_name)
        else None
    )
    pressure_client = (
        HomeAssistantPressureClient(
            entity_ids=(settings.pressure_weather_entity_primary, settings.pressure_weather_entity_secondary),
            provider_name=settings.pressure_weather_source_name,
            max_age_seconds=settings.pressure_weather_max_age_seconds,
            max_difference_hpa=settings.pressure_weather_max_difference_hpa,
        )
        if settings.cosmic_hint_enabled
        else None
    )
    threads = [
        threading.Thread(
            target=_run_device,
            args=(
                settings,
                device,
                device_index,
                len(configured_devices),
                history_store,
                app_started_at,
                gmcmap_coordinator,
                temperature_client,
                pressure_client,
                serial_scheduler,
                serial_startup_delays[device_index],
            ),
            name=f"gmc-{os.path.basename(device.port)}",
            daemon=True,
        )
        for device_index, device in enumerate(configured_devices)
    ]
    for thread in threads:
        thread.start()
    try:
        while not STOP_EVENT.is_set() and any(thread.is_alive() for thread in threads):
            time.sleep(0.5)
    finally:
        STOP_EVENT.set()
        for thread in threads:
            thread.join(timeout=10.0)
    return 0
