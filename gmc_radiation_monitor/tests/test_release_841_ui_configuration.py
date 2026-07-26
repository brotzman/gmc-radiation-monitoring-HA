from __future__ import annotations

import json
from pathlib import Path

import yaml
from gmc_bridge.calibration_web import render_calibration_panel
from gmc_bridge.options_migration import merge_single_and_dual_device_options
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
    assert APP_VERSION == "9.2.0"
    assert config["version"] == "9.2.0"


def test_supervisor_configuration_has_one_entry_per_physical_device() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    single_schema = config["schema"]["devices"][0]
    dual_schema = config["schema"]["dual_tube_devices"][0]
    single_options = config["options"]["devices"]
    dual_options = config["options"]["dual_tube_devices"]

    assert DUAL_KEYS.isdisjoint(single_schema)
    assert set(dual_schema) >= DUAL_KEYS | {
        "scan_interval",
        "detector_profile",
        "cpm_per_usvh",
        "dead_time_us",
        "tube_model",
    }
    assert [item["name"] for item in single_options] == ["GMC-320"]
    assert [item["name"] for item in dual_options] == ["GMC-500+"]
    assert dual_options[0]["detector_profile"] == "gmc_500_plus"
    assert dual_options[0]["dual_tube_mode"] == "separate"
    assert dual_options[0]["high_dose_tube_model"] == "SI-3BG"

    for path in (ROOT / "translations").glob("*.yaml"):
        translation = yaml.safe_load(path.read_text(encoding="utf-8"))["configuration"]
        assert DUAL_KEYS.isdisjoint(translation["devices"]["fields"])
        assert set(translation["dual_tube_devices"]["fields"]) >= set(dual_schema)


def test_legacy_split_gmc500_options_migrate_losslessly() -> None:
    legacy = {
        "devices": [
            {"name": "GMC-320", "scan_interval": 120, "detector_profile": "gmc_320_plus_v4"},
            {
                "name": "GMC-500+",
                "scan_interval": 75,
                "detector_profile": "gmc_500_plus",
                "orientation_calibration_enabled": True,
                "orientation_calibration_serial": "serial-500",
            },
        ],
        "dual_tube_devices": [
            {
                "name": "GMC-500+",
                "device_serial": "SERIAL-500",
                "dual_tube_mode": "separate",
                "dual_tube_switch_cpm": 30000,
                "high_dose_tube_model": "SI-3BG",
            }
        ],
    }
    migrated, changed = merge_single_and_dual_device_options(legacy)
    assert changed is True
    assert [item["name"] for item in migrated["devices"]] == ["GMC-320"]
    assert len(migrated["dual_tube_devices"]) == 1
    gmc500 = migrated["dual_tube_devices"][0]
    assert gmc500["scan_interval"] == 75
    assert gmc500["orientation_calibration_serial"] == "serial-500"
    assert gmc500["device_serial"] == "SERIAL-500"
    assert gmc500["high_dose_tube_model"] == "SI-3BG"
    assert merge_single_and_dual_device_options(migrated) == (migrated, False)


def test_complete_gmc500_entry_is_emitted_once_without_affecting_gmc320() -> None:
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


def test_detector_profile_card_moves_conversion_factor_into_tube_card() -> None:
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

    assert "Detektorprofil" in panel
    assert "Aktuelle CPM" not in panel
    assert "<dt>Umrechnungsfaktor</dt>" in panel
    assert "154\xa0CPM/(µSv/h)" in panel
    assert "measurement-quality-card" not in panel
    assert "Ein physisches Zählrohr" in panel
    assert "<dt>Totzeit</dt>" in panel
    assert "<dt>Modell</dt>" in panel


def test_expert_statistics_have_explicit_label_value_spacing() -> None:
    assert ".expert-statistics > div" in DASHBOARD_CSS
    assert "column-gap:1rem" in DASHBOARD_CSS
    assert "grid-template-columns:minmax(10.5rem,36%)" in DASHBOARD_CSS
    assert 'body[data-analysis-level="expert"] .device-grid { grid-template-columns:1fr; }' in DASHBOARD_CSS
    assert ".calibration-grid > :only-child" in DASHBOARD_CSS
    assert ".tube-profile-grid > :only-child" in DASHBOARD_CSS


def test_public_package_contains_no_installation_specific_orientation_defaults() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    devices = config["options"]["devices"] + config["options"]["dual_tube_devices"]
    assert all(not item.get("orientation_calibration_enabled") for item in devices)
    assert all(not item.get("orientation_calibration_serial") for item in devices)
    orientation = (ROOT / "rootfs/usr/local/lib/gmc_bridge/orientation.py").read_text(encoding="utf-8")
    assert "BUILTIN_CALIBRATIONS: dict[str, AccelerometerCalibration] = {}" in orientation
    assert "f488c59b0031f0" not in orientation
    assert "080048303838a0" not in orientation


def test_startup_persists_legacy_split_options_with_supervisor_api() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert config["hassio_api"] is True
    run_script = (ROOT / "rootfs/etc/services.d/gmc/run").read_text(encoding="utf-8")
    migration_script = (ROOT / "rootfs/usr/local/bin/gmc_options_migrate.py").read_text(
        encoding="utf-8"
    )
    supervisor_module = (
        ROOT / "rootfs/usr/local/lib/gmc_bridge/supervisor_options.py"
    ).read_text(encoding="utf-8")
    assert "gmc_options_migrate.py" in run_script
    assert "bashio::addon.option" not in run_script
    assert "jq " not in run_script
    assert "persist_self_options" in migration_script
    assert "http://supervisor/addons/self/options" in supervisor_module
    assert '{"options": options}' in supervisor_module
