from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_manual_serial_fields_are_absent_from_configuration():
    config = yaml.safe_load((ROOT / "config.yaml").read_text())

    assert config["version"] == "8.1.0"
    assert config["uart"] is True
    assert len(config["options"]["devices"]) == 2
    for device in config["options"]["devices"]:
        assert "port" not in device
        assert "baudrate" not in device
    device_schema = config["schema"]["devices"][0]
    assert "port" not in device_schema
    assert "baudrate" not in device_schema
    assert "automatic_serial_detection" not in config["options"]["system"]
    assert "automatic_serial_detection" not in config["schema"]["system"]


def test_manual_serial_fields_are_absent_from_translations():
    for language in ("de", "en", "es", "fr", "it", "nl", "pl", "hr"):
        translations = yaml.safe_load((ROOT / "translations" / f"{language}.yaml").read_text())
        device_fields = translations["configuration"]["devices"]["fields"]
        system_fields = translations["configuration"]["system"]["fields"]
        assert "port" not in device_fields
        assert "baudrate" not in device_fields
        assert "automatic_serial_detection" not in system_fields
