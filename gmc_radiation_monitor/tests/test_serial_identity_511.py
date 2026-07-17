from pathlib import Path

from gmc_bridge.serial_device import SerialGmc


def _device_with_responses(*responses: bytes) -> SerialGmc:
    device = SerialGmc("/dev/null", 115200, timeout=1.0, delay_ms=0)
    values = iter(responses)
    device.request_until_idle = lambda *args, **kwargs: next(values)  # type: ignore[method-assign]
    device._recover_protocol_stream = lambda: None  # type: ignore[method-assign]
    return device


def test_service_imports_orientation_calculator():
    source = Path("rootfs/usr/local/lib/gmc_bridge/service.py").read_text()
    assert "from .orientation import calculate_orientation, calibration_for_serial" in source


def test_get_serial_ignores_leading_ff():
    device = _device_with_responses(bytes.fromhex("ff080048303838a0"))
    assert device.get_serial() == "080048303838a0"


def test_get_serial_ignores_trailing_ff():
    device = _device_with_responses(bytes.fromhex("080048303838a0ff"))
    assert device.get_serial() == "080048303838a0"


def test_get_serial_prefers_expected_serial_inside_dirty_response():
    device = _device_with_responses(bytes.fromhex("aa080048303838a0ff"))
    assert device.get_serial(expected_serial="080048303838a0") == "080048303838a0"
