from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .health_settings import (
    DEFAULT_BRIDGE_HEARTBEAT_INTERVAL_SECONDS,
    DEFAULT_HEALTH_BRIDGE_ERROR_SECONDS,
    DEFAULT_HEALTH_BRIDGE_WARNING_SECONDS,
    DEFAULT_HEALTH_MEASUREMENT_ERROR_SECONDS,
    DEFAULT_HEALTH_MEASUREMENT_WARNING_SECONDS,
    DEFAULT_HEALTH_STARTUP_GRACE_SECONDS,
)
from .options_migration import merge_single_and_dual_device_options

Severity = Literal["warning", "error"]
KNOWN_GROUPS = {
    "devices",
    "dual_tube_devices",
    "gmcmap",
    "history",
    "analysis",
    "safety",
    "interface",
    "system",
}
OBJECT_GROUPS = {"gmcmap", "history", "analysis", "safety", "interface", "system"}


@dataclass(frozen=True, slots=True)
class ValidationIssue:
    code: str
    severity: Severity
    message: str
    path: str = ""

    def as_dict(self) -> dict[str, str]:
        return {
            "code": self.code,
            "severity": self.severity,
            "message": self.message,
            "path": self.path,
        }


@dataclass(frozen=True, slots=True)
class ValidationResult:
    issues: tuple[ValidationIssue, ...]

    @property
    def errors(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "error")

    @property
    def warnings(self) -> tuple[ValidationIssue, ...]:
        return tuple(issue for issue in self.issues if issue.severity == "warning")

    @property
    def valid(self) -> bool:
        return not self.errors

    @property
    def clean(self) -> bool:
        return not self.issues

    @property
    def status(self) -> str:
        return "error" if self.errors else "warning" if self.warnings else "ok"

    def messages(self) -> list[str]:
        return [issue.message for issue in self.issues]

    def as_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "clean": self.clean,
            "status": self.status,
            "errors": [issue.message for issue in self.errors],
            "warnings": [issue.message for issue in self.warnings],
            "issues": [issue.as_dict() for issue in self.issues],
        }


class ConfigurationValidationError(ValueError):
    def __init__(self, result: ValidationResult) -> None:
        self.result = result
        super().__init__("; ".join(issue.message for issue in result.errors))


def _issue(
    issues: list[ValidationIssue],
    code: str,
    severity: Severity,
    message: str,
    path: str = "",
) -> None:
    issues.append(ValidationIssue(code=code, severity=severity, message=message, path=path))


def validate_options(payload: object) -> ValidationResult:
    issues: list[ValidationIssue] = []
    if not isinstance(payload, dict):
        _issue(
            issues,
            "configuration_not_object",
            "error",
            "Configuration must be a JSON object",
        )
        return ValidationResult(tuple(issues))

    unknown = sorted(set(payload) - KNOWN_GROUPS)
    if unknown:
        _issue(
            issues,
            "unknown_top_level_groups",
            "warning",
            "Unknown top-level groups: " + ", ".join(unknown),
        )

    for group in sorted(OBJECT_GROUPS):
        value = payload.get(group, {})
        if value is not None and not isinstance(value, dict):
            _issue(issues, "group_not_object", "error", f"{group} must be an object", group)

    devices_raw = payload.get("devices", [])
    dual_devices_raw = payload.get("dual_tube_devices", [])
    devices: list[object]
    dual_devices: list[object]
    if devices_raw in (None, []):
        devices = []
    elif isinstance(devices_raw, list):
        devices = devices_raw
    else:
        devices = []
        _issue(issues, "devices_not_list", "error", "devices must be a list", "devices")
    if dual_devices_raw in (None, []):
        dual_devices = []
    elif isinstance(dual_devices_raw, list):
        dual_devices = dual_devices_raw
    else:
        dual_devices = []
        _issue(
            issues,
            "dual_devices_not_list",
            "error",
            "dual_tube_devices must be a list",
            "dual_tube_devices",
        )

    if not devices and not dual_devices:
        _issue(
            issues,
            "no_devices",
            "error",
            "At least one device configuration is required across devices and dual_tube_devices",
        )

    names: dict[str, str] = {}
    device_ordinal = 0

    def validate_common_device(group: str, index: int, item: object) -> dict[str, Any] | None:
        nonlocal device_ordinal
        path = f"{group}[{index}]"
        if not isinstance(item, dict):
            _issue(issues, "device_not_object", "error", f"{path} must be an object", path)
            return None
        name = str(item.get("name") or "").strip()
        folded = name.casefold()
        if not name:
            _issue(issues, "device_name_missing", "error", f"{path}.name is required", f"{path}.name")
        elif folded in names:
            _issue(
                issues,
                "duplicate_device_name",
                "error",
                f"Duplicate device name across devices and dual_tube_devices: {name} "
                f"(already used by {names[folded]})",
                f"{path}.name",
            )
        else:
            names[folded] = path
        try:
            if int(item.get("scan_interval", 60)) < 5:
                _issue(
                    issues,
                    "scan_interval_too_short",
                    "error",
                    f"{path}.scan_interval must be at least 5 seconds",
                    f"{path}.scan_interval",
                )
        except (TypeError, ValueError):
            _issue(
                issues,
                "scan_interval_not_numeric",
                "error",
                f"{path}.scan_interval must be numeric",
                f"{path}.scan_interval",
            )
        try:
            default_delay = 0 if device_ordinal == 0 else 15
            delay = float(item.get("serial_startup_delay", default_delay))
            if device_ordinal > 0 and delay < 15:
                _issue(
                    issues,
                    "serial_startup_delay_short",
                    "warning",
                    f"{path}.serial_startup_delay should be at least 15 seconds",
                    f"{path}.serial_startup_delay",
                )
        except (TypeError, ValueError):
            _issue(
                issues,
                "serial_startup_delay_not_numeric",
                "error",
                f"{path}.serial_startup_delay must be numeric",
                f"{path}.serial_startup_delay",
            )
        device_ordinal += 1
        return item

    for index, item in enumerate(devices):
        validate_common_device("devices", index, item)

    for index, item in enumerate(dual_devices):
        validated = validate_common_device("dual_tube_devices", index, item)
        if validated is None:
            continue
        path = f"dual_tube_devices[{index}]"
        mode = str(validated.get("dual_tube_mode") or "separate").strip().lower()
        if mode not in {"separate", "curve"}:
            _issue(
                issues,
                "dual_tube_mode_invalid",
                "error",
                f"{path}.dual_tube_mode must be separate or curve",
                f"{path}.dual_tube_mode",
            )
        try:
            switch = validated.get("dual_tube_switch_cpm")
            if switch not in (None, "") and int(switch) <= 0:
                _issue(
                    issues,
                    "dual_tube_switch_not_positive",
                    "error",
                    f"{path}.dual_tube_switch_cpm must be greater than zero",
                    f"{path}.dual_tube_switch_cpm",
                )
        except (TypeError, ValueError):
            _issue(
                issues,
                "dual_tube_switch_not_numeric",
                "error",
                f"{path}.dual_tube_switch_cpm must be numeric",
                f"{path}.dual_tube_switch_cpm",
            )

    history = payload.get("history", {})
    if isinstance(history, dict):
        try:
            retention = int(history.get("retention_days", 90))
            if not 7 <= retention <= 3650:
                _issue(
                    issues,
                    "retention_out_of_range",
                    "error",
                    "history.retention_days must be between 7 and 3650",
                    "history.retention_days",
                )
        except (TypeError, ValueError):
            _issue(
                issues,
                "retention_not_numeric",
                "error",
                "history.retention_days must be numeric",
                "history.retention_days",
            )
        timezone_name = str(history.get("report_timezone", "UTC"))
        try:
            ZoneInfo(timezone_name)
        except ZoneInfoNotFoundError:
            _issue(
                issues,
                "timezone_unknown",
                "error",
                f"Unknown timezone: {timezone_name}",
                "history.report_timezone",
            )

    analysis = payload.get("analysis", {})
    if isinstance(analysis, dict):
        try:
            yellow = float(analysis.get("traffic_light_yellow_percent", 125.0))
            red = float(analysis.get("traffic_light_red_percent", 175.0))
            if yellow < 100 or red <= yellow:
                _issue(
                    issues,
                    "analysis_threshold_order",
                    "error",
                    "Analysis red threshold must be greater than the yellow threshold and yellow must be at least 100",
                    "analysis",
                )
        except (TypeError, ValueError):
            _issue(
                issues,
                "analysis_threshold_not_numeric",
                "error",
                "Analysis thresholds must be numeric",
                "analysis",
            )

    safety = payload.get("safety", {})
    if isinstance(safety, dict):
        try:
            warning_cpm = float(safety.get("warning_cpm", 51))
            danger_cpm = float(safety.get("danger_cpm", 100))
            if danger_cpm <= warning_cpm:
                _issue(
                    issues,
                    "safety_cpm_order",
                    "error",
                    "safety.danger_cpm must be greater than safety.warning_cpm",
                    "safety",
                )
            warning_dose = float(safety.get("warning_usvh", 0.326))
            danger_dose = float(safety.get("danger_usvh", 0.651))
            if danger_dose <= warning_dose:
                _issue(
                    issues,
                    "safety_dose_order",
                    "error",
                    "safety.danger_usvh must be greater than safety.warning_usvh",
                    "safety",
                )
        except (TypeError, ValueError):
            _issue(
                issues,
                "safety_threshold_not_numeric",
                "error",
                "Safety thresholds must be numeric",
                "safety",
            )

    system = payload.get("system", {})
    if isinstance(system, dict):
        defaults = {
            "bridge_heartbeat_interval_seconds": DEFAULT_BRIDGE_HEARTBEAT_INTERVAL_SECONDS,
            "health_startup_grace_seconds": DEFAULT_HEALTH_STARTUP_GRACE_SECONDS,
            "health_bridge_warning_seconds": DEFAULT_HEALTH_BRIDGE_WARNING_SECONDS,
            "health_bridge_error_seconds": DEFAULT_HEALTH_BRIDGE_ERROR_SECONDS,
            "health_measurement_warning_seconds": DEFAULT_HEALTH_MEASUREMENT_WARNING_SECONDS,
            "health_measurement_error_seconds": DEFAULT_HEALTH_MEASUREMENT_ERROR_SECONDS,
        }
        ranges = {
            "bridge_heartbeat_interval_seconds": (5, 60),
            "health_startup_grace_seconds": (30, 3600),
            "health_bridge_warning_seconds": (10, 600),
            "health_bridge_error_seconds": (20, 1800),
            "health_measurement_warning_seconds": (30, 86400),
            "health_measurement_error_seconds": (60, 172800),
        }
        parsed: dict[str, int] = {}
        for key, default in defaults.items():
            try:
                parsed[key] = int(system.get(key, default))
            except (TypeError, ValueError):
                _issue(
                    issues,
                    "health_limit_not_numeric",
                    "error",
                    f"system.{key} must be an integer",
                    f"system.{key}",
                )
                parsed[key] = default
                continue
            minimum, maximum = ranges[key]
            if not minimum <= parsed[key] <= maximum:
                _issue(
                    issues,
                    "health_limit_out_of_range",
                    "error",
                    f"system.{key} must be between {minimum} and {maximum} seconds",
                    f"system.{key}",
                )

        if parsed["health_bridge_error_seconds"] <= parsed["health_bridge_warning_seconds"]:
            _issue(
                issues,
                "bridge_health_threshold_order",
                "error",
                "system.health_bridge_error_seconds must be greater than system.health_bridge_warning_seconds",
                "system",
            )
        if parsed["health_measurement_error_seconds"] <= parsed["health_measurement_warning_seconds"]:
            _issue(
                issues,
                "measurement_health_threshold_order",
                "error",
                "system.health_measurement_error_seconds must be greater than system.health_measurement_warning_seconds",
                "system",
            )
        if parsed["health_bridge_warning_seconds"] < parsed["bridge_heartbeat_interval_seconds"] * 2:
            _issue(
                issues,
                "bridge_health_warning_too_short",
                "warning",
                "system.health_bridge_warning_seconds should be at least twice the bridge heartbeat interval",
                "system.health_bridge_warning_seconds",
            )

        configured_scan_intervals: list[int] = []
        for item in [*devices, *dual_devices]:
            if not isinstance(item, dict):
                continue
            try:
                configured_scan_intervals.append(int(item.get("scan_interval", 60)))
            except (TypeError, ValueError):
                continue
        longest_scan = max(configured_scan_intervals, default=60)
        if parsed["health_measurement_warning_seconds"] < longest_scan * 2:
            _issue(
                issues,
                "measurement_health_warning_too_short",
                "warning",
                "system.health_measurement_warning_seconds should be at least twice the longest device scan interval",
                "system.health_measurement_warning_seconds",
            )

    return ValidationResult(tuple(issues))


def validate_candidate_options(payload: object) -> list[str]:
    """Backward-compatible flat list used by the dashboard and older tests."""
    return validate_options(payload).messages()


def runtime_device_options(options: dict[str, Any]) -> list[dict[str, Any]]:
    """Return one normalized runtime list.

    Strict validation is performed when the options file is loaded at service
    startup and by the shared self-test, migration and health-check paths. This
    helper remains tolerant for callers that assemble partial option mappings
    while deriving one service environment.
    """
    normalized, _changed = merge_single_and_dual_device_options(options)

    devices: list[dict[str, Any]] = []
    for group_name in ("devices", "dual_tube_devices"):
        values = normalized.get(group_name, []) or []
        if not isinstance(values, list):
            continue
        for item in values:
            if not isinstance(item, dict):
                continue
            device = dict(item)
            if group_name == "dual_tube_devices":
                serial = str(device.pop("device_serial", "") or "").strip().lower()
                if serial:
                    device["expected_serial"] = serial
                device.setdefault("dual_tube_mode", "separate")
            devices.append(device)
    return devices


def load_and_validate_options(path: str | Path) -> tuple[object, ValidationResult]:
    source = Path(path)
    import json

    payload = json.loads(source.read_text(encoding="utf-8"))
    return payload, validate_options(payload)
