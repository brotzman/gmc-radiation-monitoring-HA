from __future__ import annotations

from pathlib import Path

from gmc_bridge.history import HistoryStore


def _insert(store: HistoryStore, serial: str, timestamp: int, cpm: int) -> None:
    sample = {"cpm": cpm, "voltage_v": 4.1}
    store.insert_raw_measurement(
        sample,
        device_serial=serial,
        timestamp_utc=timestamp,
        gate_state="accepted_normal",
        accepted=True,
    )
    store.insert_measurement(
        sample,
        device_serial=serial,
        timestamp_utc=timestamp,
        cpm_quality="normal",
        expected_interval_seconds=60,
    )


def test_cleanup_removes_isolated_5887_peak_from_raw_and_normal_history(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    start = 1_700_000_000
    for index, cpm in enumerate((14, 15, 16, 15, 17, 14, 16, 15)):
        _insert(store, "GMC500", start + index * 60, cpm)
    peak_timestamp = start + 8 * 60
    _insert(store, "GMC500", peak_timestamp, 5887)
    _insert(store, "GMC500", start + 9 * 60, 16)

    result = store.purge_unconfirmed_adaptive_spikes()

    assert result["raw_deleted"] == 1
    assert result["measurements_deleted"] == 1
    raw = store.query_raw_measurements(start, start + 20 * 60, device_serial="GMC500")
    accepted = store.query_range(start, start + 20 * 60, device_serial="GMC500")
    assert all(row["cpm"] != 5887 for row in raw)
    assert all(row.cpm != 5887 for row in accepted)
    rerun = store.purge_unconfirmed_adaptive_spikes()
    assert rerun["already_done"] is False
    assert rerun["previously_run"] is True
    assert rerun["raw_deleted"] == 0


def test_cleanup_preserves_three_consecutive_confirmed_high_values(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    start = 1_700_100_000
    for index, cpm in enumerate((14, 15, 16, 15, 17, 14, 16, 15)):
        _insert(store, "GMC320", start + index * 60, cpm)
    for offset, cpm in enumerate((5800, 6100, 5900), start=8):
        _insert(store, "GMC320", start + offset * 60, cpm)
    _insert(store, "GMC320", start + 11 * 60, 16)

    result = store.purge_unconfirmed_adaptive_spikes()

    assert result["raw_deleted"] == 0
    assert result["measurements_deleted"] == 0
    raw = store.query_raw_measurements(start, start + 20 * 60, device_serial="GMC320")
    assert [row["cpm"] for row in raw if row["cpm"] > 1000] == [5800, 6100, 5900]
