from __future__ import annotations

import math
import statistics
import time
from collections import defaultdict
from collections.abc import Iterable
from datetime import datetime
from typing import Any
from zoneinfo import ZoneInfo

from .history import HistoryRow
from .quality_pipeline import fuse_device_rows


def _median(values: Iterable[float]) -> float | None:
    finite = [float(value) for value in values if math.isfinite(float(value))]
    return float(statistics.median(finite)) if finite else None


def _mad(values: list[float], center: float) -> float:
    return float(statistics.median(abs(value - center) for value in values)) if values else 0.0


def _pearson(xs: list[float], ys: list[float]) -> float | None:
    if len(xs) < 3 or len(xs) != len(ys):
        return None
    mean_x = statistics.fmean(xs)
    mean_y = statistics.fmean(ys)
    dx = [value - mean_x for value in xs]
    dy = [value - mean_y for value in ys]
    denominator = math.sqrt(sum(value * value for value in dx) * sum(value * value for value in dy))
    if denominator <= 0:
        return None
    return float(sum(a * b for a, b in zip(dx, dy, strict=True)) / denominator)


def _hourly_points(rows: Iterable[HistoryRow]) -> list[dict[str, float | int]]:
    buckets: dict[int, list[HistoryRow]] = defaultdict(list)
    for row in rows:
        if row.pressure_hpa is None:
            continue
        pressure = float(row.pressure_hpa)
        if not math.isfinite(pressure) or not 750.0 <= pressure <= 1150.0:
            continue
        buckets[int(row.timestamp_utc) // 3600 * 3600].append(row)
    points: list[dict[str, float | int]] = []
    for timestamp, bucket in sorted(buckets.items()):
        cpm = _median(float(row.cpm) for row in bucket)
        pressure = _median(float(row.pressure_hpa) for row in bucket if row.pressure_hpa is not None)
        if cpm is None or pressure is None:
            continue
        points.append({"timestamp_utc": timestamp, "cpm": cpm, "pressure_hpa": pressure})
    return points


def _fit_pressure_model(
    points: list[dict[str, float | int]], *, timezone_name: str
) -> dict[str, Any]:
    tz = ZoneInfo(timezone_name)
    global_typical = _median(float(point["cpm"]) for point in points)
    if global_typical is None or global_typical <= 0:
        return {"available": False, "reason": "No valid CPM baseline"}

    by_week_slot: dict[tuple[int, int], list[float]] = defaultdict(list)
    by_hour: dict[int, list[float]] = defaultdict(list)
    for point in points:
        local = datetime.fromtimestamp(int(point["timestamp_utc"]), tz=tz)
        value = float(point["cpm"])
        by_week_slot[(local.weekday(), local.hour)].append(value)
        by_hour[local.hour].append(value)

    slot_typical: dict[tuple[int, int], float] = {}
    hour_typical: dict[int, float] = {}
    for key, values in by_week_slot.items():
        if len(values) >= 3:
            typical = _median(values)
            if typical is not None:
                slot_typical[key] = typical
    for key, values in by_hour.items():
        if len(values) >= 8:
            typical = _median(values)
            if typical is not None:
                hour_typical[key] = typical

    prepared: list[tuple[float, float, float, int]] = []
    for point in points:
        local = datetime.fromtimestamp(int(point["timestamp_utc"]), tz=tz)
        typical = slot_typical.get((local.weekday(), local.hour), hour_typical.get(local.hour, global_typical))
        if typical <= 0:
            continue
        residual_percent = (float(point["cpm"]) / typical - 1.0) * 100.0
        prepared.append((float(point["pressure_hpa"]), residual_percent, typical, int(point["timestamp_utc"])))

    if len(prepared) < 3:
        return {"available": False, "reason": "Too few pressure/CPM pairs"}

    residuals = [item[1] for item in prepared]
    center = float(statistics.median(residuals))
    mad = _mad(residuals, center)
    robust_sigma = max(1.0, 1.4826 * mad)
    filtered = [item for item in prepared if abs(item[1] - center) <= max(8.0, 6.0 * robust_sigma)]
    if len(filtered) < 3:
        filtered = prepared

    xs = [item[0] for item in filtered]
    ys = [item[1] for item in filtered]
    mean_x = statistics.fmean(xs)
    mean_y = statistics.fmean(ys)
    variance_x = sum((value - mean_x) ** 2 for value in xs)
    if variance_x <= 0:
        return {"available": False, "reason": "No pressure variation"}
    slope = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys, strict=True)) / variance_x
    intercept = mean_y - slope * mean_x
    correlation = _pearson(xs, ys)
    return {
        "available": True,
        "slope_percent_per_hpa": float(slope),
        "intercept_percent": float(intercept),
        "correlation": correlation,
        "reference_pressure_hpa": float(statistics.median(xs)),
        "fit_sample_count": len(filtered),
        "fit_excluded_count": len(prepared) - len(filtered),
        "global_typical_cpm": global_typical,
        "slot_typical": slot_typical,
        "hour_typical": hour_typical,
    }


def _snapshot_dict(snapshot: Any) -> dict[str, Any]:
    if snapshot is None:
        return {}
    if isinstance(snapshot, dict):
        return dict(snapshot)
    method = getattr(snapshot, "as_dict", None)
    if callable(method):
        value = method()
        return dict(value) if isinstance(value, dict) else {}
    return {}


def build_barometric_cosmic_hint(
    rows_by_serial: dict[str, Iterable[HistoryRow]],
    *,
    timezone_name: str,
    device_weights: dict[str, float] | None = None,
    tolerance_seconds: int = 90,
    pressure_snapshot: Any = None,
    enabled: bool = True,
    now_utc: int | None = None,
    minimum_days: float = 30.0,
    minimum_hourly_samples: int = 500,
    minimum_pressure_span_hpa: float = 10.0,
) -> dict[str, Any]:
    """Estimate a barometric signature and provide a cautious cosmic-ray hint.

    The result is deliberately an explanatory statistical proxy.  It never
    changes alert thresholds and never claims to identify individual cosmic
    particles or a cosmic percentage of total radiation.
    """
    snapshot = _snapshot_dict(pressure_snapshot)
    if not enabled:
        return {"enabled": False, "state": "Disabled", "pressure_snapshot": snapshot}

    fused = fuse_device_rows(
        rows_by_serial,
        weights=device_weights,
        tolerance_seconds=tolerance_seconds,
        include_single_device_samples=True,
    )
    points = _hourly_points(fused.rows)
    current_time = int(now_utc or time.time())
    data_span_days = 0.0
    if points:
        data_span_days = max(0.0, (int(points[-1]["timestamp_utc"]) - int(points[0]["timestamp_utc"])) / 86400.0)
    pressures = [float(point["pressure_hpa"]) for point in points]
    pressure_span = max(pressures) - min(pressures) if pressures else 0.0

    reasons: list[dict[str, Any]] = []
    if data_span_days < minimum_days:
        reasons.append({"key": "At least {days} days of learning data are required", "params": {"days": int(minimum_days)}})
    if len(points) < minimum_hourly_samples:
        reasons.append({"key": "At least {count} valid hourly values are required", "params": {"count": minimum_hourly_samples}})
    if pressure_span < minimum_pressure_span_hpa:
        reasons.append({"key": "At least {span:g} hPa pressure variation is required", "params": {"span": minimum_pressure_span_hpa}})

    result: dict[str, Any] = {
        "enabled": True,
        "available": bool(points),
        "learning": bool(reasons),
        "state": "Pressure model is still being formed" if reasons else "No pressure-typical signature",
        "confidence": "Insufficient" if reasons else "Low",
        "reasons": reasons,
        "hourly_sample_count": len(points),
        "data_span_days": data_span_days,
        "pressure_span_hpa": pressure_span,
        "paired_samples": fused.paired_samples,
        "single_device_samples": fused.single_device_samples,
        "excluded_samples": fused.rejected_samples,
        "contributing_devices": list(fused.contributing_devices),
        "pressure_snapshot": snapshot,
        "statistical_only": True,
    }
    if not points:
        return result

    model = _fit_pressure_model(points, timezone_name=timezone_name)
    if not model.get("available"):
        result["reasons"] = [*reasons, {"key": str(model.get("reason") or "Pressure model unavailable"), "params": {}}]
        return result

    result.update({
        "pressure_coefficient_percent_per_hpa": model["slope_percent_per_hpa"],
        "correlation": model["correlation"],
        "reference_pressure_hpa": model["reference_pressure_hpa"],
        "fit_sample_count": model["fit_sample_count"],
        "fit_excluded_count": model["fit_excluded_count"],
    })

    snapshot_pressure = snapshot.get("pressure_hpa") if snapshot.get("available") else None
    current_pressure = float(snapshot_pressure) if snapshot_pressure is not None else _median(
        float(point["pressure_hpa"]) for point in points if int(point["timestamp_utc"]) >= current_time - 3 * 3600
    )
    if current_pressure is None:
        current_pressure = float(points[-1]["pressure_hpa"])
    recent_rows = [row for row in fused.rows if row.timestamp_utc >= current_time - 3 * 3600]
    current_cpm = _median(float(row.cpm) for row in recent_rows) or float(fused.rows[-1].cpm)
    latest_local = datetime.fromtimestamp(fused.rows[-1].timestamp_utc, tz=ZoneInfo(timezone_name))
    typical = model["slot_typical"].get(
        (latest_local.weekday(), latest_local.hour),
        model["hour_typical"].get(latest_local.hour, model["global_typical_cpm"]),
    )
    observed_deviation = (current_cpm / typical - 1.0) * 100.0 if typical and typical > 0 else None
    pressure_effect = float(model["slope_percent_per_hpa"]) * (
        current_pressure - float(model["reference_pressure_hpa"])
    )
    remaining = observed_deviation - pressure_effect if observed_deviation is not None else None
    result.update({
        "current_pressure_hpa": current_pressure,
        "current_cpm_3h": current_cpm,
        "time_profile_typical_cpm": typical,
        "observed_deviation_percent": observed_deviation,
        "estimated_pressure_effect_percent": pressure_effect,
        "remaining_deviation_percent": remaining,
    })

    if reasons:
        return result

    slope = float(model["slope_percent_per_hpa"])
    correlation = model.get("correlation")
    correlation_value = float(correlation) if correlation is not None else 0.0
    if slope >= -0.001 or correlation_value > -0.10:
        result.update({
            "state": "No pressure-typical signature",
            "confidence": "Low",
            "learning": False,
        })
        return result

    confidence = "Medium"
    if len(points) >= 1000 and pressure_span >= 15.0 and correlation_value <= -0.30:
        confidence = "High"
    elif correlation_value > -0.20:
        confidence = "Low"

    effect_sign_matches = (
        observed_deviation is not None
        and abs(pressure_effect) >= 0.3
        and observed_deviation * pressure_effect > 0
    )
    tolerance = max(1.5, abs(pressure_effect) * 0.75)
    close_match = remaining is not None and abs(remaining) <= tolerance
    clear_match = (
        effect_sign_matches
        and remaining is not None
        and abs(remaining) <= max(1.0, abs(pressure_effect) * 0.5)
        and correlation_value <= -0.30
    )
    if clear_match:
        state = "Pressure-typical signature is pronounced"
    elif effect_sign_matches and close_match:
        state = "Cosmic influence is possible"
    else:
        state = "No pressure-typical signature"
    result.update({"state": state, "confidence": confidence, "learning": False})
    return result
