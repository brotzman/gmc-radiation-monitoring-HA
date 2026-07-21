from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

DEFAULT_BRIDGE_HEARTBEAT_INTERVAL_SECONDS = 15
DEFAULT_HEALTH_STARTUP_GRACE_SECONDS = 15 * 60
DEFAULT_HEALTH_BRIDGE_WARNING_SECONDS = 45
DEFAULT_HEALTH_BRIDGE_ERROR_SECONDS = 120
DEFAULT_HEALTH_MEASUREMENT_WARNING_SECONDS = 10 * 60
DEFAULT_HEALTH_MEASUREMENT_ERROR_SECONDS = 20 * 60


@dataclass(frozen=True, slots=True)
class HealthThresholds:
    startup_grace_seconds: int = DEFAULT_HEALTH_STARTUP_GRACE_SECONDS
    bridge_warning_seconds: int = DEFAULT_HEALTH_BRIDGE_WARNING_SECONDS
    bridge_error_seconds: int = DEFAULT_HEALTH_BRIDGE_ERROR_SECONDS
    measurement_warning_seconds: int = DEFAULT_HEALTH_MEASUREMENT_WARNING_SECONDS
    measurement_error_seconds: int = DEFAULT_HEALTH_MEASUREMENT_ERROR_SECONDS

    def as_dict(self) -> dict[str, int]:
        return {
            "startup_grace_seconds": self.startup_grace_seconds,
            "bridge_warning_seconds": self.bridge_warning_seconds,
            "bridge_error_seconds": self.bridge_error_seconds,
            "measurement_warning_seconds": self.measurement_warning_seconds,
            "measurement_error_seconds": self.measurement_error_seconds,
        }


def _safe_int(mapping: Mapping[str, Any], key: str, default: int) -> int:
    try:
        value = int(mapping.get(key, default))
    except (TypeError, ValueError):
        return default
    return value if value > 0 else default


def health_thresholds_from_options(
    payload: object,
    *,
    scan_interval_seconds: int,
) -> HealthThresholds:
    """Resolve health limits without allowing invalid options to crash /health.

    The shared configuration validator reports malformed values separately. This
    function therefore falls back to conservative defaults whenever a value is
    absent or cannot be parsed.
    """

    system: Mapping[str, Any] = {}
    if isinstance(payload, dict) and isinstance(payload.get("system"), dict):
        system = payload["system"]

    scan = max(5, int(scan_interval_seconds))
    startup_default = max(DEFAULT_HEALTH_STARTUP_GRACE_SECONDS, scan * 5)
    measurement_warning_default = max(DEFAULT_HEALTH_MEASUREMENT_WARNING_SECONDS, scan * 10)
    measurement_error_default = max(DEFAULT_HEALTH_MEASUREMENT_ERROR_SECONDS, scan * 20)

    startup = _safe_int(system, "health_startup_grace_seconds", startup_default)
    bridge_warning = _safe_int(
        system, "health_bridge_warning_seconds", DEFAULT_HEALTH_BRIDGE_WARNING_SECONDS
    )
    bridge_error = _safe_int(
        system, "health_bridge_error_seconds", DEFAULT_HEALTH_BRIDGE_ERROR_SECONDS
    )
    measurement_warning = _safe_int(
        system, "health_measurement_warning_seconds", measurement_warning_default
    )
    measurement_error = _safe_int(
        system, "health_measurement_error_seconds", measurement_error_default
    )
    return HealthThresholds(
        startup_grace_seconds=startup,
        bridge_warning_seconds=bridge_warning,
        bridge_error_seconds=max(bridge_warning + 1, bridge_error),
        measurement_warning_seconds=measurement_warning,
        measurement_error_seconds=max(measurement_warning + 1, measurement_error),
    )
