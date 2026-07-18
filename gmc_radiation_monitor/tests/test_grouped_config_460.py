from __future__ import annotations

from pathlib import Path

import yaml

ROOT = Path(__file__).parents[1]
BRIDGE_RUN = ROOT / "rootfs/etc/services.d/gmc/run"
REPORT_RUN = ROOT / "rootfs/etc/services.d/gmc-reports/run"


def test_visible_configuration_has_only_devices_and_shared_sections():
    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    assert config["version"] == "8.2.1"
    assert list(config["options"]) == [
        "devices",
        "gmcmap",
        "history",
        "analysis",
        "safety",
        "interface",
        "system",
    ]
    assert list(config["schema"]) == list(config["options"])
    devices = config["options"]["devices"]
    assert [device["name"] for device in devices] == ["GMC-320", "GMC-500+"]
    assert devices[0] == {
        "name": "GMC-320",
        "scan_interval": 60,
        "command_timeout": 3.0,
        "inter_command_delay_ms": 250,
        "serial_startup_delay": 0,
        "auxiliary_read_interval": 300,
        "read_gyro": False,
        "read_device_time": False,
        "device_clock_warning_seconds": 120,
        "heartbeat_enabled": False,
        "cpm_per_usvh": 154.0,
        "gmcmap_counter_id": "",
        "serial_debug": False,
        "serial_debug_max_bytes": 64,
        "orientation_calibration_enabled": True,
        "orientation_calibration_serial": "f488c59b0031f0",
        "orientation_offset_x": 25.385,
        "orientation_offset_y": 0.430,
        "orientation_offset_z": 18.430,
        "orientation_scale_x": 263.285,
        "orientation_scale_y": 261.430,
        "orientation_scale_z": 254.570,
        "orientation_calibration_name": "GMC-320 six-position calibration",
    }
    assert devices[1] == {
        "name": "GMC-500+",
        "scan_interval": 75,
        "command_timeout": 4.0,
        "inter_command_delay_ms": 600,
        "serial_startup_delay": 15,
        "auxiliary_read_interval": 300,
        "read_gyro": False,
        "read_device_time": False,
        "device_clock_warning_seconds": 120,
        "heartbeat_enabled": False,
        "cpm_per_usvh": 154.0,
        "gmcmap_counter_id": "",
        "serial_debug": False,
        "serial_debug_max_bytes": 64,
        "orientation_calibration_enabled": True,
        "orientation_calibration_serial": "080048303838a0",
        "orientation_offset_x": 84.000,
        "orientation_offset_y": -112.500,
        "orientation_offset_z": -193.905,
        "orientation_scale_x": 16380.000,
        "orientation_scale_y": 15951.500,
        "orientation_scale_z": 15879.235,
        "orientation_calibration_name": "GMC-500+ six-position calibration",
    }
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
        "cpm_per_usvh",
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
    assert "Keller GMC-320Re" in readme
    assert "Wohnzimmer GMC-500+" in readme
    assert "Serial ports and baud rates are discovered automatically" in readme
    assert "gmcmap:\n  enabled:" in readme
    assert "history:\n  retention_days:" in readme
