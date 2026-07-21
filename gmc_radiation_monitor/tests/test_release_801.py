from __future__ import annotations

import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from gmc_bridge.gmcmap import AcpmAccumulator, GmcMapConfig, GmcMapReading, build_upload_url
from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import Translator, validate_catalogs
from gmc_bridge.version import APP_VERSION


def test_version_801() -> None:
    assert APP_VERSION == "8.4.5"


def test_acpm_accumulator_uses_all_accepted_session_readings() -> None:
    acpm = AcpmAccumulator()
    assert acpm.add(10) == 10.0
    assert acpm.add(20) == 15.0
    assert acpm.add(30) == 20.0
    assert acpm.sample_count == 3


def test_gmcmap_url_transmits_session_acpm() -> None:
    reading = GmcMapReading(
        cpm=24,
        average_cpm=18.25,
        dose_rate_usvh=0.156,
        captured_at_utc=1,
        average_sample_count=42,
    )
    query = parse_qs(
        urlsplit(build_upload_url(GmcMapConfig(account_id="0230111", counter_id="0034021"), reading)).query
    )
    assert query["CPM"] == ["24"]
    assert query["ACPM"] == ["18.2"]


def test_gmcmap_dashboard_shows_translated_cpm_and_acpm() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        store = HistoryStore(Path(temp_dir) / "history.sqlite3")
        store.upsert_device_registry(
            "SERIAL",
            {
                "device_model": "GMC-500+ Re 2.53",
                "runtime_online": True,
                "gmcmap_enabled": True,
                "gmcmap_configured": True,
                "gmcmap_upload_status": "success",
                "gmcmap_counter_id_masked": "***4021",
                "gmcmap_last_upload_utc": "2026-07-16T12:00:00Z",
                "gmcmap_last_cpm": 24,
                "gmcmap_last_average_cpm": 18.2,
                "gmcmap_acpm_sample_count": 42,
            },
        )
        store.insert_measurement({"cpm": 24}, device_serial="SERIAL", timestamp_utc=1_800_000_000)
        app = ReportApplication(
            store=store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
            ui_mode="advanced",
            restore_enabled=False,
            purge_all_history_enabled=False,
        )
        page = app.render_index(language_override="de", mode_override="advanced").decode()
        assert "Zuletzt übermitteltes CPM" in page
        assert "Zuletzt übermitteltes ACPM" in page
        assert "18.2 ACPM" in page
        assert "aktuellen Messsitzung der App" in page


def test_acpm_keys_exist_in_every_catalog() -> None:
    validate_catalogs()
    keys = (
        "Last uploaded CPM",
        "Last uploaded ACPM",
        "GMCMap last uploaded ACPM",
        "GMCMap ACPM accepted samples",
        "ACPM is the average of all accepted CPM readings since the current app measurement session began.",
    )
    for language in ("en", "de", "fr", "es", "it", "nl", "pl", "hr"):
        translator = Translator(language)
        for key in keys:
            assert translator(key) != key or language == "en"
