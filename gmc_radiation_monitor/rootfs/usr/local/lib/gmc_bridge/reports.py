from __future__ import annotations

import csv
import io
import json
import math
import os
import statistics
import tempfile
import textwrap
import zipfile
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from datetime import time as dt_time
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .analysis import baseline_drift_summary, data_quality_summary, temperature_bin_summary
from .analysis_presentation import build_period_analysis_result, build_primary_analysis_result
from .device_profiles import normalize_device_version_display
from .events import current_hysteretic_state, detect_events
from .file_security import secure_file
from .history import HistoryRow, HistoryStore
from .quality_pipeline import filter_history_rows, robust_sigma, robust_trimmed_mean
from .scientific_analysis import counting_uncertainty, detect_persistent_level_shift, recent_change_significance
from .translations import Translator
from .version import APP_VERSION


@dataclass(frozen=True)
class ReportPeriod:
    kind: str
    label: str
    start_local: datetime
    end_local: datetime

    @property
    def start_utc(self) -> datetime:
        return self.start_local.astimezone(UTC)

    @property
    def end_utc(self) -> datetime:
        return self.end_local.astimezone(UTC)

    @property
    def filename_label(self) -> str:
        if self.kind == "daily":
            return self.start_local.strftime("%Y-%m-%d")
        iso = self.start_local.isocalendar()
        return f"{iso.year}-W{iso.week:02d}"


def load_timezone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unknown IANA timezone: {name}") from exc


def resolve_period(
    *,
    kind: str,
    selection: str,
    tz: ZoneInfo,
    now: datetime | None = None,
    date_value: str | None = None,
    week_value: str | None = None,
) -> ReportPeriod:
    current = (now or datetime.now(tz)).astimezone(tz)
    if kind == "daily":
        if selection == "today":
            chosen = current.date()
        elif selection == "previous":
            chosen = current.date() - timedelta(days=1)
        elif selection == "specific":
            if not date_value:
                raise ValueError("A date is required for a specific daily report")
            chosen = date.fromisoformat(date_value)
        else:
            raise ValueError(f"Unsupported daily selection: {selection}")
        start = datetime.combine(chosen, dt_time.min, tzinfo=tz)
        end = start + timedelta(days=1)
        return ReportPeriod("daily", chosen.isoformat(), start, end)

    if kind == "weekly":
        if selection in {"current", "previous"}:
            monday = current.date() - timedelta(days=current.weekday())
            if selection == "previous":
                monday -= timedelta(days=7)
        elif selection == "specific":
            if not week_value:
                raise ValueError("An ISO week is required for a specific weekly report")
            try:
                year_text, week_text = week_value.upper().split("-W", 1)
                monday = date.fromisocalendar(int(year_text), int(week_text), 1)
            except (TypeError, ValueError) as exc:
                raise ValueError("ISO week must use the form YYYY-Www") from exc
        else:
            raise ValueError(f"Unsupported weekly selection: {selection}")
        start = datetime.combine(monday, dt_time.min, tzinfo=tz)
        end = start + timedelta(days=7)
        iso = monday.isocalendar()
        return ReportPeriod("weekly", f"{iso.year}-W{iso.week:02d}", start, end)

    raise ValueError(f"Unsupported report period: {kind}")


def expected_samples(period: ReportPeriod, scan_interval_seconds: int) -> int:
    effective_end = min(period.end_utc, datetime.now(UTC))
    duration = max(0.0, (effective_end - period.start_utc).total_seconds())
    return max(1, round(duration / scan_interval_seconds))


def _percentile(values: list[float], percent: float) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return values[0]
    ordered = sorted(values)
    rank = (len(ordered) - 1) * percent
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[lower]
    weight = rank - lower
    return ordered[lower] * (1.0 - weight) + ordered[upper] * weight


def _pearson_correlation(pairs: list[tuple[float, float]]) -> tuple[float | None, str]:
    if len(pairs) < 2:
        return None, "insufficient paired samples"
    x_values = [pair[0] for pair in pairs]
    y_values = [pair[1] for pair in pairs]
    if len(set(x_values)) < 2:
        return None, "no CPM variation"
    if len(set(y_values)) < 2:
        return None, "no sensor variation"
    return statistics.correlation(x_values, y_values), "ok"


def build_statistics(
    rows: list[HistoryRow],
    *,
    expected_count: int,
) -> dict[str, Any]:
    cpm_values = [float(row.cpm) for row in rows]
    completeness = min(100.0, 100.0 * len(rows) / expected_count) if expected_count else 0.0
    stats: dict[str, Any] = {
        "samples": len(rows),
        "expected_samples": expected_count,
        "missing_samples": max(0, expected_count - len(rows)),
        "completeness_percent": completeness,
    }
    if not cpm_values:
        stats.update(
            {
                "cpm_min": None,
                "cpm_max": None,
                "cpm_mean": None,
                "cpm_median": None,
                "cpm_standard_deviation": None,
                "cpm_95th_percentile": None,
            }
        )
        return stats
    stats.update(
        {
            "cpm_min": min(cpm_values),
            "cpm_max": max(cpm_values),
            "cpm_mean": statistics.fmean(cpm_values),
            "cpm_median": statistics.median(cpm_values),
            "cpm_standard_deviation": statistics.stdev(cpm_values) if len(cpm_values) > 1 else 0.0,
            "cpm_95th_percentile": _percentile(cpm_values, 0.95),
        }
    )
    return stats




def _analysis_for_rows(
    rows: list[HistoryRow],
    *,
    expected_count: int,
    scan_interval_seconds: int,
    baseline_rows: list[HistoryRow],
    yellow_percent: float,
    red_percent: float,
) -> dict[str, Any]:
    stats = build_statistics(rows, expected_count=expected_count)
    baseline_values = [float(row.cpm) for row in baseline_rows]
    baseline_mean = statistics.fmean(baseline_values) if baseline_values else stats.get("cpm_mean")
    period_mean = stats.get("cpm_mean")
    deviation_cpm = None if period_mean is None or baseline_mean is None else float(period_mean) - float(baseline_mean)
    deviation_percent = None
    if deviation_cpm is not None and baseline_mean and baseline_mean > 0:
        deviation_percent = 100.0 * deviation_cpm / baseline_mean
    temperature_pairs = [(float(row.cpm), float(row.temperature_c)) for row in rows if row.temperature_c is not None]
    voltage_pairs = [(float(row.cpm), float(row.voltage_v)) for row in rows if row.voltage_v is not None]
    temp_corr, temp_status = _pearson_correlation(temperature_pairs)
    volt_corr, volt_status = _pearson_correlation(voltage_pairs)
    mean = stats.get("cpm_mean")
    sd = stats.get("cpm_standard_deviation")
    variance = statistics.variance([float(row.cpm) for row in rows]) if len(rows) > 1 else None
    fano = variance / mean if variance is not None and mean and mean > 0 else None
    poisson_ratio = sd / math.sqrt(mean) if sd is not None and mean and mean > 0 else None
    events = detect_events(
        rows, baseline_mean=baseline_mean, yellow_percent=yellow_percent, red_percent=red_percent,
        scan_interval_seconds=scan_interval_seconds,
    )
    return {
        **stats,
        "data_quality": data_quality_summary(rows, expected_count=expected_count, scan_interval_seconds=scan_interval_seconds),
        "baseline_mean_cpm": baseline_mean,
        "baseline_deviation_cpm": deviation_cpm,
        "baseline_deviation_percent": deviation_percent,
        "baseline_drift": baseline_drift_summary(baseline_rows or rows),
        "temperature_correlation": temp_corr,
        "temperature_correlation_status": temp_status,
        "voltage_correlation": volt_corr,
        "voltage_correlation_status": volt_status,
        "fano_factor": fano,
        "poisson_sd_ratio": poisson_ratio,
        "temperature_bins": temperature_bin_summary(rows),
        "events": events,
        "event_count": len(events),
    }

def build_live_analysis(
    store: HistoryStore,
    *,
    scan_interval_seconds: int,
    traffic_light_yellow_percent: float = 125.0,
    traffic_light_red_percent: float = 175.0,
    device_serial: str | None = None,
) -> dict[str, Any]:
    """Build robust rolling statistics from the shared quality-filtered data pipeline."""
    _, raw_latest_timestamp = store.bounds(device_serial=device_serial)
    empty = {
        "available": False, "latest_timestamp_utc": None, "latest_cpm": None,
        "mean_1h": None, "mean_24h": None, "sd_24h": None, "median_24h": None,
        "p95_24h": None, "p99_24h": None, "min_24h": None, "max_24h": None,
        "temperature_correlation_24h": None, "temperature_correlation_status_24h": "insufficient paired samples", "temperature_pairs_24h": 0,
        "voltage_correlation_24h": None, "voltage_correlation_status_24h": "insufficient paired samples", "voltage_pairs_24h": 0,
        "z_score_24h": None, "fano_factor_24h": None, "poisson_sd_ratio_24h": None,
        "mean_7d": None, "background_index_percent": None,
        "samples_1h": 0, "samples_24h": 0, "samples_7d": 0,
        "raw_samples_24h": 0, "excluded_samples_24h": 0, "quality_filter_reasons_24h": {},
        "coverage_1h_percent": 0.0, "coverage_24h_percent": 0.0, "coverage_7d_percent": 0.0,
        "data_quality_label_24h": "Poor", "data_quality_score_24h": 0.0,
        "data_quality_reasons_24h": ["no measurements"], "longest_gap_24h_seconds": 0,
        "duplicate_timestamps_24h": 0, "clock_regressions_since_start": 0,
        "short_intervals_24h": 0, "long_intervals_24h": 0, "traffic_state": "learning",
        "baseline_minimum_samples": max(6, round(21600 / scan_interval_seconds)),
        "baseline_ready": False, "recent_window_ready": False, "baseline_readiness_percent": 0.0,
        "baseline_deviation_cpm": None, "baseline_deviation_percent": None,
        "baseline_drift_percent": None, "events_24h": 0, "temperature_bins_24h": [],
        "serial_error_count_since_start": 0, "serial_reconnect_count_since_start": 0,
        "temperature_error_count_since_start": 0, "voltage_error_count_since_start": 0,
        "gyro_error_count_since_start": 0, "trend_30m_cpm": None,
        "counting_uncertainty_latest": counting_uncertainty([]),
        "counting_uncertainty_1h": counting_uncertainty([]),
        "counting_uncertainty_24h": counting_uncertainty([]),
        "counting_uncertainty_7d": counting_uncertainty([]),
        "level_shift": {"available": False, "detected": False, "state": "Insufficient history for level-shift detection"},
        "change_significance": {"available": False, "state": "Insufficient history for significance assessment"},
        "raw_archive_samples_24h": 0, "raw_archive_accepted_24h": 0,
        "raw_archive_pending_24h": 0, "raw_archive_available": False,
    }
    def with_presentation(result: dict[str, Any]) -> dict[str, Any]:
        enriched = dict(result)
        enriched["presentation"] = build_primary_analysis_result(enriched).as_dict()
        return enriched

    if device_serial == "" or raw_latest_timestamp is None:
        return with_presentation(empty)

    raw_rows = store.query_range(int(raw_latest_timestamp) - 7 * 86400, int(raw_latest_timestamp) + 1, device_serial=device_serial)
    if not raw_rows:
        return with_presentation(empty)
    filtered = filter_history_rows(raw_rows, purpose="analysis")
    baseline_filtered = filter_history_rows(raw_rows, purpose="baseline")
    rows = filtered.rows
    baseline_rows = baseline_filtered.rows
    if not rows:
        result = dict(empty)
        result.update({"raw_samples_24h": len(raw_rows), "excluded_samples_24h": filtered.rejected_count, "quality_filter_reasons_24h": filtered.rejected_by_reason})
        return with_presentation(result)

    latest_timestamp = rows[-1].timestamp_utc
    def window(source: list[HistoryRow], seconds: int) -> list[HistoryRow]:
        cutoff = latest_timestamp - seconds
        return [row for row in source if row.timestamp_utc > cutoff]

    rows_1h = window(rows, 3600)
    rows_24h = window(rows, 86400)
    rows_7d = window(baseline_rows, 7 * 86400)
    raw_rows_24h = window(raw_rows, 86400)
    cpm_1h = [float(row.cpm) for row in rows_1h]
    cpm_24h = [float(row.cpm) for row in rows_24h]
    cpm_7d = [float(row.cpm) for row in rows_7d]

    mean_1h = robust_trimmed_mean(cpm_1h)
    mean_24h = robust_trimmed_mean(cpm_24h)
    mean_7d = float(statistics.median(cpm_7d)) if cpm_7d else None
    median_24h = float(statistics.median(cpm_24h)) if cpm_24h else None
    sd_24h = robust_sigma(cpm_24h)
    variance_24h = sd_24h * sd_24h if sd_24h is not None else None
    latest_cpm = float(rows[-1].cpm)

    rows_30m = window(rows, 1800)
    trend_30m_cpm = None
    if len(rows_30m) >= 4:
        midpoint = len(rows_30m) // 2
        first_level = robust_trimmed_mean(float(row.cpm) for row in rows_30m[:midpoint])
        second_level = robust_trimmed_mean(float(row.cpm) for row in rows_30m[midpoint:])
        if first_level is not None and second_level is not None:
            trend_30m_cpm = second_level - first_level

    z_score = None
    if median_24h is not None and sd_24h is not None and sd_24h > 0:
        z_score = (latest_cpm - median_24h) / sd_24h
    fano_factor = variance_24h / mean_24h if mean_24h and variance_24h is not None else None
    poisson_sd_ratio = sd_24h / math.sqrt(mean_24h) if mean_24h and sd_24h is not None else None
    background_index = 100.0 * mean_1h / mean_7d if mean_1h is not None and mean_7d else None

    temperature_pairs = [(float(row.cpm), float(row.temperature_c)) for row in rows_24h if row.temperature_c is not None]
    voltage_pairs = [(float(row.cpm), float(row.voltage_v)) for row in rows_24h if row.voltage_v is not None]
    temperature_correlation, temperature_correlation_status = _pearson_correlation(temperature_pairs)
    voltage_correlation, voltage_correlation_status = _pearson_correlation(voltage_pairs)

    expected_24h = max(1, round(86400 / scan_interval_seconds))
    ingest_diagnostics = store.get_ingest_diagnostics(device_serial=device_serial)
    capabilities = store.get_device_capabilities(device_serial=device_serial)
    quality_24h = data_quality_summary(
        rows_24h, expected_count=expected_24h, scan_interval_seconds=scan_interval_seconds,
        ingest_diagnostics=ingest_diagnostics, capabilities=capabilities,
    )
    excluded_24h = max(0, len(raw_rows_24h) - len(rows_24h))
    if excluded_24h:
        penalty = min(25.0, 100.0 * excluded_24h / max(1, len(raw_rows_24h)) * 0.5)
        quality_24h["score"] = max(0.0, float(quality_24h["score"]) - penalty)
        quality_24h["reasons"] = [*list(quality_24h["reasons"]), f"{excluded_24h} quality-filtered samples"]
        quality_24h["label"] = "Excellent" if quality_24h["score"] >= 95 else "Good" if quality_24h["score"] >= 85 else "Limited" if quality_24h["score"] >= 65 else "Poor"

    deviation_cpm = mean_1h - mean_7d if mean_1h is not None and mean_7d is not None else None
    deviation_percent = 100.0 * deviation_cpm / mean_7d if deviation_cpm is not None and mean_7d else None
    drift_7d = baseline_drift_summary(rows_7d)
    events_24h = detect_events(
        rows_24h, baseline_mean=mean_7d, yellow_percent=traffic_light_yellow_percent,
        red_percent=traffic_light_red_percent, scan_interval_seconds=scan_interval_seconds,
    )
    uncertainty_latest = counting_uncertainty([rows[-1]])
    uncertainty_1h = counting_uncertainty(rows_1h)
    uncertainty_24h = counting_uncertainty(rows_24h)
    uncertainty_7d = counting_uncertainty(rows_7d)
    level_shift = detect_persistent_level_shift(rows_7d)
    baseline_reference = [row for row in rows_7d if row.timestamp_utc <= latest_timestamp - 3600]
    change_significance = recent_change_significance(
        rows_1h, baseline_reference, quality_score=float(quality_24h["score"]),
    )
    raw_archive = store.raw_measurement_summary(
        start_timestamp_utc=latest_timestamp - 86400,
        end_timestamp_utc=latest_timestamp + 1,
        device_serial=device_serial,
    )

    traffic_indices: list[float] = []
    if mean_7d:
        rolling_hour: list[HistoryRow] = []
        for row in sorted(rows_24h, key=lambda item: item.timestamp_utc):
            rolling_hour.append(row)
            cutoff = row.timestamp_utc - 3600
            while rolling_hour and rolling_hour[0].timestamp_utc <= cutoff:
                rolling_hour.pop(0)
            rolling_level = robust_trimmed_mean(float(item.cpm) for item in rolling_hour)
            if rolling_level is not None:
                traffic_indices.append(100.0 * rolling_level / mean_7d)
    traffic_state = current_hysteretic_state(traffic_indices, yellow=traffic_light_yellow_percent, red=traffic_light_red_percent)

    def coverage(sample_count: int, seconds: int) -> float:
        expected = max(1, round(seconds / scan_interval_seconds))
        return min(100.0, 100.0 * sample_count / expected)

    minimum_baseline_samples = max(6, round(21600 / scan_interval_seconds))
    baseline_readiness_percent = min(100.0, 100.0 * len(rows_7d) / minimum_baseline_samples)
    baseline_ready = mean_7d is not None and len(rows_7d) >= minimum_baseline_samples
    recent_window_ready = mean_1h is not None and coverage(len(rows_1h), 3600) >= 50.0

    runtime_metadata = store.get_metadata()
    def runtime_counter(name: str) -> int:
        try:
            return int(runtime_metadata.get(name, "0"))
        except ValueError:
            return 0

    result = {
        "available": True, "latest_timestamp_utc": latest_timestamp, "latest_cpm": latest_cpm,
        "mean_1h": mean_1h, "mean_24h": mean_24h, "sd_24h": sd_24h,
        "median_24h": median_24h, "p95_24h": _percentile(cpm_24h, 0.95), "p99_24h": _percentile(cpm_24h, 0.99),
        "min_24h": min(cpm_24h) if cpm_24h else None, "max_24h": max(cpm_24h) if cpm_24h else None,
        "temperature_correlation_24h": temperature_correlation, "temperature_correlation_status_24h": temperature_correlation_status,
        "temperature_pairs_24h": len(temperature_pairs), "voltage_correlation_24h": voltage_correlation,
        "voltage_correlation_status_24h": voltage_correlation_status, "voltage_pairs_24h": len(voltage_pairs),
        "z_score_24h": z_score, "fano_factor_24h": fano_factor, "poisson_sd_ratio_24h": poisson_sd_ratio,
        "mean_7d": mean_7d, "background_index_percent": background_index,
        "samples_1h": len(rows_1h), "samples_24h": len(rows_24h), "samples_7d": len(rows_7d),
        "raw_samples_24h": len(raw_rows_24h), "excluded_samples_24h": excluded_24h,
        "quality_filter_reasons_24h": filtered.rejected_by_reason,
        "coverage_1h_percent": coverage(len(rows_1h), 3600), "coverage_24h_percent": coverage(len(rows_24h), 86400),
        "coverage_7d_percent": coverage(len(rows_7d), 7 * 86400),
        "data_quality_label_24h": quality_24h["label"], "data_quality_score_24h": quality_24h["score"],
        "data_quality_reasons_24h": quality_24h["reasons"], "longest_gap_24h_seconds": quality_24h["longest_gap_seconds"],
        "duplicate_timestamps_24h": quality_24h["duplicate_timestamps"], "clock_regressions_since_start": quality_24h["clock_regressions"],
        "short_intervals_24h": quality_24h["short_intervals"], "long_intervals_24h": quality_24h["long_intervals"],
        "traffic_state": traffic_state, "baseline_minimum_samples": minimum_baseline_samples,
        "baseline_ready": baseline_ready, "recent_window_ready": recent_window_ready,
        "baseline_readiness_percent": baseline_readiness_percent, "baseline_deviation_cpm": deviation_cpm,
        "baseline_deviation_percent": deviation_percent, "baseline_drift_percent": drift_7d["percent"],
        "events_24h": len(events_24h), "temperature_bins_24h": temperature_bin_summary(rows_24h),
        "serial_error_count_since_start": runtime_counter("serial_error_count"),
        "serial_reconnect_count_since_start": runtime_counter("serial_reconnect_count"),
        "temperature_error_count_since_start": runtime_counter("temperature_error_count"),
        "voltage_error_count_since_start": runtime_counter("voltage_error_count"),
        "gyro_error_count_since_start": runtime_counter("gyro_error_count"), "trend_30m_cpm": trend_30m_cpm,
        "counting_uncertainty_latest": uncertainty_latest,
        "counting_uncertainty_1h": uncertainty_1h,
        "counting_uncertainty_24h": uncertainty_24h,
        "counting_uncertainty_7d": uncertainty_7d,
        "level_shift": level_shift,
        "change_significance": change_significance,
        "raw_archive_samples_24h": int(raw_archive.get("total", 0)),
        "raw_archive_accepted_24h": int(raw_archive.get("accepted", 0)),
        "raw_archive_pending_24h": int(raw_archive.get("pending", 0)),
        "raw_archive_available": bool(raw_archive.get("available", False)),
    }
    return with_presentation(result)


def metadata_document(
    *,
    period: ReportPeriod,
    timezone_name: str,
    scan_interval_seconds: int,
    rows: list[HistoryRow],
    device_metadata: dict[str, str],
) -> dict[str, Any]:
    stats = build_statistics(
        rows,
        expected_count=expected_samples(period, scan_interval_seconds),
    )
    return {
        "report_schema_version": 1,
        "app_version": device_metadata.get("app_version", APP_VERSION),
        "device_model": normalize_device_version_display(device_metadata.get("device_model", "Unknown GMC")),
        "hardware_model": device_metadata.get("hardware_model"),
        "firmware_version": device_metadata.get("firmware_version"),
        "device_time": device_metadata.get("device_time"),
        "device_clock_offset_seconds": _metadata_int(device_metadata.get("device_clock_offset_seconds")),
        "heartbeat_enabled": device_metadata.get("heartbeat_enabled") == "True",
        "serial": device_metadata.get("serial", "unknown"),
        "period_kind": period.kind,
        "period_label": period.label,
        "period_start_utc": period.start_utc.isoformat().replace("+00:00", "Z"),
        "period_end_utc": period.end_utc.isoformat().replace("+00:00", "Z"),
        "period_start_local": period.start_local.isoformat(),
        "period_end_local": period.end_local.isoformat(),
        "timezone": timezone_name,
        "sample_interval_seconds": scan_interval_seconds,
        "high_cpm_threshold": _metadata_int(device_metadata.get("high_cpm_threshold")),
        "high_cpm_confirmations": _metadata_int(device_metadata.get("high_cpm_confirmations")),
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        **stats,
    }



def _metadata_int(value: str | None) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except ValueError:
        return None

def csv_bytes(rows: Iterable[HistoryRow], tz: ZoneInfo, *, language: str = "en") -> bytes:
    # Keep stable machine-readable field identifiers for backwards compatibility.
    # Human-readable reports and explanatory text are localized separately.
    del language
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(
        [
            "timestamp_utc",
            "timestamp_local",
            "cpm",
            "temperature_c",
            "voltage_v",
            "gyro_x",
            "gyro_y",
            "gyro_z",
            "cpm_quality",
        ]
    )
    for row in rows:
        utc_dt = datetime.fromtimestamp(row.timestamp_utc, UTC)
        local_dt = utc_dt.astimezone(tz)
        writer.writerow(
            [
                utc_dt.isoformat(timespec="seconds").replace("+00:00", "Z"),
                local_dt.isoformat(timespec="seconds"),
                row.cpm,
                _csv_value(row.temperature_c),
                _csv_value(row.voltage_v),
                _csv_value(row.gyro_x),
                _csv_value(row.gyro_y),
                _csv_value(row.gyro_z),
                row.cpm_quality,
            ]
        )
    return output.getvalue().encode("utf-8")

def raw_measurements_csv_bytes(rows: Iterable[dict[str, Any]], tz: ZoneInfo) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow([
        "raw_id", "device_serial", "timestamp_utc", "timestamp_local", "cpm",
        "tube_low_cpm", "tube_high_cpm", "temperature_c", "voltage_v",
        "gyro_x", "gyro_y", "gyro_z", "gate_state", "accepted", "raw_json",
    ])
    for row in rows:
        timestamp = int(row.get("timestamp_utc") or 0)
        utc_dt = datetime.fromtimestamp(timestamp, UTC)
        writer.writerow([
            row.get("id", ""),
            row.get("device_serial", ""),
            utc_dt.isoformat(timespec="seconds").replace("+00:00", "Z"),
            utc_dt.astimezone(tz).isoformat(timespec="seconds"),
            row.get("cpm", ""),
            _csv_value(row.get("tube_low_cpm")),
            _csv_value(row.get("tube_high_cpm")),
            _csv_value(row.get("temperature_c")),
            _csv_value(row.get("voltage_v")),
            _csv_value(row.get("gyro_x")),
            _csv_value(row.get("gyro_y")),
            _csv_value(row.get("gyro_z")),
            row.get("gate_state", ""),
            int(bool(row.get("accepted"))),
            row.get("raw_json", ""),
        ])
    return output.getvalue().encode("utf-8")


def _csv_value(value: Any) -> Any:
    return "" if value is None else value



def _gap_aware_series(
    times: list[datetime],
    values: list[float | int | None],
    scan_interval_seconds: int,
) -> tuple[list[datetime], list[float | int | None]]:
    if not times:
        return [], []
    out_times: list[datetime] = [times[0]]
    out_values: list[float | int | None] = [values[0]]
    gap_threshold = scan_interval_seconds * 1.5
    for previous, current, value in zip(times[:-1], times[1:], values[1:], strict=True):
        if (current - previous).total_seconds() > gap_threshold:
            out_times.append(previous + timedelta(seconds=scan_interval_seconds))
            out_values.append(None)
        out_times.append(current)
        out_values.append(value)
    return out_times, out_values

def png_bytes(
    rows: list[HistoryRow],
    *,
    period: ReportPeriod,
    tz: ZoneInfo,
    timezone_name: str,
    scan_interval_seconds: int,
    device_metadata: dict[str, str],
    language: str = "en",
) -> bytes:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt

    t = Translator(language)
    metadata = metadata_document(
        period=period,
        timezone_name=timezone_name,
        scan_interval_seconds=scan_interval_seconds,
        rows=rows,
        device_metadata=device_metadata,
    )
    local_times = [datetime.fromtimestamp(row.timestamp_utc, UTC).astimezone(tz) for row in rows]

    channels: list[tuple[str, str, list[float | int | None]]] = [
        (t("Radiation count rate [CPM]"), "CPM", [row.cpm for row in rows]),
        (t("Temperature [°C]"), t("Temperature [°C]"), [row.temperature_c for row in rows]),
        (t("Supply voltage [V]"), t("Voltage [V]"), [row.voltage_v for row in rows]),
    ]
    gyro_present = any(
        row.gyro_x is not None or row.gyro_y is not None or row.gyro_z is not None for row in rows
    )
    panel_count = 4 if gyro_present else 3
    fig, axes = plt.subplots(panel_count, 1, figsize=(13, 3.0 * panel_count + 2.6), sharex=True)
    if panel_count == 1:
        axes = [axes]

    for axis, (_, y_label, values) in zip(axes, channels, strict=False):
        plot_times, plot_values = _gap_aware_series(local_times, values, scan_interval_seconds)
        axis.plot(plot_times, plot_values, linewidth=1.0)
        axis.set_ylabel(y_label)
        axis.grid(True, linewidth=0.5, alpha=0.35)

    if gyro_present:
        gyro_axis = axes[-1]
        for label, values in (
            ("X", [row.gyro_x for row in rows]),
            ("Y", [row.gyro_y for row in rows]),
            ("Z", [row.gyro_z for row in rows]),
        ):
            plot_times, plot_values = _gap_aware_series(local_times, values, scan_interval_seconds)
            gyro_axis.plot(plot_times, plot_values, linewidth=0.9, label=label)
        gyro_axis.set_ylabel(t("Raw gyro [signed int16]"))
        gyro_axis.grid(True, linewidth=0.5, alpha=0.35)
        gyro_axis.legend(loc="best", ncol=3)

    for axis in axes:
        axis.set_xlim(period.start_local, period.end_local)
    axes[-1].set_xlabel(t("Local time [{timezone}]", timezone=timezone_name))
    if period.kind == "daily":
        axes[-1].xaxis.set_major_locator(mdates.HourLocator(interval=2, tz=tz))
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M", tz=tz))
    else:
        axes[-1].xaxis.set_major_locator(mdates.DayLocator(tz=tz))
        axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.", tz=tz))

    model = metadata["device_model"]
    serial = metadata["serial"]
    fig.suptitle(
        t("{model} — Radiation monitoring report", model=model) + "\n" +
        t("Serial: {serial} | Period: {period} | Timezone: {timezone}", serial=serial, period=period.label, timezone=timezone_name),
        fontsize=14,
    )

    stats = build_statistics(rows, expected_count=expected_samples(period, scan_interval_seconds))
    stats_text = _statistics_text(stats, t=t)
    footer = t(
        "Sampling interval: {interval} s | Samples: {samples}/{expected} | Completeness: {completeness:.2f}% | Generated: {generated} | App {version}",
        interval=scan_interval_seconds,
        samples=stats["samples"],
        expected=stats["expected_samples"],
        completeness=stats["completeness_percent"],
        generated=metadata["generated_at_utc"],
        version=metadata["app_version"],
    )
    fig.text(0.01, 0.048, stats_text, va="bottom", ha="left", family="monospace", fontsize=8.5)
    fig.text(0.01, 0.012, footer, va="bottom", ha="left", fontsize=8)
    fig.tight_layout(rect=(0, 0.12, 1, 0.93))

    output = io.BytesIO()
    fig.savefig(
        output,
        format="png",
        dpi=160,
        bbox_inches="tight",
        metadata={
            "Title": t("GMC radiation monitoring report {period}", period=period.label),
            "Author": "GMC Home Assistant App",
            "Description": json.dumps(metadata, separators=(",", ":"), sort_keys=True),
        },
    )
    plt.close(fig)
    return output.getvalue()


def _statistics_text(stats: dict[str, Any], *, t: Translator | None = None) -> str:
    t = t or Translator("en")
    if stats["cpm_mean"] is None:
        return t("CPM statistics: no accepted measurements in selected period")
    return t(
        "CPM statistics  min {minimum:.0f} | max {maximum:.0f} | mean {mean:.2f} | median {median:.2f} | SD {sd:.2f} | P95 {p95:.2f} | missing {missing}",
        minimum=stats["cpm_min"],
        maximum=stats["cpm_max"],
        mean=stats["cpm_mean"],
        median=stats["cpm_median"],
        sd=stats["cpm_standard_deviation"],
        p95=stats["cpm_95th_percentile"],
        missing=stats["missing_samples"],
    )


def analysis_document(
    *,
    period: ReportPeriod,
    timezone_name: str,
    scan_interval_seconds: int,
    rows: list[HistoryRow],
    baseline_rows: list[HistoryRow],
    device_metadata: dict[str, str],
    cpm_per_usvh: float,
    yellow_percent: float,
    red_percent: float,
    language: str = "en",
) -> dict[str, Any]:
    t = Translator(language)
    expected_count = expected_samples(period, scan_interval_seconds)
    analysis = _analysis_for_rows(
        rows,
        expected_count=expected_count,
        scan_interval_seconds=scan_interval_seconds,
        baseline_rows=baseline_rows,
        yellow_percent=yellow_percent,
        red_percent=red_percent,
    )
    return {
        "analysis_schema_version": 1,
        "app_version": device_metadata.get("app_version", APP_VERSION),
        "device_model": normalize_device_version_display(device_metadata.get("device_model", t("Unknown GMC"))),
        "hardware_model": device_metadata.get("hardware_model"),
        "firmware_version": device_metadata.get("firmware_version"),
        "device_time": device_metadata.get("device_time"),
        "device_clock_offset_seconds": _metadata_int(device_metadata.get("device_clock_offset_seconds")),
        "heartbeat_enabled": device_metadata.get("heartbeat_enabled") == "True",
        "serial": device_metadata.get("serial", t("unknown")),
        "period_kind": period.kind,
        "period_label": period.label,
        "timezone": timezone_name,
        "sample_interval_seconds": scan_interval_seconds,
        "cpm_per_usvh": cpm_per_usvh,
        "traffic_light_yellow_percent": yellow_percent,
        "traffic_light_red_percent": red_percent,
        "generated_at_utc": datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "language": language,
        "presentation": build_period_analysis_result(analysis).as_dict(),
        "statistics": analysis,
        "derived_dose_rate_usvh": {
            "mean": analysis.get("cpm_mean") / cpm_per_usvh if analysis.get("cpm_mean") is not None else None,
            "median": analysis.get("cpm_median") / cpm_per_usvh if analysis.get("cpm_median") is not None else None,
            "maximum": analysis.get("cpm_max") / cpm_per_usvh if analysis.get("cpm_max") is not None else None,
        },
        "notes": [
            t("CPM is the primary measurement."),
            t("Dose-rate values are derived from CPM using the configured conversion factor."),
            t("The traffic light and events are relative anomaly indicators, not safety classifications."),
        ],
        "display_labels": {
            "statistics": t("Statistics"),
            "derived_dose_rate_usvh": t("Derived dose rate"),
            "mean": t("Mean"),
            "median": t("Median"),
            "maximum": t("Maximum"),
        },
    }


def daily_summary_csv_bytes(
    rows: list[HistoryRow], *, tz: ZoneInfo, scan_interval_seconds: int, language: str = "en"
) -> bytes:
    # CSV field identifiers and enum values stay stable for automation consumers.
    del language
    groups: dict[date, list[HistoryRow]] = {}
    for row in rows:
        local_date = datetime.fromtimestamp(row.timestamp_utc, UTC).astimezone(tz).date()
        groups.setdefault(local_date, []).append(row)
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow([
        "date", "samples", "expected_samples", "coverage_percent", "mean_cpm", "median_cpm",
        "sd_cpm", "p95_cpm", "p99_cpm", "min_cpm", "max_cpm", "fano_factor",
        "poisson_sd_ratio", "temperature_correlation", "voltage_correlation", "longest_gap_seconds",
        "data_quality",
    ])
    for day, day_rows in sorted(groups.items()):
        start = datetime.combine(day, dt_time.min, tzinfo=tz)
        end = start + timedelta(days=1)
        period = ReportPeriod("daily", day.isoformat(), start, end)
        stats = build_statistics(day_rows, expected_count=expected_samples(period, scan_interval_seconds))
        cpms = [float(row.cpm) for row in day_rows]
        variance = statistics.variance(cpms) if len(cpms) > 1 else None
        mean = stats.get("cpm_mean")
        sd = stats.get("cpm_standard_deviation")
        fano = variance / mean if variance is not None and mean and mean > 0 else None
        poisson = sd / math.sqrt(mean) if sd is not None and mean and mean > 0 else None
        temp_corr, _ = _pearson_correlation([(float(row.cpm), float(row.temperature_c)) for row in day_rows if row.temperature_c is not None])
        volt_corr, _ = _pearson_correlation([(float(row.cpm), float(row.voltage_v)) for row in day_rows if row.voltage_v is not None])
        quality = data_quality_summary(
            day_rows, expected_count=int(stats["expected_samples"]), scan_interval_seconds=scan_interval_seconds
        )
        writer.writerow([
            day.isoformat(), stats["samples"], stats["expected_samples"], f"{stats['completeness_percent']:.3f}",
            _csv_value(mean), _csv_value(stats.get("cpm_median")), _csv_value(sd),
            _csv_value(stats.get("cpm_95th_percentile")), _csv_value(_percentile(cpms, 0.99)),
            _csv_value(stats.get("cpm_min")), _csv_value(stats.get("cpm_max")), _csv_value(fano),
            _csv_value(poisson), _csv_value(temp_corr), _csv_value(volt_corr), quality["longest_gap_seconds"],
            quality["label"],
        ])
    return output.getvalue().encode("utf-8")


def events_csv_bytes(events: list[dict[str, Any]], tz: ZoneInfo, *, language: str = "en") -> bytes:
    # Preserve stable machine-readable CSV names and severity enum values.
    del language
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow([
        "start_time_utc", "start_time_local", "end_time_utc", "end_time_local", "duration_seconds",
        "severity", "max_cpm", "mean_cpm", "max_background_index_percent",
    ])
    for event in events:
        start_utc = datetime.fromtimestamp(int(event["start_timestamp_utc"]), UTC)
        end_utc = datetime.fromtimestamp(int(event["end_timestamp_utc"]), UTC)
        writer.writerow([
            start_utc.isoformat(timespec="seconds").replace("+00:00", "Z"),
            start_utc.astimezone(tz).isoformat(timespec="seconds"),
            end_utc.isoformat(timespec="seconds").replace("+00:00", "Z"),
            end_utc.astimezone(tz).isoformat(timespec="seconds"),
            event["duration_seconds"], event["severity"], event["max_cpm"],
            f"{event['mean_cpm']:.6f}", f"{event['max_background_index_percent']:.3f}",
        ])
    return output.getvalue().encode("utf-8")


def annotations_csv_bytes(annotations: list[dict[str, Any]], tz: ZoneInfo) -> bytes:
    output = io.StringIO(newline="")
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow([
        "id", "device_serial", "start_time_utc", "start_time_local", "end_time_utc",
        "end_time_local", "category", "status", "note", "created_at_utc", "updated_at_utc",
    ])
    for item in annotations:
        start = datetime.fromtimestamp(int(item["start_timestamp_utc"]), UTC)
        end = datetime.fromtimestamp(int(item["end_timestamp_utc"]), UTC)
        writer.writerow([
            int(item.get("id") or 0), str(item.get("device_serial") or ""),
            start.isoformat(timespec="seconds").replace("+00:00", "Z"),
            start.astimezone(tz).isoformat(timespec="seconds"),
            end.isoformat(timespec="seconds").replace("+00:00", "Z"),
            end.astimezone(tz).isoformat(timespec="seconds"),
            str(item.get("category") or ""), str(item.get("status") or ""),
            str(item.get("note") or ""), int(item.get("created_at_utc") or 0),
            int(item.get("updated_at_utc") or 0),
        ])
    return output.getvalue().encode("utf-8")


def histogram_png_bytes(rows: list[HistoryRow], *, title: str, language: str = "en") -> bytes:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    t = Translator(language)
    values = [int(row.cpm) for row in rows]
    fig, axis = plt.subplots(figsize=(10, 6))
    if values:
        minimum, maximum = min(values), max(values)
        bins = list(range(minimum, maximum + 2))
        axis.hist(values, bins=bins, align="left", rwidth=0.82, alpha=0.65, label=t("Observed"))
        mean = statistics.fmean(values)
        xs = list(range(minimum, maximum + 1))
        expected = [len(values) * math.exp(-mean + x * math.log(mean) - math.lgamma(x + 1)) for x in xs] if mean > 0 else [0.0 for _ in xs]
        axis.plot(xs, expected, marker="o", linewidth=1.5, label=t("Poisson expectation (λ={mean:.2f})", mean=mean))
        axis.legend()
    else:
        axis.text(0.5, 0.5, t("No measurements in selected period"), ha="center", va="center", transform=axis.transAxes)
    axis.set_title(t("CPM distribution — {title}", title=title))
    axis.set_xlabel("CPM")
    axis.set_ylabel(t("Number of samples"))
    axis.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    output = io.BytesIO()
    fig.savefig(output, format="png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    return output.getvalue()


def heatmap_png_bytes(rows: list[HistoryRow], *, tz: ZoneInfo, title: str, language: str = "en") -> bytes:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    t = Translator(language)
    sums = [[0.0 for _ in range(24)] for _ in range(7)]
    counts = [[0 for _ in range(24)] for _ in range(7)]
    for row in rows:
        local = datetime.fromtimestamp(row.timestamp_utc, UTC).astimezone(tz)
        sums[local.weekday()][local.hour] += float(row.cpm)
        counts[local.weekday()][local.hour] += 1
    matrix = [
        [sums[d][h] / counts[d][h] if counts[d][h] else math.nan for h in range(24)]
        for d in range(7)
    ]
    fig, axis = plt.subplots(figsize=(12, 5.5))
    image = axis.imshow(matrix, aspect="auto", interpolation="nearest")
    axis.set_title(t("Mean CPM by weekday and hour — {title}", title=title))
    axis.set_xlabel(t("Local hour"))
    axis.set_ylabel(t("Weekday"))
    axis.set_xticks(range(0, 24, 2))
    axis.set_yticks(range(7), labels=[t("Mon"), t("Tue"), t("Wed"), t("Thu"), t("Fri"), t("Sat"), t("Sun")])
    fig.colorbar(image, ax=axis, label=t("Mean CPM"))
    fig.tight_layout()
    output = io.BytesIO()
    fig.savefig(output, format="png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    return output.getvalue()


def pdf_bytes(
    rows: list[HistoryRow], *, period: ReportPeriod, tz: ZoneInfo, timezone_name: str,
    scan_interval_seconds: int, device_metadata: dict[str, str], analysis: dict[str, Any],
    language: str = "en",
) -> bytes:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    t = Translator(language)
    output = io.BytesIO()
    with PdfPages(output, metadata={
        "Title": t("GMC analysis report {period}", period=period.label),
        "Author": "GMC Home Assistant App",
        "Subject": t("Radiation monitoring analysis"),
    }) as pdf:
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.suptitle(t("GMC radiation analysis report"), fontsize=18, y=0.97)
        quality = analysis["data_quality"]
        lines = [
            t("Device: {value}", value=normalize_device_version_display(device_metadata.get("device_model", t("Unknown GMC")))),
            t("Serial: {value}", value=device_metadata.get("serial", t("unknown"))),
            t("Period: {period} ({timezone})", period=period.label, timezone=timezone_name),
            t("Sampling interval: {seconds} s", seconds=scan_interval_seconds),
            "",
            t("Samples: {samples} / {expected}", samples=analysis["samples"], expected=analysis["expected_samples"]),
            t("Completeness: {value:.2f}%", value=analysis["completeness_percent"]),
            t("Data quality: {value}", value=t(str(quality["label"]))),
            t("Longest gap: {seconds} s", seconds=quality["longest_gap_seconds"]),
            "",
            t("Mean: {value} CPM", value=_format_number(analysis.get("cpm_mean"))),
            t("Median: {value} CPM", value=_format_number(analysis.get("cpm_median"))),
            t("SD: {value} CPM", value=_format_number(analysis.get("cpm_standard_deviation"))),
            t("P95: {value} CPM", value=_format_number(analysis.get("cpm_95th_percentile"))),
            t("P99: {value} CPM", value=_format_number(_percentile([float(r.cpm) for r in rows], 0.99))),
            t("Minimum / maximum: {minimum} / {maximum} CPM", minimum=_format_number(analysis.get("cpm_min")), maximum=_format_number(analysis.get("cpm_max"))),
            t("Fano factor: {value}", value=_format_number(analysis.get("fano_factor"), 3)),
            t("Poisson SD ratio: {value}", value=_format_number(analysis.get("poisson_sd_ratio"), 3)),
            "",
            t("Baseline: {value} CPM", value=_format_number(analysis.get("baseline_mean_cpm"))),
            t("Baseline deviation: {cpm} CPM ({percent}%)", cpm=_format_signed(analysis.get("baseline_deviation_cpm")), percent=_format_signed(analysis.get("baseline_deviation_percent"))),
            t("Baseline drift: {value}%", value=_format_signed(analysis.get("baseline_drift", {}).get("percent"))),
            t("Detected relative anomaly events: {count}", count=analysis.get("event_count", 0)),
            "",
            t("Dose-rate values, traffic-light states and events are derived indicators. CPM remains the primary measurement."),
            t("This report is descriptive and is not a radiation-safety classification."),
        ]
        fig.text(0.08, 0.91, "\n".join(lines), va="top", family="monospace", fontsize=10)
        pdf.savefig(fig, bbox_inches="tight")
        plt.close(fig)

        annotations = list(analysis.get("annotations") or [])
        if annotations:
            annotation_lines: list[str] = []
            for item in sorted(annotations, key=lambda value: int(value.get("start_timestamp_utc") or 0)):
                start = datetime.fromtimestamp(int(item.get("start_timestamp_utc") or 0), UTC).astimezone(tz).strftime("%Y-%m-%d %H:%M %Z")
                end = datetime.fromtimestamp(int(item.get("end_timestamp_utc") or item.get("start_timestamp_utc") or 0), UTC).astimezone(tz).strftime("%Y-%m-%d %H:%M %Z")
                heading = f"{start} – {end} · {t(str(item.get('category') or 'Other'))} · {t(str(item.get('status') or 'Note'))}"
                annotation_lines.append(heading)
                annotation_lines.extend("  " + line for line in textwrap.wrap(str(item.get("note") or ""), width=92) or [""])
                annotation_lines.append("")
            page_size = 38
            for offset in range(0, len(annotation_lines), page_size):
                fig = plt.figure(figsize=(8.27, 11.69))
                fig.suptitle(t("Event notes"), fontsize=18, y=0.97)
                fig.text(0.07, 0.92, "\n".join(annotation_lines[offset:offset + page_size]), va="top", family="monospace", fontsize=9)
                pdf.savefig(fig, bbox_inches="tight")
                plt.close(fig)

        for payload, caption in (
            (png_bytes(rows, period=period, tz=tz, timezone_name=timezone_name, scan_interval_seconds=scan_interval_seconds, device_metadata=device_metadata, language=language), t("Time series")),
            (histogram_png_bytes(rows, title=period.label, language=language), t("CPM distribution and Poisson comparison")),
            (heatmap_png_bytes(rows, tz=tz, title=period.label, language=language), t("Weekday/hour heatmap")),
        ):
            fig, axis = plt.subplots(figsize=(11.69, 8.27))
            axis.imshow(plt.imread(io.BytesIO(payload)))
            axis.set_title(caption)
            axis.axis("off")
            pdf.savefig(fig, bbox_inches="tight")
            plt.close(fig)
    return output.getvalue()


def _format_number(value: Any, decimals: int = 2) -> str:
    return "—" if value is None else f"{float(value):.{decimals}f}"


def _format_signed(value: Any, decimals: int = 2) -> str:
    return "—" if value is None else f"{float(value):+.{decimals}f}"

def report_filename(device_metadata: dict[str, str], period: ReportPeriod, extension: str) -> str:
    serial = device_metadata.get("serial", "unknown")
    return f"gmc_{serial}_{period.kind}_{period.filename_label}.{extension}"


def _prepare_report(
    store: HistoryStore,
    *,
    period: ReportPeriod,
    timezone_name: str,
    scan_interval_seconds: int,
    cpm_per_usvh: float,
    traffic_light_yellow_percent: float,
    traffic_light_red_percent: float,
    device_serial: str | None,
    all_devices: bool,
    language: str,
) -> tuple[
    Translator,
    ZoneInfo,
    list[HistoryRow],
    list[dict[str, Any]],
    dict[str, str],
    dict[str, Any],
    dict[str, Any],
]:
    t = Translator(language)
    tz = load_timezone(timezone_name)
    start_ts = int(period.start_utc.timestamp())
    end_ts = int(period.end_utc.timestamp())
    rows = store.query_range(
        start_ts, end_ts, device_serial=device_serial, all_devices=all_devices
    )
    raw_rows = store.query_raw_measurements(
        start_ts, end_ts, device_serial=None if all_devices else device_serial
    )
    baseline_rows = store.query_range(
        start_ts - 7 * 86400,
        start_ts,
        device_serial=device_serial,
        all_devices=all_devices,
    )
    metadata = store.get_metadata()
    if all_devices:
        metadata = {
            **metadata,
            "serial": "all_devices",
            "device_model": t("All connected GMC devices"),
            "device_profile": "mixed",
            "device_profile_name": t("Mixed device profiles"),
        }
    elif device_serial:
        device = next(
            (item for item in store.list_devices() if str(item.get("serial")) == device_serial),
            None,
        )
        if device:
            metadata = {
                **metadata,
                "serial": device_serial,
                "device_model": normalize_device_version_display(
                    str(device.get("device_model", t("Unknown GMC")))
                ),
                "hardware_model": str(device.get("hardware_model", "")),
                "firmware_version": str(device.get("firmware_version", "")),
                "device_time": str(device.get("device_time", "")),
                "device_clock_offset_seconds": str(
                    device.get("device_clock_offset_seconds", "")
                ),
                "heartbeat_enabled": str(bool(device.get("heartbeat_enabled", False))),
                "device_profile": str(device.get("device_profile", "unknown")),
                "device_profile_name": t(
                    str(
                        device.get(
                            "device_profile_name",
                            device.get("device_profile", "unknown"),
                        )
                    )
                ),
            }
    annotations = store.list_event_annotations(
        start_utc=start_ts,
        end_utc=end_ts,
        device_serial=None if all_devices else device_serial,
        limit=1000,
    )
    analysis = _analysis_for_rows(
        rows,
        expected_count=expected_samples(period, scan_interval_seconds),
        scan_interval_seconds=scan_interval_seconds,
        baseline_rows=baseline_rows,
        yellow_percent=traffic_light_yellow_percent,
        red_percent=traffic_light_red_percent,
    )
    analysis["annotations"] = annotations
    analysis_payload = analysis_document(
        period=period,
        timezone_name=timezone_name,
        scan_interval_seconds=scan_interval_seconds,
        rows=rows,
        baseline_rows=baseline_rows,
        device_metadata=metadata,
        cpm_per_usvh=cpm_per_usvh,
        yellow_percent=traffic_light_yellow_percent,
        red_percent=traffic_light_red_percent,
        language=language,
    )
    analysis_payload["annotations"] = annotations
    return t, tz, rows, raw_rows, metadata, analysis, analysis_payload


def build_report_to_path(
    store: HistoryStore,
    destination_path: str | Path,
    *,
    period: ReportPeriod,
    timezone_name: str,
    scan_interval_seconds: int,
    output_format: str,
    cpm_per_usvh: float = 154.0,
    traffic_light_yellow_percent: float = 125.0,
    traffic_light_red_percent: float = 175.0,
    device_serial: str | None = None,
    all_devices: bool = False,
    language: str = "en",
) -> tuple[str, str, Path]:
    """Build a report directly into a file.

    ZIP bundles are written incrementally and no longer retain the complete
    archive plus every artifact in memory at the same time.
    """
    destination = Path(destination_path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    _t, tz, rows, raw_rows, metadata, analysis, analysis_payload = _prepare_report(
        store,
        period=period,
        timezone_name=timezone_name,
        scan_interval_seconds=scan_interval_seconds,
        cpm_per_usvh=cpm_per_usvh,
        traffic_light_yellow_percent=traffic_light_yellow_percent,
        traffic_light_red_percent=traffic_light_red_percent,
        device_serial=device_serial,
        all_devices=all_devices,
        language=language,
    )

    def write(payload: bytes) -> None:
        with destination.open("wb") as handle:
            handle.write(payload)

    if output_format == "csv":
        filename, content_type = report_filename(metadata, period, "csv"), "text/csv; charset=utf-8"
        write(csv_bytes(rows, tz, language=language))
    elif output_format == "raw-archive-csv":
        filename, content_type = (
            report_filename(metadata, period, "raw_archive.csv"),
            "text/csv; charset=utf-8",
        )
        write(raw_measurements_csv_bytes(raw_rows, tz))
    elif output_format == "png":
        filename, content_type = report_filename(metadata, period, "png"), "image/png"
        write(
            png_bytes(
                rows,
                period=period,
                tz=tz,
                timezone_name=timezone_name,
                scan_interval_seconds=scan_interval_seconds,
                device_metadata=metadata,
                language=language,
            )
        )
    elif output_format == "analysis-json":
        filename, content_type = (
            report_filename(metadata, period, "analysis.json"),
            "application/json; charset=utf-8",
        )
        write(json.dumps(analysis_payload, indent=2, sort_keys=True).encode("utf-8"))
    elif output_format == "daily-summary-csv":
        filename, content_type = (
            report_filename(metadata, period, "daily_summary.csv"),
            "text/csv; charset=utf-8",
        )
        write(
            daily_summary_csv_bytes(
                rows,
                tz=tz,
                scan_interval_seconds=scan_interval_seconds,
                language=language,
            )
        )
    elif output_format == "events-csv":
        filename, content_type = (
            report_filename(metadata, period, "events.csv"),
            "text/csv; charset=utf-8",
        )
        write(events_csv_bytes(analysis["events"], tz, language=language))
    elif output_format == "histogram-png":
        filename, content_type = report_filename(metadata, period, "histogram.png"), "image/png"
        write(histogram_png_bytes(rows, title=period.label, language=language))
    elif output_format == "heatmap-png":
        filename, content_type = report_filename(metadata, period, "heatmap.png"), "image/png"
        write(
            heatmap_png_bytes(
                rows, tz=tz, title=period.label, language=language
            )
        )
    elif output_format == "pdf":
        filename, content_type = (
            report_filename(metadata, period, "analysis.pdf"),
            "application/pdf",
        )
        write(
            pdf_bytes(
                rows,
                period=period,
                tz=tz,
                timezone_name=timezone_name,
                scan_interval_seconds=scan_interval_seconds,
                device_metadata=metadata,
                analysis=analysis,
                language=language,
            )
        )
    elif output_format == "zip":
        filename, content_type = report_filename(metadata, period, "zip"), "application/zip"
        with zipfile.ZipFile(
            destination,
            "w",
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=True,
        ) as bundle:
            bundle.writestr(
                report_filename(metadata, period, "csv"),
                csv_bytes(rows, tz, language=language),
            )
            bundle.writestr(
                report_filename(metadata, period, "raw_archive.csv"),
                raw_measurements_csv_bytes(raw_rows, tz),
            )
            bundle.writestr(
                report_filename(metadata, period, "png"),
                png_bytes(
                    rows,
                    period=period,
                    tz=tz,
                    timezone_name=timezone_name,
                    scan_interval_seconds=scan_interval_seconds,
                    device_metadata=metadata,
                    language=language,
                ),
            )
            bundle.writestr(
                report_filename(metadata, period, "analysis.json"),
                json.dumps(analysis_payload, indent=2, sort_keys=True).encode("utf-8"),
            )
            bundle.writestr(
                report_filename(metadata, period, "daily_summary.csv"),
                daily_summary_csv_bytes(
                    rows,
                    tz=tz,
                    scan_interval_seconds=scan_interval_seconds,
                    language=language,
                ),
            )
            bundle.writestr(
                report_filename(metadata, period, "events.csv"),
                events_csv_bytes(analysis["events"], tz, language=language),
            )
            bundle.writestr(
                report_filename(metadata, period, "annotations.csv"),
                annotations_csv_bytes(list(analysis.get("annotations") or []), tz),
            )
            bundle.writestr(
                report_filename(metadata, period, "histogram.png"),
                histogram_png_bytes(rows, title=period.label, language=language),
            )
            bundle.writestr(
                report_filename(metadata, period, "heatmap.png"),
                heatmap_png_bytes(rows, tz=tz, title=period.label, language=language),
            )
            bundle.writestr(
                report_filename(metadata, period, "analysis.pdf"),
                pdf_bytes(
                    rows,
                    period=period,
                    tz=tz,
                    timezone_name=timezone_name,
                    scan_interval_seconds=scan_interval_seconds,
                    device_metadata=metadata,
                    analysis=analysis,
                    language=language,
                ),
            )
            bundle.writestr(
                report_filename(metadata, period, "metadata.json"),
                json.dumps(
                    metadata_document(
                        period=period,
                        timezone_name=timezone_name,
                        scan_interval_seconds=scan_interval_seconds,
                        rows=rows,
                        device_metadata=metadata,
                    ),
                    indent=2,
                    sort_keys=True,
                ).encode("utf-8"),
            )
    else:
        raise ValueError(f"Unsupported report format: {output_format}")
    secure_file(destination)
    return filename, content_type, destination


def build_report(
    store: HistoryStore,
    *,
    period: ReportPeriod,
    timezone_name: str,
    scan_interval_seconds: int,
    output_format: str,
    cpm_per_usvh: float = 154.0,
    traffic_light_yellow_percent: float = 125.0,
    traffic_light_red_percent: float = 175.0,
    device_serial: str | None = None,
    all_devices: bool = False,
    language: str = "en",
) -> tuple[str, str, bytes]:
    """Compatibility wrapper returning bytes for callers outside the web server."""
    fd, temp_name = tempfile.mkstemp(prefix="gmc-report-build-", suffix=".tmp")
    os.close(fd)
    temp_path = Path(temp_name)
    try:
        filename, content_type, _path = build_report_to_path(
            store,
            temp_path,
            period=period,
            timezone_name=timezone_name,
            scan_interval_seconds=scan_interval_seconds,
            output_format=output_format,
            cpm_per_usvh=cpm_per_usvh,
            traffic_light_yellow_percent=traffic_light_yellow_percent,
            traffic_light_red_percent=traffic_light_red_percent,
            device_serial=device_serial,
            all_devices=all_devices,
            language=language,
        )
        return filename, content_type, temp_path.read_bytes()
    finally:
        temp_path.unlink(missing_ok=True)
