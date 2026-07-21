from __future__ import annotations

from pathlib import Path

from gmc_bridge.analysis_presentation import build_fleet_intelligence_result
from gmc_bridge.fleet_analytics import build_fleet_snapshot
from gmc_bridge.history import HistoryStore
from gmc_bridge.translations import Translator
from gmc_bridge.web_analysis_views import render_fleet_intelligence


def _register(store: HistoryStore, serial: str, model: str, interval: int) -> None:
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


def test_exact_half_open_24h_window_prevents_721_samples(tmp_path: Path, monkeypatch) -> None:
    now = 2_000_000_000
    monkeypatch.setattr("gmc_bridge.fleet_analytics.time.time", lambda: now)
    store = HistoryStore(tmp_path / "history.sqlite3")
    _register(store, "gmc320", "GMC-320 Re 4.52", 120)

    # 721 stored samples include both boundaries of the old, over-wide query.
    for timestamp in range(now - 86_400, now + 1, 120):
        store.insert_measurement(
            {"cpm": 15},
            device_serial="gmc320",
            timestamp_utc=timestamp,
            expected_interval_seconds=120,
        )

    item = build_fleet_snapshot(store)["stability"][0]
    assert item.valid_samples == 720
    assert item.expected_samples == 720
    assert item.total_stored_samples == 721
    assert item.analysis_window_seconds == 86_400
    assert item.longest_gap_seconds == 120
    assert item.interval_deviation_seconds == 0


def test_each_connected_device_uses_its_own_interval_and_total(tmp_path: Path, monkeypatch) -> None:
    now = 2_000_100_000
    monkeypatch.setattr("gmc_bridge.fleet_analytics.time.time", lambda: now)
    store = HistoryStore(tmp_path / "history.sqlite3")
    _register(store, "gmc320", "GMC-320 Re 4.52", 120)
    _register(store, "gmc500", "GMC-500+ Re 1.14", 60)

    for index in range(4):
        store.insert_measurement(
            {"cpm": 12}, device_serial="gmc320", timestamp_utc=now - 363 + index * 121
        )
    for index in range(8):
        store.insert_measurement(
            {"cpm": 13}, device_serial="gmc500", timestamp_utc=now - 420 + index * 60
        )

    by_serial = {item.serial: item for item in build_fleet_snapshot(store)["stability"]}
    assert by_serial["gmc320"].scan_interval_seconds == 120
    assert by_serial["gmc320"].total_stored_samples == 4
    assert by_serial["gmc320"].longest_gap_seconds == 121
    assert by_serial["gmc320"].interval_deviation_seconds == 1
    assert by_serial["gmc500"].scan_interval_seconds == 60
    assert by_serial["gmc500"].total_stored_samples == 8
    assert by_serial["gmc500"].interval_deviation_seconds == 0


def test_german_dashboard_explains_window_and_total_per_device(tmp_path: Path, monkeypatch) -> None:
    now = 2_000_200_000
    monkeypatch.setattr("gmc_bridge.fleet_analytics.time.time", lambda: now)
    store = HistoryStore(tmp_path / "history.sqlite3")
    _register(store, "gmc320", "GMC-320 Re 4.52", 120)
    for index in range(3):
        store.insert_measurement(
            {"cpm": 14}, device_serial="gmc320", timestamp_utc=now - 242 + index * 121
        )

    result = build_fleet_intelligence_result(build_fleet_snapshot(store))
    html = render_fleet_intelligence(result, Translator("de"))
    assert "Gültige Messwerte (24 h): 3 / 3" in html
    assert "Gesamt gespeicherte Messwerte: 3" in html
    assert "Größter Messabstand: 121 s" in html
    assert "Erwartetes Messintervall: 120 s" in html
    assert "Maximale Intervallabweichung: +1 s" in html
    assert "Qualitätsgewicht:" in html and "%" in html
