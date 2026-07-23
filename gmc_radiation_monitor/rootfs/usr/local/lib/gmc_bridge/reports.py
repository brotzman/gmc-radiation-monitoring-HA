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
from dataclasses import dataclass, replace
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
from .metrology import (
    ALGORITHM_VERSION,
    DualTubeMetrologyConfig,
    MetrologyConfig,
    TubeMetrologyProfile,
    derived_dose_estimate,
    derived_dual_tube_dose_estimate,
    integrated_dose_estimate,
    integrated_dual_tube_dose_estimate,
)
from .quality_pipeline import filter_history_rows, robust_sigma, robust_trimmed_mean
from .report_statistics import build_statistics, pearson_correlation as _pearson_correlation, percentile as _percentile
from .scientific_analysis import (
    counting_uncertainty,
    detect_persistent_level_shift,
    recent_change_significance,
)
from .time_series import time_weighted_summary
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


def _analysis_for_rows(
    rows: list[HistoryRow],
    *,
    expected_count: int,
    scan_interval_seconds: int,
    start_utc: int | None = None,
    end_utc: int | None = None,
    baseline_rows: list[HistoryRow],
    yellow_percent: float,
    red_percent: float,
) -> dict[str, Any]:
    stats = build_statistics(
        rows,
        expected_count=expected_count,
        start_utc=start_utc,
        end_utc=end_utc,
        scan_interval_seconds=scan_interval_seconds,
    )
    baseline_values = [float(row.cpm) for row in baseline_rows]
    baseline_mean = None
    if baseline_rows:
        baseline_start = int(baseline_rows[0].timestamp_utc)
        baseline_end = max(baseline_start + scan_interval_seconds, int(baseline_rows[-1].timestamp_utc) + scan_interval_seconds)
        baseline_weighted = time_weighted_summary(
            baseline_rows, timestamp=lambda row: row.timestamp_utc, value=lambda row: row.cpm,
            start_utc=baseline_start, end_utc=baseline_end, expected_interval_seconds=scan_interval_seconds,
        )
        baseline_mean = baseline_weighted.mean if baseline_weighted.available else statistics.fmean(baseline_values)
    if baseline_mean is None:
        baseline_mean = stats.get("cpm_mean")
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
    quality = data_quality_summary(
        rows, expected_count=expected_count, scan_interval_seconds=scan_interval_seconds
    )
    recent_rows: list[HistoryRow] = []
    reference_rows: list[HistoryRow] = list(baseline_rows)
    if rows:
        recent_cutoff = int(rows[-1].timestamp_utc) - 3600
        recent_rows = [row for row in rows if int(row.timestamp_utc) > recent_cutoff]
        reference_rows.extend(row for row in rows if int(row.timestamp_utc) <= recent_cutoff)
    change_significance = recent_change_significance(
        recent_rows,
        reference_rows,
        quality_score=float(quality.get("score") or 0.0),
    )
    level_shift = detect_persistent_level_shift([*baseline_rows, *rows])
    return {
        **stats,
        "data_quality": quality,
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
        "change_significance": change_significance,
        "level_shift": level_shift,
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

    weighted_1h = time_weighted_summary(
        rows_1h, timestamp=lambda row: row.timestamp_utc, value=lambda row: row.cpm,
        start_utc=latest_timestamp - 3600, end_utc=latest_timestamp + 1,
        expected_interval_seconds=scan_interval_seconds,
    )
    weighted_24h = time_weighted_summary(
        rows_24h, timestamp=lambda row: row.timestamp_utc, value=lambda row: row.cpm,
        start_utc=latest_timestamp - 86400, end_utc=latest_timestamp + 1,
        expected_interval_seconds=scan_interval_seconds,
    )
    weighted_7d = time_weighted_summary(
        rows_7d, timestamp=lambda row: row.timestamp_utc, value=lambda row: row.cpm,
        start_utc=latest_timestamp - 7 * 86400, end_utc=latest_timestamp + 1,
        expected_interval_seconds=scan_interval_seconds,
    )
    mean_1h = weighted_1h.mean
    mean_24h = weighted_24h.mean
    mean_7d = weighted_7d.mean
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
    uncertainty_1h = counting_uncertainty(rows_1h, minimum_independent_window_seconds=60)
    uncertainty_24h = counting_uncertainty(rows_24h, minimum_independent_window_seconds=60)
    uncertainty_7d = counting_uncertainty(rows_7d, minimum_independent_window_seconds=60)
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

    def coverage(summary) -> float:
        return float(summary.coverage_percent)

    minimum_baseline_samples = max(6, round(21600 / max(60, scan_interval_seconds)))
    minimum_baseline_covered_seconds = max(0, 6 * 3600 - max(1, scan_interval_seconds))
    baseline_readiness_percent = min(
        100.0,
        100.0 * float(weighted_7d.covered_seconds) / float(minimum_baseline_covered_seconds),
    )
    baseline_ready = (
        mean_7d is not None
        and weighted_7d.covered_seconds >= minimum_baseline_covered_seconds
        and len(rows_7d) >= minimum_baseline_samples
    )
    recent_window_ready = mean_1h is not None and coverage(weighted_1h) >= 50.0

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
        "coverage_1h_percent": coverage(weighted_1h), "coverage_24h_percent": coverage(weighted_24h),
        "coverage_7d_percent": coverage(weighted_7d),
        "sample_coverage_1h_percent": min(100.0, 100.0 * len(rows_1h) / max(1, round(3600 / scan_interval_seconds))),
        "sample_coverage_24h_percent": min(100.0, 100.0 * len(rows_24h) / max(1, round(86400 / scan_interval_seconds))),
        "sample_coverage_7d_percent": min(100.0, 100.0 * len(rows_7d) / max(1, round(7 * 86400 / scan_interval_seconds))),
        "time_weighted_1h": weighted_1h.as_dict(),
        "time_weighted_24h": weighted_24h.as_dict(),
        "time_weighted_7d": weighted_7d.as_dict(),
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
        start_utc=int(period.start_utc.timestamp()),
        end_utc=int(period.end_utc.timestamp()),
        scan_interval_seconds=scan_interval_seconds,
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



def _metadata_int(value: object) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _metadata_float(value: object) -> float | None:
    if value in (None, ""):
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _metadata_mapping(value: object) -> dict[str, Any]:
    if isinstance(value, dict):
        return dict(value)
    if isinstance(value, str) and value.strip():
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            return {}
        return dict(parsed) if isinstance(parsed, dict) else {}
    return {}


def _tube_profile_from_metadata(value: object) -> TubeMetrologyProfile | None:
    profile = _metadata_mapping(value)
    if not profile:
        return None
    return TubeMetrologyProfile(
        tube_model=str(profile.get("tube_model") or ""),
        cpm_per_usvh=_metadata_float(profile.get("cpm_per_usvh")),
        dead_time_us=_metadata_float(profile.get("dead_time_us")),
        reliable_max_cpm=_metadata_int(profile.get("reliable_max_cpm")),
        dead_time_model=str(profile.get("dead_time_model") or "none"),
        conversion_factor_uncertainty_percent=_metadata_float(
            profile.get("conversion_factor_uncertainty_percent")
        ),
        calibration_uncertainty_percent=_metadata_float(
            profile.get("calibration_uncertainty_percent")
        ),
        calibration_reference=str(profile.get("calibration_reference") or ""),
    )


def _dual_tube_config_from_metadata(
    device_metadata: dict[str, Any],
    *,
    legacy_cpm_per_usvh: float,
) -> DualTubeMetrologyConfig:
    legacy_low = TubeMetrologyProfile(
        tube_model=str(device_metadata.get("tube_model") or ""),
        cpm_per_usvh=legacy_cpm_per_usvh,
        dead_time_us=_metadata_float(device_metadata.get("dead_time_us")),
        reliable_max_cpm=_metadata_int(device_metadata.get("reliable_max_cpm")),
        dead_time_model=str(device_metadata.get("dead_time_model") or "none"),
        conversion_factor_uncertainty_percent=_metadata_float(
            device_metadata.get("conversion_factor_uncertainty_percent")
        ),
        calibration_uncertainty_percent=_metadata_float(
            device_metadata.get("calibration_uncertainty_percent")
        ),
        calibration_reference=str(device_metadata.get("calibration_reference") or ""),
    )
    return DualTubeMetrologyConfig(
        mode=str(device_metadata.get("dual_tube_mode") or "single"),
        switch_cpm=_metadata_int(device_metadata.get("dual_tube_switch_cpm")),
        low_dose=(
            _tube_profile_from_metadata(device_metadata.get("low_dose_tube_profile"))
            or legacy_low
        ),
        high_dose=_tube_profile_from_metadata(device_metadata.get("high_dose_tube_profile")),
    )

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
        (t("Radiation count rate [CPM]"), t("Count rate [CPM]"), [row.cpm for row in rows]),
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
    axes[-1].set_xlabel(t("Local date and time") + f" [{timezone_name}]")
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

    stats = build_statistics(
        rows, expected_count=expected_samples(period, scan_interval_seconds),
        start_utc=int(period.start_utc.timestamp()), end_utc=int(period.end_utc.timestamp()),
        scan_interval_seconds=scan_interval_seconds,
    )
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
        start_utc=int(period.start_utc.timestamp()),
        end_utc=int(period.end_utc.timestamp()),
        baseline_rows=baseline_rows,
        yellow_percent=yellow_percent,
        red_percent=red_percent,
    )
    metrology = MetrologyConfig(
        dead_time_us=_metadata_float(device_metadata.get("dead_time_us")),
        reliable_max_cpm=_metadata_int(device_metadata.get("reliable_max_cpm")),
        dead_time_model=str(device_metadata.get("dead_time_model") or "none"),
        conversion_factor_uncertainty_percent=_metadata_float(
            device_metadata.get("conversion_factor_uncertainty_percent")
        ),
        calibration_uncertainty_percent=_metadata_float(
            device_metadata.get("calibration_uncertainty_percent")
        ),
        calibration_reference=str(device_metadata.get("calibration_reference") or ""),
        tube_model=str(device_metadata.get("tube_model") or ""),
    )
    dual_tube = _dual_tube_config_from_metadata(
        device_metadata, legacy_cpm_per_usvh=cpm_per_usvh
    )
    counting = counting_uncertainty(rows)
    low_values = [float(row.tube_low_cpm) for row in rows if row.tube_low_cpm is not None]
    high_values = [float(row.tube_high_cpm) for row in rows if row.tube_high_cpm is not None]
    low_mean = statistics.fmean(low_values) if low_values else None
    high_mean = statistics.fmean(high_values) if high_values else None

    if dual_tube.mode == "single":
        dose_estimate = derived_dose_estimate(
            cpm=analysis.get("cpm_mean"),
            cpm_per_usvh=cpm_per_usvh,
            counting_relative_percent=counting.get("relative_uncertainty_percent"),
            config=metrology,
            coverage_percent=analysis.get("completeness_percent"),
            gap_count=analysis.get("missing_samples"),
        )
        integrated_dose = integrated_dose_estimate(
            samples=[(row.timestamp_utc, row.cpm) for row in rows],
            cpm_per_usvh=cpm_per_usvh,
            config=metrology,
            expected_interval_seconds=scan_interval_seconds,
        )
        dose_rate_values = [
            estimate["value_usvh"]
            for row in rows
            if (
                estimate := derived_dose_estimate(
                    cpm=row.cpm,
                    cpm_per_usvh=cpm_per_usvh,
                    counting_relative_percent=None,
                    config=metrology,
                )
            )["available"]
        ]
    else:
        dose_estimate = derived_dual_tube_dose_estimate(
            primary_cpm=analysis.get("cpm_mean"),
            low_cpm=low_mean,
            high_cpm=high_mean,
            counting_relative_percent=counting.get("relative_uncertainty_percent"),
            config=dual_tube,
        )
        dose_estimate["coverage_percent"] = analysis.get("completeness_percent")
        dose_estimate["gap_count"] = analysis.get("missing_samples")
        integrated_dose = integrated_dual_tube_dose_estimate(
            samples=[
                (row.timestamp_utc, row.cpm, row.tube_low_cpm, row.tube_high_cpm)
                for row in rows
            ],
            config=dual_tube,
            expected_interval_seconds=scan_interval_seconds,
        )
        dose_rate_values = [
            estimate["value_usvh"]
            for row in rows
            if (
                estimate := derived_dual_tube_dose_estimate(
                    primary_cpm=row.cpm,
                    low_cpm=row.tube_low_cpm,
                    high_cpm=row.tube_high_cpm,
                    counting_relative_percent=None,
                    config=dual_tube,
                )
            )["available"]
        ]
    dose_rate_values = [float(value) for value in dose_rate_values if value is not None]
    return {
        "analysis_schema_version": 3,
        "algorithm_version": ALGORITHM_VERSION,
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
        "derived_dose_estimate": dose_estimate,
        "derived_integrated_dose_estimate": integrated_dose,
        "metrology_configuration": metrology.as_dict(),
        "dual_tube_configuration": dual_tube.as_dict(),
        "derived_dose_rate_usvh": {
            "qualification": "derived estimate",
            "mean": statistics.fmean(dose_rate_values) if dose_rate_values else None,
            "median": statistics.median(dose_rate_values) if dose_rate_values else None,
            "maximum": max(dose_rate_values) if dose_rate_values else None,
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
        stats = build_statistics(
            day_rows, expected_count=expected_samples(period, scan_interval_seconds),
            start_utc=int(start.timestamp()), end_utc=int(end.timestamp()),
            scan_interval_seconds=scan_interval_seconds,
        )
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
    axis.set_xlabel(t("Count rate [CPM]"))
    axis.set_ylabel(t("Accepted measurements [count]"))
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
    axis.set_xlabel(t("Local hour [h]"))
    axis.set_ylabel(t("Weekday"))
    axis.set_xticks(range(0, 24, 2))
    axis.set_yticks(range(7), labels=[t("Mon"), t("Tue"), t("Wed"), t("Thu"), t("Fri"), t("Sat"), t("Sun")])
    fig.colorbar(image, ax=axis, label=t("Mean count rate [CPM]"))
    fig.tight_layout()
    output = io.BytesIO()
    fig.savefig(output, format="png", dpi=160, bbox_inches="tight")
    plt.close(fig)
    return output.getvalue()


def _report_phrase(language: str, german: str, english: str) -> str:
    return german if language == "de" else english


def _report_state_label(language: str, state: object) -> str:
    value = str(state or "")
    german = {
        "Insufficient history for significance assessment": "Noch nicht genügend Verlauf für die Signifikanzbewertung",
        "Consistent with normal counting variation": "Mit normaler Zählstreuung vereinbar",
        "Statistically significant increase": "Statistisch signifikanter Anstieg",
        "Statistically significant decrease": "Statistisch signifikanter Rückgang",
        "Insufficient history for level-shift detection": "Verlauf für Niveauwechsel-Erkennung unzureichend",
        "Persistent level shift detected": "Niveauwechsel erkannt",
        "Possible persistent level shift": "Möglicher Niveauwechsel",
        "No persistent level shift detected": "Kein Niveauwechsel erkannt",
        "Very high": "Sehr hoch",
        "High": "Hoch",
        "Medium": "Mittel",
        "Low": "Niedrig",
        "Excellent": "Sehr hoch",
        "Good": "Hoch",
        "Fair": "Mittel",
        "Poor": "Niedrig",
        "no sensor variation": "Keine Sensorvariation",
        "insufficient paired samples": "Zu wenige gepaarte Messwerte",
    }
    return german.get(value, value) if language == "de" else value


def _rolling_mean(values: list[float], window: int) -> list[float]:
    if not values:
        return []
    effective = max(1, min(int(window), len(values)))
    result: list[float] = []
    running = 0.0
    for index, value in enumerate(values):
        running += float(value)
        if index >= effective:
            running -= float(values[index - effective])
        result.append(running / min(index + 1, effective))
    return result


def _report_assessment(
    analysis: dict[str, Any], *, language: str
) -> tuple[str, str, str, str]:
    if not int(analysis.get("samples") or 0):
        return (
            _report_phrase(language, "Keine Zeitraumsauswertung", "No period assessment"),
            _report_phrase(
                language,
                "Im ausgewählten Zeitraum liegen keine akzeptierten Messwerte vor.",
                "No accepted measurements are available for the selected period.",
            ),
            _report_phrase(
                language,
                "Geräteverbindung und Messintervall prüfen und den Bericht erneut erstellen.",
                "Check the device connection and sampling interval, then create the report again.",
            ),
            "unavailable",
        )
    quality = analysis.get("data_quality") or {}
    events = list(analysis.get("events") or [])
    change = analysis.get("change_significance") or {}
    red_event = any(str(item.get("severity")) == "red" for item in events)
    significant_increase = (
        bool(change.get("available"))
        and float(change.get("significance_sigma") or 0.0) >= 3.0
        and float(change.get("change_cpm") or 0.0) > 0.0
    )
    if red_event:
        return (
            _report_phrase(language, "Deutliche Anomalie erkannt", "Pronounced anomaly detected"),
            _report_phrase(
                language,
                "Mindestens ein anhaltendes Ereignis erreichte die rote relative Anomalieschwelle.",
                "At least one sustained event reached the red relative-anomaly threshold.",
            ),
            _report_phrase(
                language,
                "Messaufbau, Standort und mögliche lokale Quellen prüfen und die Entwicklung engmaschig weiter beobachten.",
                "Check the measurement setup, location and possible local sources, and continue close observation.",
            ),
            "warning",
        )
    if significant_increase:
        return (
            _report_phrase(language, "Statistisch signifikanter Anstieg", "Statistically significant increase"),
            _report_phrase(
                language,
                "Der jüngste Stundenwert weicht stärker von der Referenz ab, als durch normale Zählstreuung zu erwarten wäre.",
                "The most recent hourly rate differs from the reference more than expected from normal counting variation.",
            ),
            _report_phrase(
                language,
                "Messung fortsetzen, Position des Geräts unverändert lassen und bei anhaltendem Anstieg eine Vergleichsmessung durchführen.",
                "Continue measuring, keep the detector position unchanged and perform a comparison measurement if the increase persists.",
            ),
            "notice",
        )
    if events:
        return (
            _report_phrase(language, "Erhöhte Phase beobachten", "Observe elevated period"),
            _report_phrase(
                language,
                "Im Zeitraum wurde mindestens ein anhaltendes relatives Anomalieereignis erkannt.",
                "At least one sustained relative-anomaly event was detected in the period.",
            ),
            _report_phrase(
                language,
                "Ereigniszeiten mit Ortswechseln, Wartung oder bekannten Quellen abgleichen und den Verlauf weiter beobachten.",
                "Compare event times with movement, maintenance or known sources and continue monitoring the trend.",
            ),
            "notice",
        )
    if str(quality.get("label") or "Poor") == "Poor":
        return (
            _report_phrase(language, "Aussagekraft eingeschränkt", "Assessment limited"),
            _report_phrase(
                language,
                "Die Datenabdeckung oder zeitliche Kontinuität reicht für eine belastbare Zeitraumsaussage nicht aus.",
                "Data coverage or temporal continuity is insufficient for a robust period assessment.",
            ),
            _report_phrase(
                language,
                "Messlücken reduzieren und nach ausreichender zusätzlicher Messzeit einen neuen Bericht erstellen.",
                "Reduce measurement gaps and create a new report after sufficient additional measurement time.",
            ),
            "limited",
        )
    return (
        _report_phrase(language, "Im lokalen Hintergrundbereich", "Within local background range"),
        _report_phrase(
            language,
            "Es wurde kein anhaltender statistisch auffälliger Anstieg gegenüber dem lokalen Hintergrund erkannt.",
            "No sustained statistically unusual increase relative to the local background was detected.",
        ),
        _report_phrase(
            language,
            "Keine unmittelbare Maßnahme aus den Messdaten ableitbar; kontinuierliche Hintergrundmessung fortsetzen.",
            "No immediate action is indicated by the measurements; continue continuous background monitoring.",
        ),
        "normal",
    )


def _configure_report_axis(axis: Any) -> None:
    axis.spines[["top", "right"]].set_visible(False)
    axis.grid(True, linewidth=0.45, alpha=0.24)
    axis.tick_params(labelsize=7.5)


def _format_report_time_axis(axis: Any, tz: ZoneInfo) -> None:
    import matplotlib.dates as mdates

    start, end = axis.get_xlim()
    span_days = max(0.0, float(end - start))
    locator = mdates.AutoDateLocator(minticks=3, maxticks=7, tz=tz)
    axis.xaxis.set_major_locator(locator)
    if span_days <= 2.0:
        date_format = "%d.%m.\n%H:%M"
    elif span_days <= 90.0:
        date_format = "%d.%m.%Y"
    else:
        date_format = "%m.%Y"
    axis.xaxis.set_major_formatter(mdates.DateFormatter(date_format, tz=tz))


def _draw_report_header(
    fig: Any,
    *,
    title: str,
    subtitle: str,
    report_id: str,
    page_number: int,
    page_count: int,
    generated_at: datetime,
    language: str,
) -> None:
    fig.text(0.065, 0.965, title, fontsize=17, fontweight="bold", va="top")
    fig.text(0.065, 0.932, subtitle, fontsize=9.5, color="#475569", va="top")
    fig.text(
        0.935,
        0.965,
        report_id,
        fontsize=8.5,
        color="#475569",
        ha="right",
        va="top",
    )
    from matplotlib.lines import Line2D

    fig.lines.append(
        Line2D(
            [0.065, 0.935], [0.912, 0.912], transform=fig.transFigure, color="#cbd5e1", linewidth=0.8
        )
    )
    disclaimer = _report_phrase(
        language,
        "Orientierungshilfe; keine amtliche Dosimetrie, Gesundheits- oder Strahlenschutzberatung.",
        "Orientation only; not official dosimetry, health or radiation-protection advice.",
    )
    fig.text(0.065, 0.023, disclaimer, fontsize=6.8, color="#64748b", va="bottom")
    footer = (
        f"Radiation Monitoring {APP_VERSION} · {report_id} · "
        f"{generated_at.strftime('%Y-%m-%d %H:%M UTC')} · "
        f"{_report_phrase(language, 'Seite', 'Page')} {page_number}/{page_count}"
    )
    fig.text(0.935, 0.009, footer, fontsize=6.8, color="#64748b", ha="right", va="bottom")
    fig.lines.append(
        Line2D(
            [0.065, 0.935], [0.038, 0.038], transform=fig.transFigure, color="#cbd5e1", linewidth=0.7
        )
    )


def _draw_kpi(
    fig: Any,
    *,
    x: float,
    width: float,
    title: str,
    value: str,
    detail: str = "",
    value_font_size: float = 12.2,
    wrap_value: bool = False,
) -> None:
    from matplotlib.patches import FancyBboxPatch

    patch = FancyBboxPatch(
        (x, 0.805),
        width,
        0.075,
        boxstyle="round,pad=0.006,rounding_size=0.008",
        transform=fig.transFigure,
        linewidth=0.8,
        edgecolor="#bfdbfe",
        facecolor="#eff6ff",
    )
    fig.patches.append(patch)
    fig.text(x + 0.012, 0.863, title, fontsize=7.4, color="#475569", va="top")
    shown_value = textwrap.fill(value, width=22) if wrap_value else value
    fig.text(x + 0.012, 0.838, shown_value, fontsize=value_font_size, fontweight="bold", color="#0f172a", va="top", linespacing=1.05)
    if detail:
        fig.text(x + 0.012, 0.813, detail, fontsize=6.8, color="#64748b", va="bottom")


def _draw_table(
    axis: Any,
    rows: list[list[str]],
    *,
    columns: list[str] | None = None,
    font_size: float = 7.8,
    column_widths: list[float] | None = None,
) -> None:
    axis.axis("off")
    table = axis.table(
        cellText=rows,
        colLabels=columns,
        cellLoc="left",
        colLoc="left",
        colWidths=column_widths,
        bbox=[0, 0, 1, 1],
    )
    table.auto_set_font_size(False)
    table.set_fontsize(font_size)
    for (row_index, _column_index), cell in table.get_celld().items():
        cell.set_edgecolor("#d7dee8")
        cell.set_linewidth(0.55)
        if row_index == 0 and columns:
            cell.set_facecolor("#eaf2fb")
            cell.set_text_props(weight="bold", color="#334155")
        elif row_index % 2 == (1 if columns else 0):
            cell.set_facecolor("#f8fafc")
        cell.PAD = 0.08


def _daily_report_statistics(
    rows: list[HistoryRow], *, tz: ZoneInfo
) -> list[tuple[date, float, float, float]]:
    grouped: dict[date, list[float]] = {}
    for row in rows:
        day = datetime.fromtimestamp(row.timestamp_utc, UTC).astimezone(tz).date()
        grouped.setdefault(day, []).append(float(row.cpm))
    return [
        (day, min(values), statistics.median(values), max(values))
        for day, values in sorted(grouped.items())
        if values
    ]


def _report_weekday_hour_matrix(rows: list[HistoryRow], tz: ZoneInfo) -> list[list[float]]:
    sums = [[0.0 for _ in range(24)] for _ in range(7)]
    counts = [[0 for _ in range(24)] for _ in range(7)]
    for row in rows:
        local = datetime.fromtimestamp(row.timestamp_utc, UTC).astimezone(tz)
        sums[local.weekday()][local.hour] += float(row.cpm)
        counts[local.weekday()][local.hour] += 1
    return [
        [sums[day][hour] / counts[day][hour] if counts[day][hour] else math.nan for hour in range(24)]
        for day in range(7)
    ]


def _report_calendar_matrix(
    rows: list[HistoryRow], tz: ZoneInfo
) -> tuple[list[list[float]], list[date]]:
    grouped: dict[date, list[float]] = {}
    for row in rows:
        day = datetime.fromtimestamp(row.timestamp_utc, UTC).astimezone(tz).date()
        grouped.setdefault(day, []).append(float(row.cpm))
    if not grouped:
        return [[math.nan]], []
    dates = sorted(grouped)
    first_monday = dates[0] - timedelta(days=dates[0].weekday())
    last_monday = dates[-1] - timedelta(days=dates[-1].weekday())
    week_count = (last_monday - first_monday).days // 7 + 1
    matrix = [[math.nan for _ in range(week_count)] for _ in range(7)]
    for day, values in grouped.items():
        week_index = ((day - timedelta(days=day.weekday())) - first_monday).days // 7
        matrix[day.weekday()][week_index] = statistics.fmean(values)
    weeks = [first_monday + timedelta(days=7 * index) for index in range(week_count)]
    return matrix, weeks


# Normalized figure coordinates for page 1.  Keeping these values in one
# place makes the executive-summary layout testable and prevents the chart
# x-axis label from colliding with the assessment heading below it.
_PAGE1_CHART_RECT = (0.09, 0.555, 0.84, 0.19)
# Dedicated baseline for the metrology summary.  It sits below the complete
# x-axis label area and above the assessment panel so neither element can
# overlap, even with long localized labels.
_PAGE1_METROLOGY_Y = 0.495
_PAGE1_ASSESSMENT_RECT = (0.065, 0.345, 0.87, 0.125)
_PAGE1_STATS_HEADING_Y = 0.315


def _report_display_end(period: ReportPeriod, generated_at: datetime) -> datetime:
    """Return the visible end of a report chart.

    Completed periods retain their full calendar range.  A report for the
    currently running day or week ends at generation time instead of showing
    a large, misleading area of future time with no measurements.
    """
    generated_local = generated_at.astimezone(period.start_local.tzinfo)
    if period.start_local <= generated_local < period.end_local:
        return generated_local
    return period.end_local


def _draw_assessment_panel(
    fig: Any,
    *,
    title: str,
    explanation: str,
    recommendation: str,
) -> None:
    from matplotlib.patches import FancyBboxPatch

    x, y, width, height = _PAGE1_ASSESSMENT_RECT
    panel = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.008,rounding_size=0.008",
        transform=fig.transFigure,
        linewidth=0.7,
        edgecolor="#d7dee8",
        facecolor="#f8fafc",
    )
    fig.patches.append(panel)
    fig.text(x + 0.012, y + height - 0.018, title, fontsize=12.0, fontweight="bold", va="top")
    fig.text(
        x + 0.012,
        y + height - 0.052,
        textwrap.fill(explanation, width=112),
        fontsize=8.25,
        va="top",
        linespacing=1.25,
    )
    fig.text(
        x + 0.012,
        y + 0.020,
        textwrap.fill(recommendation, width=112),
        fontsize=8.25,
        va="bottom",
        linespacing=1.25,
    )


def _report_rows_for_data_mode(rows: list[HistoryRow], data_mode: str) -> list[HistoryRow]:
    mode = data_mode if data_mode in {"raw", "corrected", "comparison"} else "raw"
    result: list[HistoryRow] = []
    for row in rows:
        raw = float(row.raw_cpm if row.raw_cpm is not None else row.cpm)
        corrected = float(row.corrected_cpm if row.corrected_cpm is not None else raw)
        selected = corrected if mode == "corrected" else raw
        result.append(replace(row, cpm=round(selected), raw_cpm=raw, corrected_cpm=corrected))
    return result


def _report_metrology_summary(rows: list[HistoryRow], metadata: dict[str, Any]) -> dict[str, Any]:
    quality_values = [int(row.measurement_quality_index) for row in rows if row.measurement_quality_index is not None]
    load_values = [float(row.detector_load_percent) for row in rows if row.detector_load_percent is not None]
    loss_values = [float(row.dead_time_loss_percent) for row in rows if row.dead_time_loss_percent is not None]
    factor_values = [float(row.correction_factor) for row in rows if row.correction_factor is not None and math.isfinite(float(row.correction_factor))]
    quality_index = round(statistics.fmean(quality_values)) if quality_values else 0
    stars = 5 if quality_index >= 90 else 4 if quality_index >= 75 else 3 if quality_index >= 55 else 2 if quality_index >= 30 else 1
    status = str(metadata.get("calibration_status") or (rows[-1].calibration_status if rows else "unknown") or "unknown")
    source = str(metadata.get("calibration_source") or (rows[-1].calibration_source if rows else "unknown") or "unknown")
    validity = "fully_valid" if quality_index >= 85 else "qualified" if quality_index >= 50 else "limited"
    return {
        "quality_index": quality_index,
        "stars": "★" * stars + "☆" * (5 - stars),
        "load_mean": statistics.fmean(load_values) if load_values else None,
        "load_max": max(load_values) if load_values else None,
        "loss_mean": statistics.fmean(loss_values) if loss_values else None,
        "correction_factor_mean": statistics.fmean(factor_values) if factor_values else 1.0,
        "calibration_status": status,
        "calibration_source": source,
        "validity": validity,
        "detector_type": str(metadata.get("tube_model") or (rows[-1].detector_type if rows else "") or "—"),
        "dead_time_model": str(metadata.get("dead_time_model") or (rows[-1].dead_time_model if rows else "none") or "none"),
        "dead_time_us": metadata.get("dead_time_us") if metadata.get("dead_time_us") not in (None, "") else (rows[-1].dead_time_us if rows else None),
        "active_tube": str(rows[-1].active_tube if rows and rows[-1].active_tube else "—"),
    }


def pdf_bytes(
    rows: list[HistoryRow],
    *,
    period: ReportPeriod,
    tz: ZoneInfo,
    timezone_name: str,
    scan_interval_seconds: int,
    device_metadata: dict[str, str],
    analysis: dict[str, Any],
    cpm_per_usvh: float = 154.0,
    yellow_percent: float = 125.0,
    red_percent: float = 175.0,
    language: str = "en",
    data_mode: str = "raw",
    scientific_page: bool = False,
) -> bytes:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backends.backend_pdf import PdfPages

    generated_at = datetime.now(UTC)
    display_end_local = _report_display_end(period, generated_at)
    report_id = f"RM-{generated_at.strftime('%Y%m%d-%H%M%S')}"
    page_count = 6 if scientific_page else 5
    output = io.BytesIO()
    model = normalize_device_version_display(
        device_metadata.get("device_model", _report_phrase(language, "Unbekanntes GMC", "Unknown GMC"))
    )
    serial = device_metadata.get("serial", _report_phrase(language, "unbekannt", "unknown"))
    subtitle = _report_phrase(
        language,
        f"Beta-/Gamma-Strahlungsbericht · {period.label} · {model} · Seriennummer {serial}",
        f"Beta/gamma radiation report · {period.label} · {model} · serial {serial}",
    )
    assessment, explanation, recommendation, _assessment_code = _report_assessment(
        analysis, language=language
    )
    values = [float(row.cpm) for row in rows]
    raw_values = [float(row.raw_cpm if row.raw_cpm is not None else row.cpm) for row in rows]
    corrected_values = [float(row.corrected_cpm if row.corrected_cpm is not None else row.cpm) for row in rows]
    local_times = [datetime.fromtimestamp(row.timestamp_utc, UTC).astimezone(tz) for row in rows]
    metrology_summary = _report_metrology_summary(rows, device_metadata)
    last_cpm = values[-1] if values else None
    quality = analysis.get("data_quality") or {}
    baseline = analysis.get("baseline_mean_cpm")
    rolling_window = max(1, round(3600 / max(1, scan_interval_seconds)))
    rolling_values = _rolling_mean(values, rolling_window)

    with PdfPages(
        output,
        metadata={
            "Title": _report_phrase(
                language,
                f"Radiation Monitoring Beta-/Gamma-Bericht {period.label}",
                f"Radiation Monitoring beta/gamma report {period.label}",
            ),
            "Author": "Radiation Monitoring Home Assistant App",
            "Subject": _report_phrase(
                language,
                "Professionelle Auswertung kombinierter Beta-/Gamma-Zählraten",
                "Professional evaluation of combined beta/gamma count rates",
            ),
            "Keywords": "radiation,beta,gamma,CPM,Geiger-Mueller,Home Assistant",
        },
    ) as pdf:
        # Page 1: executive summary.
        fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        _draw_report_header(
            fig,
            title="Radiation Monitoring",
            subtitle=subtitle,
            report_id=report_id,
            page_number=1,
            page_count=page_count,
            generated_at=generated_at,
            language=language,
        )
        kpi_width = 0.205
        kpi_positions = [0.065, 0.285, 0.505, 0.725]
        _draw_kpi(
            fig,
            x=kpi_positions[0],
            width=kpi_width,
            title=_report_phrase(language, "Letzter Wert im Zeitraum", "Last value in period"),
            value="—" if last_cpm is None else f"{last_cpm:.1f} CPM",
            detail="—" if last_cpm is None else f"{last_cpm / cpm_per_usvh:.3f} µSv/h*",
        )
        _draw_kpi(
            fig,
            x=kpi_positions[1],
            width=kpi_width,
            title=_report_phrase(language, "Zeitraummittel", "Period mean"),
            value=f"{float(analysis.get('cpm_mean')):.1f} CPM" if analysis.get("cpm_mean") is not None else "—",
            detail=(
                f"{float(analysis.get('cpm_mean')) / cpm_per_usvh:.3f} µSv/h*"
                if analysis.get("cpm_mean") is not None
                else "—"
            ),
        )
        _draw_kpi(
            fig,
            x=kpi_positions[2],
            width=kpi_width,
            title=_report_phrase(language, "Maximum", "Maximum"),
            value=f"{float(analysis.get('cpm_max')):.1f} CPM" if analysis.get("cpm_max") is not None else "—",
            detail=(
                f"{float(analysis.get('cpm_max')) / cpm_per_usvh:.3f} µSv/h*"
                if analysis.get("cpm_max") is not None
                else "—"
            ),
        )
        _draw_kpi(
            fig,
            x=kpi_positions[3],
            width=kpi_width,
            title=_report_phrase(language, "Zeitraumbewertung", "Period assessment"),
            value=assessment,
            detail="",
            value_font_size=8.8,
            wrap_value=True,
        )
        chart_axis = fig.add_axes(_PAGE1_CHART_RECT)
        if values:
            chart_axis.plot(local_times, values, linewidth=0.8, alpha=0.55, label=_report_phrase(language, "Rohwert" if data_mode == "comparison" else "Messwert", "Raw value" if data_mode == "comparison" else "Measurement"))
            if data_mode == "comparison":
                chart_axis.plot(local_times, corrected_values, linewidth=1.0, alpha=0.75, label=_report_phrase(language, "Totzeitkorrigiert", "Dead-time corrected"))
            chart_axis.plot(local_times, rolling_values, linewidth=1.8, label=_report_phrase(language, "Gleitendes 1-h-Mittel", "Rolling 1 h mean"))
            if baseline is not None:
                chart_axis.axhline(float(baseline), linewidth=1.0, linestyle="--", label=_report_phrase(language, "Lokale Basislinie", "Local baseline"))
                chart_axis.axhline(float(baseline) * yellow_percent / 100.0, linewidth=0.9, linestyle=":", label=_report_phrase(language, "Relative Warnschwelle", "Relative warning threshold"))
                chart_axis.axhline(float(baseline) * red_percent / 100.0, linewidth=0.9, linestyle=":", label=_report_phrase(language, "Relative Alarmgrenze", "Relative alarm threshold"))
            chart_axis.set_xlim(period.start_local, display_end_local)
            _format_report_time_axis(chart_axis, tz)
            chart_axis.legend(loc="upper left", fontsize=6.8, ncol=2, frameon=False)
        else:
            chart_axis.text(0.5, 0.5, _report_phrase(language, "Keine akzeptierten Messwerte im Zeitraum", "No accepted measurements in period"), ha="center", va="center", transform=chart_axis.transAxes)
        chart_axis.set_title(_report_phrase(language, "Verlauf der kombinierten Beta-/Gamma-Zählrate", "Combined beta/gamma count-rate trend"), fontsize=10.5, fontweight="bold", pad=8)
        chart_axis.set_ylabel(_report_phrase(language, "Zählrate [CPM]", "Count rate [CPM]"), fontsize=8.5)
        chart_axis.set_xlabel(
            _report_phrase(language, f"Lokale Zeit [{timezone_name}]", f"Local date and time [{timezone_name}]"),
            fontsize=8.5,
            labelpad=4,
        )
        chart_axis.text(
            1.0,
            1.015,
            _report_phrase(
                language,
                f"Datenstand {display_end_local.strftime('%d.%m.%Y %H:%M')}",
                f"Data through {display_end_local.strftime('%Y-%m-%d %H:%M')}",
            ),
            transform=chart_axis.transAxes,
            ha="right",
            va="bottom",
            fontsize=6.8,
            color="#64748b",
        )
        _configure_report_axis(chart_axis)

        calibration_labels = {
            "documented": _report_phrase(language, "Werkswert", "Factory value"),
            "predefined": _report_phrase(language, "Werkswert", "Factory value"),
            "customized": _report_phrase(language, "Benutzerprofil", "User profile"),
            "working_values": _report_phrase(language, "Arbeitswert", "Working value"),
            "incomplete": _report_phrase(language, "nicht kalibriert", "not calibrated"),
            "unknown": _report_phrase(language, "unbekannt", "unknown"),
        }
        validity_labels = {
            "fully_valid": _report_phrase(language, "vollständig gültig", "fully valid"),
            "qualified": _report_phrase(language, "mit Einschränkungen gültig", "qualified"),
            "limited": _report_phrase(language, "nur eingeschränkt verwendbar", "limited"),
        }
        fig.text(
            0.065,
            _PAGE1_METROLOGY_Y,
            _report_phrase(language, "Messqualität", "Measurement quality") + ": "
            + str(metrology_summary["stars"]) + " · "
            + _report_phrase(language, "Totzeit", "Dead time") + " "
            + (_format_number(metrology_summary.get("load_mean"), 2) + "%" if metrology_summary.get("load_mean") is not None else "—")
            + " · " + _report_phrase(language, "Kalibrierung", "Calibration") + ": "
            + calibration_labels.get(str(metrology_summary.get("calibration_status")), str(metrology_summary.get("calibration_status")))
            + " · " + validity_labels.get(str(metrology_summary.get("validity")), str(metrology_summary.get("validity"))),
            fontsize=7.4,
            color="#334155",
            fontweight="bold",
        )
        recommendation_text = _report_phrase(language, "Empfehlung: ", "Recommendation: ") + recommendation
        _draw_assessment_panel(
            fig,
            title=_report_phrase(language, "Bewertung des Berichtszeitraums", "Assessment of the reporting period"),
            explanation=explanation,
            recommendation=recommendation_text,
        )
        fig.text(0.065, _PAGE1_STATS_HEADING_Y, _report_phrase(language, "Messwertstatistik des Berichtszeitraums", "Measurement statistics for the reporting period"), fontsize=12.5, fontweight="bold")
        stats_rows = [
            [_report_phrase(language, "Messwerte", "Measurements"), f"{int(analysis.get('samples') or 0):,}", _report_phrase(language, "Datenabdeckung", "Data coverage"), f"{float(analysis.get('completeness_percent') or 0.0):.1f}%"],
            [_report_phrase(language, "Minimum", "Minimum"), _format_number(analysis.get("cpm_min")) + " CPM", _report_phrase(language, "Maximum", "Maximum"), _format_number(analysis.get("cpm_max")) + " CPM"],
            [_report_phrase(language, "Median", "Median"), _format_number(analysis.get("cpm_median")) + " CPM", _report_phrase(language, "Mittelwert", "Mean"), _format_number(analysis.get("cpm_mean")) + " CPM"],
            ["P95", _format_number(analysis.get("cpm_95th_percentile")) + " CPM", _report_phrase(language, "Standardabweichung", "Standard deviation"), _format_number(analysis.get("cpm_standard_deviation")) + " CPM"],
            [_report_phrase(language, "Lokale Basislinie", "Local baseline"), _format_number(baseline) + " CPM", _report_phrase(language, "Abweichung", "Deviation"), _format_signed(analysis.get("baseline_deviation_percent")) + "%"],
            [_report_phrase(language, "Datenqualität", "Data quality"), _report_state_label(language, quality.get("label") or "—"), _report_phrase(language, "Anomalieereignisse", "Anomaly events"), str(int(analysis.get("event_count") or 0))],
        ]
        stats_axis = fig.add_axes([0.065, 0.075, 0.87, 0.215])
        _draw_table(stats_axis, stats_rows, font_size=7.8, column_widths=[0.22, 0.23, 0.27, 0.28])
        fig.text(0.065, 0.052, _report_phrase(language, "* Aus CPM und dem konfigurierten Umrechnungsfaktor abgeleitete Dosisleistung; keine unabhängige Dosimetrie.", "* Dose rate derived from CPM and the configured conversion factor; not independent dosimetry."), fontsize=6.8, color="#64748b")
        pdf.savefig(fig)
        plt.close(fig)

        # Page 2: time series and distribution.
        fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        _draw_report_header(fig, title=_report_phrase(language, "Zeitreihe und Verteilung", "Time series and distribution"), subtitle=_report_phrase(language, "Alle Diagramme verwenden ausschließlich akzeptierte Messwerte des ausgewählten Berichtszeitraums.", "All charts use only accepted measurements from the selected reporting period."), report_id=report_id, page_number=2, page_count=page_count, generated_at=generated_at, language=language)
        time_axis = fig.add_axes([0.09, 0.64, 0.84, 0.22])
        if values:
            time_axis.plot(local_times, values, linewidth=0.75, alpha=0.55, label=_report_phrase(language, "Messwert", "Measurement"))
            time_axis.plot(local_times, rolling_values, linewidth=1.65, label=_report_phrase(language, "Gleitendes 1-h-Mittel", "Rolling 1 h mean"))
            time_axis.set_xlim(period.start_local, display_end_local)
            _format_report_time_axis(time_axis, tz)
            time_axis.legend(loc="upper left", fontsize=7, frameon=False)
        time_axis.set_title(_report_phrase(language, "Zählratenverlauf", "Count-rate trend"), fontsize=10.5, fontweight="bold")
        time_axis.set_ylabel(_report_phrase(language, "Zählrate [CPM]", "Count rate [CPM]"), fontsize=8.5)
        time_axis.set_xlabel(_report_phrase(language, f"Lokale Zeit [{timezone_name}]", f"Local date and time [{timezone_name}]"), fontsize=8.5)
        _configure_report_axis(time_axis)

        hist_axis = fig.add_axes([0.09, 0.365, 0.84, 0.205])
        if values:
            bin_count = min(30, max(5, round(math.sqrt(len(values)))))
            _counts, edges, _patches = hist_axis.hist(values, bins=bin_count, alpha=0.68, label=_report_phrase(language, "Beobachtete Verteilung", "Observed distribution"))
            mean = statistics.fmean(values)
            if mean > 0 and len(set(values)) > 1:
                centers = (edges[:-1] + edges[1:]) / 2.0
                widths = np.diff(edges)
                poisson = np.exp(-mean + centers * np.log(mean) - np.vectorize(math.lgamma)(centers + 1.0))
                expected = poisson * len(values) * widths
                hist_axis.plot(centers, expected, linewidth=1.35, marker="o", markersize=2.5, label=_report_phrase(language, "Poisson-Referenz", "Poisson reference"))
            hist_axis.legend(loc="upper right", fontsize=7, frameon=False)
        hist_axis.set_title(_report_phrase(language, "Messwertverteilung und Poisson-Referenz", "Measurement distribution and Poisson reference"), fontsize=10.5, fontweight="bold")
        hist_axis.set_xlabel(_report_phrase(language, "Zählrate [CPM]", "Count rate [CPM]"), fontsize=8.5)
        hist_axis.set_ylabel(_report_phrase(language, "Akzeptierte Messwerte [Anzahl]", "Accepted samples [count]"), fontsize=8.5)
        _configure_report_axis(hist_axis)

        daily_axis = fig.add_axes([0.09, 0.085, 0.84, 0.205])
        daily = _daily_report_statistics(rows, tz=tz)
        if daily:
            days = [item[0] for item in daily]
            minima = [item[1] for item in daily]
            medians = [item[2] for item in daily]
            maxima = [item[3] for item in daily]
            if len(days) == 1:
                center = datetime.combine(days[0], dt_time(hour=12), tzinfo=tz)
                plotted_days = [center]
                daily_axis.set_xlim(center - timedelta(hours=12), center + timedelta(hours=12))
                daily_axis.set_xticks([center])
                daily_axis.set_xticklabels([days[0].strftime("%d.%m.%Y")])
            else:
                plotted_days = [datetime.combine(day, dt_time(hour=12), tzinfo=tz) for day in days]
                _format_report_time_axis(daily_axis, tz)
            daily_axis.vlines(plotted_days, minima, maxima, linewidth=1.2, alpha=0.7, label=_report_phrase(language, "Minimum bis Maximum", "Minimum to maximum"))
            daily_axis.scatter(plotted_days, medians, s=13, zorder=3, label=_report_phrase(language, "Median", "Median"))
            daily_axis.legend(loc="upper left", fontsize=7, frameon=False)
        daily_axis.set_title(_report_phrase(language, "Tagesvergleich: Minimum, Median und Maximum", "Daily comparison: minimum, median and maximum"), fontsize=10.5, fontweight="bold")
        daily_axis.set_xlabel(_report_phrase(language, f"Lokales Datum [{timezone_name}]", f"Local date [{timezone_name}]"), fontsize=8.5)
        daily_axis.set_ylabel(_report_phrase(language, "Zählrate [CPM]", "Count rate [CPM]"), fontsize=8.5)
        _configure_report_axis(daily_axis)
        pdf.savefig(fig)
        plt.close(fig)

        # Page 3: temporal patterns and heat maps.
        fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        _draw_report_header(fig, title=_report_phrase(language, "Zeitmuster und Heatmaps", "Temporal patterns and heat maps"), subtitle=_report_phrase(language, "Farben zeigen mittlere akzeptierte CPM-Werte; graue Felder enthalten keine ausreichenden Daten.", "Colors show mean accepted CPM values; gray cells contain insufficient data."), report_id=report_id, page_number=3, page_count=page_count, generated_at=generated_at, language=language)
        weekday_labels = [_report_phrase(language, value[0], value[1]) for value in [("Mo", "Mon"), ("Di", "Tue"), ("Mi", "Wed"), ("Do", "Thu"), ("Fr", "Fri"), ("Sa", "Sat"), ("So", "Sun")]]
        weekly_axis = fig.add_axes([0.10, 0.59, 0.75, 0.25])
        weekly_matrix = np.ma.masked_invalid(np.array(_report_weekday_hour_matrix(rows, tz), dtype=float))
        cmap = plt.get_cmap("viridis").copy()
        cmap.set_bad("#e5e7eb")
        weekly_image = weekly_axis.imshow(weekly_matrix, aspect="auto", interpolation="nearest", cmap=cmap)
        weekly_axis.set_title(_report_phrase(language, "Typischer Mittelwert nach Wochentag und Stunde", "Typical mean by weekday and hour"), fontsize=10.5, fontweight="bold")
        weekly_axis.set_xlabel(_report_phrase(language, "Lokale Stunde [h]", "Local hour [h]"), fontsize=8.5)
        weekly_axis.set_ylabel(_report_phrase(language, "Wochentag", "Weekday"), fontsize=8.5)
        weekly_axis.set_xticks(range(0, 24, 3), labels=[f"{hour:02d}" for hour in range(0, 24, 3)])
        weekly_axis.set_yticks(range(7), labels=weekday_labels)
        weekly_axis.tick_params(labelsize=7.5)
        weekly_cbar_axis = fig.add_axes([0.87, 0.59, 0.025, 0.25])
        weekly_cbar = fig.colorbar(weekly_image, cax=weekly_cbar_axis)
        weekly_cbar.set_label(_report_phrase(language, "Mittlere Zählrate [CPM]", "Mean count rate [CPM]"), fontsize=8)
        weekly_cbar.ax.tick_params(labelsize=7)

        calendar_axis = fig.add_axes([0.10, 0.27, 0.75, 0.22])
        calendar_matrix, weeks = _report_calendar_matrix(rows, tz)
        calendar_image = calendar_axis.imshow(np.ma.masked_invalid(np.array(calendar_matrix, dtype=float)), aspect="auto", interpolation="nearest", cmap=cmap)
        calendar_axis.set_title(_report_phrase(language, "Kalender-Heatmap der Tagesmittelwerte", "Calendar heat map of daily means"), fontsize=10.5, fontweight="bold")
        calendar_axis.set_xlabel(_report_phrase(language, "ISO-Woche", "ISO week"), fontsize=8.5)
        calendar_axis.set_ylabel(_report_phrase(language, "Wochentag", "Weekday"), fontsize=8.5)
        calendar_axis.set_yticks(range(7), labels=weekday_labels)
        if weeks:
            tick_step = max(1, math.ceil(len(weeks) / 8))
            tick_indices = list(range(0, len(weeks), tick_step))
            week_years = sorted({week.isocalendar().year for week in weeks})
            calendar_axis.set_xticks(
                tick_indices,
                labels=[f"W{weeks[index].isocalendar().week:02d}" for index in tick_indices],
            )
            year_suffix = "/".join(str(year) for year in week_years)
            calendar_axis.set_xlabel(
                _report_phrase(language, f"ISO-Woche [{year_suffix}]", f"ISO week [{year_suffix}]"),
                fontsize=8.5,
            )
        calendar_axis.tick_params(labelsize=7.2)
        calendar_cbar_axis = fig.add_axes([0.87, 0.27, 0.025, 0.22])
        calendar_cbar = fig.colorbar(calendar_image, cax=calendar_cbar_axis)
        calendar_cbar.set_label(_report_phrase(language, "Tagesmittel [CPM]", "Daily mean [CPM]"), fontsize=8)
        calendar_cbar.ax.tick_params(labelsize=7)

        weekday_values: list[float] = []
        weekend_values: list[float] = []
        day_values: list[float] = []
        night_values: list[float] = []
        for row in rows:
            local = datetime.fromtimestamp(row.timestamp_utc, UTC).astimezone(tz)
            (weekday_values if local.weekday() < 5 else weekend_values).append(float(row.cpm))
            (day_values if 6 <= local.hour < 22 else night_values).append(float(row.cpm))
        pattern_rows = [
            [_report_phrase(language, "Werktagsmittel", "Weekday mean"), _format_number(statistics.fmean(weekday_values) if weekday_values else None) + " CPM", _report_phrase(language, "Wochenendmittel", "Weekend mean"), _format_number(statistics.fmean(weekend_values) if weekend_values else None) + " CPM"],
            [_report_phrase(language, "Tagesmittel (06-22 Uhr)", "Daytime mean (06-22)"), _format_number(statistics.fmean(day_values) if day_values else None) + " CPM", _report_phrase(language, "Nachtmittel (22-06 Uhr)", "Night mean (22-06)"), _format_number(statistics.fmean(night_values) if night_values else None) + " CPM"],
        ]
        pattern_axis = fig.add_axes([0.09, 0.105, 0.84, 0.09])
        _draw_table(pattern_axis, pattern_rows, font_size=7.8, column_widths=[0.25, 0.22, 0.28, 0.25])
        fig.text(0.09, 0.075, _report_phrase(language, "Zeitmuster beschreiben statistische Verteilungen und identifizieren keine Strahlungsquelle.", "Temporal patterns describe statistical distributions and do not identify a radiation source."), fontsize=7.2, color="#64748b")
        pdf.savefig(fig)
        plt.close(fig)

        # Page 4: statistical analysis and events.
        fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        _draw_report_header(fig, title=_report_phrase(language, "Statistische Analyse und Ereignisse", "Statistical analysis and events"), subtitle=_report_phrase(language, "Bewertung von Zählstatistik, Basislinie und Änderungen; keine Bestimmung von Nuklid oder Strahlungsart.", "Assessment of counting statistics, baseline and changes; no identification of radionuclide or radiation type."), report_id=report_id, page_number=4, page_count=page_count, generated_at=generated_at, language=language)
        change = analysis.get("change_significance") or {}
        shift = analysis.get("level_shift") or {}
        rarity = change.get("historical_rarity_one_in")
        change_available = bool(change.get("available"))
        shift_available = bool(shift.get("available"))
        significance_value = (
            _format_signed(change.get("significance_sigma"), 2) + " σ"
            if change_available
            else "—"
        )
        significance_context = _report_state_label(
            language,
            change.get("state") or _report_phrase(language, "Nicht verfügbar", "Unavailable"),
        )
        if change_available and change.get("confidence"):
            significance_context += " · " + _report_phrase(language, "Vertrauen", "confidence") + ": " + _report_state_label(language, change.get("confidence"))
        p_value = _format_number(change.get("p_value_two_sided"), 6) if change_available else "—"
        noise_probability = (
            f"{float(change.get('probability_not_counting_noise_percent') or 0.0):.3f}% "
            + _report_phrase(language, "nicht durch reine Zählstreuung", "not explained by counting variation alone")
            if change_available
            else "—"
        )
        percentile = change.get("empirical_percentile")
        percentile_value = (
            f"{float(percentile):.1f} " + _report_phrase(language, "Perzentil", "percentile")
            if percentile is not None
            else "—"
        )
        rarity_value = (
            (
                f"≈ einmal in {float(rarity):.0f} historischen Stunden"
                if language == "de"
                else f"≈ once in {float(rarity):.0f} historical hours"
            )
            if rarity is not None
            else "—"
        )
        statistics_rows = [
            [_report_phrase(language, "Datenqualität", "Data quality"), _report_state_label(language, quality.get("label") or "—"), f"{float(quality.get('score') or 0.0):.1f}/100"],
            [_report_phrase(language, "Fano-Faktor", "Fano factor"), _format_number(analysis.get("fano_factor"), 3), _report_phrase(language, "1,0 entspricht idealisierter Poisson-Streuung", "1.0 represents idealized Poisson dispersion")],
            [_report_phrase(language, "Poisson-SD-Verhältnis", "Poisson SD ratio"), _format_number(analysis.get("poisson_sd_ratio"), 3), _report_phrase(language, "Beobachtete SD geteilt durch √Mittelwert", "Observed SD divided by √mean")],
            [_report_phrase(language, "Basislinienabweichung", "Baseline deviation"), _format_signed(analysis.get("baseline_deviation_percent")) + "%", _format_signed(analysis.get("baseline_deviation_cpm")) + " CPM"],
            [_report_phrase(language, "Basisliniendrift", "Baseline drift"), _format_signed((analysis.get("baseline_drift") or {}).get("percent")) + "%", _report_state_label(language, (analysis.get("baseline_drift") or {}).get("state") or "—")],
            [_report_phrase(language, "Änderungssignifikanz", "Change significance"), significance_value, significance_context],
            [_report_phrase(language, "Zweiseitiger p-Wert", "Two-sided p-value"), p_value, noise_probability],
            [_report_phrase(language, "Historische Einordnung", "Historical context"), percentile_value, rarity_value],
            [_report_phrase(language, "Persistenter Niveauwechsel", "Persistent level shift"), _report_state_label(language, shift.get("state") or _report_phrase(language, "Nicht verfügbar", "Unavailable")), (_format_signed(shift.get("change_percent"), 1) + "%" if shift_available else "—")],
        ]
        fig.text(0.065, 0.875, _report_phrase(language, "Statistische Kennzahlen", "Statistical metrics"), fontsize=12.5, fontweight="bold")
        statistics_axis = fig.add_axes([0.065, 0.49, 0.87, 0.36])
        _draw_table(statistics_axis, statistics_rows, columns=[_report_phrase(language, "Kennzahl", "Metric"), _report_phrase(language, "Wert", "Value"), _report_phrase(language, "Einordnung", "Interpretation")], font_size=7.25, column_widths=[0.28, 0.25, 0.47])

        fig.text(0.065, 0.45, _report_phrase(language, "Anomalieereignisse im Berichtszeitraum", "Anomaly events in the reporting period"), fontsize=12.5, fontweight="bold")
        event_rows: list[list[str]] = []
        for event in list(analysis.get("events") or [])[:10]:
            start_local = datetime.fromtimestamp(int(event["start_timestamp_utc"]), UTC).astimezone(tz)
            end_local = datetime.fromtimestamp(int(event["end_timestamp_utc"]), UTC).astimezone(tz)
            event_rows.append([
                start_local.strftime("%Y-%m-%d %H:%M"),
                end_local.strftime("%Y-%m-%d %H:%M"),
                _report_phrase(language, {"yellow": "gelb", "red": "rot", "green": "grün"}.get(str(event.get("severity") or ""), str(event.get("severity") or "—")), str(event.get("severity") or "—")),
                f"{float(event.get('mean_cpm') or 0.0):.1f}",
                f"{float(event.get('max_cpm') or 0.0):.1f}",
                f"{float(event.get('max_background_index_percent') or 0.0):.1f}%",
            ])
        events_axis = fig.add_axes([0.065, 0.245, 0.87, 0.18])
        if event_rows:
            _draw_table(events_axis, event_rows, columns=[_report_phrase(language, "Beginn lokal", "Start local"), _report_phrase(language, "Ende lokal", "End local"), _report_phrase(language, "Stufe", "Level"), _report_phrase(language, "Mittel CPM", "Mean CPM"), _report_phrase(language, "Max CPM", "Max CPM"), _report_phrase(language, "Hintergrundindex", "Background index")], font_size=6.8, column_widths=[0.19, 0.19, 0.10, 0.14, 0.13, 0.25])
        else:
            events_axis.axis("off")
            events_axis.text(0.0, 0.82, _report_phrase(language, "Keine anhaltenden relativen Anomalieereignisse erkannt.", "No sustained relative-anomaly events were detected."), fontsize=8.5, va="top")

        fig.text(0.065, 0.205, _report_phrase(language, "Einflussfaktoren und Hinweise", "Influencing factors and notes"), fontsize=12.5, fontweight="bold")
        temp_corr = analysis.get("temperature_correlation")
        volt_corr = analysis.get("voltage_correlation")
        note_lines = [
            _report_phrase(language, "Temperaturkorrelation: ", "Temperature correlation: ") + (_format_number(temp_corr, 3) if temp_corr is not None else _report_state_label(language, analysis.get("temperature_correlation_status") or "—")),
            _report_phrase(language, "Spannungskorrelation: ", "Voltage correlation: ") + (_format_number(volt_corr, 3) if volt_corr is not None else _report_state_label(language, analysis.get("voltage_correlation_status") or "—")),
            _report_phrase(language, "Korrelationen zeigen statistische Zusammenhänge und beweisen keine Ursache-Wirkungs-Beziehung.", "Correlations show statistical associations and do not prove causation."),
            _report_phrase(language, "Ein Geiger-Müller-Zählrohr liefert typischerweise eine kombinierte Beta-/Gamma-Antwort; die Anteile werden nicht getrennt gemessen.", "A Geiger-Mueller tube typically provides a combined beta/gamma response; the components are not measured separately."),
        ]
        fig.text(0.075, 0.174, "\n".join("• " + textwrap.fill(line, width=110, subsequent_indent="  ") for line in note_lines), fontsize=7.8, va="top", linespacing=1.45)
        pdf.savefig(fig)
        plt.close(fig)

        # Page 5: traceability and selected measurements.
        fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
        _draw_report_header(fig, title=_report_phrase(language, "Messort, Gerät und Nachvollziehbarkeit", "Location, device and traceability"), subtitle=_report_phrase(language, "Technische Angaben und ausgewählte Messwerte zur Reproduzierbarkeit des Berichts.", "Technical details and selected measurements for report reproducibility."), report_id=report_id, page_number=5, page_count=page_count, generated_at=generated_at, language=language)
        device_rows = [
            [_report_phrase(language, "Gerätemodell", "Device model"), model, _report_phrase(language, "Seriennummer", "Serial number"), serial],
            [_report_phrase(language, "Hardware", "Hardware"), str(device_metadata.get("hardware_model") or "—"), _report_phrase(language, "Firmware", "Firmware"), str(device_metadata.get("firmware_version") or "—")],
            [_report_phrase(language, "Berichtsstart", "Report start"), period.start_local.isoformat(timespec="seconds"), _report_phrase(language, "Berichtsende", "Report end"), period.end_local.isoformat(timespec="seconds")],
            [_report_phrase(language, "Zeitzone", "Time zone"), timezone_name, _report_phrase(language, "Messintervall", "Sampling interval"), f"{scan_interval_seconds} s"],
            [_report_phrase(language, "Umrechnungsfaktor", "Conversion factor"), f"{cpm_per_usvh:g} CPM/(µSv/h)", _report_phrase(language, "Datenquelle", "Data source"), str(device_metadata.get("data_source") or "USB / local history")],
            [_report_phrase(language, "App-Version", "App version"), APP_VERSION, _report_phrase(language, "Bericht-ID", "Report ID"), report_id],
            [_report_phrase(language, "Datenmodus", "Data mode"), {"raw": _report_phrase(language, "Rohdaten", "Raw data"), "corrected": _report_phrase(language, "Totzeitkorrigiert", "Dead-time corrected"), "comparison": _report_phrase(language, "Roh-/Korrekturvergleich", "Raw/corrected comparison")}.get(data_mode, data_mode), _report_phrase(language, "Messqualität", "Measurement quality"), str(metrology_summary["stars"]) + f" ({int(metrology_summary['quality_index'])}/100)"],
        ]
        device_axis = fig.add_axes([0.065, 0.67, 0.87, 0.19])
        _draw_table(device_axis, device_rows, font_size=7.25, column_widths=[0.18, 0.31, 0.18, 0.33])
        fig.text(0.065, 0.885, _report_phrase(language, "Technische Metadaten", "Technical metadata"), fontsize=12.5, fontweight="bold")

        fig.text(0.065, 0.625, _report_phrase(language, "Ausgewählte Messwerte aus dem Berichtszeitraum", "Selected measurements from the reporting period"), fontsize=12.5, fontweight="bold")
        selected_rows = rows[-18:]
        tube_present = any(row.tube_low_cpm is not None or row.tube_high_cpm is not None for row in selected_rows)
        measurement_rows: list[list[str]] = []
        for row in selected_rows:
            local = datetime.fromtimestamp(row.timestamp_utc, UTC).astimezone(tz)
            item = [local.strftime("%Y-%m-%d %H:%M:%S"), str(int(row.cpm)), f"{float(row.cpm) / cpm_per_usvh:.4f}", str(row.cpm_quality or "—")]
            if tube_present:
                item.extend(["—" if row.tube_low_cpm is None else str(row.tube_low_cpm), "—" if row.tube_high_cpm is None else str(row.tube_high_cpm)])
            measurement_rows.append(item)
        columns = [_report_phrase(language, "Lokale Zeit", "Local time"), "CPM", _report_phrase(language, "abgeleitet µSv/h", "derived µSv/h"), _report_phrase(language, "Qualität", "Quality")]
        widths = [0.31, 0.12, 0.19, 0.18]
        if tube_present:
            columns.extend([_report_phrase(language, "Niedrigdosis-Rohr CPM", "Low-dose tube CPM"), _report_phrase(language, "Hochdosis-Rohr CPM", "High-dose tube CPM")])
            widths = [0.24, 0.08, 0.14, 0.13, 0.20, 0.21]
        measurement_axis = fig.add_axes([0.065, 0.17, 0.87, 0.43])
        if measurement_rows:
            _draw_table(measurement_axis, measurement_rows, columns=columns, font_size=6.65, column_widths=widths)
        else:
            measurement_axis.axis("off")
            measurement_axis.text(0, 0.95, _report_phrase(language, "Keine akzeptierten Messwerte verfügbar.", "No accepted measurements available."), fontsize=8.5, va="top")
        fig.text(0.065, 0.125, _report_phrase(language, "Methodischer Hinweis", "Method note"), fontsize=10.5, fontweight="bold")
        method_note = _report_phrase(
            language,
            "CPM ist die primäre Messgröße. Die angezeigte Dosisleistung wird ausschließlich aus CPM und dem konfigurierten gerätespezifischen Faktor berechnet. Ohne energiekalibrierte Dosimetrie oder Spektrometrie können Beta- und Gammaanteile, Nuklide und eine amtliche Dosis nicht bestimmt werden.",
            "CPM is the primary measurement. The displayed dose rate is calculated solely from CPM and the configured device-specific factor. Without energy-calibrated dosimetry or spectrometry, beta and gamma components, radionuclides and an official dose cannot be determined.",
        )
        fig.text(0.065, 0.095, textwrap.fill(method_note, width=120), fontsize=7.5, va="top")
        pdf.savefig(fig)
        plt.close(fig)

        if scientific_page:
            fig = plt.figure(figsize=(8.27, 11.69), facecolor="white")
            _draw_report_header(
                fig,
                title=_report_phrase(language, "Wissenschaftliche Detektor- und Korrekturdokumentation", "Scientific detector and correction documentation"),
                subtitle=_report_phrase(language, "Transparente Darstellung von Rohwert, Totzeitmodell, Korrektur und Kalibrierstatus.", "Transparent presentation of raw count rate, dead-time model, correction and calibration status."),
                report_id=report_id,
                page_number=6,
                page_count=page_count,
                generated_at=generated_at,
                language=language,
            )
            science_rows = [
                [_report_phrase(language, "Detektor", "Detector"), str(metrology_summary.get("detector_type") or "—")],
                [_report_phrase(language, "Aktives Zählrohr", "Active tube"), str(metrology_summary.get("active_tube") or "—")],
                [_report_phrase(language, "Totzeitmodell", "Dead-time model"), str(metrology_summary.get("dead_time_model") or "none")],
                [_report_phrase(language, "Totzeit", "Dead time"), _format_number(metrology_summary.get("dead_time_us"), 2) + " µs"],
                [_report_phrase(language, "Mittlere Detektorauslastung", "Mean detector load"), _format_number(metrology_summary.get("load_mean"), 3) + "%"],
                [_report_phrase(language, "Maximale Detektorauslastung", "Maximum detector load"), _format_number(metrology_summary.get("load_max"), 3) + "%"],
                [_report_phrase(language, "Mittlere Totzeitverluste", "Mean dead-time losses"), _format_number(metrology_summary.get("loss_mean"), 3) + "%"],
                [_report_phrase(language, "Mittlerer Korrekturfaktor", "Mean correction factor"), _format_number(metrology_summary.get("correction_factor_mean"), 5)],
                [_report_phrase(language, "Kalibrierstatus", "Calibration status"), calibration_labels.get(str(metrology_summary.get("calibration_status")), str(metrology_summary.get("calibration_status")))],
                [_report_phrase(language, "Kalibrierquelle", "Calibration source"), str(metrology_summary.get("calibration_source") or "—")],
                [_report_phrase(language, "Messqualität", "Measurement quality"), str(metrology_summary["stars"]) + f" ({int(metrology_summary['quality_index'])}/100)"],
                [_report_phrase(language, "Datenmodus", "Data mode"), data_mode],
            ]
            fig.text(0.065, 0.875, _report_phrase(language, "Metrologische Parameter", "Metrological parameters"), fontsize=12.5, fontweight="bold")
            science_axis = fig.add_axes([0.065, 0.53, 0.87, 0.32])
            _draw_table(science_axis, science_rows, columns=[_report_phrase(language, "Parameter", "Parameter"), _report_phrase(language, "Wert", "Value")], font_size=7.8, column_widths=[0.43, 0.57])
            comparison_axis = fig.add_axes([0.09, 0.22, 0.84, 0.22])
            if rows:
                comparison_axis.plot(local_times, raw_values, linewidth=0.9, label=_report_phrase(language, "Roh-CPM", "Raw CPM"))
                comparison_axis.plot(local_times, corrected_values, linewidth=1.1, label=_report_phrase(language, "Korrigierte CPM", "Corrected CPM"))
                comparison_axis.legend(loc="upper left", fontsize=7, frameon=False)
                comparison_axis.set_xlim(period.start_local, display_end_local)
                _format_report_time_axis(comparison_axis, tz)
            else:
                comparison_axis.text(0.5, 0.5, _report_phrase(language, "Keine Messwerte", "No measurements"), ha="center", va="center", transform=comparison_axis.transAxes)
            comparison_axis.set_title(_report_phrase(language, "Rohdaten- und Totzeitkorrekturvergleich", "Raw-data and dead-time-correction comparison"), fontsize=10.5, fontweight="bold")
            comparison_axis.set_ylabel("CPM", fontsize=8.5)
            _configure_report_axis(comparison_axis)
            note = _report_phrase(
                language,
                "Die Totzeitkorrektur ist ein mathematisches Modell. Bei Sättigung oder unvollständiger Kalibrierung darf sie nicht als Ersatz für eine rückführbare Dosimetrie interpretiert werden.",
                "Dead-time correction is a mathematical model. During saturation or with incomplete calibration it must not be interpreted as a substitute for traceable dosimetry.",
            )
            fig.text(0.065, 0.145, textwrap.fill(note, width=118), fontsize=7.8, va="top")
            pdf.savefig(fig)
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
    data_mode: str = "raw",
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
                "cpm_per_usvh": device.get("cpm_per_usvh", cpm_per_usvh),
                "dead_time_us": device.get("dead_time_us"),
                "reliable_max_cpm": device.get("reliable_max_cpm"),
                "dead_time_model": device.get("dead_time_model", "none"),
                "conversion_factor_uncertainty_percent": device.get(
                    "conversion_factor_uncertainty_percent"
                ),
                "calibration_uncertainty_percent": device.get(
                    "calibration_uncertainty_percent"
                ),
                "calibration_reference": device.get("calibration_reference", ""),
                "tube_model": device.get("tube_model", ""),
                "dual_tube_mode": device.get("dual_tube_mode", "single"),
                "dual_tube_switch_cpm": device.get("dual_tube_switch_cpm"),
                "low_dose_tube_profile": device.get("low_dose_tube_profile"),
                "high_dose_tube_profile": device.get("high_dose_tube_profile"),
                "calibration_status": device.get("calibration_status", "working_values"),
            }
    rows = _report_rows_for_data_mode(rows, data_mode)
    baseline_rows = _report_rows_for_data_mode(baseline_rows, "corrected" if data_mode == "corrected" else "raw")
    metadata["data_mode"] = data_mode
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
        start_utc=int(period.start_utc.timestamp()),
        end_utc=int(period.end_utc.timestamp()),
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
    data_mode: str = "raw",
    scientific_page: bool = False,
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
        data_mode=data_mode,
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
                cpm_per_usvh=cpm_per_usvh,
                yellow_percent=traffic_light_yellow_percent,
                red_percent=traffic_light_red_percent,
                language=language,
                data_mode=data_mode,
                scientific_page=scientific_page,
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
                    cpm_per_usvh=cpm_per_usvh,
                    yellow_percent=traffic_light_yellow_percent,
                    red_percent=traffic_light_red_percent,
                    language=language,
                    data_mode=data_mode,
                    scientific_page=scientific_page,
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
    data_mode: str = "raw",
    scientific_page: bool = False,
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
            data_mode=data_mode,
            scientific_page=scientific_page,
        )
        return filename, content_type, temp_path.read_bytes()
    finally:
        temp_path.unlink(missing_ok=True)
