from __future__ import annotations

import json
import logging
import threading
from typing import Any, ClassVar

import paho.mqtt.client as mqtt

from .config import Settings
from .device_profiles import DeviceCapabilities
from .errors import MqttError
from .orientation import calibration_for_serial
from .translations import SUPPORTED_UI_LANGUAGES, Translator
from .utils import slugify

LOG = logging.getLogger("gmc_bridge")

MQTT_MAX_QUEUED_MESSAGES = 100
MQTT_MAX_INFLIGHT_MESSAGES = 10
MQTT_PUBLISH_TIMEOUT = 5.0


class MqttPublisher:
    """Thread-safe MQTT publisher with retryable retained-state synchronization."""

    GYRO_OBJECT_IDS = ("gyro_x", "gyro_y", "gyro_z")
    DIAGNOSTIC_OBJECT_IDS: ClassVar[set[str]] = {
        "last_successful_measurement",
        "serial_reconnect_count",
        "serial_error_count",
        "temperature_error_count",
        "voltage_error_count",
        "gyro_error_count",
        "history_write_error_count",
        "device_profile",
        "capabilities",
        "app_started_at",
        "hardware_model",
        "firmware_version",
        "device_time",
        "device_clock_offset_seconds",
        "device_clock_status",
        "heartbeat_enabled",
        "device_time_error_count",
        "heartbeat_error_count",
        "gmcmap_upload_status",
        "gmcmap_last_attempt_utc",
        "gmcmap_last_upload_utc",
        "gmcmap_next_upload_utc",
        "gmcmap_last_cpm",
        "gmcmap_upload_success_count",
        "gmcmap_upload_error_count",
        "gmcmap_consecutive_error_count",
        "gmcmap_last_error_utc",
        "gmcmap_last_error",
        "gmcmap_last_http_status",
        "gmcmap_last_response",
        "gmcmap_counter_id_masked",
        "configured_name",
        "configured_baudrate",
        "configured_scan_interval_seconds",
        "configured_cpm_per_usvh",
        "gyro_x", "gyro_y", "gyro_z",
        "gyro_calibrated_x", "gyro_calibrated_y", "gyro_calibrated_z",
        "gyro_acceleration_magnitude", "gyro_calibration_profile",
        "gyro_roll_degrees", "gyro_pitch_degrees", "gyro_inclination_degrees",
        "gyro_position",
    }
    CHANNELS = ("cpm", "temperature", "voltage", "gyro")

    def __init__(
        self,
        settings: Settings,
        serial: str,
        version: str,
        capabilities: DeviceCapabilities | None = None,
        device_name: str = "",
        read_gyro: bool | None = None,
    ) -> None:
        self.settings = settings
        self.serial = serial
        mqtt_language = settings.ui_language if settings.ui_language in SUPPORTED_UI_LANGUAGES else "en"
        self.t = Translator(mqtt_language)
        self.version = version
        self.device_name = device_name.strip()
        self.read_gyro = settings.read_gyro if read_gyro is None else bool(read_gyro)
        self.capabilities = capabilities or DeviceCapabilities(
            cpm=True, temperature=True, voltage=True, gyro=self.read_gyro,
            gyro_probe_requested=self.read_gyro,
        )
        self.node_id = f"gmc_{slugify(serial)}"
        base = f"gmc/{serial}"
        self.state_topic = f"{base}/state"
        self.diagnostics_topic = f"{base}/diagnostics"
        self.device_availability_topic = f"{base}/device_availability"
        self.availability_topics = {
            "cpm": f"{base}/availability",  # preserve historical CPM availability topic
            "temperature": f"{base}/temperature_availability",
            "voltage": f"{base}/voltage_availability",
            "gyro": f"{base}/gyro_availability",
        }
        self.availability_topic = self.availability_topics["cpm"]
        self.measurement_availability_topic = self.availability_topic
        self.gyro_availability_topic = self.availability_topics["gyro"]

        self._state_lock = threading.RLock()
        self._sync_lock = threading.Lock()
        self._stopping = threading.Event()
        self._connected_event = threading.Event()
        self._sync_worker_running = False

        self._connected = False
        self._device_online = False
        self._channel_ready = {channel: False for channel in self.CHANNELS}
        self._pending_state_payload: str | None = None
        self._pending_diagnostics_payload: str | None = None
        self._discovery_dirty = True
        self._published_device_online: bool | None = None
        self._published_channel_online: dict[str, bool | None] = {
            channel: None for channel in self.CHANNELS
        }
        self._generation = 0
        self._synced_generation = -1

        try:
            self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=self.node_id)
        except (AttributeError, TypeError):
            self.client = mqtt.Client(client_id=self.node_id)

        if settings.mqtt_username:
            self.client.username_pw_set(settings.mqtt_username, settings.mqtt_password)
        self.client.enable_logger(LOG)
        self.client.will_set(self.device_availability_topic, payload="offline", qos=1, retain=True)
        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.reconnect_delay_set(min_delay=1, max_delay=60)
        try:
            self.client.max_queued_messages_set(MQTT_MAX_QUEUED_MESSAGES)
            self.client.max_inflight_messages_set(MQTT_MAX_INFLIGHT_MESSAGES)
        except (AttributeError, RuntimeError, ValueError):
            LOG.debug("MQTT queue limits are not supported by this Paho version")

    def _bump_generation(self) -> None:
        self._generation += 1

    def _on_connect(
        self,
        client: Any,
        userdata: Any,
        flags: Any,
        reason_code: Any,
        properties: Any = None,
    ) -> None:
        if self._stopping.is_set():
            return
        reason_value = getattr(reason_code, "value", reason_code)
        if reason_value != 0:
            with self._state_lock:
                self._connected = False
            self._connected_event.clear()
            LOG.error("MQTT connection rejected: %s", reason_code)
            return
        with self._state_lock:
            self._connected = True
            self._discovery_dirty = True
            self._published_device_online = None
            self._published_channel_online = {channel: None for channel in self.CHANNELS}
            self._bump_generation()
        self._connected_event.set()
        LOG.info("Connected to MQTT broker")
        self._schedule_sync()

    def _on_disconnect(self, client: Any, userdata: Any, *args: Any) -> None:
        with self._state_lock:
            self._connected = False
            self._published_device_online = None
            self._published_channel_online = {channel: None for channel in self.CHANNELS}
            self._bump_generation()
        self._connected_event.clear()
        if self._stopping.is_set():
            return
        if len(args) >= 2:
            reason_code = args[1]
        elif len(args) == 1:
            reason_code = args[0]
        else:
            reason_code = "unknown"
        LOG.warning("MQTT disconnected: %s", reason_code)

    def _schedule_sync(self) -> None:
        with self._state_lock:
            if self._stopping.is_set() or self._sync_worker_running:
                return
            self._sync_worker_running = True
        thread = threading.Thread(target=self._sync_worker, name="mqtt-state-sync", daemon=True)
        thread.start()

    def _sync_worker(self) -> None:
        try:
            self.sync_mqtt_state()
        finally:
            reschedule = False
            with self._state_lock:
                self._sync_worker_running = False
                reschedule = (
                    not self._stopping.is_set()
                    and self._connected
                    and self._synced_generation != self._generation
                )
            if reschedule:
                self._schedule_sync()

    def start(self, wait_timeout: float = 15.0) -> bool:
        self.client.connect_async(self.settings.mqtt_host, self.settings.mqtt_port, keepalive=60)
        self.client.loop_start()
        return self._connected_event.wait(timeout=wait_timeout)

    def stop(self) -> None:
        self._stopping.set()
        with self._state_lock:
            connected = self._connected
            self._device_online = False
            self._channel_ready = {channel: False for channel in self.CHANNELS}
            self._pending_state_payload = None
            self._bump_generation()

        acquired = self._sync_lock.acquire(timeout=MQTT_PUBLISH_TIMEOUT)
        try:
            if connected and acquired:
                for topic in [*self.availability_topics.values(), self.device_availability_topic]:
                    try:
                        self._publish_confirmed(topic, "offline", retain=True, qos=1)
                    except MqttError as exc:
                        LOG.debug("Could not confirm offline state during shutdown: %s", exc)
            try:
                self.client.disconnect()
            except (OSError, RuntimeError, ValueError) as exc:
                LOG.debug("MQTT disconnect during shutdown failed: %s", exc)
        finally:
            if acquired:
                self._sync_lock.release()
            self.client.loop_stop()

    def _publish_async(self, topic: str, payload: str, *, retain: bool, qos: int) -> Any:
        if self._stopping.is_set() and payload != "offline":
            raise MqttError("publisher is stopping")
        info = self.client.publish(topic, payload=payload, qos=qos, retain=retain)
        if info.rc != mqtt.MQTT_ERR_SUCCESS:
            raise MqttError(f"publish rc={info.rc} for topic {topic}")
        return info

    def _publish_confirmed(self, topic: str, payload: str, *, retain: bool, qos: int) -> None:
        info = self._publish_async(topic, payload, retain=retain, qos=qos)
        wait_for_publish = getattr(info, "wait_for_publish", None)
        if wait_for_publish is None:
            return
        try:
            result = wait_for_publish(timeout=MQTT_PUBLISH_TIMEOUT)
        except (RuntimeError, ValueError) as exc:
            raise MqttError(f"publish confirmation failed for topic {topic}: {exc}") from exc
        if result is False:
            raise MqttError(f"publish confirmation timed out for topic {topic}")
        is_published = getattr(info, "is_published", None)
        if callable(is_published) and not is_published():
            raise MqttError(f"publish was not confirmed for topic {topic}")

    def _discovery_topic(self, object_id: str) -> str:
        return f"homeassistant/sensor/{self.node_id}/{object_id}/config"

    def _availability_for(self, object_id: str) -> list[dict[str, str]]:
        if object_id.startswith("gyro_"):
            return [
                {"topic": self.device_availability_topic},
                {"topic": self.availability_topics["gyro"]},
            ]
        if object_id in self.DIAGNOSTIC_OBJECT_IDS:
            return [{"topic": self.device_availability_topic}]
        if object_id in {"cpm", "cps", "heartbeat_cpm_60s", "tube_low_cpm", "tube_high_cpm"}:
            channel = "cpm"
        elif object_id == "temperature":
            channel = "temperature"
        elif object_id == "voltage":
            channel = "voltage"
        else:
            channel = "gyro"
        return [
            {"topic": self.device_availability_topic},
            {"topic": self.availability_topics[channel]},
        ]

    def _discovery_messages(self) -> list[tuple[str, str]]:
        capabilities = getattr(
            self,
            "capabilities",
            DeviceCapabilities(
                cpm=True,
                temperature=True,
                voltage=True,
                gyro=getattr(self, "read_gyro", self.settings.read_gyro),
                gyro_probe_requested=getattr(self, "read_gyro", self.settings.read_gyro),
            ),
        )
        t = getattr(self, "t", Translator("en"))
        device = {
            "identifiers": [f"gq_gmc_{self.serial}"],
            "name": getattr(self, "device_name", "") or t("GMC Radiation Monitor"),
            "manufacturer": "GQ Electronics",
            "model": self.version,
            "serial_number": self.serial,
        }
        entities: dict[str, dict[str, Any]] = {
            "cpm": {
                "name": t("Radiation CPM"), "unit_of_measurement": "CPM",
                "state_class": "measurement", "icon": "mdi:radioactive",
                "value_template": "{{ value_json.cpm }}",
            },
            "cps": {
                "name": t("Live radiation CPS"), "unit_of_measurement": "CPS",
                "state_class": "measurement", "icon": "mdi:pulse",
                "value_template": "{{ value_json.cps }}",
            },
            "heartbeat_cpm_60s": {
                "name": t("Heartbeat rolling 60 s CPM"), "unit_of_measurement": "CPM",
                "state_class": "measurement", "icon": "mdi:chart-timeline-variant-shimmer",
                "value_template": "{{ value_json.heartbeat_cpm_60s }}",
            },
            "tube_low_cpm": {
                "name": t("Low-dose Tube CPM"), "unit_of_measurement": "CPM",
                "state_class": "measurement", "icon": "mdi:radioactive-circle",
                "value_template": "{{ value_json.tube_low_cpm }}",
            },
            "tube_high_cpm": {
                "name": t("High-dose Tube CPM"), "unit_of_measurement": "CPM",
                "state_class": "measurement", "icon": "mdi:radioactive-circle-outline",
                "value_template": "{{ value_json.tube_high_cpm }}",
            },
            "smart_alert_state": {"name": t("Smart Alert State"), "icon": "mdi:shield-alert-outline", "value_template": "{{ value_json.smart_alert_state }}"},
            "mean_1h_cpm": {"name": t("Radiation 1 h Mean"), "unit_of_measurement": "CPM", "state_class": "measurement", "icon": "mdi:chart-bell-curve", "value_template": "{{ value_json.mean_1h_cpm }}"},
            "median_1h_cpm": {"name": t("Radiation 1 h Median"), "unit_of_measurement": "CPM", "state_class": "measurement", "icon": "mdi:chart-bell-curve-cumulative", "value_template": "{{ value_json.median_1h_cpm }}"},
            "sd_1h_cpm": {"name": t("Radiation 1 h Standard Deviation"), "unit_of_measurement": "CPM", "state_class": "measurement", "icon": "mdi:sigma", "value_template": "{{ value_json.sd_1h_cpm }}"},
            "rapid_change_percent": {"name": t("Radiation Rapid Change"), "unit_of_measurement": "%", "state_class": "measurement", "icon": "mdi:trending-up", "value_template": "{{ value_json.rapid_change_percent }}"},
            "baseline_cpm": {"name": t("Learned Radiation Baseline"), "unit_of_measurement": "CPM", "state_class": "measurement", "icon": "mdi:chart-timeline-variant", "value_template": "{{ value_json.baseline_cpm }}"},
            "baseline_deviation_percent": {"name": t("Radiation Baseline Deviation"), "unit_of_measurement": "%", "state_class": "measurement", "icon": "mdi:delta", "value_template": "{{ value_json.baseline_deviation_percent }}"},
            "sustained_alert": {"name": t("Sustained Radiation Alert"), "device_class": "problem", "payload_on": True, "payload_off": False, "icon": "mdi:alarm-light-outline", "value_template": "{{ value_json.sustained_alert }}"},
            "temperature": {
                "name": t("Temperature"), "device_class": "temperature",
                "unit_of_measurement": "°C", "state_class": "measurement",
                "value_template": "{{ value_json.temperature_c }}",
            },
            "voltage": {
                "name": t("Voltage"), "device_class": "voltage",
                "unit_of_measurement": "V", "state_class": "measurement",
                "value_template": "{{ value_json.voltage_v }}",
            },
            "hardware_model": {
                "name": t("Hardware model"), "entity_category": "diagnostic",
                "icon": "mdi:developer-board",
                "value_template": "{{ value_json.hardware_model }}",
            },
            "firmware_version": {
                "name": t("Firmware version"), "entity_category": "diagnostic",
                "icon": "mdi:chip",
                "value_template": "{{ value_json.firmware_version }}",
            },
            "configured_name": {
                "name": t("Configured device name"), "entity_category": "diagnostic",
                "icon": "mdi:label-outline",
                "value_template": "{{ value_json.configured_name }}",
            },
            "configured_baudrate": {
                "name": t("Configured baud rate"), "entity_category": "diagnostic",
                "unit_of_measurement": "Bd", "icon": "mdi:serial-port",
                "value_template": "{{ value_json.configured_baudrate }}",
            },
            "configured_scan_interval_seconds": {
                "name": t("Configured measurement interval"), "entity_category": "diagnostic",
                "unit_of_measurement": "s", "icon": "mdi:timer-outline",
                "value_template": "{{ value_json.configured_scan_interval_seconds }}",
            },
            "configured_cpm_per_usvh": {
                "name": t("Configured CPM conversion factor"), "entity_category": "diagnostic",
                "unit_of_measurement": "CPM/(µSv/h)", "icon": "mdi:calculator-variant-outline",
                "value_template": "{{ value_json.configured_cpm_per_usvh }}",
            },
            "device_time": {
                "name": t("Device clock"), "device_class": "timestamp",
                "entity_category": "diagnostic", "icon": "mdi:clock-digital",
                "value_template": "{{ value_json.device_time }}",
            },
            "device_clock_offset_seconds": {
                "name": t("Device clock offset"), "unit_of_measurement": "s",
                "state_class": "measurement", "entity_category": "diagnostic",
                "icon": "mdi:clock-alert-outline",
                "value_template": "{{ value_json.device_clock_offset_seconds }}",
            },
            "device_clock_status": {
                "name": t("Device clock status"), "entity_category": "diagnostic",
                "icon": "mdi:clock-check-outline",
                "value_template": "{{ value_json.device_clock_status }}",
            },
            "heartbeat_enabled": {
                "name": t("Heartbeat mode"), "entity_category": "diagnostic",
                "icon": "mdi:heart-pulse",
                "value_template": "{{ value_json.heartbeat_enabled }}",
            },
            "last_successful_measurement": {
                "name": t("Last Successful Measurement"), "device_class": "timestamp",
                "entity_category": "diagnostic",
                "value_template": "{{ value_json.last_successful_measurement }}",
            },
            "serial_reconnect_count": {
                "name": t("Serial Reconnects Since Start"), "state_class": "total_increasing",
                "entity_category": "diagnostic", "icon": "mdi:connection",
                "value_template": "{{ value_json.serial_reconnect_count }}",
            },
            "serial_error_count": {
                "name": t("Serial Errors Since Start"), "state_class": "total_increasing",
                "entity_category": "diagnostic", "icon": "mdi:alert-circle-outline",
                "value_template": "{{ value_json.serial_error_count }}",
            },
            "temperature_error_count": {
                "name": t("Temperature Errors Since Start"), "state_class": "total_increasing",
                "entity_category": "diagnostic",
                "value_template": "{{ value_json.temperature_error_count }}",
            },
            "voltage_error_count": {
                "name": t("Voltage Errors Since Start"), "state_class": "total_increasing",
                "entity_category": "diagnostic",
                "value_template": "{{ value_json.voltage_error_count }}",
            },
            "gyro_error_count": {
                "name": t("Gyro Errors Since Start"), "state_class": "total_increasing",
                "entity_category": "diagnostic",
                "value_template": "{{ value_json.gyro_error_count }}",
            },
            "device_time_error_count": {
                "name": t("Device Time Errors Since Start"), "state_class": "total_increasing",
                "entity_category": "diagnostic",
                "value_template": "{{ value_json.device_time_error_count }}",
            },
            "heartbeat_error_count": {
                "name": t("Heartbeat Errors Since Start"), "state_class": "total_increasing",
                "entity_category": "diagnostic",
                "value_template": "{{ value_json.heartbeat_error_count }}",
            },
            "history_write_error_count": {
                "name": t("History Write Errors Since Start"), "state_class": "total_increasing",
                "entity_category": "diagnostic", "icon": "mdi:database-alert-outline",
                "value_template": "{{ value_json.history_write_error_count }}",
            },
            "device_profile": {
                "name": t("Device Profile"), "entity_category": "diagnostic",
                "icon": "mdi:devices",
                "value_template": "{{ value_json.device_profile }}",
            },
            "capabilities": {
                "name": t("Detected Capabilities"), "entity_category": "diagnostic",
                "icon": "mdi:list-status",
                "value_template": "{{ value_json.capabilities }}",
            },
            "gmcmap_upload_status": {
                "name": t("GMCMap upload status"), "entity_category": "diagnostic",
                "icon": "mdi:map-marker-radius-outline",
                "value_template": "{{ value_json.gmcmap_upload_status }}",
            },
            "gmcmap_last_attempt_utc": {
                "name": t("GMCMap last upload attempt"), "device_class": "timestamp",
                "entity_category": "diagnostic", "icon": "mdi:cloud-clock-outline",
                "value_template": "{{ value_json.gmcmap_last_attempt_utc }}",
            },
            "gmcmap_last_upload_utc": {
                "name": t("GMCMap last successful upload"), "device_class": "timestamp",
                "entity_category": "diagnostic", "icon": "mdi:cloud-check-outline",
                "value_template": "{{ value_json.gmcmap_last_upload_utc }}",
            },
            "gmcmap_next_upload_utc": {
                "name": t("GMCMap next upload"), "device_class": "timestamp",
                "entity_category": "diagnostic", "icon": "mdi:cloud-sync-outline",
                "value_template": "{{ value_json.gmcmap_next_upload_utc }}",
            },
            "gmcmap_last_cpm": {
                "name": t("GMCMap last uploaded CPM"), "unit_of_measurement": "CPM",
                "state_class": "measurement", "entity_category": "diagnostic",
                "icon": "mdi:radioactive",
                "value_template": "{{ value_json.gmcmap_last_cpm }}",
            },
            "gmcmap_last_average_cpm": {
                "name": t("GMCMap last uploaded ACPM"), "unit_of_measurement": "ACPM",
                "state_class": "measurement", "entity_category": "diagnostic",
                "icon": "mdi:chart-timeline-variant",
                "value_template": "{{ value_json.gmcmap_last_average_cpm }}",
            },
            "gmcmap_acpm_sample_count": {
                "name": t("GMCMap ACPM accepted samples"),
                "state_class": "total", "entity_category": "diagnostic",
                "icon": "mdi:counter",
                "value_template": "{{ value_json.gmcmap_acpm_sample_count }}",
            },
            "gmcmap_upload_success_count": {
                "name": t("GMCMap successful uploads since start"),
                "state_class": "total_increasing", "entity_category": "diagnostic",
                "icon": "mdi:cloud-upload-outline",
                "value_template": "{{ value_json.gmcmap_upload_success_count }}",
            },
            "gmcmap_upload_error_count": {
                "name": t("GMCMap upload errors since start"),
                "state_class": "total_increasing", "entity_category": "diagnostic",
                "icon": "mdi:cloud-alert-outline",
                "value_template": "{{ value_json.gmcmap_upload_error_count }}",
            },
            "gmcmap_consecutive_error_count": {
                "name": t("GMCMap consecutive upload errors"),
                "entity_category": "diagnostic", "icon": "mdi:cloud-alert",
                "value_template": "{{ value_json.gmcmap_consecutive_error_count }}",
            },
            "gmcmap_last_error_utc": {
                "name": t("GMCMap last error time"), "device_class": "timestamp",
                "entity_category": "diagnostic", "icon": "mdi:clock-alert-outline",
                "value_template": "{{ value_json.gmcmap_last_error_utc }}",
            },
            "gmcmap_last_error": {
                "name": t("GMCMap last upload error"),
                "entity_category": "diagnostic", "icon": "mdi:alert-circle-outline",
                "value_template": "{{ value_json.gmcmap_last_error }}",
            },
            "gmcmap_last_http_status": {
                "name": t("GMCMap last HTTP status"),
                "entity_category": "diagnostic", "icon": "mdi:web-check",
                "value_template": "{{ value_json.gmcmap_last_http_status }}",
            },
            "gmcmap_last_response": {
                "name": t("GMCMap last server response"),
                "entity_category": "diagnostic", "icon": "mdi:message-text-outline",
                "value_template": "{{ value_json.gmcmap_last_response }}",
            },
            "gmcmap_counter_id_masked": {
                "name": t("GMCMap counter ID"), "entity_category": "diagnostic",
                "icon": "mdi:identifier",
                "value_template": "{{ value_json.gmcmap_counter_id_masked }}",
            },
            "app_started_at": {
                "name": t("App Started At"), "device_class": "timestamp",
                "entity_category": "diagnostic", "icon": "mdi:clock-start",
                "value_template": "{{ value_json.app_started_at }}",
            },
        }
        if not self.settings.publish_advanced_sensors:
            for object_id in ("smart_alert_state", "mean_1h_cpm", "median_1h_cpm", "sd_1h_cpm", "rapid_change_percent", "baseline_cpm", "baseline_deviation_percent", "sustained_alert"):
                entities.pop(object_id, None)
        if not capabilities.dual_tube:
            entities.pop("tube_low_cpm", None)
            entities.pop("tube_high_cpm", None)
        if not capabilities.temperature:
            entities.pop("temperature", None)
        if not capabilities.voltage:
            entities.pop("voltage", None)
        heartbeat_enabled = bool(getattr(self.settings, "heartbeat_enabled", False))
        if not (heartbeat_enabled and capabilities.heartbeat):
            entities.pop("cps", None)
            entities.pop("heartbeat_cpm_60s", None)
            entities.pop("heartbeat_enabled", None)
            entities.pop("heartbeat_error_count", None)
        read_device_time = bool(getattr(self.settings, "read_device_time", True))
        if not (read_device_time and capabilities.device_time):
            entities.pop("device_time", None)
            entities.pop("device_clock_offset_seconds", None)
            entities.pop("device_clock_status", None)
            entities.pop("device_time_error_count", None)

        if not bool(getattr(self.settings, "gmcmap_enabled", False)):
            for object_id in (
                "gmcmap_upload_status", "gmcmap_last_attempt_utc",
                "gmcmap_last_upload_utc", "gmcmap_next_upload_utc", "gmcmap_last_cpm",
                "gmcmap_upload_success_count", "gmcmap_upload_error_count",
                "gmcmap_consecutive_error_count", "gmcmap_last_error_utc",
                "gmcmap_last_error", "gmcmap_last_http_status", "gmcmap_last_response",
                "gmcmap_counter_id_masked",
            ):
                entities.pop(object_id, None)

        if getattr(self, "read_gyro", self.settings.read_gyro) and capabilities.gyro:
            for axis in ("x", "y", "z"):
                entities[f"gyro_{axis}"] = {
                    "name": t("Gyro Raw {axis}", axis=axis.upper()),
                    "entity_category": "diagnostic",
                    "value_template": f"{{{{ value_json.gyro_{axis} }}}}",
                }
            if calibration_for_serial(self.serial) is not None:
                for axis in ("x", "y", "z"):
                    entities[f"gyro_calibrated_{axis}"] = {
                        "name": t("Gyro Calibrated {axis}", axis=axis.upper()),
                        "unit_of_measurement": "g",
                        "state_class": "measurement",
                        "entity_category": "diagnostic",
                        "value_template": f"{{{{ value_json.gyro_calibrated_{axis} }}}}",
                    }
                entities.update({
                    "gyro_acceleration_magnitude": {
                        "name": t("Acceleration magnitude"), "unit_of_measurement": "g",
                        "state_class": "measurement", "entity_category": "diagnostic",
                        "value_template": "{{ value_json.gyro_acceleration_magnitude }}",
                    },
                    "gyro_calibration_profile": {
                        "name": t("Calibration profile"), "entity_category": "diagnostic",
                        "value_template": "{{ value_json.gyro_calibration_profile }}",
                    },
                    "gyro_roll_degrees": {
                        "name": t("Roll angle"), "unit_of_measurement": "°",
                        "state_class": "measurement", "entity_category": "diagnostic",
                        "value_template": "{{ value_json.gyro_roll_degrees }}",
                    },
                    "gyro_pitch_degrees": {
                        "name": t("Pitch angle"), "unit_of_measurement": "°",
                        "state_class": "measurement", "entity_category": "diagnostic",
                        "value_template": "{{ value_json.gyro_pitch_degrees }}",
                    },
                    "gyro_inclination_degrees": {
                        "name": t("Inclination"), "unit_of_measurement": "°",
                        "state_class": "measurement", "entity_category": "diagnostic",
                        "value_template": "{{ value_json.gyro_inclination_degrees }}",
                    },
                    "gyro_position": {
                        "name": t("Device position"), "entity_category": "diagnostic",
                        "value_template": "{{ value_json.gyro_position }}",
                    },
                })

        messages: list[tuple[str, str]] = []
        for object_id, extra in entities.items():
            diagnostic = object_id in self.DIAGNOSTIC_OBJECT_IDS
            payload = {
                "unique_id": f"{self.node_id}_{object_id}",
                "object_id": f"{self.node_id}_{object_id}",
                "state_topic": self.diagnostics_topic if diagnostic else self.state_topic,
                "availability": self._availability_for(object_id),
                "availability_mode": "all",
                "payload_available": "online",
                "payload_not_available": "offline",
                "device": device,
                **extra,
            }
            messages.append((self._discovery_topic(object_id), json.dumps(payload, separators=(",", ":"))))

        unsupported_measurements = []
        if not self.settings.publish_advanced_sensors:
            for object_id in ("smart_alert_state", "mean_1h_cpm", "median_1h_cpm", "sd_1h_cpm", "rapid_change_percent", "baseline_cpm", "baseline_deviation_percent", "sustained_alert"):
                entities.pop(object_id, None)
        if not capabilities.dual_tube and "500" in self.version:
            unsupported_measurements.extend(("tube_low_cpm", "tube_high_cpm"))
        if not capabilities.temperature:
            unsupported_measurements.append("temperature")
        if not capabilities.voltage:
            unsupported_measurements.append("voltage")
        if not (bool(getattr(self.settings, "heartbeat_enabled", False)) and capabilities.heartbeat):
            unsupported_measurements.extend(("cps", "heartbeat_cpm_60s", "heartbeat_enabled", "heartbeat_error_count"))
        if not (bool(getattr(self.settings, "read_device_time", True)) and capabilities.device_time):
            unsupported_measurements.extend(("device_time", "device_clock_offset_seconds", "device_clock_status", "device_time_error_count"))
        if not bool(getattr(self.settings, "gmcmap_enabled", False)):
            unsupported_measurements.extend((
                "gmcmap_upload_status", "gmcmap_last_attempt_utc",
                "gmcmap_last_upload_utc", "gmcmap_next_upload_utc", "gmcmap_last_cpm",
                "gmcmap_upload_success_count", "gmcmap_upload_error_count",
                "gmcmap_consecutive_error_count", "gmcmap_last_error_utc",
                "gmcmap_last_error", "gmcmap_last_http_status", "gmcmap_last_response",
                "gmcmap_counter_id_masked",
            ))
        if not (getattr(self, "read_gyro", self.settings.read_gyro) and capabilities.gyro):
            unsupported_measurements.extend(self.GYRO_OBJECT_IDS)
        for object_id in unsupported_measurements:
            messages.append((self._discovery_topic(object_id), ""))
        return messages

    def publish_discovery(self) -> None:
        for topic, payload in self._discovery_messages():
            self._publish_confirmed(topic, payload, retain=True, qos=1)

    def _desired_channel_online(self, channel: str) -> bool:
        return self._device_online and self._channel_ready[channel] and self._pending_state_payload is None

    def sync_mqtt_state(self) -> bool:
        if self._stopping.is_set() or not self._sync_lock.acquire(blocking=False):
            return False
        try:
            for _ in range(16):
                with self._state_lock:
                    if self._stopping.is_set() or not self._connected:
                        return False
                    generation = self._generation
                    discovery_dirty = self._discovery_dirty
                    diagnostics_payload = self._pending_diagnostics_payload
                    device_online = self._device_online
                    published_device = self._published_device_online
                    state_payload = self._pending_state_payload

                if discovery_dirty:
                    try:
                        self.publish_discovery()
                    except MqttError as exc:
                        LOG.warning("MQTT discovery synchronization failed; will retry: %s", exc)
                        return False
                    with self._state_lock:
                        if self._generation == generation:
                            self._discovery_dirty = False

                if diagnostics_payload is not None:
                    try:
                        self._publish_async(self.diagnostics_topic, diagnostics_payload, retain=True, qos=1)
                    except MqttError as exc:
                        LOG.warning("MQTT diagnostics publish failed; latest diagnostics retained: %s", exc)
                        return False
                    with self._state_lock:
                        if self._pending_diagnostics_payload == diagnostics_payload:
                            self._pending_diagnostics_payload = None

                if published_device is not device_online:
                    try:
                        self._publish_confirmed(
                            self.device_availability_topic,
                            "online" if device_online else "offline",
                            retain=True, qos=1,
                        )
                    except MqttError as exc:
                        LOG.warning("MQTT device availability synchronization failed; will retry: %s", exc)
                        return False
                    with self._state_lock:
                        if self._device_online == device_online:
                            self._published_device_online = device_online

                if state_payload is not None:
                    try:
                        self._publish_confirmed(self.state_topic, state_payload, retain=True, qos=1)
                    except MqttError as exc:
                        LOG.warning("MQTT state publish failed; latest sample retained: %s", exc)
                        return False
                    with self._state_lock:
                        if self._pending_state_payload == state_payload:
                            self._pending_state_payload = None

                for channel in self.CHANNELS:
                    with self._state_lock:
                        desired = self._desired_channel_online(channel)
                        published = self._published_channel_online[channel]
                    if published is desired:
                        continue
                    try:
                        self._publish_confirmed(
                            self.availability_topics[channel],
                            "online" if desired else "offline",
                            retain=True, qos=1,
                        )
                    except MqttError as exc:
                        LOG.warning("MQTT %s availability synchronization failed; will retry: %s", channel, exc)
                        return False
                    with self._state_lock:
                        if self._desired_channel_online(channel) == desired:
                            self._published_channel_online[channel] = desired

                with self._state_lock:
                    if self._generation == generation:
                        self._synced_generation = generation
                        return True
            LOG.warning("MQTT state changed continuously during synchronization; deferring retry")
            return False
        finally:
            self._sync_lock.release()

    def set_device_online(self, online: bool) -> None:
        with self._state_lock:
            self._device_online = online
            if not online:
                self._channel_ready = {channel: False for channel in self.CHANNELS}
                self._pending_state_payload = None
            self._bump_generation()
        self.sync_mqtt_state()

    def mark_all_measurements_unavailable(self) -> None:
        with self._state_lock:
            self._channel_ready = {channel: False for channel in self.CHANNELS}
            self._pending_state_payload = None
            self._bump_generation()
        self.sync_mqtt_state()

    def publish_sample(self, sample: dict[str, Any], available: dict[str, bool]) -> bool:
        payload = json.dumps(sample, separators=(",", ":"))
        with self._state_lock:
            self._pending_state_payload = payload
            for channel in self.CHANNELS:
                self._channel_ready[channel] = bool(available.get(channel, False))
            self._bump_generation()
        synced = self.sync_mqtt_state()
        with self._state_lock:
            return synced and self._pending_state_payload is None and self._published_channel_online["cpm"] is True

    def publish_state(self, sample: dict[str, Any]) -> bool:
        """Compatibility wrapper used by tests and older callers."""
        available = {
            "cpm": "cpm" in sample,
            "temperature": "temperature_c" in sample,
            "voltage": "voltage_v" in sample,
            "gyro": all(key in sample for key in ("gyro_x", "gyro_y", "gyro_z")),
        }
        return self.publish_sample(sample, available)

    def publish_diagnostics(self, diagnostics: dict[str, Any]) -> bool:
        t = getattr(self, "t", Translator("en"))
        localized = dict(diagnostics)
        profile = localized.get("device_profile")
        profile_names = {
            "gmc_300_320": "GMC-300/320 family",
            "gmc_500": "GMC-500 family",
            "gmc_600": "GMC-600 family",
            "gmc_generic": "Generic GQ GMC / RFC1201-compatible device",
            "generic_rfc1201": "Generic RFC1201-compatible device",
        }
        if profile in profile_names:
            localized["device_profile"] = t(profile_names[str(profile)])
        clock_status = localized.get("device_clock_status")
        clock_status_labels = {
            "ok": "Clock synchronized",
            "warning": "Clock offset exceeds warning threshold",
            "unavailable": "Device clock unavailable",
            "invalid": "Invalid device clock response",
        }
        if clock_status in clock_status_labels:
            localized["device_clock_status"] = t(clock_status_labels[str(clock_status)])
        gmcmap_status = localized.get("gmcmap_upload_status")
        gmcmap_status_labels = {
            "disabled": "Disabled",
            "not_configured": "Not configured",
            "waiting": "Waiting for first upload",
            "uploading": "Uploading",
            "success": "Upload successful",
            "error": "Upload failed",
        }
        if gmcmap_status in gmcmap_status_labels:
            localized["gmcmap_upload_status"] = t(gmcmap_status_labels[str(gmcmap_status)])
        capabilities = localized.get("capabilities")
        if isinstance(capabilities, str):
            labels = {
                "cpm": "CPM",
                "temperature": "Temperature",
                "voltage": "Voltage",
                "gyro": "Gyroscope",
                "dual_tube": "Dual-tube measurement",
                "device_time": "Device clock",
                "heartbeat": "Heartbeat mode",
            }
            localized["capabilities"] = ", ".join(
                t(labels.get(item.strip(), item.strip()))
                for item in capabilities.split(",") if item.strip()
            )
        payload = json.dumps(localized, separators=(",", ":"))
        with self._state_lock:
            self._pending_diagnostics_payload = payload
            self._bump_generation()
        synced = self.sync_mqtt_state()
        with self._state_lock:
            return synced and self._pending_diagnostics_payload is None
