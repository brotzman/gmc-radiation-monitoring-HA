from __future__ import annotations

import time
from pathlib import Path

from gmc_bridge.fleet_analytics import build_fleet_snapshot
from gmc_bridge.history import HistoryStore


def test_fleet_snapshot_compares_two_devices(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    now = int(time.time())
    for serial, model, interval, values in (
        ("a", "GMC-320", 60, [10 + index for index in range(12)]),
        ("b", "GMC-500+", 60, [11 + index for index in range(12)]),
    ):
        store.upsert_device_registry(
            serial,
            {
                "device_model": model,
                "runtime_online": True,
                "scan_interval_seconds": interval,
                "serial_error_count": 0,
                "serial_reconnect_count": 0,
            },
        )
        for index, cpm in enumerate(values):
            store.insert_measurement(
                {"cpm": cpm},
                device_serial=serial,
                timestamp_utc=now - 660 + index * 60,
                expected_interval_seconds=60,
            )
    snapshot = build_fleet_snapshot(store)
    assert len(snapshot["stability"]) == 2
    assert snapshot["comparison"] is not None
    assert snapshot["comparison"]["pairs"] >= 10
    assert snapshot["comparison"]["correlation"] > 0.99
    assert snapshot["comparison"]["bland_altman_available"] is True
    assert snapshot["comparison"]["bland_altman_bias_cpm"] == -1.0
    assert snapshot["comparison"]["bland_altman_lower_cpm"] == -1.0
    assert snapshot["comparison"]["bland_altman_upper_cpm"] == -1.0
