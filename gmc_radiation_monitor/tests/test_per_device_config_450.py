from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest
from gmc_bridge.config import DeviceConfig, Settings
from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def _settings(**overrides: object) -> Settings:
    values: dict[str, object] = {
        "port": "/dev/default",
        "ports": ("/dev/a", "/dev/b"),
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


def test_legacy_ports_inherit_global_defaults():
    settings = _settings(baudrate=38400, scan_interval=45, cpm_per_usvh=123.0)
    devices = settings.effective_devices()
    assert [device.port for device in devices] == ["/dev/a", "/dev/b"]
    assert all(device.baudrate == 38400 for device in devices)
    assert all(device.scan_interval == 45 for device in devices)
    assert all(device.cpm_per_usvh == 123.0 for device in devices)


def test_structured_devices_override_independent_values():
    defaults = _settings()
    raw = json.dumps(
        [
            {
                "port": "/dev/serial/by-id/gmc320",
                "name": "Keller",
                "baudrate": 19200,
                "scan_interval": 60,
                "cpm_per_usvh": 154.0,
                "heartbeat_enabled": False,
                "gmcmap_counter_id": "0034021",
            },
            {
                "port": "/dev/serial/by-id/gmc500",
                "name": "Wohnzimmer",
                "baudrate": 115200,
                "scan_interval": 30,
                "cpm_per_usvh": 120.0,
                "heartbeat_enabled": True,
                "gmcmap_counter_id": "0034022",
            },
        ]
    )
    devices = Settings._parse_devices_json(raw, defaults)
    assert devices[0].baudrate == 19200
    assert devices[1].baudrate == 115200
    assert devices[0].scan_interval == 60
    assert devices[1].scan_interval == 30
    assert devices[1].heartbeat_enabled is True
    assert devices[0].gmcmap_counter_id == "0034021"
    settings = _settings(devices=devices)
    assert settings.effective_devices() == devices
    settings.validate()


def test_structured_devices_reject_duplicate_ports_and_unknown_fields():
    defaults = _settings()
    with pytest.raises(ValueError, match="unique port"):
        Settings._parse_devices_json('[{"port":"/dev/a"},{"port":"/dev/a"}]', defaults)
    with pytest.raises(ValueError, match="unknown fields"):
        Settings._parse_devices_json('[{"port":"/dev/a","baudrat":19200}]', defaults)


def test_gmcmap_can_use_per_device_counter_ids_without_legacy_mapping():
    settings = _settings(
        devices=(
            DeviceConfig(port="/dev/a", gmcmap_counter_id="0034021"),
            DeviceConfig(port="/dev/b", gmcmap_counter_id="0034022"),
        ),
        gmcmap_enabled=True,
        gmcmap_privacy_confirmed=True,
        gmcmap_account_id="0230111",
        gmcmap_device_ids=(),
    )
    settings.validate()


def test_from_env_reads_nested_devices_json():
    env = {
        "PORT": "/dev/default",
        "PORTS": "",
        "DEVICES_JSON": '[{"port":"/dev/a","name":"Keller","baudrate":19200},{"port":"/dev/b","name":"Wohnzimmer","baudrate":115200}]',
        "BAUDRATE": "19200",
        "SCAN_INTERVAL": "60",
        "COMMAND_TIMEOUT": "2.0",
        "INTER_COMMAND_DELAY_MS": "150",
        "HIGH_CPM_THRESHOLD": "10000",
        "HIGH_CPM_CONFIRMATIONS": "3",
        "READ_GYRO": "false",
        "READ_DEVICE_TIME": "true",
        "DEVICE_CLOCK_WARNING_SECONDS": "120",
        "HEARTBEAT_ENABLED": "false",
        "HISTORY_RETENTION_DAYS": "90",
        "REPORT_TIMEZONE": "Europe/Berlin",
        "MQTT_HOST": "localhost",
        "MQTT_PORT": "1883",
        "CPM_PER_USVH": "154.0",
    }
    with patch.dict(os.environ, env, clear=True):
        settings = Settings.from_env()
    assert [device.name for device in settings.devices] == ["Keller", "Wohnzimmer"]
    assert [device.baudrate for device in settings.devices] == [19200, 115200]


def test_dashboard_and_reports_use_selected_device_settings():
    with tempfile.TemporaryDirectory() as temp_dir:
        store = HistoryStore(Path(temp_dir) / "history.sqlite3")
        store.upsert_device_registry(
            "SERIAL-A",
            {
                "configured_name": "Keller",
                "device_model": "GMC-320Re 4.52",
                "port": "/dev/a",
                "baudrate": 19200,
                "scan_interval_seconds": 60,
                "cpm_per_usvh": 154.0,
            },
        )
        store.upsert_device_registry(
            "SERIAL-B",
            {
                "configured_name": "Wohnzimmer",
                "device_model": "GMC-500+ 2.20",
                "port": "/dev/b",
                "baudrate": 115200,
                "scan_interval_seconds": 30,
                "cpm_per_usvh": 100.0,
            },
        )
        store.insert_measurement({"cpm": 10}, device_serial="SERIAL-A", timestamp_utc=1_800_000_000)
        store.insert_measurement({"cpm": 20}, device_serial="SERIAL-B", timestamp_utc=1_800_000_000)
        app = ReportApplication(
            store=store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
            ui_language="de",
        )
        assert app._device_report_settings("SERIAL-B") == (30, 100.0)
        page = app.render_index(
            language_override="de", device_override="SERIAL-B", report_device_override="SERIAL-B"
        ).decode("utf-8")
        assert "Wohnzimmer" in page
        assert "115.200" in page
        assert "100,0" in page
        assert "0,200 µSv/h" in page


def test_all_languages_translate_every_per_device_field():
    import yaml

    root = Path(__file__).parents[1]
    config = yaml.safe_load((root / "config.yaml").read_text())
    expected = set(config["schema"]["devices"][0])
    for path in sorted((root / "translations").glob("*.yaml")):
        translated = yaml.safe_load(path.read_text())["configuration"]["devices"]
        assert set(translated["fields"]) == expected
        assert all(field["name"] and field["description"] for field in translated["fields"].values())
