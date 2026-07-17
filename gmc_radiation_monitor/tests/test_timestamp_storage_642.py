import sys
from datetime import UTC, datetime
from pathlib import Path

LIB_DIR = Path(__file__).parents[1] / "rootfs/usr/local/lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from gmc_bridge.history import HistoryStore  # noqa: E402


def test_history_accepts_iso_timestamp_for_measurement_and_raw_sample(tmp_path):
    store = HistoryStore(tmp_path / "history.sqlite3")
    iso_timestamp = "2026-07-15T11:01:15Z"
    expected = int(datetime(2026, 7, 15, 11, 1, 15, tzinfo=UTC).timestamp())

    store.insert_raw_measurement(
        {"cpm": 17, "temperature_c": 29.7},
        device_serial="device-a",
        timestamp_utc=iso_timestamp,
        gate_state="accepted_normal",
        accepted=True,
    )
    store.insert_measurement(
        {"cpm": 17, "temperature_c": 29.7},
        device_serial="device-a",
        timestamp_utc=iso_timestamp,
        expected_interval_seconds=60,
    )

    raw_rows = store.query_raw_measurements(expected, expected + 1, device_serial="device-a")
    rows = store.query_range(expected, expected + 1, device_serial="device-a")
    assert raw_rows[0]["timestamp_utc"] == expected
    assert rows[0].timestamp_utc == expected


def test_history_accepts_iso_timestamp_for_operational_event(tmp_path):
    store = HistoryStore(tmp_path / "history.sqlite3")
    iso_timestamp = "2026-07-15T11:01:41Z"
    expected = int(datetime(2026, 7, 15, 11, 1, 41, tzinfo=UTC).timestamp())

    store.insert_operational_event(
        {"timestamp_utc": iso_timestamp, "event_type": "orientation_changed"},
        device_serial="device-a",
    )

    events = store.recent_operational_events(device_serial="device-a")
    assert events[0]["timestamp_utc"] == expected
