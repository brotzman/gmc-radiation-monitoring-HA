import tempfile
from pathlib import Path

from gmc_bridge.config import Settings
from gmc_bridge.history import HistoryStore


def test_parse_multiple_ports_and_deduplicate():
    assert Settings._parse_ports("/dev/a, /dev/b;/dev/a\n/dev/c", "/dev/fallback") == (
        "/dev/a",
        "/dev/b",
        "/dev/c",
    )
    assert Settings._parse_ports("", "/dev/fallback") == ("/dev/fallback",)


def test_device_registry_and_shared_latest_dashboard_data():
    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        store.upsert_device_registry("SERIAL-A", {"device_model": "GMC-320", "port": "/dev/a"})
        store.upsert_device_registry("SERIAL-B", {"device_model": "GMC-500+", "port": "/dev/b"})
        store.insert_measurement({"cpm": 12}, device_serial="SERIAL-A", timestamp_utc=100)
        store.insert_measurement(
            {"cpm": 34, "tube_low_cpm": 30, "tube_high_cpm": 4}, device_serial="SERIAL-B", timestamp_utc=101
        )
        devices = {item["serial"]: item for item in store.list_devices()}
        assert devices["SERIAL-A"]["cpm"] == 12
        assert devices["SERIAL-A"]["port"] == "/dev/a"
        assert devices["SERIAL-B"]["cpm"] == 34
        assert devices["SERIAL-B"]["tube_low_cpm"] == 30


def test_device_inventory_contains_per_device_counts_capabilities_and_bounds():
    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        store.upsert_device_registry(
            "SERIAL-A",
            {"device_model": "GMC-320", "port": "/dev/a", "device_profile_name": "GMC-300/320 family"},
        )
        store.set_device_capabilities("SERIAL-A", {"cpm": True, "temperature": True, "gyro": False})
        store.insert_measurement({"cpm": 12}, device_serial="SERIAL-A", timestamp_utc=100)
        store.insert_measurement({"cpm": 13}, device_serial="SERIAL-A", timestamp_utc=160)
        device = store.list_devices()[0]
        assert device["stored_samples"] == 2
        assert device["first_timestamp_utc"] == 100
        assert device["last_timestamp_utc"] == 160
        assert device["capabilities_map"]["temperature"] is True
        assert device["capabilities_map"]["gyro"] is False
        assert store.count(all_devices=True) == 2


def test_report_dashboard_moves_device_details_into_device_cards():
    from gmc_bridge.report_web import ReportApplication

    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        store.upsert_device_registry(
            "SERIAL-A",
            {
                "device_model": "GMC-320",
                "port": "/dev/a",
                "device_profile_name": "GMC-300/320 family",
                "last_seen_utc": "2099-01-01T00:00:00Z",
            },
        )
        store.set_device_capabilities("SERIAL-A", {"cpm": True, "temperature": True})
        store.insert_measurement(
            {"cpm": 12, "temperature_c": 21.0}, device_serial="SERIAL-A", timestamp_utc=1_800_000_000
        )
        app = ReportApplication(
            store=store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
        )
        page = app.render_index(
            language_override="de", device_override="SERIAL-A", report_device_override="all"
        ).decode("utf-8")
        assert "Globale Berichts- und Exporteinstellungen" not in page
        assert "GMC-Strahlungsüberwachung" in page
        assert "Messwerte aller Geräte" in page
        assert "Verbundene GMC-Geräte" in page
        assert "Serieller Port" in page and "/dev/a" in page
        assert "Gerätefähigkeiten" in page
        assert "Messwerte dieses Geräts" in page
        assert "Analyse für GMC-320 · SERIAL-A" in page
        assert 'name="report_device"' not in page
        assert "Berichte für die angezeigte Analyse" in page


def test_device_time_capability_is_localized_in_german_dashboard():
    from gmc_bridge.report_web import ReportApplication

    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        store.upsert_device_registry(
            "SERIAL-TIME",
            {
                "device_model": "GMC-500+ Re 2.53",
                "port": "/dev/ttyUSB0",
                "device_profile_name": "GMC-500 family",
                "last_seen_utc": "2099-01-01T00:00:00Z",
            },
        )
        store.set_device_capabilities(
            "SERIAL-TIME",
            {"cpm": True, "device_time": True, "dual_tube": True, "gyro": True, "voltage": True},
        )
        store.insert_measurement(
            {"cpm": 12, "voltage_v": 4.1},
            device_serial="SERIAL-TIME",
            timestamp_utc=1_800_000_000,
        )
        app = ReportApplication(
            store=store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=True,
            cpm_per_usvh=154.0,
        )
        page = app.render_index(
            language_override="de",
            device_override="SERIAL-TIME",
            report_device_override="all",
        ).decode("utf-8")
        assert "CPM, Gerätezeit, Dual-Tube-Messung, Gyroskop, Spannung" in page
        assert "device time" not in page.lower()


def test_live_analysis_can_select_a_specific_device():
    from gmc_bridge.reports import build_live_analysis

    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        store.set_metadata({"serial": "SERIAL-A"})
        store.insert_measurement({"cpm": 10}, device_serial="SERIAL-A", timestamp_utc=1_800_000_000)
        store.insert_measurement({"cpm": 99}, device_serial="SERIAL-B", timestamp_utc=1_800_000_000)
        result = build_live_analysis(store, scan_interval_seconds=60, device_serial="SERIAL-B")
        assert result["latest_cpm"] == 99
