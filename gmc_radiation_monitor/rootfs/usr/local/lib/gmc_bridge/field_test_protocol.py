from __future__ import annotations

import json
import time
from collections import Counter
from contextlib import closing
from datetime import UTC, datetime
from typing import Any

from .history import HistoryStore
from .version import APP_VERSION


def _parse_timestamp(value: Any) -> int | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return int(value)
    text = str(value).strip()
    if not text:
        return None
    try:
        return int(float(text))
    except ValueError:
        pass
    try:
        return int(datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(UTC).timestamp())
    except (ValueError, OSError):
        return None


def _gap_summary(store: HistoryStore, device_serial: str, expected_interval_seconds: int) -> dict[str, Any]:
    expected = max(1, int(expected_interval_seconds or 60))
    with closing(store._connect(read_only=True)) as connection:
        row = connection.execute(
            """
            WITH ordered AS (
              SELECT timestamp_utc,
                     timestamp_utc - LAG(timestamp_utc) OVER (ORDER BY timestamp_utc) AS gap
              FROM measurements WHERE device_serial=?
            )
            SELECT COALESCE(MAX(gap),0),
                   COALESCE(SUM(CASE WHEN gap >= ? THEN 1 ELSE 0 END),0),
                   COALESCE(SUM(CASE WHEN gap >= ? THEN gap - ? ELSE 0 END),0)
            FROM ordered
            """,
            (device_serial, expected * 2, expected * 2, expected),
        ).fetchone()
    return {
        "longest_gap_seconds": int(row[0] or 0),
        "gap_count": int(row[1] or 0),
        "estimated_missing_seconds": int(row[2] or 0),
        "gap_threshold_seconds": expected * 2,
    }


def build_field_test_protocol(
    store: HistoryStore,
    *,
    device_serial: str,
    timezone_name: str,
) -> dict[str, Any]:
    devices = {str(item.get("serial") or ""): item for item in store.list_devices()}
    device = dict(devices.get(device_serial) or {})
    expected_interval = int(device.get("scan_interval_seconds") or device.get("configured_scan_interval_seconds") or 60)
    now = int(time.time())
    started_at = _parse_timestamp(device.get("app_started_at"))
    first, last = store.bounds(device_serial=device_serial)
    gaps = _gap_summary(store, device_serial, expected_interval)
    events = store.recent_operational_events(limit=1000, device_serial=device_serial)
    event_counts = Counter(str(item.get("event_type") or "unknown") for item in events)
    db = store.database_stats()
    return {
        "schema": "gmc-field-test-protocol-v1",
        "app_version": APP_VERSION,
        "generated_at_utc": now,
        "timezone": timezone_name,
        "device": {
            "serial": device_serial,
            "name": device.get("configured_name") or device.get("device_model") or device_serial,
            "model": device.get("device_model"),
            "firmware": device.get("device_version") or device.get("firmware"),
            "detector_type": device.get("detector_type") or device.get("tube_model"),
            "runtime_online": bool(device.get("runtime_online")),
            "expected_interval_seconds": expected_interval,
        },
        "runtime": {
            "app_started_at_utc": started_at,
            "uptime_seconds": max(0, now - started_at) if started_at else None,
            "serial_error_count": int(device.get("serial_error_count") or 0),
            "serial_reconnect_count": int(device.get("serial_reconnect_count") or 0),
            "history_write_error_count": int(device.get("history_write_error_count") or 0),
            "temperature_error_count": int(device.get("temperature_error_count") or 0),
            "voltage_error_count": int(device.get("voltage_error_count") or 0),
            "gyro_error_count": int(device.get("gyro_error_count") or 0),
        },
        "history": {
            "stored_samples": int(device.get("stored_samples") or 0),
            "first_timestamp_utc": int(first) if first is not None else None,
            "last_timestamp_utc": int(last) if last is not None else None,
            **gaps,
        },
        "gmcmap": {
            "enabled": bool(device.get("gmcmap_enabled")),
            "status": device.get("gmcmap_upload_status"),
            "successful_uploads": int(device.get("gmcmap_upload_success_count") or 0),
            "upload_errors": int(device.get("gmcmap_upload_error_count") or 0),
            "consecutive_errors": int(device.get("gmcmap_consecutive_error_count") or 0),
            "last_upload_utc": device.get("gmcmap_last_upload_utc"),
            "last_error_utc": device.get("gmcmap_last_error_utc"),
        },
        "database": db,
        "operational_events": {
            "total_returned": len(events),
            "counts_by_type": dict(sorted(event_counts.items())),
        },
        "field_test_checklist": [
            "continuous_30_day_operation",
            "usb_disconnect_5_minutes",
            "usb_disconnect_multiple_hours",
            "application_restart",
            "home_assistant_restart",
            "mqtt_restart",
            "network_outage",
            "gmcmap_outage",
            "backup_restore_test",
            "report_generation_30_60_90_days",
        ],
        "interpretation": {
            "diagnostic_only": True,
            "does_not_certify_measurement_accuracy": True,
            "counters_are_cumulative_since_service_start_or_last_reset": True,
        },
    }


def field_test_protocol_json(store: HistoryStore, *, device_serial: str, timezone_name: str) -> bytes:
    return json.dumps(
        build_field_test_protocol(store, device_serial=device_serial, timezone_name=timezone_name),
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
    ).encode("utf-8")


__all__ = ["build_field_test_protocol", "field_test_protocol_json"]
