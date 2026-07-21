from __future__ import annotations

import json
from pathlib import Path

import yaml
from gmc_bridge.calibration_web import render_calibration_panel
from gmc_bridge.config import Settings
from gmc_bridge.translations import Translator

ROOT = Path(__file__).parents[1]


def _defaults() -> Settings:
    return Settings(
        port="/dev/ttyUSB0",
        baudrate=19200,
        scan_interval=60,
        command_timeout=3.0,
        inter_command_delay_ms=250,
        high_cpm_threshold=10000,
        high_cpm_confirmations=3,
        read_gyro=False,
        mqtt_host="localhost",
        mqtt_port=1883,
        mqtt_username="",
        mqtt_password="",
    )


def _device(payload: dict[str, object]):
    return Settings._parse_devices_json(json.dumps([payload]), _defaults())[0]


def test_gmc320_preset_supplies_single_tube_working_values() -> None:
    device = _device(
        {
            "port": "/dev/ttyUSB0",
            "name": "GMC-320",
            "detector_profile": "gmc_320_plus_v4",
        }
    )

    assert device.detector_profile == "gmc_320_plus_v4"
    assert device.dual_tube_mode == "single"
    assert device.tube_model == "M4011"
    assert device.cpm_per_usvh == 154.0
    assert device.dead_time_us == 120.0
    assert device.reliable_max_cpm == 50_000
    assert device.dead_time_model == "nonparalyzable"
    assert device.conversion_factor_uncertainty_percent == 20.0
    assert device.high_dose_tube is None
    assert device.calibration_status() == "predefined"


def test_gmc320_preset_ignores_stale_second_tube_fields() -> None:
    device = _device(
        {
            "port": "/dev/ttyUSB0",
            "name": "GMC-320",
            "detector_profile": "gmc_320_plus_v4",
            "dual_tube_mode": "separate",
            "dual_tube_switch_cpm": 30_000,
            "high_dose_tube_model": "SI-3BG",
            "high_dose_cpm_per_usvh": 5.15,
        }
    )

    assert device.dual_tube_mode == "single"
    assert device.dual_tube_switch_cpm is None
    assert device.high_dose_tube is None


def test_gmc500_preset_keeps_si3bg_uncalibrated() -> None:
    device = _device(
        {
            "port": "/dev/ttyUSB1",
            "name": "GMC-500+",
            "detector_profile": "gmc_500_plus",
        }
    )

    assert device.dual_tube_mode == "separate"
    assert device.tube_model == "M4011"
    assert device.reliable_max_cpm == 30_000
    assert device.high_dose_tube is not None
    assert device.high_dose_tube.tube_model == "SI-3BG"
    assert device.high_dose_tube.cpm_per_usvh is None
    assert device.calibration_status() == "incomplete"


def test_explicit_primary_override_is_marked_customized() -> None:
    device = _device(
        {
            "port": "/dev/ttyUSB0",
            "name": "GMC-320",
            "detector_profile": "gmc_320_plus_v4",
            "dead_time_us": 200.0,
        }
    )
    assert device.dead_time_us == 200.0
    assert device.calibration_overrides is True
    assert device.calibration_status() == "customized"


def test_supervisor_form_removes_duplicate_low_dose_fields() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    schema = config["schema"]["devices"][0]
    assert schema["detector_profile"].startswith("list(")
    assert not any(key.startswith("low_dose_") for key in schema)
    assert config["options"]["devices"][0]["detector_profile"] == "gmc_320_plus_v4"
    assert config["options"]["dual_tube_devices"][0]["detector_profile"] == "gmc_500_plus"

    for path in (ROOT / "translations").glob("*.yaml"):
        fields = yaml.safe_load(path.read_text(encoding="utf-8"))["configuration"]["devices"]["fields"]
        assert "detector_profile" in fields
        assert not any(key.startswith("low_dose_") for key in fields)


def test_single_tube_panel_does_not_render_dual_tube_details() -> None:
    device = _device(
        {
            "port": "/dev/ttyUSB0",
            "name": "GMC-320",
            "detector_profile": "gmc_320_plus_v4",
        }
    )
    item = {
        "configured_name": device.name,
        "detector_profile": device.detector_profile,
        "cpm_per_usvh": device.cpm_per_usvh,
        "dead_time_us": device.dead_time_us,
        "reliable_max_cpm": device.reliable_max_cpm,
        "dead_time_model": device.dead_time_model,
        "conversion_factor_uncertainty_percent": device.conversion_factor_uncertainty_percent,
        "calibration_reference": device.calibration_reference,
        "tube_model": device.tube_model,
        **device.calibration_registry_values(),
    }
    panel = render_calibration_panel(item=item, latest_cpm=20, t=Translator("de"))
    assert "Ein physisches Zählrohr" in panel
    assert "M4011" in panel
    assert "Zweites Zählrohr" not in panel
    assert "Umschaltung des zweiten Zählrohrs" not in panel
    assert panel.count("tube-profile-card") == 1
    assert panel.count("M4011") == 1
    assert "Aktuelle CPM" not in panel
    assert "154 CPM/(µSv/h)" not in panel
    assert "Detektorprofil" in panel
