from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Mapping

from .config_validation import validate_options
from .history import HistoryStore
from .migrations import SCHEMA_VERSION

HEALTH_STARTUP_GRACE_SECONDS = 15 * 60
HEALTH_MIN_STALE_SECONDS = 10 * 60
HEALTH_MIN_ERROR_STALE_SECONDS = 20 * 60
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


def assess_health(
    *,
    store: HistoryStore,
    devices: list[dict[str, Any]],
    options_path: str | Path,
    scan_interval_seconds: int,
    started_at_utc: int,
    now_utc: int | None = None,
) -> HealthAssessment:
    """Run the lightweight watchdog checks used by ``/health``.

    Transient startup and reconnect states remain warnings. Database/schema,
    invalid configuration, critically low storage and prolonged absence of
    device data are errors and therefore produce HTTP 503 at the watchdog URL.
    """

    now = int(time.time()) if now_utc is None else int(now_utc)
    elapsed = max(0, now - int(started_at_utc))
    scan = max(5, int(scan_interval_seconds))
    startup_grace = max(HEALTH_STARTUP_GRACE_SECONDS, scan * 5)
    stale_warning = max(HEALTH_MIN_STALE_SECONDS, scan * 10)
    stale_error = max(HEALTH_MIN_ERROR_STALE_SECONDS, scan * 20)
    checks: list[HealthCheck] = [
        HealthCheck(
            "measurement_service",
            "ok",
            "Report and measurement status service is responding",
            {"uptime_seconds": elapsed},
        )
    ]

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

    options = Path(options_path)
    if not options.exists():
        checks.append(
            HealthCheck(
                "configuration",
                "warning",
                "Options file is unavailable in this environment",
                {"path": str(options)},
            )
        )
    else:
        try:
            payload = json.loads(options.read_text(encoding="utf-8"))
            validation = validate_options(payload)
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
                    },
                )
            )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            checks.append(HealthCheck("configuration", "error", f"Configuration cannot be read: {exc}"))

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
