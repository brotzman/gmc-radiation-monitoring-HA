from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "rootfs/usr/local/lib"))

from gmc_bridge.config import Settings
from gmc_bridge.device_profiles import DeviceCapabilities
from gmc_bridge.serial_device import read_sample


def _settings(devices: list[dict]) -> Settings:
    import os

    values = {
        "PORT": "/dev/ttyUSB0",
        "PORTS": "",
        "DEVICES_JSON": json.dumps(devices),
        "BAUDRATE": "19200",
        "SCAN_INTERVAL": "60",
        "COMMAND_TIMEOUT": "2",
        "INTER_COMMAND_DELAY_MS": "150",
        "HIGH_CPM_THRESHOLD": "10000",
        "HIGH_CPM_CONFIRMATIONS": "3",
        "READ_GYRO": "false",
        "READ_DEVICE_TIME": "false",
        "HEARTBEAT_ENABLED": "false",
        "HISTORY_RETENTION_DAYS": "90",
        "REPORT_TIMEZONE": "Europe/Berlin",
        "MQTT_HOST": "localhost",
        "MQTT_PORT": "1883",
    }
    old = dict(os.environ)
    try:
        os.environ.update(values)
        return Settings.from_env()
    finally:
        os.environ.clear()
        os.environ.update(old)


def test_new_per_device_serial_timing_options_parse():
    settings = _settings(
        [
            {
                "port": "/dev/ttyUSB0",
                "serial_startup_delay": 15,
                "auxiliary_read_interval": 300,
            }
        ]
    )
    device = settings.devices[0]
    assert device.serial_startup_delay == 15.0
    assert device.auxiliary_read_interval == 300


def test_new_timing_defaults_are_stable():
    settings = _settings([{"port": "/dev/ttyUSB0"}])
    device = settings.devices[0]
    assert device.serial_startup_delay is None
    assert device.auxiliary_read_interval == 300


def test_read_sample_can_skip_all_optional_commands():
    class Device:
        def __init__(self):
            self.calls = []

        def get_cpm(self):
            self.calls.append("cpm")
            return 42

        def get_temperature_c(self):
            self.calls.append("temperature")
            return 20.0

        def get_voltage_v(self):
            self.calls.append("voltage")
            return 4.0

        def get_low_dose_tube_cpm(self):
            self.calls.append("low")
            return 20

        def get_high_dose_tube_cpm(self):
            self.calls.append("high")
            return 22

    device = Device()
    result = read_sample(
        device,
        False,
        DeviceCapabilities(cpm=True, temperature=True, voltage=True, dual_tube=True),
        read_optional_channels=False,
    )
    assert result.state == {"cpm": 42}
    assert device.calls == ["cpm"]
    assert result.reconnect_required is False


def test_serial_startup_stagger_never_falls_below_15_seconds_per_device():
    from gmc_bridge.serial_autoconfig import effective_serial_startup_delay

    assert effective_serial_startup_delay(None, 0) == 0.0
    assert effective_serial_startup_delay(0, 1) == 15.0
    assert effective_serial_startup_delay(10, 1) == 15.0
    assert effective_serial_startup_delay(25, 1) == 25.0
    assert effective_serial_startup_delay(15, 2) == 30.0
    assert effective_serial_startup_delay(45, 2) == 45.0


def test_serial_startup_stagger_preserves_order_after_large_first_delay():
    from gmc_bridge.serial_autoconfig import effective_serial_startup_delays

    assert effective_serial_startup_delays([30, 15, None]) == (30.0, 45.0, 60.0)
    assert effective_serial_startup_delays([0, 40, 41]) == (0.0, 40.0, 55.0)
