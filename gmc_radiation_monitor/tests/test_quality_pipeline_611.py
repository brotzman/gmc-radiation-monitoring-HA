from __future__ import annotations

import time
from pathlib import Path

from gmc_bridge.adaptive_background import build_site_adaptive_background
from gmc_bridge.fleet_analytics import build_fleet_snapshot
from gmc_bridge.history import HistoryStore
from gmc_bridge.quality_pipeline import filter_history_rows


def _online(store: HistoryStore, serial: str, model: str, interval: int = 60) -> None:
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


def test_extreme_cpm_does_not_distort_comparison(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    now = int(time.time())
    _online(store, "a", "GMC-320")
    _online(store, "b", "GMC-500+")
    values_a = [15 + index % 3 for index in range(20)] + [5623]
    values_b = [14 + index % 3 for index in range(21)]
    for serial, values in (("a", values_a), ("b", values_b)):
        for index, cpm in enumerate(values):
            store.insert_measurement(
                {"cpm": cpm},
                device_serial=serial,
                timestamp_utc=now - (len(values) - 1 - index) * 60,
                expected_interval_seconds=60,
            )
    comparison = build_fleet_snapshot(store)["comparison"]
    assert comparison is not None
    assert comparison["pairs"] >= 20
    assert comparison["excluded_measurements"] >= 1
    assert comparison["a_mean_1h"] < 30
    assert comparison["mean_difference"] < 5
    assert comparison["correlation"] is not None


def test_correlation_requires_ten_valid_pairs(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    now = int(time.time())
    for serial, model, offset in (("a", "GMC-320", 0), ("b", "GMC-500+", 1)):
        _online(store, serial, model)
        for index in range(3):
            store.insert_measurement(
                {"cpm": 15 + index + offset},
                device_serial=serial,
                timestamp_utc=now - (2 - index) * 60,
                expected_interval_seconds=60,
            )
    comparison = build_fleet_snapshot(store)["comparison"]
    assert comparison is not None
    assert comparison["pairs"] == 3
    assert comparison["correlation"] is None
    assert comparison["confidence"] == "Insufficient"


def test_site_profile_uses_two_devices_then_single_fallback(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    now = int(time.time())
    for serial, model, offset in (("a", "GMC-320", 0), ("b", "GMC-500+", 1)):
        _online(store, serial, model)
        for index in range(24):
            store.insert_measurement(
                {"cpm": 15 + index % 2 + offset},
                device_serial=serial,
                timestamp_utc=now - (23 - index) * 3600,
                expected_interval_seconds=3600,
            )
    rows = {serial: store.query_all(device_serial=serial) for serial in ("a", "b")}
    combined = build_site_adaptive_background(
        rows,
        timezone_name="UTC",
        device_weights={"a": 1.0, "b": 0.9},
        tolerance_seconds=60,
    )
    assert combined["paired_samples"] >= 20
    assert combined["confidence"] == "High"
    single = build_site_adaptive_background(
        {"a": rows["a"]},
        timezone_name="UTC",
        device_weights={"a": 1.0},
        tolerance_seconds=60,
    )
    assert single["confidence"] == "Reduced"
    assert single["fusion_mode"] == "single_device_fallback"


def test_baseline_filter_rejects_extreme_value() -> None:
    from gmc_bridge.history import HistoryRow

    rows = [
        HistoryRow("a", index, 15 + index % 2, None, None, None, None, None, "normal") for index in range(20)
    ]
    rows.append(HistoryRow("a", 21, 5623, None, None, None, None, None, "confirmed_high"))
    result = filter_history_rows(rows, purpose="baseline")
    assert len(result.rows) == 20
    assert result.rejected_by_reason["robust_outlier"] == 1
