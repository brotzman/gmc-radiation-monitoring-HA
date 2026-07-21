from __future__ import annotations

import json

from gmc_bridge.orientation import calculate_orientation, orientation_status


def _calibration(serial: str) -> dict[str, object]:
    if serial == "080048303838a0":
        return {
            "orientation_calibration_enabled": True,
            "orientation_calibration_serial": serial,
            "orientation_offset_x": 84.000,
            "orientation_offset_y": -112.500,
            "orientation_offset_z": -193.905,
            "orientation_scale_x": 16380.000,
            "orientation_scale_y": 15951.500,
            "orientation_scale_z": 15879.235,
            "orientation_calibration_name": "Test GMC-500+ calibration",
        }
    return {
        "orientation_calibration_enabled": True,
        "orientation_calibration_serial": serial,
        "orientation_offset_x": 25.385,
        "orientation_offset_y": 0.430,
        "orientation_offset_z": 18.430,
        "orientation_scale_x": 263.285,
        "orientation_scale_y": 261.430,
        "orientation_scale_z": 254.570,
        "orientation_calibration_name": "Test GMC-320 calibration",
    }


def _enable(monkeypatch, *serials: str) -> None:
    monkeypatch.setenv("DEVICES_JSON", json.dumps([_calibration(serial) for serial in serials]))


def test_gmc500_reference_positions_are_reconstructed(monkeypatch):
    _enable(monkeypatch, "080048303838a0")
    right = calculate_orientation("080048303838a0", 16480, 96, -96)
    assert right is not None
    assert right.position_key == "USB right"
    assert 88.0 <= right.roll_degrees <= 92.0
    assert abs(right.pitch_degrees) < 2.0
    assert 88.0 <= right.inclination_degrees <= 92.0

    display_up = calculate_orientation("080048303838a0", 64, -144, -16096)
    assert display_up is not None
    assert display_up.position_key == "Display up"
    assert display_up.inclination_degrees < 2.0
    assert 0.97 <= display_up.gravity_magnitude <= 1.03


def test_gmc320_reference_positions_are_reconstructed(monkeypatch):
    _enable(monkeypatch, "f488c59b0031f0")
    usb_down = calculate_orientation("f488c59b0031f0", 24, -261, 17)
    assert usb_down is not None
    assert usb_down.position_key == "USB down"
    assert usb_down.pitch_degrees < -88.0
    assert 88.0 <= usb_down.inclination_degrees <= 92.0

    display_down = calculate_orientation("f488c59b0031f0", 30, 2, 273)
    assert display_down is not None
    assert display_down.position_key == "Display down"
    assert display_down.inclination_degrees > 178.0


def test_unknown_serial_has_no_calibration():
    assert calculate_orientation("unknown", 1, 2, 3) is None


def test_connected_device_card_shows_calibrated_angles(tmp_path, monkeypatch):
    _enable(monkeypatch, "080048303838a0")
    from gmc_bridge.history import HistoryStore
    from gmc_bridge.report_web import ReportApplication

    store = HistoryStore(tmp_path / "history.sqlite3")
    serial = "080048303838a0"
    store.upsert_device_registry(
        serial,
        {
            "device_model": "GMC-500+",
            "port": "/dev/ttyUSB0",
            "runtime_online": True,
            "device_profile_name": "GMC-500 family",
        },
    )
    store.set_device_capabilities(serial, {"cpm": True, "gyro": True})
    store.insert_measurement(
        {"cpm": 17, "gyro_x": 16480, "gyro_y": 96, "gyro_z": -96},
        device_serial=serial,
        timestamp_utc=1_800_000_000,
    )
    listed = store.list_devices()[0]
    assert listed["gyro_x"] == 16480
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=75,
        read_gyro=True,
        cpm_per_usvh=154.0,
    )
    page = app.render_index(language_override="de", device_override=serial).decode("utf-8")
    assert "Gerätelage" in page
    assert "Hochkant, USB rechts" in page
    assert "Rollwinkel" in page and "+90." in page
    assert "Flach" not in page  # this reference is upright
    assert "Hochkant" in page
    assert "Kalibrierte Beschleunigung" not in page
    assert "Beschleunigungs-Rohwerte" not in page
    assert "Beschleunigungsbetrag" not in page
    assert "Kalibrierprofil" not in page


def test_configured_calibration_overrides_defaults(monkeypatch):

    monkeypatch.setenv(
        "DEVICES_JSON",
        json.dumps(
            [
                {
                    "orientation_calibration_enabled": True,
                    "orientation_calibration_serial": "080048303838a0",
                    "orientation_offset_x": 0,
                    "orientation_offset_y": 0,
                    "orientation_offset_z": 0,
                    "orientation_scale_x": 100,
                    "orientation_scale_y": 100,
                    "orientation_scale_z": 100,
                    "orientation_calibration_name": "Test override",
                }
            ]
        ),
    )
    result = calculate_orientation("080048303838a0", 100, 0, 0)
    assert result is not None
    assert result.position_key == "USB right"
    assert 0.99 <= result.gravity_magnitude <= 1.01


def test_configured_calibration_can_be_disabled(monkeypatch):

    monkeypatch.setenv(
        "DEVICES_JSON",
        json.dumps(
            [
                {
                    "orientation_calibration_enabled": False,
                    "orientation_calibration_serial": "080048303838a0",
                }
            ]
        ),
    )
    assert calculate_orientation("080048303838a0", 16480, 96, -96) is None


def test_orientation_status_colors(monkeypatch):
    _enable(monkeypatch, "080048303838a0")
    display_up = calculate_orientation("080048303838a0", 64, -144, -16096)
    upright = calculate_orientation("080048303838a0", 16480, 96, -96)
    display_down = calculate_orientation("080048303838a0", 144, -16, 15696)
    assert display_up and orientation_status(display_up) == ("Flat", "green")
    assert upright and orientation_status(upright) == ("Upright", "blue")
    assert display_down and orientation_status(display_down) == ("Display down", "red")
