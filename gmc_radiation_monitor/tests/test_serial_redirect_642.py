from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_serial_assignment_page_and_routes_are_removed() -> None:
    source = (ROOT / "rootfs/usr/local/lib/gmc_bridge/report_web.py").read_text()
    assert 'href="./serial-devices' not in source
    assert 'path == "/serial-devices"' not in source
    assert 'path == "/serial-devices/save"' not in source
    assert "render_serial_devices" not in source
    assert "update_serial_device_assignments" not in source
