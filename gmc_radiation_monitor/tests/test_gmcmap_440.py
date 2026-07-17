from __future__ import annotations

import tempfile
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

import pytest
from gmc_bridge.config import Settings
from gmc_bridge.gmcmap import (
    GmcMapConfig,
    GmcMapReading,
    GmcMapUploader,
    build_upload_url,
    mask_identifier,
    parse_device_id_mappings,
    resolve_counter_id,
)
from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "port": "/dev/ttyUSB0",
        "ports": ("/dev/ttyUSB0",),
        "baudrate": 19200,
        "scan_interval": 60,
        "command_timeout": 2.0,
        "inter_command_delay_ms": 150,
        "high_cpm_threshold": 10000,
        "high_cpm_confirmations": 3,
        "read_gyro": False,
        "mqtt_host": "localhost",
        "mqtt_port": 1883,
        "mqtt_username": "",
        "mqtt_password": "",
    }
    values.update(overrides)
    return Settings(**values)


def test_multi_device_counter_mapping_is_serial_specific():
    mappings = parse_device_id_mappings("SERIAL_A=0034021,SERIAL_B=0034022")
    assert resolve_counter_id("SERIAL_A", mappings, configured_device_count=2) == "0034021"
    assert resolve_counter_id("SERIAL_B", mappings, configured_device_count=2) == "0034022"
    assert resolve_counter_id("SERIAL_C", mappings, configured_device_count=2) is None


def test_single_counter_id_wildcard_is_rejected_for_multiple_devices():
    mappings = parse_device_id_mappings("0034021")
    assert resolve_counter_id("SERIAL_A", mappings, configured_device_count=1) == "0034021"
    assert resolve_counter_id("SERIAL_A", mappings, configured_device_count=2) is None


def test_upload_url_uses_official_parameter_names():
    config = GmcMapConfig(account_id="0230111", counter_id="0034021")
    reading = GmcMapReading(cpm=15, average_cpm=13.2, dose_rate_usvh=0.075, captured_at_utc=1)
    parsed = urlsplit(build_upload_url(config, reading))
    query = parse_qs(parsed.query)
    assert parsed.scheme == "https"
    assert parsed.netloc == "www.gmcmap.com"
    assert parsed.path == "/log2.asp"
    assert query == {
        "AID": ["0230111"],
        "GID": ["0034021"],
        "CPM": ["15"],
        "ACPM": ["13.2"],
        "uSV": ["0.075"],
    }


def test_uploader_tracks_success_without_exposing_full_counter_id():
    calls: list[str] = []

    def transport(url: str, timeout: float) -> tuple[int, str]:
        calls.append(url)
        assert timeout == 4.0
        return 200, "OK"

    uploader = GmcMapUploader(
        GmcMapConfig(
            account_id="0230111",
            counter_id="0034021",
            timeout_seconds=4.0,
        ),
        transport=transport,
    )
    reading = GmcMapReading(cpm=15, average_cpm=13.2, dose_rate_usvh=0.075, captured_at_utc=1)
    uploader.offer(reading)
    uploader._attempt_upload(reading)
    status = uploader.snapshot()
    assert calls
    assert status["gmcmap_upload_status"] == "success"
    assert status["gmcmap_upload_success_count"] == 1
    assert status["gmcmap_upload_error_count"] == 0
    assert status["gmcmap_counter_id_masked"] == mask_identifier("0034021")
    assert "0034021" not in str(status)
    assert "0230111" not in str(status)
    assert uploader._latest is None


def test_uploader_redacts_identifiers_from_errors():
    def transport(url: str, timeout: float) -> tuple[int, str]:
        raise RuntimeError(f"failed for {url}")

    uploader = GmcMapUploader(
        GmcMapConfig(account_id="0230111", counter_id="0034021"),
        transport=transport,
    )
    uploader._attempt_upload(GmcMapReading(cpm=15, average_cpm=13.2, dose_rate_usvh=0.075, captured_at_utc=1))
    status = uploader.snapshot()
    assert status["gmcmap_upload_status"] == "error"
    assert status["gmcmap_upload_error_count"] == 1
    assert "0230111" not in str(status["gmcmap_last_error"])
    assert "0034021" not in str(status["gmcmap_last_error"])


def test_enabling_gmcmap_requires_explicit_public_data_confirmation():
    settings = _settings(
        gmcmap_enabled=True,
        gmcmap_privacy_confirmed=False,
        gmcmap_account_id="0230111",
        gmcmap_device_ids=(("*", "0034021"),),
    )
    with pytest.raises(ValueError, match="PRIVACY_CONFIRMED"):
        settings.validate()


def test_dashboard_shows_independent_gmcmap_status_per_device():
    with tempfile.TemporaryDirectory() as temp_dir:
        store = HistoryStore(Path(temp_dir) / "history.sqlite3")
        store.upsert_device_registry(
            "SERIAL_A",
            {
                "device_model": "GMC-320Re 4.52",
                "port": "/dev/a",
                "gmcmap_enabled": True,
                "gmcmap_configured": True,
                "gmcmap_upload_status": "success",
                "gmcmap_counter_id_masked": "***4021",
                "gmcmap_last_upload_utc": "2026-07-13T10:00:00Z",
                "gmcmap_next_upload_utc": "2026-07-13T10:05:00Z",
                "gmcmap_upload_success_count": 4,
                "gmcmap_upload_error_count": 1,
            },
        )
        store.upsert_device_registry(
            "SERIAL_B",
            {
                "device_model": "GMC-500+ 2.20",
                "port": "/dev/b",
                "gmcmap_enabled": True,
                "gmcmap_configured": False,
                "gmcmap_upload_status": "not_configured",
            },
        )
        store.insert_measurement({"cpm": 12}, device_serial="SERIAL_A", timestamp_utc=1_800_000_000)
        store.insert_measurement({"cpm": 22}, device_serial="SERIAL_B", timestamp_utc=1_800_000_001)
        app = ReportApplication(
            store=store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
            ui_language="de",
        )
        page = app.render_index(language_override="de", mode_override="advanced").decode("utf-8")
        assert page.count("Öffentlicher GMCMap-Upload") == 2
        assert "Upload erfolgreich" in page
        assert "***4021" in page
        assert "keine Zähler-ID zugeordnet" in page
        assert "0230111" not in page
