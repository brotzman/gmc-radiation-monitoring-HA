from __future__ import annotations

import json
from pathlib import Path

import yaml
from gmc_bridge.config import Settings

ROOT = Path(__file__).parents[1]


def _defaults() -> Settings:
    return Settings(
        port="/dev/ttyUSB0", baudrate=19200, scan_interval=60, command_timeout=3.0,
        inter_command_delay_ms=250, high_cpm_threshold=10000, high_cpm_confirmations=3,
        read_gyro=False, mqtt_host="localhost", mqtt_port=1883, mqtt_username="", mqtt_password=""
    )


def test_supervisor_schema_has_no_mandatory_nested_tube_dictionary() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    device_schema = config["schema"]["devices"][0]
    assert "low_dose_tube" not in device_schema
    assert "high_dose_tube" not in device_schema
    assert "low_dose_tube_model" not in device_schema
    assert device_schema["detector_profile"].startswith("list(")
    assert device_schema["high_dose_tube_model"] == "str?"
    for device in config["options"]["devices"]:
        assert "low_dose_tube" not in device
        assert "high_dose_tube" not in device


def test_pre_833_device_options_parse_without_profile_placeholders() -> None:
    raw = [{
        "port": "/dev/ttyUSB0",
        "name": "GMC-500+",
        "scan_interval": 120,
        "cpm_per_usvh": 154.0,
        "dead_time_us": 120.0,
        "reliable_max_cpm": 30000,
        "dead_time_model": "nonparalyzable",
        "tube_model": "M4011 + SI-3BG (Dual)",
        "dual_tube_mode": "separate",
        "dual_tube_switch_cpm": 30000,
    }]
    device = Settings._parse_devices_json(json.dumps(raw), _defaults())[0]
    assert device.detector_profile == "gmc_500_plus"
    assert device.effective_low_dose_tube().tube_model == "M4011"
    assert device.high_dose_tube is not None
    assert device.high_dose_tube.tube_model == "SI-3BG"
    assert device.high_dose_tube.cpm_per_usvh is None
    assert device.calibration_status() == "incomplete"


def test_flat_high_dose_fields_build_a_separate_profile() -> None:
    raw = [{
        "port": "/dev/ttyUSB0",
        "name": "GMC-500+",
        "cpm_per_usvh": 154.0,
        "tube_model": "M4011 + SI-3BG (Dual)",
        "dual_tube_mode": "separate",
        "high_dose_tube_model": "SI-3BG",
        "high_dose_cpm_per_usvh": 5.15,
        "high_dose_dead_time_us": 30.0,
        "high_dose_dead_time_model": "nonparalyzable",
        "high_dose_calibration_reference": "Individual calibration",
    }]
    device = Settings._parse_devices_json(json.dumps(raw), _defaults())[0]
    assert device.high_dose_tube is not None
    assert device.high_dose_tube.cpm_per_usvh == 5.15
    assert device.high_dose_tube.dead_time_us == 30.0
