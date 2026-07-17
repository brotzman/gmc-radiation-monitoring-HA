from __future__ import annotations

import itertools
import math
import statistics
import time
from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .history import HistoryRow
from .quality_pipeline import filter_history_rows, fuse_device_rows


def _median(values: list[float]) -> float | None:
    return float(statistics.median(values)) if values else None


def _percent(current: float | None, typical: float | None) -> float | None:
    if current is None or typical is None or typical <= 0:
        return None
    return (current / typical - 1.0) * 100.0


def _window_median(rows: list[HistoryRow], start: int, end: int) -> float | None:
    return _median([float(r.cpm) for r in rows if start <= r.timestamp_utc < end])


def _relative_change(current: float | None, previous: float | None) -> float | None:
    if current is None or previous is None or previous == 0:
        return None
    return (current / previous - 1.0) * 100.0


def _historical_development(clean: list[HistoryRow], *, timezone_name: str, now: int) -> dict[str, Any]:
    """Return compact daily background history for the dashboard.

    Daily medians are intentionally used instead of individual samples so the
    chart remains stable, inexpensive to render and resistant to isolated noise.
    """
    tz = ZoneInfo(timezone_name)
    daily_cpm: dict[str, list[float]] = defaultdict(list)
    daily_temperature: dict[str, list[float]] = defaultdict(list)
    daily_pressure: dict[str, list[float]] = defaultdict(list)
    daily_timestamp: dict[str, int] = {}
    earliest = now - 365 * 86400
    for row in clean:
        if row.timestamp_utc < earliest:
            continue
        local = datetime.fromtimestamp(row.timestamp_utc, tz=tz)
        day = local.date().isoformat()
        daily_cpm[day].append(float(row.cpm))
        daily_timestamp.setdefault(day, int(row.timestamp_utc))
        if row.temperature_c is not None and math.isfinite(float(row.temperature_c)):
            daily_temperature[day].append(float(row.temperature_c))
        if row.pressure_hpa is not None and math.isfinite(float(row.pressure_hpa)):
            daily_pressure[day].append(float(row.pressure_hpa))

    days = sorted(daily_cpm)
    raw_points: list[dict[str, Any]] = []
    cpm_values: list[float] = []
    for day in days:
        cpm = float(statistics.median(daily_cpm[day]))
        cpm_values.append(cpm)
        smooth_window = cpm_values[-7:]
        raw_points.append({
            "date": day,
            "timestamp_utc": daily_timestamp[day],
            "median_cpm": cpm,
            "smoothed_cpm": float(statistics.median(smooth_window)),
            "temperature_c": _median(daily_temperature.get(day, [])),
            "pressure_hpa": _median(daily_pressure.get(day, [])),
        })

    # Keep at most 120 points in the HTML while preserving the newest point.
    if len(raw_points) > 120:
        step = math.ceil(len(raw_points) / 120)
        points = raw_points[::step]
        if points[-1] is not raw_points[-1]:
            points.append(raw_points[-1])
    else:
        points = raw_points

    def recent_previous_change(field: str, days: int = 30) -> dict[str, Any]:
        recent_start = now - days * 86400
        previous_start = now - 2 * days * 86400
        recent = [
            float(item[field]) for item in raw_points
            if item.get(field) is not None and recent_start <= int(item["timestamp_utc"]) <= now
        ]
        previous = [
            float(item[field]) for item in raw_points
            if item.get(field) is not None and previous_start <= int(item["timestamp_utc"]) < recent_start
        ]
        recent_value = _median(recent)
        previous_value = _median(previous)
        return {
            "recent_median": recent_value,
            "previous_median": previous_value,
            "change": None if recent_value is None or previous_value is None else recent_value - previous_value,
            "change_percent": _relative_change(recent_value, previous_value),
            "samples": len(recent) + len(previous),
        }

    jumps: list[dict[str, Any]] = []
    for previous, current in itertools.pairwise(raw_points):
        before = float(previous["smoothed_cpm"])
        after = float(current["smoothed_cpm"])
        if before <= 0:
            continue
        delta = after - before
        percent = delta / before * 100.0
        if abs(delta) >= 5.0 and abs(percent) >= 25.0:
            jumps.append({
                "date": current["date"],
                "from_cpm": before,
                "to_cpm": after,
                "change_percent": percent,
            })

    return {
        "available": len(points) >= 2,
        "points": points,
        "daily_points": len(raw_points),
        "span_days": 0 if len(raw_points) < 2 else max(0, (int(raw_points[-1]["timestamp_utc"]) - int(raw_points[0]["timestamp_utc"])) / 86400.0),
        "temperature_trend": recent_previous_change("temperature_c"),
        "pressure_trend": recent_previous_change("pressure_hpa"),
        "jumps": jumps[-8:],
        "jump_count": len(jumps),
    }


def build_adaptive_background(
    rows: Iterable[HistoryRow],
    *,
    timezone_name: str,
    now_utc: int | None = None,
    minimum_hour_samples: int = 6,
    minimum_week_slot_samples: int = 4,
    minimum_temperature_samples: int = 8,
    already_filtered: bool = False,
) -> dict[str, Any]:
    """Build robust, explainable time/temperature-specific background references."""
    raw = list(rows)
    quality = None if already_filtered else filter_history_rows(raw, purpose="baseline")
    clean = sorted(raw if already_filtered else quality.rows, key=lambda r: r.timestamp_utc)
    if not clean:
        return {
            "available": False,
            "learning": True,
            "reasons": ["No measurement yet"],
            "raw_sample_count": len(raw),
            "excluded_sample_count": len(raw),
        }
    now = int(now_utc or time.time())
    tz = ZoneInfo(timezone_name)
    current = float(clean[-1].cpm)
    current_local = datetime.fromtimestamp(clean[-1].timestamp_utc, tz=tz)

    hourly: dict[int, list[float]] = defaultdict(list)
    weekly: dict[tuple[int, int], list[float]] = defaultdict(list)
    temp_bins: dict[int, list[float]] = defaultdict(list)
    for row in clean:
        local = datetime.fromtimestamp(row.timestamp_utc, tz=tz)
        hourly[local.hour].append(float(row.cpm))
        weekly[(local.weekday(), local.hour)].append(float(row.cpm))
        if row.temperature_c is not None and math.isfinite(float(row.temperature_c)):
            temp_bins[int(math.floor(float(row.temperature_c) / 2.0) * 2)].append(float(row.cpm))

    week_values = weekly[(current_local.weekday(), current_local.hour)]
    hour_values = hourly[current_local.hour]
    weekly_typical = _median(week_values) if len(week_values) >= minimum_week_slot_samples else None
    hourly_typical = _median(hour_values) if len(hour_values) >= minimum_hour_samples else None
    typical = weekly_typical if weekly_typical is not None else hourly_typical
    source = "weekday_hour" if weekly_typical is not None else "hour" if hourly_typical is not None else "learning"

    latest_temp = clean[-1].temperature_c
    temp_typical = None
    temp_bin = None
    temp_samples = 0
    if latest_temp is not None and math.isfinite(float(latest_temp)):
        temp_bin = int(math.floor(float(latest_temp) / 2.0) * 2)
        values = temp_bins[temp_bin]
        temp_samples = len(values)
        if temp_samples >= minimum_temperature_samples:
            temp_typical = _median(values)

    drift: dict[str, Any] = {}
    for days in (7, 30, 90, 365):
        recent_start = now - days * 86400
        previous_start = now - 2 * days * 86400
        recent = _window_median(clean, recent_start, now + 1)
        previous = _window_median(clean, previous_start, recent_start)
        drift[str(days)] = {
            "recent_median": recent,
            "previous_median": previous,
            "change_percent": _percent(recent, previous),
        }

    deviation = _percent(current, typical)
    if typical is None:
        state = "Profile is still being formed"
    elif abs(deviation or 0.0) < 15:
        state = "Normal for this time"
    elif (deviation or 0.0) >= 15:
        state = "Above the typical time profile"
    else:
        state = "Below the typical time profile"

    excluded_count = 0 if quality is None else quality.rejected_count
    rejected_by_reason = {} if quality is None else quality.rejected_by_reason
    return {
        "available": True,
        "learning": typical is None,
        "state": state,
        "current_cpm": current,
        "typical_cpm": typical,
        "deviation_percent": deviation,
        "reference_source": source,
        "weekday": current_local.weekday(),
        "hour": current_local.hour,
        "weekday_hour_samples": len(week_values),
        "hour_samples": len(hour_values),
        "temperature_c": latest_temp,
        "temperature_bin_start_c": temp_bin,
        "temperature_typical_cpm": temp_typical,
        "temperature_samples": temp_samples,
        "temperature_deviation_percent": _percent(current, temp_typical),
        "drift": drift,
        "sample_count": len(clean),
        "raw_sample_count": len(raw),
        "excluded_sample_count": excluded_count,
        "excluded_by_reason": rejected_by_reason,
        "first_timestamp_utc": clean[0].timestamp_utc,
        "last_timestamp_utc": clean[-1].timestamp_utc,
        "historical_development": _historical_development(clean, timezone_name=timezone_name, now=now),
    }


def build_site_adaptive_background(
    rows_by_serial: dict[str, Iterable[HistoryRow]],
    *,
    timezone_name: str,
    device_weights: dict[str, float] | None = None,
    tolerance_seconds: int = 90,
    now_utc: int | None = None,
) -> dict[str, Any]:
    """Build a measurement-site profile from quality-weighted device baselines."""
    fused = fuse_device_rows(
        rows_by_serial,
        weights=device_weights,
        tolerance_seconds=tolerance_seconds,
        include_single_device_samples=True,
    )
    profile = build_adaptive_background(
        fused.rows,
        timezone_name=timezone_name,
        now_utc=now_utc,
        already_filtered=True,
    )
    active_devices = len(fused.contributing_devices)
    if active_devices >= 2 and fused.paired_samples >= 20:
        confidence = "High"
        mode = "quality_weighted_fusion"
    elif active_devices >= 2 and fused.paired_samples >= 10:
        confidence = "Medium"
        mode = "quality_weighted_fusion"
    elif active_devices >= 2 and fused.paired_samples > 0:
        confidence = "Low"
        mode = "limited_fusion"
    elif active_devices == 1:
        confidence = "Reduced"
        mode = "single_device_fallback"
    else:
        confidence = "Unavailable"
        mode = "unavailable"
    profile.update({
        "scope": "site",
        "confidence": confidence,
        "fusion_mode": mode,
        "paired_samples": fused.paired_samples,
        "single_device_samples": fused.single_device_samples,
        "fusion_rejected_samples": fused.rejected_samples,
        "contributing_devices": list(fused.contributing_devices),
        "active": bool(profile.get("available") and profile.get("typical_cpm") is not None),
    })
    return profile
