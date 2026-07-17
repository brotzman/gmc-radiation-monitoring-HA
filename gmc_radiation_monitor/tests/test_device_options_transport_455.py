from __future__ import annotations

import json
from pathlib import Path

from gmc_bridge.config import Settings
from gmc_bridge.runtime_options import runtime_environment

ROOT = Path(__file__).parents[1]
RUN_SCRIPT = ROOT / "rootfs/etc/services.d/gmc/run"


def _extract_devices(options: dict[str, object]) -> str:
    return runtime_environment(options, "bridge")["DEVICES_JSON"]


def _defaults() -> Settings:
    return Settings(
        port="/dev/default",
        ports=("/dev/default",),
        baudrate=19200,
        scan_interval=60,
        command_timeout=2.0,
        inter_command_delay_ms=150,
        high_cpm_threshold=10000,
        high_cpm_confirmations=3,
        read_gyro=False,
        mqtt_host="localhost",
        mqtt_port=1883,
        mqtt_username="",
        mqtt_password="",
    )


def test_start_script_preserves_devices_as_json_array():
    script = RUN_SCRIPT.read_text()
    assert "bashio::config 'devices'" not in script
    assert "/data/options.json" in script
    assert "gmc_runtime_env.py bridge" in script
    assert "jq " not in script


def test_one_device_remains_a_list_and_parses():
    payload = _extract_devices(
        {
            "devices": [
                {
                    "port": "/dev/serial/by-id/gmc320",
                    "name": "GMC-320Re",
                    "baudrate": 19200,
                }
            ]
        }
    )
    assert json.loads(payload)[0]["name"] == "GMC-320Re"
    parsed = Settings._parse_devices_json(payload, _defaults())
    assert len(parsed) == 1
    assert parsed[0].baudrate == 19200


def test_two_mixed_devices_remain_one_array_and_parse():
    payload = _extract_devices(
        {
            "devices": [
                {
                    "port": "/dev/serial/by-id/gmc320",
                    "name": "GMC-320Re",
                    "baudrate": 19200,
                },
                {
                    "port": "/dev/serial/by-id/gmc500plus",
                    "name": "GMC-500+",
                    "baudrate": 115200,
                    "heartbeat_enabled": True,
                },
            ]
        }
    )
    raw = json.loads(payload)
    assert isinstance(raw, list)
    assert len(raw) == 2
    parsed = Settings._parse_devices_json(payload, _defaults())
    assert [device.baudrate for device in parsed] == [19200, 115200]
    assert parsed[1].heartbeat_enabled is True


def test_missing_devices_becomes_empty_array():
    assert _extract_devices({}) == "[]"
