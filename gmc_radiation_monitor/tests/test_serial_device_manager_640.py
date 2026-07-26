from __future__ import annotations

from pathlib import Path

import yaml
from gmc_bridge.serial_autoconfig import resolve_automatic_devices
from gmc_bridge.serial_discovery import SerialDiscoveryService, SerialPortInfo

ROOT = Path(__file__).resolve().parents[1]


def _detected(
    path: str,
    model: str,
    serial: str,
    baudrate: int,
) -> SerialPortInfo:
    return SerialPortInfo(
        path=path,
        resolved_path=path,
        display_name=model,
        detail="GMC detected",
        category="gmc",
        suitable=True,
        exists=True,
        stable_path=True,
        detected_model=model,
        detected_serial=serial,
        detected_baudrate=baudrate,
        status="detected",
    )


def test_config_exposes_automatic_only_serial_profiles() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text())
    assert config["version"] == "9.1.2"
    assert "automatic_serial_detection" not in config["options"]["system"]
    assert "automatic_serial_detection" not in config["schema"]["system"]
    devices = config["options"]["devices"] + config["options"]["dual_tube_devices"]
    for device in devices:
        assert "port" not in device
        assert "baudrate" not in device

    translations = yaml.safe_load((ROOT / "translations" / "de.yaml").read_text())
    fields = translations["configuration"]["devices"]["fields"]
    assert "port" not in fields
    assert "baudrate" not in fields


def test_serial_discovery_prefers_stable_path_and_classifies_zigbee() -> None:
    stable = "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0"
    direct = "/dev/ttyUSB0"
    zigbee = "/dev/serial/by-id/usb-ITead_Sonoff_Zigbee_3.0_USB_Dongle_Plus-if00-port0"
    internal = "/dev/ttyAMA10"
    mapping = {
        stable: direct,
        direct: direct,
        zigbee: "/dev/ttyUSB1",
        internal: internal,
    }
    service = SerialDiscoveryService(
        path_provider=lambda: [direct, stable, zigbee, internal],
        realpath=lambda value: mapping.get(value, value),
        exists=lambda value: value in mapping or value in mapping.values(),
    )
    ports = service.discover(
        device_options=[],
        registry_devices=[],
    )
    by_path = {item.path: item for item in ports}
    assert stable in by_path
    assert direct not in by_path
    assert by_path[stable].suitable is True
    assert by_path[zigbee].suitable is False
    assert by_path[zigbee].status == "not_gmc"
    assert by_path[internal].category == "advanced"


def test_automatic_assignment_uses_serial_identity_and_detected_baudrate() -> None:
    configured = [
        {
            "name": "GMC-320",
            "port": "/dev/old320",
            "baudrate": 115200,
            "orientation_calibration_serial": "f488c59b0031f0",
            "scan_interval": 60,
        },
        {
            "name": "GMC-500+",
            "port": "/dev/old500",
            "baudrate": 19200,
            "orientation_calibration_serial": "080048303838a0",
            "scan_interval": 75,
        },
    ]
    # Reverse discovery order to prove that serial identity, not port order, wins.
    detected = [
        _detected(
            "/dev/serial/by-id/usb-1a86_USB_Serial-if00-port0",
            "GMC-500+",
            "080048303838a0",
            115200,
        ),
        _detected(
            "/dev/serial/by-id/usb-1a86_USB2.0-Serial-if00-port0",
            "GMC-320",
            "f488c59b0031f0",
            19200,
        ),
    ]

    resolved = resolve_automatic_devices(configured, detected)
    by_name = {item["name"]: item for item in resolved}
    assert by_name["GMC-320"]["port"].endswith("USB2.0-Serial-if00-port0")
    assert by_name["GMC-320"]["baudrate"] == 19200
    assert by_name["GMC-320"]["scan_interval"] == 60
    assert by_name["GMC-500+"]["port"].endswith("USB_Serial-if00-port0")
    assert by_name["GMC-500+"]["baudrate"] == 115200
    assert by_name["GMC-500+"]["scan_interval"] == 75


def test_automatic_assignment_connects_extra_detected_gmc() -> None:
    detected = [
        _detected("/dev/serial/by-id/gmc320", "GMC-320", "SERIAL320", 19200),
        _detected("/dev/serial/by-id/gmc600", "GMC-600+", "SERIAL600", 115200),
    ]
    resolved = resolve_automatic_devices([{"name": "GMC-320"}], detected)
    assert len(resolved) == 2
    assert {item["port"] for item in resolved} == {
        "/dev/serial/by-id/gmc320",
        "/dev/serial/by-id/gmc600",
    }
    extra = next(item for item in resolved if item["port"].endswith("gmc600"))
    assert extra["baudrate"] == 115200
    assert extra["serial_startup_delay"] is None
