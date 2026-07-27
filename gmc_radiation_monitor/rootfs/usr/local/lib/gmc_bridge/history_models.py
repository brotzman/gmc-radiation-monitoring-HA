from __future__ import annotations

from dataclasses import dataclass
import time
from datetime import UTC, datetime
from typing import Any

def _coerce_epoch_timestamp(value: Any | None = None) -> int:
    """Return UTC epoch seconds for numeric or ISO-8601 timestamp values."""
    if value is None:
        return int(time.time())
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return int(value)
    text = str(value).strip()
    try:
        return int(text)
    except ValueError:
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"Unsupported UTC timestamp: {value!r}") from exc
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return int(parsed.timestamp())


@dataclass(frozen=True)
class HistoryRow:
    device_serial: str
    timestamp_utc: int
    cpm: int
    temperature_c: float | None
    voltage_v: float | None
    gyro_x: int | None
    gyro_y: int | None
    gyro_z: int | None
    cpm_quality: str
    tube_low_cpm: int | None = None
    tube_high_cpm: int | None = None
    pressure_hpa: float | None = None
    raw_cpm: float | None = None
    corrected_cpm: float | None = None
    detector_type: str | None = None
    dual_tube_mode: str | None = None
    active_tube: str | None = None
    dead_time_model: str | None = None
    dead_time_us: float | None = None
    dead_time_loss_percent: float | None = None
    detector_load_percent: float | None = None
    correction_factor: float | None = None
    calibration_status: str | None = None
    calibration_source: str | None = None
    measurement_quality_index: int | None = None
    dose_quality: str | None = None
    derived_dose_usvh: float | None = None
