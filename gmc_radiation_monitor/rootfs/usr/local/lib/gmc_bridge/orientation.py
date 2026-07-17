from __future__ import annotations

import json
import os
from dataclasses import dataclass
from math import acos, atan2, degrees, sqrt


@dataclass(frozen=True)
class AccelerometerCalibration:
    offset_x: float
    offset_y: float
    offset_z: float
    scale_x: float
    scale_y: float
    scale_z: float
    profile_name: str


@dataclass(frozen=True)
class Orientation:
    gx: float
    gy: float
    gz: float
    roll_degrees: float
    pitch_degrees: float
    inclination_degrees: float
    gravity_magnitude: float
    position_key: str


BUILTIN_CALIBRATIONS: dict[str, AccelerometerCalibration] = {
    # GMC-320, serial f488c59b0031f0; six-position calibration from 2026-07-14.
    "f488c59b0031f0": AccelerometerCalibration(
        offset_x=25.385,
        offset_y=0.430,
        offset_z=18.430,
        scale_x=263.285,
        scale_y=261.430,
        scale_z=254.570,
        profile_name="GMC-320 six-position calibration",
    ),
    # GMC-500+, serial 080048303838a0; six-position calibration from 2026-07-14.
    "080048303838a0": AccelerometerCalibration(
        offset_x=84.000,
        offset_y=-112.500,
        offset_z=-193.905,
        scale_x=16380.000,
        scale_y=15951.500,
        scale_z=15879.235,
        profile_name="GMC-500+ six-position calibration",
    ),
}

_REFERENCE_POSITIONS: tuple[tuple[str, tuple[float, float, float]], ...] = (
    ("Display up", (0.0, 0.0, -1.0)),
    ("Display down", (0.0, 0.0, 1.0)),
    ("USB up", (0.0, 1.0, 0.0)),
    ("USB down", (0.0, -1.0, 0.0)),
    ("USB right", (1.0, 0.0, 0.0)),
    ("USB left", (-1.0, 0.0, 0.0)),
)


def _configured_calibration_overrides() -> dict[str, AccelerometerCalibration | None]:
    raw = os.environ.get("DEVICES_JSON", "").strip()
    if not raw:
        return {}
    try:
        devices = json.loads(raw)
    except (json.JSONDecodeError, TypeError):
        return {}
    if not isinstance(devices, list):
        return {}
    result: dict[str, AccelerometerCalibration | None] = {}
    for item in devices:
        if not isinstance(item, dict):
            continue
        serial = str(item.get("orientation_calibration_serial", "")).strip().lower()
        if not serial:
            continue
        if not item.get("orientation_calibration_enabled", False):
            result[serial] = None
            continue
        try:
            calibration = AccelerometerCalibration(
                offset_x=float(item.get("orientation_offset_x", 0.0)),
                offset_y=float(item.get("orientation_offset_y", 0.0)),
                offset_z=float(item.get("orientation_offset_z", 0.0)),
                scale_x=float(item.get("orientation_scale_x", 1.0)),
                scale_y=float(item.get("orientation_scale_y", 1.0)),
                scale_z=float(item.get("orientation_scale_z", 1.0)),
                profile_name=(
                    str(item.get("orientation_calibration_name", "Custom six-position calibration")).strip()
                    or "Custom six-position calibration"
                ),
            )
        except (TypeError, ValueError):
            continue
        if min(abs(calibration.scale_x), abs(calibration.scale_y), abs(calibration.scale_z)) < 1e-9:
            continue
        result[serial] = calibration
    return result


def calibration_for_serial(serial: str) -> AccelerometerCalibration | None:
    normalized = str(serial).strip().lower()
    overrides = _configured_calibration_overrides()
    if normalized in overrides:
        return overrides[normalized]
    return BUILTIN_CALIBRATIONS.get(normalized)


def calculate_orientation(
    serial: str,
    raw_x: int | float,
    raw_y: int | float,
    raw_z: int | float,
) -> Orientation | None:
    calibration = calibration_for_serial(serial)
    if calibration is None:
        return None

    gx = (float(raw_x) - calibration.offset_x) / calibration.scale_x
    gy = (float(raw_y) - calibration.offset_y) / calibration.scale_y
    gz = (float(raw_z) - calibration.offset_z) / calibration.scale_z
    magnitude = sqrt(gx * gx + gy * gy + gz * gz)
    if magnitude <= 1e-9:
        return None

    roll = degrees(atan2(gx, -gz))
    pitch = degrees(atan2(gy, sqrt(gx * gx + gz * gz)))
    inclination = degrees(acos(max(-1.0, min(1.0, -gz / magnitude))))

    unit = (gx / magnitude, gy / magnitude, gz / magnitude)
    position_key, _ = max(
        _REFERENCE_POSITIONS,
        key=lambda item: sum(a * b for a, b in zip(unit, item[1], strict=True)),
    )
    return Orientation(
        gx=gx,
        gy=gy,
        gz=gz,
        roll_degrees=roll,
        pitch_degrees=pitch,
        inclination_degrees=inclination,
        gravity_magnitude=magnitude,
        position_key=position_key,
    )


def orientation_status(orientation: Orientation) -> tuple[str, str]:
    """Return a user-facing status key and CSS color class."""
    inclination = orientation.inclination_degrees
    if inclination <= 15.0:
        return "Flat", "green"
    if inclination >= 165.0:
        return "Display down", "red"
    if 75.0 <= inclination <= 105.0 and orientation.position_key.startswith("USB "):
        return "Upright", "blue"
    if inclination < 75.0:
        return "Slightly tilted", "yellow"
    return "Tilted", "orange"
