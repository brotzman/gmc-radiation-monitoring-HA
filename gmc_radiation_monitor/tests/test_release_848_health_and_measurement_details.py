from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from gmc_bridge.config_validation import validate_options
from gmc_bridge.health import assess_health
from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication, ReportRequestHandler
from gmc_bridge.runtime_options import load_options
from gmc_bridge.translations import Translator


def _valid_options(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "devices": [
                    {
                        "name": "GMC-320",
                        "scan_interval": 60,
                        "serial_startup_delay": 0,
                    }
                ],
                "dual_tube_devices": [],
                "history": {"retention_days": 90, "report_timezone": "Europe/Berlin"},
            }
        ),
        encoding="utf-8",
    )
    return path


def _registered_store(tmp_path: Path, *, online: bool, timestamp: int) -> HistoryStore:
    store = HistoryStore(tmp_path / "history.sqlite", retention_days=90)
    store.upsert_device_registry(
        "SERIAL-1",
        {
            "configured_name": "GMC-320",
            "device_model": "GMC-320 Re 4.52",
            "runtime_online": online,
            "runtime_status": "online" if online else "offline",
            "scan_interval_seconds": 60,
            "timestamp_utc": timestamp,
            "last_timestamp_utc": timestamp,
            "cpm_per_usvh": 154.0,
            "tube_model": "M4011",
            "detector_profile": "gmc_320_plus_v4",
        },
    )
    store.insert_measurement(
        {
            "cpm": 8,
            "derived_dose_usvh": 0.0519,
            "measurement_quality_index": 100,
            "measurement_quality_stars": "★★★★★",
            "corrected_cpm": 8.0,
            "dead_time_loss_percent": 0.0,
            "dead_time_correction_factor": 1.0,
            "detector_type": "M4011",
            "active_tube": "M4011",
        },
        device_serial="SERIAL-1",
        timestamp_utc=timestamp,
    )
    return store


def test_848_shared_validator_drives_runtime_loading(tmp_path: Path) -> None:
    options_path = _valid_options(tmp_path / "options.json")
    loaded = load_options(options_path)
    assert [device["name"] for device in loaded["devices"]] == ["GMC-320"]

    invalid = json.loads(options_path.read_text(encoding="utf-8"))
    invalid["dual_tube_devices"] = [
        {
            "name": "gmc-320",
            "scan_interval": 60,
            "serial_startup_delay": 15,
            "dual_tube_mode": "separate",
        }
    ]
    result = validate_options(invalid)
    assert result.status == "error"
    assert result.valid is False
    assert any(issue.code == "duplicate_device_name" for issue in result.errors)


def test_848_health_warning_stays_healthy_and_error_is_unhealthy(tmp_path: Path) -> None:
    now = int(time.time())
    options_path = _valid_options(tmp_path / "options.json")
    online_store = _registered_store(tmp_path / "online", online=True, timestamp=now)
    online_devices = [dict(item, health_connected=True) for item in online_store.list_devices()]
    healthy = assess_health(
        store=online_store,
        devices=online_devices,
        options_path=options_path,
        scan_interval_seconds=60,
        started_at_utc=now - 3600,
        now_utc=now,
    )
    assert healthy.healthy is True
    assert healthy.status == "ok"

    stale_store = _registered_store(tmp_path / "stale", online=False, timestamp=now - 3600)
    stale_devices = [dict(item, health_connected=False) for item in stale_store.list_devices()]
    unhealthy = assess_health(
        store=stale_store,
        devices=stale_devices,
        options_path=options_path,
        scan_interval_seconds=60,
        started_at_utc=now - 3600,
        now_utc=now,
    )
    assert unhealthy.healthy is False
    assert unhealthy.status == "error"
    statuses = {item.key: item.status for item in unhealthy.checks}
    assert statuses["connections"] == "error"
    assert statuses["freshness"] == "error"


def test_848_http_health_returns_json_and_503_for_critical_state(tmp_path: Path) -> None:
    now = int(time.time())
    store = _registered_store(tmp_path, online=False, timestamp=now - 3600)
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        options_path=_valid_options(tmp_path / "options.json"),
        started_at_utc=now - 3600,
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
    server.app = app
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{server.server_port}/health", timeout=5):
            raise AssertionError("critical health endpoint unexpectedly returned HTTP 200")
    except urllib.error.HTTPError as exc:
        assert exc.code == 503
        payload = json.loads(exc.read())
        assert payload["healthy"] is False
        assert payload["status"] == "error"
        assert any(item["key"] == "database" for item in payload["checks"])
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_848_measurement_details_are_always_visible_only_in_expert_tier(tmp_path: Path) -> None:
    now = int(time.time())
    store = _registered_store(tmp_path, online=True, timestamp=now)
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
        ui_mode="advanced",
    )
    page = app.render_index(language_override="de", mode_override="advanced").decode("utf-8")
    block = page.split('<section class="measurement-details" data-analysis-tier="expert">', 1)[1].split(
        "</section>", 1
    )[0]
    assert "Messdetails" in block
    assert "Roh-CPM" in block
    assert "Korrigierte CPM" in block
    assert "Expertenansicht" not in block
    assert "<summary" not in block
    assert "<details" not in block
    assert Translator("en")("Measurement details") == "Measurement details"
    assert Translator("de")("Measurement details") == "Messdetails"
