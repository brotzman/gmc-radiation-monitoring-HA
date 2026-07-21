from pathlib import Path

from gmc_bridge.serial_device import SerialGmc
from gmc_bridge.version import APP_VERSION


def test_release_692_version_notes_and_dirty_gyro_parser_are_packaged() -> None:
    root = Path(__file__).parents[1]
    assert APP_VERSION == "8.4.1"
    assert (root / "RELEASE_NOTES_8.4.1.md").is_file()
    source = (root / "rootfs/usr/local/lib/gmc_bridge/serial_device.py").read_text()
    assert "_extract_terminated_frame" in source
    assert "Recovered %s frame from contaminated serial response" in source


def test_observed_getgyro_burst_extracts_the_valid_frame() -> None:
    raw = bytes.fromhex("ff 00 70 01 10 c1 40 aa")
    frame = SerialGmc._extract_terminated_frame(raw, 7, "GETGYRO")
    assert frame == bytes.fromhex("00 70 01 10 c1 40 aa")
