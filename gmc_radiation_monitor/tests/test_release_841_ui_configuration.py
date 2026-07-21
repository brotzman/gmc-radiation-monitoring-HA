from __future__ import annotations

import json
from pathlib import Path

import yaml
from gmc_bridge.calibration_web import render_calibration_panel
from gmc_bridge.runtime_options import runtime_environment
from gmc_bridge.translations import Translator
from gmc_bridge.version import APP_VERSION
from gmc_bridge.web_assets import DASHBOARD_CSS

ROOT = Path(__file__).parents[1]
DUAL_KEYS = {
    "dual_tube_mode",
    "dual_tube_switch_cpm",
    "high_dose_tube_model",
    "high_dose_cpm_per_usvh",
    "high_dose_dead_time_us",
    "high_dose_reliable_max_cpm",
    "high_dose_dead_time_model",
    "high_dose_conversion_factor_uncertainty_percent",
    "high_dose_calibration_uncertainty_percent",
    "high_dose_calibration_reference",
}


def test_release_metadata_is_841() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "8.4.1"
    assert config["version"] == "8.4.1"


def test_supervisor_configuration_separates_single_and_dual_tube_fields() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    device_schema = config["schema"]["devices"][0]
    dual_schema = config["schema"]["dual_tube_devices"][0]

    assert DUAL_KEYS.isdisjoint(device_schema)
    assert set(dual_schema) >= DUAL_KEYS
    assert config["options"]["dual_tube_devices"] == [
        {
            "name": "GMC-500+",
            "dual_tube_mode": "separate",
            "dual_tube_switch_cpm": 30000,
            "high_dose_tube_model": "SI-3BG",
            "high_dose_dead_time_us": 30.0,
            "high_dose_dead_time_model": "nonparalyzable",
            "high_dose_calibration_reference": (
                "No verified SI-3BG dose factor; CPM display only"
            ),
        }
    ]

    for path in (ROOT / "translations").glob("*.yaml"):
        translation = yaml.safe_load(path.read_text(encoding="utf-8"))["configuration"]
        assert DUAL_KEYS.isdisjoint(translation["devices"]["fields"])
        assert set(translation["dual_tube_devices"]["fields"]) >= DUAL_KEYS


def test_dedicated_gmc500_settings_merge_once_without_affecting_gmc320() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    env = runtime_environment(config["options"], "bridge")
    devices = json.loads(env["DEVICES_JSON"])
    gmc320 = next(item for item in devices if item["name"] == "GMC-320")
    gmc500 = next(item for item in devices if item["name"] == "GMC-500+")

    assert DUAL_KEYS.isdisjoint(gmc320)
    assert gmc500["dual_tube_mode"] == "separate"
    assert gmc500["dual_tube_switch_cpm"] == 30000
    assert gmc500["high_dose_tube_model"] == "SI-3BG"
    assert list(gmc500).count("high_dose_tube_model") == 1


def test_detector_profile_card_removes_repeated_cpm_and_conversion_factor() -> None:
    item = {
        "configured_name": "GMC-320",
        "detector_profile": "gmc_320_plus_v4",
        "dual_tube_mode": "single",
        "tube_model": "M4011",
        "cpm_per_usvh": 154.0,
        "dead_time_us": 120.0,
        "reliable_max_cpm": 50000,
        "dead_time_model": "nonparalyzable",
        "calibration_status": "predefined",
        "calibration_source": "manufacturer_profile",
    }
    panel = render_calibration_panel(item=item, latest_cpm=17, t=Translator("de"))

    assert "Detektor Profil" in panel
    assert "Aktuelle CPM" not in panel
    assert "154 CPM/(µSv/h)" not in panel
    assert "<dt>Totzeit</dt>" in panel
    assert "<dt>Modell</dt>" in panel


def test_expert_statistics_have_explicit_label_value_spacing() -> None:
    assert ".expert-statistics > div" in DASHBOARD_CSS
    assert "column-gap:.75rem" in DASHBOARD_CSS
    assert "grid-template-columns:minmax(9.5rem,max-content)" in DASHBOARD_CSS
