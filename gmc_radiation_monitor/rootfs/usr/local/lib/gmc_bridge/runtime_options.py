from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .options_migration import merge_single_and_dual_device_options


class OptionsError(ValueError):
    pass


def _mapping(value: object, name: str) -> dict[str, Any]:
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise OptionsError(f"{name} must be an object")
    return value


def _devices(options: dict[str, Any]) -> list[dict[str, Any]]:
    normalized, _changed = merge_single_and_dual_device_options(options)
    single_value = normalized.get("devices", [])
    dual_value = normalized.get("dual_tube_devices", [])
    if not isinstance(single_value, list):
        raise OptionsError("devices must be a list")
    if not isinstance(dual_value, list):
        raise OptionsError("dual_tube_devices must be a list")

    devices: list[dict[str, Any]] = []
    for group_name, values in (("devices", single_value), ("dual_tube_devices", dual_value)):
        for index, item in enumerate(values):
            if not isinstance(item, dict):
                raise OptionsError(f"{group_name}[{index}] must be an object")
            device = dict(item)
            name = str(device.get("name") or "").strip()
            if group_name == "dual_tube_devices":
                if not name:
                    raise OptionsError(f"dual_tube_devices[{index}].name is required")
                serial = str(device.pop("device_serial", "") or "").strip().lower()
                if serial:
                    device["expected_serial"] = serial
                mode = str(device.get("dual_tube_mode") or "").strip().lower()
                if mode not in {"separate", "curve"}:
                    raise OptionsError(
                        f"dual_tube_devices[{index}].dual_tube_mode must be separate or curve"
                    )
            devices.append(device)

    names = [str(item.get("name") or "").strip().casefold() for item in devices]
    named = [name for name in names if name]
    if len(named) != len(set(named)):
        raise OptionsError("Configured device names must be unique across single- and dual-tube devices")
    return devices


def load_options(path: str | Path = "/data/options.json") -> dict[str, Any]:
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise OptionsError(f"Missing Home Assistant options file: {source}") from exc
    except json.JSONDecodeError as exc:
        raise OptionsError(f"Invalid JSON in Home Assistant options file: {exc}") from exc
    if not isinstance(payload, dict):
        raise OptionsError("Home Assistant options must be a JSON object")
    return payload


def _text(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if value is None:
        return ""
    return str(value)


def _value(mapping: dict[str, Any], key: str, default: object) -> str:
    return _text(mapping.get(key, default))


def runtime_environment(options: dict[str, Any], service: str) -> dict[str, str]:
    service_name = str(service or "").strip().lower()
    if service_name not in {"bridge", "reports"}:
        raise OptionsError("service must be bridge or reports")

    devices = _devices(options)
    first = devices[0] if devices else {}
    history = _mapping(options.get("history"), "history")
    analysis = _mapping(options.get("analysis"), "analysis")
    safety = _mapping(options.get("safety"), "safety")
    interface = _mapping(options.get("interface"), "interface")
    system = _mapping(options.get("system"), "system")
    gmcmap = _mapping(options.get("gmcmap"), "gmcmap")

    common = {
        "DEVICES_JSON": json.dumps(devices, separators=(",", ":"), ensure_ascii=False),
        "SCAN_INTERVAL": _value(first, "scan_interval", 60),
        "CPM_PER_USVH": _value(first, "cpm_per_usvh", 154.0),
        "READ_GYRO": _text(any(bool(item.get("read_gyro", False)) for item in devices)),
        "HISTORY_RETENTION_DAYS": _value(history, "retention_days", 90),
        "REPORT_TIMEZONE": _value(history, "report_timezone", "Europe/Berlin"),
        "LOG_LEVEL": _value(system, "log_level", "info"),
        "UI_LANGUAGE": _value(interface, "ui_language", "auto"),
        "COSMIC_HINT_ENABLED": _value(analysis, "cosmic_hint_enabled", True),
        "PRESSURE_WEATHER_ENTITY_PRIMARY": _value(
            analysis, "pressure_weather_entity_primary", "weather.forecast_home_2"
        ),
        "PRESSURE_WEATHER_ENTITY_SECONDARY": _value(
            analysis, "pressure_weather_entity_secondary", "weather.forecast_balkon"
        ),
        "PRESSURE_WEATHER_SOURCE_NAME": _value(
            analysis, "pressure_weather_source_name", "Meteorologisk institutt (Met.no)"
        ),
        "PRESSURE_WEATHER_MAX_AGE_SECONDS": _value(
            analysis, "pressure_weather_max_age_seconds", 7200
        ),
        "PRESSURE_WEATHER_MAX_DIFFERENCE_HPA": _value(
            analysis, "pressure_weather_max_difference_hpa", 5.0
        ),
    }

    if service_name == "reports":
        legacy_history_management = bool(history.get("enable_restore", False)) or bool(
            history.get("enable_purge_all_history", False)
        )
        history_management_enabled = _value(
            history, "history_management_enabled", legacy_history_management
        )
        return {
            **common,
            "HISTORY_MANAGEMENT_ENABLED": history_management_enabled,
            # Backwards-compatible internal aliases; only one switch is exposed in Home Assistant.
            "ENABLE_RESTORE": history_management_enabled,
            "ENABLE_PURGE_ALL_HISTORY": history_management_enabled,
            "TRAFFIC_LIGHT_YELLOW_PERCENT": _value(
                analysis, "traffic_light_yellow_percent", 125.0
            ),
            "TRAFFIC_LIGHT_RED_PERCENT": _value(
                analysis, "traffic_light_red_percent", 175.0
            ),
            "SAFETY_PROFILE": _value(safety, "profile", "gq"),
            "SAFETY_THRESHOLD_BASIS": _value(safety, "threshold_basis", "either"),
            "SAFETY_WARNING_CPM": _value(safety, "warning_cpm", 51),
            "SAFETY_DANGER_CPM": _value(safety, "danger_cpm", 100),
            "SAFETY_WARNING_USVH": _value(safety, "warning_usvh", 0.326),
            "SAFETY_DANGER_USVH": _value(safety, "danger_usvh", 0.651),
            "UI_MODE": _value(interface, "ui_mode", "simple"),
            "MAIN_VALUE_SIZE": _value(interface, "main_value_size", "large"),
            "CUSTOM_VALUE_FONT_SIZE_PX": _value(interface, "custom_value_font_size_px", 36),
            # Internal safety limits are intentionally not user-configurable.
            "HTTP_MAX_WORKERS": "12",
            "HTTP_SOCKET_TIMEOUT_SECONDS": "30",
        }

    return {
        **common,
        "COMMAND_TIMEOUT": _value(first, "command_timeout", 2.0),
        "INTER_COMMAND_DELAY_MS": _value(first, "inter_command_delay_ms", 150),
        "HIGH_CPM_THRESHOLD": "10000",
        "HIGH_CPM_CONFIRMATIONS": "3",
        "READ_DEVICE_TIME": _value(first, "read_device_time", True),
        "DEVICE_CLOCK_WARNING_SECONDS": _value(first, "device_clock_warning_seconds", 120),
        "HEARTBEAT_ENABLED": _value(first, "heartbeat_enabled", False),
        "GMCMAP_ENABLED": _value(gmcmap, "enabled", False),
        "GMCMAP_PRIVACY_CONFIRMED": _value(gmcmap, "privacy_confirmed", False),
        "GMCMAP_ACCOUNT_ID": _value(gmcmap, "account_id", ""),
        "GMCMAP_DEVICE_IDS": "",
        "GMCMAP_UPLOAD_INTERVAL": _value(gmcmap, "upload_interval", 300),
        "GMCMAP_TIMEOUT": _value(gmcmap, "timeout", 10.0),
        "SMART_ALERTS_ENABLED": _value(analysis, "smart_alerts_enabled", True),
        "RAPID_RISE_PERCENT": _value(analysis, "rapid_rise_percent", 50.0),
        "RAPID_RISE_WINDOW_MINUTES": _value(analysis, "rapid_rise_window_minutes", 10),
        "SUSTAINED_ALERT_MINUTES": _value(analysis, "sustained_alert_minutes", 30),
        "BASELINE_LEARNING_DAYS": _value(analysis, "baseline_learning_days", 7),
        "EXTERNAL_TEMPERATURE_ENTITY": _value(
            analysis, "external_temperature_entity", ""
        ),
        "EXTERNAL_TEMPERATURE_NAME": _value(
            analysis, "external_temperature_name", "Raumklima (Arbeitszimmer)"
        ),
        "EXTERNAL_TEMPERATURE_MAX_AGE_SECONDS": _value(
            analysis, "external_temperature_max_age_seconds", 900
        ),
        "PUBLISH_ADVANCED_SENSORS": _value(
            interface, "publish_advanced_sensors", True
        ),
        "SERIAL_SCHEDULER_ENABLED": _value(system, "serial_scheduler_enabled", True),
        "SERIAL_SCHEDULER_GAP_SECONDS": _value(
            system, "serial_scheduler_gap_seconds", 2.0
        ),
    }
