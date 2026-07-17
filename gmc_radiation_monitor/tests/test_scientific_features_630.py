from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from gmc_bridge.history import HistoryRow, HistoryStore
from gmc_bridge.scientific_analysis import (
    counting_uncertainty,
    detect_persistent_level_shift,
    relative_device_response,
)


def row(serial: str, timestamp: int, cpm: int) -> HistoryRow:
    return HistoryRow(serial, timestamp, cpm, None, None, None, None, None, "normal")


def test_counting_uncertainty_shrinks_with_more_impulses_and_time() -> None:
    start = 1_700_000_000
    short = counting_uncertainty([row("a", start, 16)])
    long = counting_uncertainty([row("a", start + index * 60, 16) for index in range(120)])
    assert short["impulses"] == 16
    assert short["duration_seconds"] == 60
    assert long["impulses"] == 1920
    assert long["duration_seconds"] == 7200
    assert float(long["plus_cpm"]) < float(short["plus_cpm"])
    assert float(long["relative_uncertainty_percent"]) < float(short["relative_uncertainty_percent"])


def test_raw_measurements_are_kept_separately_before_filtering(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    raw_sample = {"cpm": 9999, "voltage_v": 4.1, "vendor_field": "unchanged"}
    raw_id = store.insert_raw_measurement(
        raw_sample,
        device_serial="abc",
        timestamp_utc=1_700_000_000,
        gate_state="pending_high_confirmation",
        accepted=False,
    )
    assert raw_id > 0
    assert store.count(device_serial="abc") == 0
    summary = store.raw_measurement_summary(device_serial="abc")
    assert summary == {"available": True, "total": 1, "accepted": 0, "pending": 1}
    saved = store.query_raw_measurements(1_699_999_999, 1_700_000_001, device_serial="abc")[0]
    assert json.loads(saved["raw_json"]) == raw_sample
    assert saved["gate_state"] == "pending_high_confirmation"


def test_relative_response_factor_is_not_absolute_calibration() -> None:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    pairs = []
    for index in range(600):
        timestamp = int((start + timedelta(minutes=36 * index)).timestamp())
        pairs.append((row("a", timestamp, 20), row("b", timestamp, 10)))
    result = relative_device_response(pairs, orientation_verified=False)
    assert result["learning"] is False
    assert result["factor_right_to_left"] == 2.0
    assert result["relative_only"] is True
    assert result["orientation_stable"] is None
    assert result["confidence"] == "Medium"


def test_persistent_level_shift_uses_pre_and_post_segments() -> None:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    rows = []
    for hour in range(48):
        rows.append(row("a", int((start + timedelta(hours=hour)).timestamp()), 10))
    for hour in range(48, 66):
        rows.append(row("a", int((start + timedelta(hours=hour)).timestamp()), 20))
    result = detect_persistent_level_shift(rows)
    assert result["available"] is True
    assert result["detected"] is True
    assert result["change_percent"] > 50
    assert result["post_hours"] >= 6
    assert result["statistical_only"] is True
