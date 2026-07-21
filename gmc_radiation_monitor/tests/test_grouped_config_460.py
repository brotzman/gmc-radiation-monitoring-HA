from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
BRIDGE_RUN = ROOT / "rootfs/etc/services.d/gmc/run"
REPORT_RUN = ROOT / "rootfs/etc/services.d/gmc-reports/run"


def test_visible_configuration_has_only_devices_and_shared_sections():
    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    assert config["version"] == "8.4.6"
    assert list(config["options"]) == [
        "devices",
        "dual_tube_devices",
        "gmcmap",
        "history",
        "analysis",
        "safety",
        "interface",
        "system",
    ]
    assert list(config["schema"]) == list(config["options"])
    devices = config["options"]["devices"]
    dual_devices = config["options"]["dual_tube_devices"]
    assert [device["name"] for device in devices] == ["GMC-320"]
    assert [device["name"] for device in dual_devices] == ["GMC-500+"]
    gmc320 = devices[0]
    assert gmc320["scan_interval"] == 60
    assert gmc320["detector_profile"] == "gmc_320_plus_v4"
    for redundant in (
        "cpm_per_usvh", "dead_time_us", "reliable_max_cpm", "dead_time_model",
        "conversion_factor_uncertainty_percent", "calibration_uncertainty_percent",
        "calibration_reference", "tube_model", "dual_tube_mode", "dual_tube_switch_cpm",
    ):
        assert redundant not in gmc320
    assert "low_dose_tube" not in gmc320
    assert "high_dose_tube" not in gmc320
    assert gmc320["orientation_calibration_enabled"] is False
    assert "orientation_calibration_serial" not in gmc320

    gmc500 = dual_devices[0]
    assert gmc500["scan_interval"] == 75
    assert gmc500["detector_profile"] == "gmc_500_plus"
    for redundant in (
        "cpm_per_usvh", "dead_time_us", "reliable_max_cpm", "dead_time_model",
        "conversion_factor_uncertainty_percent", "calibration_uncertainty_percent",
        "calibration_reference", "tube_model",
    ):
        assert redundant not in gmc500
    assert gmc500["dual_tube_mode"] == "separate"
    assert gmc500["dual_tube_switch_cpm"] == 30000
    assert gmc500["high_dose_tube_model"] == "SI-3BG"
    assert "low_dose_tube" not in gmc500
    assert "high_dose_tube" not in gmc500
    assert gmc500["orientation_calibration_enabled"] is False
    assert "orientation_calibration_serial" not in gmc500

    assert config["options"]["gmcmap"] == {
        "enabled": False,
        "privacy_confirmed": False,
        "account_id": "",
        "upload_interval": 300,
        "timeout": 10.0,
    }

    removed_flat_duplicates = {
        "port",
        "ports",
        "baudrate",
        "scan_interval",
        "command_timeout",
        "inter_command_delay_ms",
        "serial_startup_delay",
        "auxiliary_read_interval",
        "read_gyro",
        "read_device_time",
        "device_clock_warning_seconds",
        "heartbeat_enabled",
        "detector_profile",
        "cpm_per_usvh",
        "gmcmap_enabled",
        "gmcmap_account_id",
        "history_retention_days",
        "report_timezone",
        "ui_mode",
        "ui_language",
        "log_level",
    }
    assert removed_flat_duplicates.isdisjoint(config["schema"])


def test_each_device_owns_all_connection_and_measurement_settings():
    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    device_schema = config["schema"]["devices"][0]
    fields = set(device_schema)
    assert fields == {
        "name",
        "scan_interval",
        "command_timeout",
        "inter_command_delay_ms",
        "serial_startup_delay",
        "auxiliary_read_interval",
        "read_gyro",
        "read_device_time",
        "device_clock_warning_seconds",
        "heartbeat_enabled",
        "detector_profile",
        "cpm_per_usvh",
        "dead_time_us",
        "reliable_max_cpm",
        "dead_time_model",
        "conversion_factor_uncertainty_percent",
        "calibration_uncertainty_percent",
        "calibration_reference",
        "tube_model",
        "gmcmap_counter_id",
        "serial_debug",
        "serial_debug_max_bytes",
        "orientation_calibration_enabled",
        "orientation_calibration_serial",
        "orientation_offset_x",
        "orientation_offset_y",
        "orientation_offset_z",
        "orientation_scale_x",
        "orientation_scale_y",
        "orientation_scale_z",
        "orientation_calibration_name",
    }
    assert "high_cpm_threshold" not in fields
    assert "high_cpm_confirmations" not in fields
    assert "gmcmap_upload_interval" not in fields
    assert "gmcmap_timeout" not in fields
    dual_schema = config["schema"]["dual_tube_devices"][0]
    assert dual_schema["dual_tube_mode"] == "list(separate|curve)"
    assert dual_schema["high_dose_tube_model"] == "str?"
    assert dual_schema["high_dose_cpm_per_usvh"] == "float(0.001,)?"
    assert dual_schema["high_dose_dead_time_us"] == "float(0.001,)?"
    assert dual_schema["high_dose_reliable_max_cpm"] == "int(1,)?"
    assert dual_schema["high_dose_dead_time_model"] == "list(none|nonparalyzable)?"
    assert set(config["schema"]["gmcmap"]) == {
        "enabled",
        "privacy_confirmed",
        "account_id",
        "upload_interval",
        "timeout",
    }


def test_service_scripts_use_one_python_grouped_options_loader():
    bridge = BRIDGE_RUN.read_text()
    report = REPORT_RUN.read_text()

    assert "gmc_runtime_env.py bridge" in bridge
    assert "gmc_runtime_env.py reports" in report
    assert "jq " not in bridge
    assert "jq " not in report
    assert "automatic_serial_detection" not in bridge
    assert "Automatic GMC port and baud-rate detection enabled" in bridge
    assert "gmc_auto_bridge.py" in bridge
    assert "Manual serial override" not in bridge
    assert "Legacy 4.5.x flat options detected" not in bridge


def test_readme_documents_mixed_gmc_320_and_500_plus_configuration():
    readme = (ROOT / "README.md").read_text()
    assert "Keller GMC-320" in readme
    assert "Wohnzimmer GMC-500+" in readme
    assert "detector_profile: gmc_320_plus_v4" in readme
    assert "detector_profile: gmc_500_plus" in readme
    assert "Serial ports and baud rates are discovered automatically" in readme
    assert "gmcmap:\n  enabled:" in readme
    assert "history:\n  retention_days:" in readme
