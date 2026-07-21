from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .bridge_heartbeat import read_bridge_heartbeat
from .config_validation import validate_options
from .health_settings import HealthThresholds, health_thresholds_from_options
from .history import HistoryStore
from .migrations import SCHEMA_VERSION

HEALTH_STORAGE_WARNING_BYTES = 100 * 1024 * 1024
HEALTH_STORAGE_ERROR_BYTES = 10 * 1024 * 1024


@dataclass(frozen=True, slots=True)
class HealthCheck:
    key: str
    status: str
    detail: str
    values: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "status": self.status,
            "detail": self.detail,
            "values": dict(self.values),
        }


@dataclass(frozen=True, slots=True)
class HealthAssessment:
    checks: tuple[HealthCheck, ...]

    @property
    def status(self) -> str:
        if any(check.status == "error" for check in self.checks):
            return "error"
        if any(check.status == "warning" for check in self.checks):
            return "warning"
        return "ok"

    @property
    def healthy(self) -> bool:
        return self.status != "error"

    def as_dict(self, *, generated_at_utc: str) -> dict[str, Any]:
        return {
            "generated_at_utc": generated_at_utc,
            "healthy": self.healthy,
            "ok": self.healthy,
            "status": self.status,
            "checks": [check.as_dict() for check in self.checks],
        }


def _status_for_elapsed(*, elapsed: int, grace: int) -> str:
    return "warning" if elapsed < grace else "error"


def _bridge_heartbeat_check(
    *,
    path: Path,
    now: int,
    elapsed: int,
    thresholds: HealthThresholds,
) -> HealthCheck:
    common_values: dict[str, Any] = {
        "path": str(path),
        "warning_after_seconds": thresholds.bridge_warning_seconds,
        "error_after_seconds": thresholds.bridge_error_seconds,
    }
    try:
        payload = read_bridge_heartbeat(path)
    except FileNotFoundError:
        status = _status_for_elapsed(
            elapsed=elapsed,
            grace=thresholds.startup_grace_seconds,
        )
        return HealthCheck(
            "bridge_heartbeat",
            status,
            "Bridge heartbeat is not available yet",
            {**common_values, "age_seconds": None},
        )
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        status = _status_for_elapsed(
            elapsed=elapsed,
            grace=thresholds.startup_grace_seconds,
        )
        return HealthCheck(
            "bridge_heartbeat",
            status,
            f"Bridge heartbeat cannot be read: {exc}",
            {**common_values, "age_seconds": None},
        )

    updated = int(payload["updated_at_utc"])
    age = max(0, now - updated)
    state = str(payload.get("state") or "unknown")
    child_running = bool(payload.get("child_running"))
    values = {
        **common_values,
        "age_seconds": age,
        "updated_at_utc": updated,
        "state": state,
        "child_running": child_running,
        "supervisor_pid": payload.get("supervisor_pid"),
        "child_pid": payload.get("child_pid"),
        "configured_devices": payload.get("configured_devices"),
        "assigned_devices": payload.get("assigned_devices"),
        "last_child_exit_code": payload.get("last_child_exit_code"),
    }

    if age > thresholds.bridge_error_seconds:
        return HealthCheck(
            "bridge_heartbeat",
            "error",
            f"Bridge heartbeat is stale ({age} seconds)",
            values,
        )
    if age > thresholds.bridge_warning_seconds:
        return HealthCheck(
            "bridge_heartbeat",
            "warning",
            f"Bridge heartbeat is delayed ({age} seconds)",
            values,
        )
    if state in {"stopped", "failed"}:
        return HealthCheck(
            "bridge_heartbeat",
            "error",
            f"Bridge supervisor reports state {state}",
            values,
        )
    if state == "running" and child_running:
        return HealthCheck(
            "bridge_heartbeat",
            "ok",
            f"Bridge heartbeat is current ({age} seconds)",
            values,
        )
    return HealthCheck(
        "bridge_heartbeat",
        "warning",
        f"Bridge supervisor is alive in state {state}",
        values,
    )


def assess_health(
    *,
    store: HistoryStore,
    devices: list[dict[str, Any]],
    options_path: str | Path,
    scan_interval_seconds: int,
    started_at_utc: int,
    now_utc: int | None = None,
    bridge_heartbeat_path: str | Path | None = None,
) -> HealthAssessment:
    """Run the watchdog checks used by ``/health``.

    The bridge heartbeat proves that the acquisition supervisor itself is
    alive. Device connectivity and measurement freshness remain separate checks
    so a disconnected counter is not confused with a crashed bridge process.
    """

    now = int(time.time()) if now_utc is None else int(now_utc)
    elapsed = max(0, now - int(started_at_utc))
    scan = max(5, int(scan_interval_seconds))
    checks: list[HealthCheck] = []

    options = Path(options_path)
    options_payload: object = {}
    options_error: Exception | None = None
    if options.exists():
        try:
            options_payload = json.loads(options.read_text(encoding="utf-8"))
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            options_error = exc
    thresholds = health_thresholds_from_options(
        options_payload,
        scan_interval_seconds=scan,
    )

    if bridge_heartbeat_path is None:
        checks.append(
            HealthCheck(
                "measurement_service",
                "ok",
                "Report status service is responding; bridge heartbeat is not configured in this environment",
                {"uptime_seconds": elapsed},
            )
        )
    else:
        checks.append(
            _bridge_heartbeat_check(
                path=Path(bridge_heartbeat_path),
                now=now,
                elapsed=elapsed,
                thresholds=thresholds,
            )
        )

    try:
        integrity = store.cached_quick_check(max_age_seconds=60)
        checks.append(
            HealthCheck(
                "database",
                "ok" if integrity == "ok" else "error",
                f"Database integrity: {integrity}",
                {"result": integrity},
            )
        )
    except Exception as exc:  # pragma: no cover - defensive watchdog boundary
        checks.append(HealthCheck("database", "error", f"Database check failed: {exc}"))

    try:
        schema = store.schema_version()
        checks.append(
            HealthCheck(
                "schema",
                "ok" if schema == SCHEMA_VERSION else "error",
                f"Database schema {schema} of {SCHEMA_VERSION}",
                {"current": schema, "expected": SCHEMA_VERSION},
            )
        )
    except Exception as exc:  # pragma: no cover - defensive watchdog boundary
        checks.append(HealthCheck("schema", "error", f"Schema check failed: {exc}"))

    if not options.exists():
        checks.append(
            HealthCheck(
                "configuration",
                "warning",
                "Options file is unavailable in this environment",
                {
                    "path": str(options),
                    "health_thresholds": thresholds.as_dict(),
                },
            )
        )
    elif options_error is not None:
        checks.append(
            HealthCheck(
                "configuration",
                "error",
                f"Configuration cannot be read: {options_error}",
                {"health_thresholds": thresholds.as_dict()},
            )
        )
    else:
        validation = validate_options(options_payload)
        checks.append(
            HealthCheck(
                "configuration",
                validation.status,
                "Configuration is valid"
                if validation.clean
                else "Configuration contains warnings"
                if validation.status == "warning"
                else "Configuration contains errors",
                {
                    "errors": [issue.message for issue in validation.errors],
                    "warnings": [issue.message for issue in validation.warnings],
                    "issues": [issue.as_dict() for issue in validation.issues],
                    "health_thresholds": thresholds.as_dict(),
                },
            )
        )

    startup_grace = thresholds.startup_grace_seconds
    connected = [
        item
        for item in devices
        if bool(item.get("health_connected", item.get("runtime_online")))
    ]
    known = len(devices)
    if not devices:
        device_status = _status_for_elapsed(elapsed=elapsed, grace=startup_grace)
        checks.append(
            HealthCheck(
                "connections",
                device_status,
                "No registered device is available",
                {"connected": 0, "known": 0, "startup_grace_seconds": startup_grace},
            )
        )
    elif not connected:
        device_status = _status_for_elapsed(elapsed=elapsed, grace=startup_grace)
        checks.append(
            HealthCheck(
                "connections",
                device_status,
                "All registered devices are offline",
                {"connected": 0, "known": known, "startup_grace_seconds": startup_grace},
            )
        )
    elif len(connected) < known:
        checks.append(
            HealthCheck(
                "connections",
                "warning",
                "Some registered devices are offline",
                {"connected": len(connected), "known": known},
            )
        )
    else:
        checks.append(
            HealthCheck(
                "connections",
                "ok",
                "All registered devices are online",
                {"connected": len(connected), "known": known},
            )
        )

    stale_warning = thresholds.measurement_warning_seconds
    stale_error = thresholds.measurement_error_seconds
    latest = max(
        (int(item.get("timestamp_utc") or item.get("last_timestamp_utc") or 0) for item in devices),
        default=0,
    )
    if not latest:
        freshness_status = _status_for_elapsed(elapsed=elapsed, grace=startup_grace)
        checks.append(
            HealthCheck(
                "freshness",
                freshness_status,
                "No stored measurement is available",
                {
                    "age_seconds": None,
                    "warning_after_seconds": stale_warning,
                    "error_after_seconds": stale_error,
                },
            )
        )
    else:
        age = max(0, now - latest)
        if age <= stale_warning:
            freshness_status = "ok"
        elif age <= stale_error or elapsed < startup_grace:
            freshness_status = "warning"
        else:
            freshness_status = "error"
        checks.append(
            HealthCheck(
                "freshness",
                freshness_status,
                f"Latest measurement age: {age} seconds",
                {
                    "age_seconds": age,
                    "warning_after_seconds": stale_warning,
                    "error_after_seconds": stale_error,
                },
            )
        )

    try:
        stat = os.statvfs(store.path.parent)
        free_bytes = int(stat.f_frsize * stat.f_bavail)
        if free_bytes < HEALTH_STORAGE_ERROR_BYTES:
            storage_status = "error"
        elif free_bytes < HEALTH_STORAGE_WARNING_BYTES:
            storage_status = "warning"
        else:
            storage_status = "ok"
        checks.append(
            HealthCheck(
                "storage",
                storage_status,
                f"Free storage: {free_bytes / (1024 * 1024):.0f} MiB",
                {"free_bytes": free_bytes},
            )
        )
    except OSError as exc:
        checks.append(HealthCheck("storage", "warning", f"Storage information is unavailable: {exc}"))

    return HealthAssessment(tuple(checks))
