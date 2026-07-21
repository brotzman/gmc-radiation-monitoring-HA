from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass, replace
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .calibration_presets import PRESETS, SUPPORTED_PROFILE_IDS, detect_profile_id, resolve_preset
from .gmcmap import parse_device_id_mappings, validate_identifier

SUPPORTED_BAUDRATES = {1200, 2400, 4800, 9600, 19200, 38400, 57600, 115200}
HIGH_CPM_THRESHOLD = 10000
HIGH_CPM_CONFIRMATIONS = 3


def parse_bool(name: str, value: str) -> bool:
    normalized = value.strip().lower()
    if normalized == "true":
        return True
    if normalized == "false":
        return False
    raise ValueError(f"{name} must be exactly true or false")


def _mapping_bool(name: str, value: object, default: bool) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return parse_bool(name, value)
    raise ValueError(f"{name} must be a boolean")


@dataclass(frozen=True)
class TubeCalibrationConfig:
    """Calibration values belonging to one physical detector tube."""

    tube_model: str = ""
    cpm_per_usvh: float | None = None
    dead_time_us: float | None = None
    reliable_max_cpm: int | None = None
    dead_time_model: str = "none"
    conversion_factor_uncertainty_percent: float | None = None
    calibration_uncertainty_percent: float | None = None
    calibration_reference: str = ""

    def validate(self, name: str) -> None:
        if self.cpm_per_usvh is not None and self.cpm_per_usvh <= 0:
            raise ValueError(f"{name}.cpm_per_usvh must be greater than zero")
        if self.dead_time_us is not None and self.dead_time_us <= 0:
            raise ValueError(f"{name}.dead_time_us must be greater than zero")
        if self.reliable_max_cpm is not None and self.reliable_max_cpm <= 0:
            raise ValueError(f"{name}.reliable_max_cpm must be greater than zero")
        if self.dead_time_model not in {"none", "nonparalyzable"}:
            raise ValueError(f"{name}.dead_time_model must be none or nonparalyzable")
        if self.dead_time_model != "none" and self.dead_time_us is None:
            raise ValueError(f"{name}.dead_time_us is required for dead-time correction")
        for field_name, value in (
            ("conversion_factor_uncertainty_percent", self.conversion_factor_uncertainty_percent),
            ("calibration_uncertainty_percent", self.calibration_uncertainty_percent),
        ):
            if value is not None and value < 0:
                raise ValueError(f"{name}.{field_name} must not be negative")

    @property
    def dose_calibrated(self) -> bool:
        return self.cpm_per_usvh is not None and self.cpm_per_usvh > 0

    def as_dict(self) -> dict[str, object]:
        return asdict(self)


_TUBE_PROFILE_FIELDS = {
    "tube_model",
    "cpm_per_usvh",
    "dead_time_us",
    "reliable_max_cpm",
    "dead_time_model",
    "conversion_factor_uncertainty_percent",
    "calibration_uncertainty_percent",
    "calibration_reference",
}


def _optional_float(value: object) -> float | None:
    return None if value in (None, "") else float(value)


def _optional_int(value: object) -> int | None:
    return None if value in (None, "") else int(value)


def _parse_flat_tube_calibration(
    name: str, item: dict[str, object], prefix: str
) -> TubeCalibrationConfig | None:
    """Build one tube profile from Supervisor-compatible optional scalar fields."""

    values = {field: item.get(f"{prefix}_{field}") for field in _TUBE_PROFILE_FIELDS}
    if all(value in (None, "") for value in values.values()):
        return None
    return _parse_tube_calibration(name, values)


def _parse_tube_calibration(name: str, value: object) -> TubeCalibrationConfig | None:
    if value in (None, ""):
        return None
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be an object")
    unknown = sorted(set(value) - _TUBE_PROFILE_FIELDS)
    if unknown:
        raise ValueError(f"{name} contains unknown fields: {', '.join(unknown)}")
    profile = TubeCalibrationConfig(
        tube_model=str(value.get("tube_model", "")).strip(),
        cpm_per_usvh=_optional_float(value.get("cpm_per_usvh")),
        dead_time_us=_optional_float(value.get("dead_time_us")),
        reliable_max_cpm=_optional_int(value.get("reliable_max_cpm")),
        dead_time_model=str(value.get("dead_time_model", "none")).strip().lower(),
        conversion_factor_uncertainty_percent=_optional_float(
            value.get("conversion_factor_uncertainty_percent")
        ),
        calibration_uncertainty_percent=_optional_float(
            value.get("calibration_uncertainty_percent")
        ),
        calibration_reference=str(value.get("calibration_reference", "")).strip(),
    )
    profile.validate(name)
    return profile


@dataclass(frozen=True)
class DeviceConfig:
    """Effective serial and measurement settings for one physical GMC."""

    port: str
    name: str = ""
    baudrate: int = 19200
    scan_interval: int = 60
    command_timeout: float = 2.0
    inter_command_delay_ms: int = 150
    serial_startup_delay: float | None = None
    auxiliary_read_interval: int = 300
    high_cpm_threshold: int = HIGH_CPM_THRESHOLD
    high_cpm_confirmations: int = HIGH_CPM_CONFIRMATIONS
    read_gyro: bool = False
    read_device_time: bool = True
    device_clock_warning_seconds: int = 120
    heartbeat_enabled: bool = False
    detector_profile: str = "custom_single"
    calibration_overrides: bool = False
    cpm_per_usvh: float = 154.0
    dead_time_us: float | None = None
    reliable_max_cpm: int | None = None
    dead_time_model: str = "none"
    conversion_factor_uncertainty_percent: float | None = None
    calibration_uncertainty_percent: float | None = None
    calibration_reference: str = ""
    tube_model: str = ""
    dual_tube_mode: str = "single"
    dual_tube_switch_cpm: int | None = None
    low_dose_tube: TubeCalibrationConfig | None = None
    high_dose_tube: TubeCalibrationConfig | None = None
    gmcmap_counter_id: str = ""
    gmcmap_upload_interval: int = 300
    gmcmap_timeout: float = 10.0
    external_temperature_entity: str = ""
    external_temperature_name: str = "Raumklima (Arbeitszimmer)"
    external_temperature_max_age_seconds: int = 900
    serial_debug: bool = False
    serial_debug_max_bytes: int = 64
    orientation_calibration_enabled: bool = False
    orientation_calibration_serial: str = ""
    orientation_offset_x: float = 0.0
    orientation_offset_y: float = 0.0
    orientation_offset_z: float = 0.0
    orientation_scale_x: float = 1.0
    orientation_scale_y: float = 1.0
    orientation_scale_z: float = 1.0
    orientation_calibration_name: str = "Custom six-position calibration"

    def legacy_tube_profile(self) -> TubeCalibrationConfig:
        return TubeCalibrationConfig(
            tube_model=self.tube_model,
            cpm_per_usvh=self.cpm_per_usvh,
            dead_time_us=self.dead_time_us,
            reliable_max_cpm=self.reliable_max_cpm,
            dead_time_model=self.dead_time_model,
            conversion_factor_uncertainty_percent=self.conversion_factor_uncertainty_percent,
            calibration_uncertainty_percent=self.calibration_uncertainty_percent,
            calibration_reference=self.calibration_reference,
        )

    def effective_low_dose_tube(self) -> TubeCalibrationConfig:
        # Upgrade migration: legacy single-profile GMC-500+ values become the
        # low-dose tube profile when no explicit nested profile exists.
        return self.low_dose_tube or self.legacy_tube_profile()

    def calibration_status(self) -> str:
        if self.dual_tube_mode == "single":
            if self.calibration_overrides:
                return "customized"
            if self.detector_profile in PRESETS:
                return "predefined"
            return "documented" if self.calibration_reference.strip() else "working_values"
        low = self.effective_low_dose_tube()
        high = self.high_dose_tube
        if not low.dose_calibrated or high is None or not high.dose_calibrated:
            return "incomplete"
        if self.calibration_overrides:
            return "customized"
        if self.detector_profile in PRESETS:
            return "predefined"
        if low.calibration_reference.strip() and high.calibration_reference.strip():
            return "documented"
        return "working_values"

    def calibration_registry_values(self) -> dict[str, object]:
        return {
            "detector_profile": self.detector_profile,
            "calibration_overrides": self.calibration_overrides,
            "dual_tube_mode": self.dual_tube_mode,
            "dual_tube_switch_cpm": self.dual_tube_switch_cpm,
            "low_dose_tube_profile": self.effective_low_dose_tube().as_dict(),
            "high_dose_tube_profile": (
                self.high_dose_tube.as_dict() if self.high_dose_tube is not None else None
            ),
            "calibration_status": self.calibration_status(),
            "calibration_source": (
                "user" if self.calibration_overrides else
                (PRESETS[self.detector_profile].calibration_source if self.detector_profile in PRESETS else
                 ("documented" if self.calibration_reference.strip() else "unknown"))
            ),
            "warning_load_percent": (PRESETS[self.detector_profile].warning_load_percent if self.detector_profile in PRESETS else 5.0),
            "critical_load_percent": (PRESETS[self.detector_profile].critical_load_percent if self.detector_profile in PRESETS else 10.0),
            "invalid_load_percent": (PRESETS[self.detector_profile].invalid_load_percent if self.detector_profile in PRESETS else 25.0),
        }

    def validate(self) -> None:
        if not self.port.startswith("/dev/"):
            raise ValueError("Each device port must be a /dev device path")
        if self.baudrate not in SUPPORTED_BAUDRATES:
            raise ValueError(f"Unsupported baud rate for {self.port}: {self.baudrate}")
        if self.scan_interval < 5:
            raise ValueError(f"scan_interval for {self.port} must be at least 5 seconds")
        if not 0.2 <= self.command_timeout <= 10.0:
            raise ValueError(f"command_timeout for {self.port} must be between 0.2 and 10.0 seconds")
        if not 50 <= self.inter_command_delay_ms <= 2000:
            raise ValueError(f"inter_command_delay_ms for {self.port} must be between 50 and 2000")
        if self.serial_startup_delay is not None and not 0.0 <= self.serial_startup_delay <= 300.0:
            raise ValueError(f"serial_startup_delay for {self.port} must be between 0 and 300 seconds")
        if not 0 <= self.auxiliary_read_interval <= 86400:
            raise ValueError(f"auxiliary_read_interval for {self.port} must be between 0 and 86400 seconds")
        if not 1 <= self.high_cpm_threshold <= 65535:
            raise ValueError(f"high_cpm_threshold for {self.port} must be between 1 and 65535")
        if not 1 <= self.high_cpm_confirmations <= 10:
            raise ValueError(f"high_cpm_confirmations for {self.port} must be between 1 and 10")
        if not 10 <= self.device_clock_warning_seconds <= 86400:
            raise ValueError(
                f"device_clock_warning_seconds for {self.port} must be between 10 and 86400"
            )
        if not 16 <= self.serial_debug_max_bytes <= 1024:
            raise ValueError(f"serial_debug_max_bytes for {self.port} must be between 16 and 1024")
        if self.orientation_calibration_enabled:
            if not self.orientation_calibration_serial.strip():
                raise ValueError(
                    f"orientation_calibration_serial for {self.port} is required when calibration is enabled"
                )
            for axis, scale in (
                ("x", self.orientation_scale_x),
                ("y", self.orientation_scale_y),
                ("z", self.orientation_scale_z),
            ):
                if abs(scale) < 1e-9:
                    raise ValueError(
                        f"orientation_scale_{axis} for {self.port} must not be zero"
                    )
        if self.dead_time_us is not None and self.dead_time_us <= 0:
            raise ValueError(f"dead_time_us for {self.port} must be greater than zero")
        if self.reliable_max_cpm is not None and self.reliable_max_cpm <= 0:
            raise ValueError(f"reliable_max_cpm for {self.port} must be greater than zero")
        if self.dead_time_model not in {"none", "nonparalyzable"}:
            raise ValueError(f"dead_time_model for {self.port} must be none or nonparalyzable")
        if self.dead_time_model != "none" and self.dead_time_us is None:
            raise ValueError(f"dead_time_us for {self.port} is required for dead-time correction")
        for field_name, value in (("conversion_factor_uncertainty_percent", self.conversion_factor_uncertainty_percent), ("calibration_uncertainty_percent", self.calibration_uncertainty_percent)):
            if value is not None and value < 0:
                raise ValueError(f"{field_name} for {self.port} must not be negative")
        if self.dual_tube_mode not in {"single", "separate", "curve"}:
            raise ValueError(
                f"dual_tube_mode for {self.port} must be single, separate or curve"
            )
        if self.detector_profile not in SUPPORTED_PROFILE_IDS - {"auto"}:
            raise ValueError(f"Unsupported detector_profile for {self.port}: {self.detector_profile}")
        if self.detector_profile in {"gmc_300", "gmc_320_plus_v4", "gmc_600_plus"} and self.dual_tube_mode != "single":
            raise ValueError(
                f"Single-tube detector profile for {self.port} must use single-tube mode"
            )
        if self.dual_tube_switch_cpm is not None and self.dual_tube_switch_cpm <= 0:
            raise ValueError(f"dual_tube_switch_cpm for {self.port} must be greater than zero")
        if self.dual_tube_mode == "curve" and self.dual_tube_switch_cpm is None:
            raise ValueError(
                f"dual_tube_switch_cpm for {self.port} is required for curve mode"
            )
        self.effective_low_dose_tube().validate(f"low_dose_tube for {self.port}")
        if self.high_dose_tube is not None:
            self.high_dose_tube.validate(f"high_dose_tube for {self.port}")
        if self.cpm_per_usvh <= 0:
            raise ValueError(f"cpm_per_usvh for {self.port} must be greater than zero")
        if not 60 <= self.gmcmap_upload_interval <= 86400:
            raise ValueError(
                f"gmcmap_upload_interval for {self.port} must be between 60 and 86400 seconds"
            )
        if not 1.0 <= self.gmcmap_timeout <= 30.0:
            raise ValueError(f"gmcmap_timeout for {self.port} must be between 1 and 30 seconds")
        if self.gmcmap_counter_id:
            validate_identifier("gmcmap_counter_id", self.gmcmap_counter_id)


def apply_detected_detector_profile(config: DeviceConfig, model_or_version: str) -> DeviceConfig:
    """Apply a detected model preset when no explicit calibration override exists.

    Serial identity is more reliable than a user-entered name. Explicit custom values
    always win, while automatic/predefined configurations follow the detected device.
    """

    detected_id = detect_profile_id(model_or_version)
    if detected_id is None or config.calibration_overrides:
        return config
    preset = PRESETS[detected_id]
    high = None
    if preset.high_dose_tube_model:
        high = TubeCalibrationConfig(
            tube_model=preset.high_dose_tube_model,
            dead_time_us=preset.high_dose_dead_time_us,
            reliable_max_cpm=preset.high_dose_reliable_max_cpm,
            dead_time_model=(
                "nonparalyzable" if preset.high_dose_dead_time_us is not None else "none"
            ),
            calibration_reference=(
                "Automatic second-tube model detection; dose conversion is not calibrated."
            ),
        )
    return replace(
        config,
        detector_profile=detected_id,
        calibration_overrides=False,
        cpm_per_usvh=preset.cpm_per_usvh,
        dead_time_us=preset.dead_time_us,
        reliable_max_cpm=preset.reliable_max_cpm,
        dead_time_model=preset.dead_time_model,
        conversion_factor_uncertainty_percent=preset.conversion_factor_uncertainty_percent,
        calibration_uncertainty_percent=None,
        calibration_reference=preset.calibration_reference,
        tube_model=preset.tube_model,
        dual_tube_mode=preset.dual_tube_mode,
        dual_tube_switch_cpm=preset.dual_tube_switch_cpm,
        low_dose_tube=None,
        high_dose_tube=high,
    )


@dataclass(frozen=True)
class Settings:
    port: str
    baudrate: int
    scan_interval: int
    command_timeout: float
    inter_command_delay_ms: int
    high_cpm_threshold: int
    high_cpm_confirmations: int
    read_gyro: bool
    mqtt_host: str
    mqtt_port: int
    mqtt_username: str
    mqtt_password: str
    read_device_time: bool = True
    device_clock_warning_seconds: int = 120
    heartbeat_enabled: bool = False
    ports: tuple[str, ...] = ()
    devices: tuple[DeviceConfig, ...] = ()
    history_retention_days: int = 90
    report_timezone: str = "UTC"
    smart_alerts_enabled: bool = True
    rapid_rise_percent: float = 50.0
    rapid_rise_window_minutes: int = 10
    sustained_alert_minutes: int = 30
    baseline_learning_days: int = 7
    publish_advanced_sensors: bool = True
    ui_language: str = "en"
    cpm_per_usvh: float = 154.0
    gmcmap_enabled: bool = False
    gmcmap_privacy_confirmed: bool = False
    gmcmap_account_id: str = ""
    gmcmap_device_ids: tuple[tuple[str, str], ...] = ()
    gmcmap_upload_interval: int = 300
    gmcmap_timeout: float = 10.0
    external_temperature_entity: str = ""
    external_temperature_name: str = "Raumklima (Arbeitszimmer)"
    external_temperature_max_age_seconds: int = 900
    cosmic_hint_enabled: bool = True
    pressure_weather_entity_primary: str = "weather.forecast_home_2"
    pressure_weather_entity_secondary: str = "weather.forecast_balkon"
    pressure_weather_source_name: str = "Meteorologisk institutt (Met.no)"
    pressure_weather_max_age_seconds: int = 7200
    pressure_weather_max_difference_hpa: float = 5.0
    serial_scheduler_enabled: bool = True
    serial_scheduler_gap_seconds: float = 2.0

    @classmethod
    def from_env(cls) -> Settings:
        def required(name: str) -> str:
            value = os.environ.get(name, "")
            if not value:
                raise ValueError(f"Missing required environment variable: {name}")
            return value

        settings = cls(
            port=required("PORT"),
            ports=cls._parse_ports(os.environ.get("PORTS", ""), required("PORT")),
            baudrate=int(required("BAUDRATE")),
            scan_interval=int(required("SCAN_INTERVAL")),
            command_timeout=float(required("COMMAND_TIMEOUT")),
            inter_command_delay_ms=int(required("INTER_COMMAND_DELAY_MS")),
            high_cpm_threshold=int(required("HIGH_CPM_THRESHOLD")),
            high_cpm_confirmations=int(required("HIGH_CPM_CONFIRMATIONS")),
            read_gyro=parse_bool("READ_GYRO", required("READ_GYRO")),
            read_device_time=parse_bool("READ_DEVICE_TIME", os.environ.get("READ_DEVICE_TIME", "true")),
            device_clock_warning_seconds=int(os.environ.get("DEVICE_CLOCK_WARNING_SECONDS", "120")),
            heartbeat_enabled=parse_bool("HEARTBEAT_ENABLED", os.environ.get("HEARTBEAT_ENABLED", "false")),
            history_retention_days=int(required("HISTORY_RETENTION_DAYS")),
            report_timezone=required("REPORT_TIMEZONE"),
            mqtt_host=required("MQTT_HOST"),
            mqtt_port=int(required("MQTT_PORT")),
            mqtt_username=os.environ.get("MQTT_USERNAME", ""),
            mqtt_password=os.environ.get("MQTT_PASSWORD", ""),
            smart_alerts_enabled=parse_bool("SMART_ALERTS_ENABLED", os.environ.get("SMART_ALERTS_ENABLED", "true")),
            rapid_rise_percent=float(os.environ.get("RAPID_RISE_PERCENT", "50.0")),
            rapid_rise_window_minutes=int(os.environ.get("RAPID_RISE_WINDOW_MINUTES", "10")),
            sustained_alert_minutes=int(os.environ.get("SUSTAINED_ALERT_MINUTES", "30")),
            baseline_learning_days=int(os.environ.get("BASELINE_LEARNING_DAYS", "7")),
            publish_advanced_sensors=parse_bool(
                "PUBLISH_ADVANCED_SENSORS", os.environ.get("PUBLISH_ADVANCED_SENSORS", "true")
            ),
            ui_language=os.environ.get("UI_LANGUAGE", "en").strip().lower(),
            cpm_per_usvh=float(os.environ.get("CPM_PER_USVH", "154.0")),
            gmcmap_enabled=parse_bool("GMCMAP_ENABLED", os.environ.get("GMCMAP_ENABLED", "false")),
            gmcmap_privacy_confirmed=parse_bool(
                "GMCMAP_PRIVACY_CONFIRMED", os.environ.get("GMCMAP_PRIVACY_CONFIRMED", "false")
            ),
            gmcmap_account_id=os.environ.get("GMCMAP_ACCOUNT_ID", "").strip(),
            gmcmap_device_ids=parse_device_id_mappings(os.environ.get("GMCMAP_DEVICE_IDS", "")),
            gmcmap_upload_interval=int(os.environ.get("GMCMAP_UPLOAD_INTERVAL", "300")),
            gmcmap_timeout=float(os.environ.get("GMCMAP_TIMEOUT", "10.0")),
            external_temperature_entity=os.environ.get("EXTERNAL_TEMPERATURE_ENTITY", "").strip(),
            external_temperature_name=os.environ.get("EXTERNAL_TEMPERATURE_NAME", "Raumklima (Arbeitszimmer)").strip(),
            external_temperature_max_age_seconds=int(os.environ.get("EXTERNAL_TEMPERATURE_MAX_AGE_SECONDS", "900")),
            cosmic_hint_enabled=parse_bool("COSMIC_HINT_ENABLED", os.environ.get("COSMIC_HINT_ENABLED", "true")),
            pressure_weather_entity_primary=os.environ.get("PRESSURE_WEATHER_ENTITY_PRIMARY", "weather.forecast_home_2").strip(),
            pressure_weather_entity_secondary=os.environ.get("PRESSURE_WEATHER_ENTITY_SECONDARY", "weather.forecast_balkon").strip(),
            pressure_weather_source_name=os.environ.get("PRESSURE_WEATHER_SOURCE_NAME", "Meteorologisk institutt (Met.no)").strip(),
            pressure_weather_max_age_seconds=int(os.environ.get("PRESSURE_WEATHER_MAX_AGE_SECONDS", "7200")),
            pressure_weather_max_difference_hpa=float(os.environ.get("PRESSURE_WEATHER_MAX_DIFFERENCE_HPA", "5.0")),
            serial_scheduler_enabled=parse_bool("SERIAL_SCHEDULER_ENABLED", os.environ.get("SERIAL_SCHEDULER_ENABLED", "true")),
            serial_scheduler_gap_seconds=float(os.environ.get("SERIAL_SCHEDULER_GAP_SECONDS", "2.0")),
        )
        devices = cls._parse_devices_json(os.environ.get("DEVICES_JSON", ""), settings)
        settings = cls(**{**settings.__dict__, "devices": devices})
        settings.validate()
        return settings

    @staticmethod
    def _parse_ports(value: str, fallback: str) -> tuple[str, ...]:
        raw = value.replace("\n", ",").replace(";", ",")
        ports: list[str] = []
        for item in raw.split(","):
            port = item.strip()
            if port and port not in ports:
                ports.append(port)
        if not ports:
            ports.append(fallback.strip())
        return tuple(ports)

    @staticmethod
    def _parse_devices_json(value: str, defaults: Settings) -> tuple[DeviceConfig, ...]:
        if not value.strip() or value.strip() in {"null", "[]"}:
            return ()
        try:
            raw = json.loads(value)
        except json.JSONDecodeError as exc:
            raise ValueError("DEVICES_JSON must be a JSON array") from exc
        if not isinstance(raw, list):
            raise ValueError("DEVICES_JSON must contain a list")
        allowed = {
            "port", "name", "baudrate", "scan_interval", "command_timeout",
            "inter_command_delay_ms", "serial_startup_delay", "auxiliary_read_interval",
            "read_gyro", "read_device_time", "device_clock_warning_seconds",
            "heartbeat_enabled", "detector_profile", "cpm_per_usvh", "dead_time_us", "reliable_max_cpm",
            "dead_time_model", "conversion_factor_uncertainty_percent",
            "calibration_uncertainty_percent", "calibration_reference", "tube_model",
            "dual_tube_mode", "dual_tube_switch_cpm", "low_dose_tube", "high_dose_tube",
            "low_dose_tube_model", "low_dose_cpm_per_usvh", "low_dose_dead_time_us",
            "low_dose_reliable_max_cpm", "low_dose_dead_time_model",
            "low_dose_conversion_factor_uncertainty_percent",
            "low_dose_calibration_uncertainty_percent", "low_dose_calibration_reference",
            "high_dose_tube_model", "high_dose_cpm_per_usvh", "high_dose_dead_time_us",
            "high_dose_reliable_max_cpm", "high_dose_dead_time_model",
            "high_dose_conversion_factor_uncertainty_percent",
            "high_dose_calibration_uncertainty_percent", "high_dose_calibration_reference",
            "gmcmap_counter_id",
            "gmcmap_upload_interval", "gmcmap_timeout", "serial_debug", "serial_debug_max_bytes",
            "orientation_calibration_enabled", "orientation_calibration_serial",
            "orientation_offset_x", "orientation_offset_y", "orientation_offset_z",
            "orientation_scale_x", "orientation_scale_y", "orientation_scale_z",
            "orientation_calibration_name",
        }
        deprecated_fields = {
            "firmware_reference_version", "firmware_information_url",
            "high_cpm_threshold", "high_cpm_confirmations",
        }
        devices: list[DeviceConfig] = []
        for index, item in enumerate(raw):
            if not isinstance(item, dict):
                raise ValueError(f"devices[{index}] must be an object")
            unknown = sorted(set(item) - allowed - deprecated_fields)
            if unknown:
                raise ValueError(f"devices[{index}] contains unknown fields: {', '.join(unknown)}")
            port = str(item.get("port", "")).strip()
            if not port:
                raise ValueError(f"devices[{index}].port is required")
            configured_name = str(item.get("name", "")).strip()
            configured_tube_model = str(item.get("tube_model", "")).strip()
            configured_dual_mode = str(item.get("dual_tube_mode", "single")).strip().lower()
            resolved_profile_id, preset = resolve_preset(
                str(item.get("detector_profile", "auto")),
                name=configured_name,
                tube_model=configured_tube_model,
                dual_tube_mode=configured_dual_mode,
            )

            # The primary fields represent the only tube on single-tube models
            # and the low-dose tube on dual-tube models. 8.3.4 low_dose_* values
            # are accepted as a migration source but are no longer duplicated in
            # the Supervisor form.
            migrated_low = (
                _parse_tube_calibration(
                    f"devices[{index}].low_dose_tube", item.get("low_dose_tube")
                )
                or _parse_flat_tube_calibration(
                    f"devices[{index}].low_dose", item, "low_dose"
                )
            )

            def primary_value(
                key: str,
                preset_value: object,
                fallback: object,
                *,
                source: dict[str, object] = item,
                migrated_profile: TubeCalibrationConfig | None = migrated_low,
                use_preset: bool = preset is not None,
            ) -> object:
                if key in source and source.get(key) not in (None, ""):
                    return source[key]
                if migrated_profile is not None:
                    migrated = getattr(migrated_profile, key, None)
                    if migrated not in (None, ""):
                        return migrated
                return preset_value if use_preset else fallback

            preset_tube_model = preset.tube_model if preset is not None else ""
            if (
                preset is not None
                and not item.get("detector_profile")
                and resolved_profile_id == "gmc_500_plus"
                and "SI-3BG" in configured_tube_model.upper()
            ):
                # Migrate the old combined label into two physical tube profiles.
                configured_tube_model = ""

            effective_tube_model = str(
                configured_tube_model
                or (migrated_low.tube_model if migrated_low is not None else "")
                or preset_tube_model
            ).strip()
            effective_cpm_per_usvh = float(
                primary_value(
                    "cpm_per_usvh",
                    preset.cpm_per_usvh if preset is not None else None,
                    defaults.cpm_per_usvh,
                )
            )
            effective_dead_time_us = _optional_float(
                primary_value(
                    "dead_time_us",
                    preset.dead_time_us if preset is not None else None,
                    None,
                )
            )
            effective_reliable_max_cpm = _optional_int(
                primary_value(
                    "reliable_max_cpm",
                    preset.reliable_max_cpm if preset is not None else None,
                    None,
                )
            )
            effective_dead_time_model = str(
                primary_value(
                    "dead_time_model",
                    preset.dead_time_model if preset is not None else "none",
                    "none",
                )
            ).strip().lower()
            effective_factor_uncertainty = _optional_float(
                primary_value(
                    "conversion_factor_uncertainty_percent",
                    (
                        preset.conversion_factor_uncertainty_percent
                        if preset is not None
                        else None
                    ),
                    None,
                )
            )
            effective_calibration_uncertainty = _optional_float(
                primary_value("calibration_uncertainty_percent", None, None)
            )
            effective_reference = str(
                primary_value(
                    "calibration_reference",
                    preset.calibration_reference if preset is not None else "",
                    "",
                )
            ).strip()
            effective_dual_mode = str(
                item.get(
                    "dual_tube_mode",
                    preset.dual_tube_mode if preset is not None else "single",
                )
            ).strip().lower()
            effective_switch_cpm = _optional_int(
                item.get(
                    "dual_tube_switch_cpm",
                    preset.dual_tube_switch_cpm if preset is not None else None,
                )
            )

            explicit_high = (
                _parse_tube_calibration(
                    f"devices[{index}].high_dose_tube", item.get("high_dose_tube")
                )
                or _parse_flat_tube_calibration(
                    f"devices[{index}].high_dose", item, "high_dose"
                )
            )
            effective_high = explicit_high
            if effective_high is None and preset is not None and preset.high_dose_tube_model:
                effective_high = TubeCalibrationConfig(
                    tube_model=preset.high_dose_tube_model
                )

            if resolved_profile_id in {"gmc_300", "gmc_320_plus_v4", "gmc_600_plus"}:
                # A GMC-320 has one M4011 tube. Stale dual-tube fields from the
                # 8.3.4 form are deliberately ignored instead of becoming a
                # second detector profile.
                effective_dual_mode = "single"
                effective_switch_cpm = None
                effective_high = None

            calibration_overrides = False
            if preset is not None:
                comparable = {
                    "tube_model": effective_tube_model,
                    "cpm_per_usvh": effective_cpm_per_usvh,
                    "dead_time_us": effective_dead_time_us,
                    "reliable_max_cpm": effective_reliable_max_cpm,
                    "dead_time_model": effective_dead_time_model,
                    "conversion_factor_uncertainty_percent": effective_factor_uncertainty,
                    "dual_tube_mode": effective_dual_mode,
                    "dual_tube_switch_cpm": effective_switch_cpm,
                }
                expected = {
                    "tube_model": preset.tube_model,
                    "cpm_per_usvh": preset.cpm_per_usvh,
                    "dead_time_us": preset.dead_time_us,
                    "reliable_max_cpm": preset.reliable_max_cpm,
                    "dead_time_model": preset.dead_time_model,
                    "conversion_factor_uncertainty_percent": preset.conversion_factor_uncertainty_percent,
                    "dual_tube_mode": preset.dual_tube_mode,
                    "dual_tube_switch_cpm": preset.dual_tube_switch_cpm,
                }
                calibration_overrides = comparable != expected
                if explicit_high is not None:
                    calibration_overrides = True
                if not calibration_overrides and not item.get("detector_profile"):
                    # Clean migration of old matching working values to the new
                    # predefined profile, including its unambiguous reference.
                    effective_reference = preset.calibration_reference
                    effective_calibration_uncertainty = None
            else:
                calibration_overrides = any(
                    key in item
                    for key in (
                        "cpm_per_usvh",
                        "dead_time_us",
                        "reliable_max_cpm",
                        "dead_time_model",
                        "conversion_factor_uncertainty_percent",
                        "calibration_uncertainty_percent",
                        "calibration_reference",
                        "tube_model",
                        "dual_tube_mode",
                        "dual_tube_switch_cpm",
                    )
                ) or migrated_low is not None or explicit_high is not None
            device = DeviceConfig(
                port=port,
                name=configured_name,
                baudrate=int(item.get("baudrate", defaults.baudrate)),
                scan_interval=int(item.get("scan_interval", defaults.scan_interval)),
                command_timeout=float(item.get("command_timeout", defaults.command_timeout)),
                inter_command_delay_ms=int(
                    item.get("inter_command_delay_ms", defaults.inter_command_delay_ms)
                ),
                serial_startup_delay=(
                    None if item.get("serial_startup_delay") is None
                    else float(item["serial_startup_delay"])
                ),
                auxiliary_read_interval=int(item.get("auxiliary_read_interval", 300)),
                high_cpm_threshold=HIGH_CPM_THRESHOLD,
                high_cpm_confirmations=HIGH_CPM_CONFIRMATIONS,
                read_gyro=_mapping_bool(
                    f"devices[{index}].read_gyro", item.get("read_gyro"), defaults.read_gyro
                ),
                read_device_time=_mapping_bool(
                    f"devices[{index}].read_device_time",
                    item.get("read_device_time"),
                    defaults.read_device_time,
                ),
                device_clock_warning_seconds=int(
                    item.get("device_clock_warning_seconds", defaults.device_clock_warning_seconds)
                ),
                heartbeat_enabled=_mapping_bool(
                    f"devices[{index}].heartbeat_enabled",
                    item.get("heartbeat_enabled"),
                    defaults.heartbeat_enabled,
                ),
                detector_profile=resolved_profile_id,
                calibration_overrides=calibration_overrides,
                cpm_per_usvh=effective_cpm_per_usvh,
                dead_time_us=effective_dead_time_us,
                reliable_max_cpm=effective_reliable_max_cpm,
                dead_time_model=effective_dead_time_model,
                conversion_factor_uncertainty_percent=effective_factor_uncertainty,
                calibration_uncertainty_percent=effective_calibration_uncertainty,
                calibration_reference=effective_reference,
                tube_model=effective_tube_model,
                dual_tube_mode=effective_dual_mode,
                dual_tube_switch_cpm=effective_switch_cpm,
                low_dose_tube=None,
                high_dose_tube=effective_high,
                gmcmap_counter_id=str(item.get("gmcmap_counter_id", "")).strip(),
                gmcmap_upload_interval=int(
                    item.get("gmcmap_upload_interval", defaults.gmcmap_upload_interval)
                ),
                gmcmap_timeout=float(item.get("gmcmap_timeout", defaults.gmcmap_timeout)),
                serial_debug=_mapping_bool(f"devices[{index}].serial_debug", item.get("serial_debug"), False),
                serial_debug_max_bytes=int(item.get("serial_debug_max_bytes", 64)),
                orientation_calibration_enabled=_mapping_bool(
                    f"devices[{index}].orientation_calibration_enabled",
                    item.get("orientation_calibration_enabled"),
                    False,
                ),
                orientation_calibration_serial=str(
                    item.get("orientation_calibration_serial", "")
                ).strip().lower(),
                orientation_offset_x=float(item.get("orientation_offset_x", 0.0)),
                orientation_offset_y=float(item.get("orientation_offset_y", 0.0)),
                orientation_offset_z=float(item.get("orientation_offset_z", 0.0)),
                orientation_scale_x=float(item.get("orientation_scale_x", 1.0)),
                orientation_scale_y=float(item.get("orientation_scale_y", 1.0)),
                orientation_scale_z=float(item.get("orientation_scale_z", 1.0)),
                orientation_calibration_name=str(
                    item.get("orientation_calibration_name", "Custom six-position calibration")
                ).strip() or "Custom six-position calibration",
            )
            device.validate()
            devices.append(device)
        ports = [device.port for device in devices]
        if len(ports) != len(set(ports)):
            raise ValueError("Each devices entry must use a unique port")
        names = [device.name.casefold() for device in devices if device.name]
        if len(names) != len(set(names)):
            raise ValueError("Configured device names must be unique")
        calibration_serials = [
            device.orientation_calibration_serial.casefold()
            for device in devices
            if device.orientation_calibration_serial
        ]
        if len(calibration_serials) != len(set(calibration_serials)):
            raise ValueError("Orientation calibration serials must be unique")
        return tuple(devices)

    def effective_devices(self) -> tuple[DeviceConfig, ...]:
        if self.devices:
            return self.devices
        return tuple(
            DeviceConfig(
                port=port,
                baudrate=self.baudrate,
                scan_interval=self.scan_interval,
                command_timeout=self.command_timeout,
                inter_command_delay_ms=self.inter_command_delay_ms,
                high_cpm_threshold=self.high_cpm_threshold,
                high_cpm_confirmations=self.high_cpm_confirmations,
                read_gyro=self.read_gyro,
                read_device_time=self.read_device_time,
                device_clock_warning_seconds=self.device_clock_warning_seconds,
                heartbeat_enabled=self.heartbeat_enabled,
                cpm_per_usvh=self.cpm_per_usvh,
                gmcmap_upload_interval=self.gmcmap_upload_interval,
                gmcmap_timeout=self.gmcmap_timeout,
                serial_debug=False,
                serial_debug_max_bytes=64,
            )
            for port in (self.ports or (self.port,))
        )

    def validate(self) -> None:
        effective_devices = self.effective_devices()
        if not effective_devices:
            raise ValueError("At least one GMC device must be configured")
        for device in effective_devices:
            device.validate()
        if not 7 <= self.history_retention_days <= 3650:
            raise ValueError("HISTORY_RETENTION_DAYS must be between 7 and 3650")
        try:
            ZoneInfo(self.report_timezone)
        except ZoneInfoNotFoundError as exc:
            raise ValueError(f"Unknown REPORT_TIMEZONE: {self.report_timezone}") from exc
        if self.rapid_rise_percent < 1:
            raise ValueError("RAPID_RISE_PERCENT must be at least 1")
        if not 1 <= self.rapid_rise_window_minutes <= 1440:
            raise ValueError("RAPID_RISE_WINDOW_MINUTES must be between 1 and 1440")
        if not 1 <= self.sustained_alert_minutes <= 1440:
            raise ValueError("SUSTAINED_ALERT_MINUTES must be between 1 and 1440")
        if not 1 <= self.baseline_learning_days <= 90:
            raise ValueError("BASELINE_LEARNING_DAYS must be between 1 and 90")
        if self.ui_language not in {"auto", "en", "de", "fr", "es", "it", "nl", "pl", "hr"}:
            raise ValueError("UI_LANGUAGE is unsupported")
        if not 1 <= self.mqtt_port <= 65535:
            raise ValueError("MQTT_PORT must be between 1 and 65535")
        if not 60 <= self.gmcmap_upload_interval <= 86400:
            raise ValueError("GMCMAP_UPLOAD_INTERVAL must be between 60 and 86400 seconds")
        if not 1.0 <= self.gmcmap_timeout <= 30.0:
            raise ValueError("GMCMAP_TIMEOUT must be between 1 and 30 seconds")
        if not 0.0 <= self.serial_scheduler_gap_seconds <= 30.0:
            raise ValueError("SERIAL_SCHEDULER_GAP_SECONDS must be between 0 and 30 seconds")
        if self.external_temperature_entity and not self.external_temperature_entity.startswith("sensor."):
            raise ValueError("EXTERNAL_TEMPERATURE_ENTITY must be a sensor entity ID")
        if not 30 <= self.external_temperature_max_age_seconds <= 86400:
            raise ValueError("EXTERNAL_TEMPERATURE_MAX_AGE_SECONDS must be between 30 and 86400 seconds")
        for name, entity_id in (
            ("PRESSURE_WEATHER_ENTITY_PRIMARY", self.pressure_weather_entity_primary),
            ("PRESSURE_WEATHER_ENTITY_SECONDARY", self.pressure_weather_entity_secondary),
        ):
            if entity_id and not entity_id.startswith("weather."):
                raise ValueError(f"{name} must be a weather entity ID")
        if not 60 <= self.pressure_weather_max_age_seconds <= 86400:
            raise ValueError("PRESSURE_WEATHER_MAX_AGE_SECONDS must be between 60 and 86400 seconds")
        if not 0.1 <= self.pressure_weather_max_difference_hpa <= 20.0:
            raise ValueError("PRESSURE_WEATHER_MAX_DIFFERENCE_HPA must be between 0.1 and 20 hPa")
        if self.cosmic_hint_enabled and not (self.pressure_weather_entity_primary or self.pressure_weather_entity_secondary):
            raise ValueError("At least one pressure weather entity is required when the cosmic hint is enabled")
        per_device_counter_ids = [
            device.gmcmap_counter_id for device in effective_devices if device.gmcmap_counter_id
        ]
        if len(per_device_counter_ids) != len(set(per_device_counter_ids)):
            raise ValueError("Each configured GMCMap counter ID must be unique")
        if self.gmcmap_enabled:
            if not self.gmcmap_privacy_confirmed:
                raise ValueError("GMCMAP_PRIVACY_CONFIRMED must be true when GMCMap uploads are enabled")
            if not self.gmcmap_account_id:
                raise ValueError("GMCMAP_ACCOUNT_ID is required when GMCMap uploads are enabled")
            validate_identifier("GMCMAP_ACCOUNT_ID", self.gmcmap_account_id)
            has_per_device_id = any(device.gmcmap_counter_id for device in effective_devices)
            if not self.gmcmap_device_ids and not has_per_device_id:
                raise ValueError(
                    "A gmcmap_counter_id per device or GMCMAP_DEVICE_IDS is required when GMCMap uploads are enabled"
                )
