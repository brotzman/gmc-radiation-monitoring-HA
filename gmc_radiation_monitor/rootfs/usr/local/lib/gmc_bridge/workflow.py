from __future__ import annotations

import json
import math
import os
import statistics
import time
from collections.abc import Mapping
from dataclasses import asdict, dataclass, field
from datetime import UTC, date, datetime, timedelta
from datetime import time as dt_time
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

from .history import HistoryRow, HistoryStore
from .i18n import validate_catalogs
from .migrations import SCHEMA_VERSION

WORKFLOW_SETTINGS_KEY = "workflow_settings_v1"


@dataclass(frozen=True, slots=True)
class WorkflowSettings:
    notifications_enabled: bool = False
    notify_device_offline: bool = True
    notify_data_stale: bool = True
    notify_confirmed_event: bool = True
    notify_database_problem: bool = True
    offline_minutes: int = 15
    stale_minutes: int = 15
    cooldown_minutes: int = 180
    scheduled_reports_enabled: bool = False
    daily_report: bool = False
    weekly_report: bool = True
    monthly_summary: bool = True
    report_hour: int = 6
    managed_backup_retention: int = 7

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any] | None) -> WorkflowSettings:
        source = dict(value or {})

        def flag(name: str, default: bool) -> bool:
            raw = source.get(name, default)
            if isinstance(raw, bool):
                return raw
            return str(raw).strip().lower() in {"1", "true", "yes", "on"}

        def number(name: str, default: int, minimum: int, maximum: int) -> int:
            try:
                parsed = int(source.get(name, default))
            except (TypeError, ValueError):
                parsed = default
            return max(minimum, min(maximum, parsed))

        return cls(
            notifications_enabled=flag("notifications_enabled", False),
            notify_device_offline=flag("notify_device_offline", True),
            notify_data_stale=flag("notify_data_stale", True),
            notify_confirmed_event=flag("notify_confirmed_event", True),
            notify_database_problem=flag("notify_database_problem", True),
            offline_minutes=number("offline_minutes", 15, 2, 1440),
            stale_minutes=number("stale_minutes", 15, 2, 1440),
            cooldown_minutes=number("cooldown_minutes", 180, 15, 10080),
            scheduled_reports_enabled=flag("scheduled_reports_enabled", False),
            daily_report=flag("daily_report", False),
            weekly_report=flag("weekly_report", True),
            monthly_summary=flag("monthly_summary", True),
            report_hour=number("report_hour", 6, 0, 23),
            managed_backup_retention=number("managed_backup_retention", 7, 1, 50),
        )

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


def load_workflow_settings(store: HistoryStore) -> WorkflowSettings:
    raw = store.get_metadata().get(WORKFLOW_SETTINGS_KEY, "")
    try:
        value = json.loads(raw) if raw else {}
    except (TypeError, ValueError, json.JSONDecodeError):
        value = {}
    return WorkflowSettings.from_mapping(value if isinstance(value, dict) else {})


def save_workflow_settings(store: HistoryStore, settings: WorkflowSettings) -> None:
    store.set_metadata({WORKFLOW_SETTINGS_KEY: json.dumps(settings.as_dict(), sort_keys=True, separators=(",", ":"))})


@dataclass(frozen=True, slots=True)
class PeriodSummary:
    start_utc: int
    end_utc: int
    samples: int
    mean_cpm: float | None
    median_cpm: float | None
    min_cpm: int | None
    max_cpm: int | None
    standard_deviation: float | None
    coverage_percent: float

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True, slots=True)
class PeriodComparison:
    first: PeriodSummary
    second: PeriodSummary
    mean_difference_cpm: float | None
    mean_difference_percent: float | None
    median_difference_cpm: float | None
    z_indication: float | None
    interpretation: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "first": self.first.as_dict(),
            "second": self.second.as_dict(),
            "mean_difference_cpm": self.mean_difference_cpm,
            "mean_difference_percent": self.mean_difference_percent,
            "median_difference_cpm": self.median_difference_cpm,
            "z_indication": self.z_indication,
            "interpretation": self.interpretation,
        }


def summarize_period(rows: list[HistoryRow], *, start_utc: int, end_utc: int, scan_interval_seconds: int) -> PeriodSummary:
    values = [int(row.cpm) for row in rows]
    duration = max(1, int(end_utc) - int(start_utc))
    expected = max(1, round(duration / max(1, int(scan_interval_seconds))))
    return PeriodSummary(
        start_utc=int(start_utc),
        end_utc=int(end_utc),
        samples=len(values),
        mean_cpm=statistics.fmean(values) if values else None,
        median_cpm=statistics.median(values) if values else None,
        min_cpm=min(values) if values else None,
        max_cpm=max(values) if values else None,
        standard_deviation=statistics.stdev(values) if len(values) >= 2 else None,
        coverage_percent=min(100.0, 100.0 * len(values) / expected),
    )


def compare_periods(
    store: HistoryStore,
    *,
    device_serial: str,
    first_start_utc: int,
    first_end_utc: int,
    second_start_utc: int,
    second_end_utc: int,
    scan_interval_seconds: int,
) -> PeriodComparison:
    first_rows = store.query_range(first_start_utc, first_end_utc, device_serial=device_serial)
    second_rows = store.query_range(second_start_utc, second_end_utc, device_serial=device_serial)
    first = summarize_period(first_rows, start_utc=first_start_utc, end_utc=first_end_utc, scan_interval_seconds=scan_interval_seconds)
    second = summarize_period(second_rows, start_utc=second_start_utc, end_utc=second_end_utc, scan_interval_seconds=scan_interval_seconds)
    if first.mean_cpm is None or second.mean_cpm is None:
        return PeriodComparison(first, second, None, None, None, None, "insufficient_data")
    mean_diff = second.mean_cpm - first.mean_cpm
    percent = 100.0 * mean_diff / first.mean_cpm if first.mean_cpm else None
    median_diff = (
        second.median_cpm - first.median_cpm
        if first.median_cpm is not None and second.median_cpm is not None
        else None
    )
    variance_term = 0.0
    if first.standard_deviation is not None and first.samples:
        variance_term += (first.standard_deviation ** 2) / first.samples
    if second.standard_deviation is not None and second.samples:
        variance_term += (second.standard_deviation ** 2) / second.samples
    z = mean_diff / math.sqrt(variance_term) if variance_term > 0 else None
    if min(first.coverage_percent, second.coverage_percent) < 25 or min(first.samples, second.samples) < 5:
        interpretation = "low_coverage"
    elif z is None or abs(z) < 1.0:
        interpretation = "no_clear_difference"
    elif abs(z) < 2.0:
        interpretation = "possible_difference"
    else:
        interpretation = "clear_statistical_difference"
    return PeriodComparison(first, second, mean_diff, percent, median_diff, z, interpretation)


def local_date_range(value: str, timezone: ZoneInfo) -> tuple[int, int]:
    selected = date.fromisoformat(value)
    start = datetime.combine(selected, dt_time.min, tzinfo=timezone)
    end = start + timedelta(days=1)
    return int(start.astimezone(UTC).timestamp()), int(end.astimezone(UTC).timestamp())


def local_range(start_value: str, end_value: str, timezone: ZoneInfo) -> tuple[int, int]:
    start_day = date.fromisoformat(start_value)
    end_day = date.fromisoformat(end_value)
    if end_day < start_day:
        raise ValueError("End date must not be before start date")
    start = datetime.combine(start_day, dt_time.min, tzinfo=timezone)
    end = datetime.combine(end_day + timedelta(days=1), dt_time.min, tzinfo=timezone)
    return int(start.astimezone(UTC).timestamp()), int(end.astimezone(UTC).timestamp())


def default_comparison_ranges(timezone: ZoneInfo, now: datetime | None = None) -> tuple[tuple[int, int], tuple[int, int]]:
    local_now = (now or datetime.now(timezone)).astimezone(timezone)
    second_end = datetime.combine(local_now.date() + timedelta(days=1), dt_time.min, tzinfo=timezone)
    second_start = second_end - timedelta(days=7)
    first_end = second_start
    first_start = first_end - timedelta(days=7)
    return (
        (int(first_start.astimezone(UTC).timestamp()), int(first_end.astimezone(UTC).timestamp())),
        (int(second_start.astimezone(UTC).timestamp()), int(second_end.astimezone(UTC).timestamp())),
    )


def downsample_history(rows: list[HistoryRow], *, maximum_points: int = 600) -> list[dict[str, Any]]:
    if not rows:
        return []
    step = max(1, math.ceil(len(rows) / maximum_points))
    points: list[dict[str, Any]] = []
    for index in range(0, len(rows), step):
        group = rows[index:index + step]
        raw_values = [float(row.raw_cpm if row.raw_cpm is not None else row.cpm) for row in group]
        corrected_values = [
            float(row.corrected_cpm if row.corrected_cpm is not None else (row.raw_cpm if row.raw_cpm is not None else row.cpm))
            for row in group
        ]
        points.append(
            {
                "timestamp_utc": group[-1].timestamp_utc,
                "cpm": round(statistics.fmean(row.cpm for row in group), 3),
                "raw_cpm": round(statistics.fmean(raw_values), 3),
                "corrected_cpm": round(statistics.fmean(corrected_values), 3),
                "samples": len(group),
                "quality": "confirmed_high" if any(row.cpm_quality == "confirmed_high" for row in group) else "normal",
            }
        )
    return points


@dataclass(frozen=True, slots=True)
class CheckResult:
    key: str
    status: str
    title_key: str
    detail_key: str
    values: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {"key": self.key, "status": self.status, "title_key": self.title_key, "detail_key": self.detail_key, "values": dict(self.values)}


def run_self_test(
    *,
    store: HistoryStore,
    timezone_name: str,
    devices: list[dict[str, Any]],
    home_assistant_available: bool,
    options_path: str | Path = "/data/options.json",
    backup_directory: str | Path | None = None,
    now_utc: int | None = None,
) -> list[CheckResult]:
    now = int(time.time()) if now_utc is None else int(now_utc)
    results: list[CheckResult] = []
    integrity = store.cached_quick_check(max_age_seconds=60)
    results.append(CheckResult("database", "ok" if integrity == "ok" else "error", "Database integrity", "Database check result: {result}", {"result": integrity}))
    schema = store.schema_version()
    results.append(CheckResult("schema", "ok" if schema == SCHEMA_VERSION else "error", "Database schema", "Schema version {current} of {expected}", {"current": schema, "expected": SCHEMA_VERSION}))
    results.append(CheckResult("devices", "ok" if devices else "warning", "Known devices", "{count} devices are registered", {"count": len(devices)}))
    connected = [item for item in devices if bool(item.get("runtime_online"))]
    results.append(CheckResult("connections", "ok" if connected and len(connected) == len(devices) else "warning", "Device connections", "{connected} of {known} devices are connected", {"connected": len(connected), "known": len(devices)}))
    latest = max((int(item.get("timestamp_utc") or item.get("last_timestamp_utc") or 0) for item in devices), default=0)
    age = max(0, now - latest) if latest else None
    freshness_status = "ok" if age is not None and age <= 600 else "warning"
    results.append(CheckResult("freshness", freshness_status, "Measurement freshness", "Latest measurement age: {seconds} seconds" if age is not None else "No stored measurement is available", {"seconds": age or 0}))
    results.append(CheckResult("home_assistant", "ok" if home_assistant_available else "warning", "Home Assistant API", "Home Assistant API is available" if home_assistant_available else "Home Assistant API is currently unavailable"))
    try:
        ZoneInfo(timezone_name)
        results.append(CheckResult("timezone", "ok", "Timezone", "Timezone {timezone} is valid", {"timezone": timezone_name}))
    except ZoneInfoNotFoundError:
        results.append(CheckResult("timezone", "error", "Timezone", "Timezone {timezone} is invalid", {"timezone": timezone_name}))
    try:
        stat = os.statvfs(store.path.parent)
        free_bytes = stat.f_frsize * stat.f_bavail
        results.append(CheckResult("storage", "ok" if free_bytes >= 100 * 1024 * 1024 else "warning", "Free storage", "{mib:.0f} MiB are available", {"mib": free_bytes / (1024 * 1024)}))
    except OSError as exc:
        results.append(CheckResult("storage", "warning", "Free storage", "Storage information is unavailable: {error}", {"error": str(exc)}))
    catalogue_problems = validate_catalogs()
    results.append(CheckResult("translations", "ok" if not catalogue_problems else "error", "Translations", "All translation catalogues are valid" if not catalogue_problems else "Translation catalogue problems: {count}", {"count": len(catalogue_problems)}))
    options = Path(options_path)
    if options.exists():
        try:
            payload = json.loads(options.read_text(encoding="utf-8"))
            config_problems = validate_candidate_options(payload)
            results.append(CheckResult("configuration", "ok" if not config_problems else "warning", "App configuration", "Configuration is valid" if not config_problems else "Configuration warnings: {count}", {"count": len(config_problems)}))
        except (OSError, json.JSONDecodeError, ValueError) as exc:
            results.append(CheckResult("configuration", "error", "App configuration", "Configuration cannot be read: {error}", {"error": str(exc)}))
    else:
        results.append(CheckResult("configuration", "warning", "App configuration", "The options file is not available in this environment"))
    directory = Path(backup_directory or store.path.parent / "managed_backups")
    try:
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        probe = directory / ".write-test"
        probe.write_text("ok", encoding="utf-8")
        probe.unlink(missing_ok=True)
        results.append(CheckResult("backups", "ok", "Managed backups", "The managed backup directory is writable"))
    except OSError as exc:
        results.append(CheckResult("backups", "error", "Managed backups", "The managed backup directory is not writable: {error}", {"error": str(exc)}))
    return results


def validate_candidate_options(payload: object) -> list[str]:
    problems: list[str] = []
    if not isinstance(payload, dict):
        return ["Configuration must be a JSON object"]
    known_groups = {"devices", "dual_tube_devices", "gmcmap", "history", "analysis", "safety", "interface", "system"}
    unknown = sorted(set(payload) - known_groups)
    if unknown:
        problems.append("Unknown top-level groups: " + ", ".join(unknown))
    devices = payload.get("devices", [])
    if not isinstance(devices, list) or not devices:
        problems.append("At least one device configuration is required")
    else:
        names: set[str] = set()
        for index, item in enumerate(devices):
            if not isinstance(item, dict):
                problems.append(f"devices[{index}] must be an object")
                continue
            name = str(item.get("name") or "").strip()
            if name and name.casefold() in names:
                problems.append(f"Duplicate device name: {name}")
            names.add(name.casefold())
            try:
                if int(item.get("scan_interval", 60)) < 5:
                    problems.append(f"devices[{index}].scan_interval must be at least 5 seconds")
            except (TypeError, ValueError):
                problems.append(f"devices[{index}].scan_interval must be numeric")
            try:
                delay = float(item.get("serial_startup_delay", 0 if index == 0 else 15))
                if index > 0 and delay < 15:
                    problems.append(f"devices[{index}].serial_startup_delay should be at least 15 seconds")
            except (TypeError, ValueError):
                problems.append(f"devices[{index}].serial_startup_delay must be numeric")
    dual_devices = payload.get("dual_tube_devices", [])
    if dual_devices not in (None, []):
        if not isinstance(dual_devices, list):
            problems.append("dual_tube_devices must be a list")
        else:
            configured_names = {
                str(item.get("name") or "").strip().casefold()
                for item in devices
                if isinstance(item, dict) and str(item.get("name") or "").strip()
            } if isinstance(devices, list) else set()
            seen_dual_names: set[str] = set()
            for index, item in enumerate(dual_devices):
                if not isinstance(item, dict):
                    problems.append(f"dual_tube_devices[{index}] must be an object")
                    continue
                name = str(item.get("name") or "").strip()
                folded = name.casefold()
                if not name:
                    problems.append(f"dual_tube_devices[{index}].name is required")
                elif folded not in configured_names:
                    problems.append(f"dual_tube_devices[{index}] references unknown device name: {name}")
                elif folded in seen_dual_names:
                    problems.append(f"Duplicate dual-tube device name: {name}")
                seen_dual_names.add(folded)
                mode = str(item.get("dual_tube_mode") or "separate").strip().lower()
                if mode not in {"separate", "curve"}:
                    problems.append(f"dual_tube_devices[{index}].dual_tube_mode must be separate or curve")
                try:
                    switch = item.get("dual_tube_switch_cpm")
                    if switch not in (None, "") and int(switch) <= 0:
                        problems.append(f"dual_tube_devices[{index}].dual_tube_switch_cpm must be greater than zero")
                except (TypeError, ValueError):
                    problems.append(f"dual_tube_devices[{index}].dual_tube_switch_cpm must be numeric")

    history = payload.get("history", {})
    if isinstance(history, dict):
        try:
            retention = int(history.get("retention_days", 90))
            if not 7 <= retention <= 3650:
                problems.append("history.retention_days must be between 7 and 3650")
        except (TypeError, ValueError):
            problems.append("history.retention_days must be numeric")
        timezone_name = str(history.get("report_timezone", "UTC"))
        try:
            ZoneInfo(timezone_name)
        except ZoneInfoNotFoundError:
            problems.append(f"Unknown timezone: {timezone_name}")
    analysis = payload.get("analysis", {})
    if isinstance(analysis, dict):
        try:
            yellow = float(analysis.get("traffic_light_yellow_percent", 125.0))
            red = float(analysis.get("traffic_light_red_percent", 175.0))
            if yellow < 100 or red <= yellow:
                problems.append("Analysis red threshold must be greater than the yellow threshold and yellow must be at least 100")
        except (TypeError, ValueError):
            problems.append("Analysis thresholds must be numeric")
    safety = payload.get("safety", {})
    if isinstance(safety, dict):
        try:
            warning_cpm = float(safety.get("warning_cpm", 51))
            danger_cpm = float(safety.get("danger_cpm", 100))
            if danger_cpm <= warning_cpm:
                problems.append("safety.danger_cpm must be greater than safety.warning_cpm")
            warning_dose = float(safety.get("warning_usvh", 0.326))
            danger_dose = float(safety.get("danger_usvh", 0.651))
            if danger_dose <= warning_dose:
                problems.append("safety.danger_usvh must be greater than safety.warning_usvh")
        except (TypeError, ValueError):
            problems.append("Safety thresholds must be numeric")
    return problems


def onboarding_steps(*, devices: list[dict[str, Any]], sample_count: int, first_timestamp: int | None, baseline_days: int = 7) -> list[dict[str, Any]]:
    now = int(time.time())
    connected = sum(1 for item in devices if bool(item.get("runtime_online")))
    age_days = max(0.0, (now - first_timestamp) / 86400.0) if first_timestamp else 0.0
    return [
        {"key": "device", "complete": bool(devices), "title_key": "Device detected", "detail_key": "At least one GMC device is known"},
        {"key": "connection", "complete": connected > 0, "title_key": "Measurement running", "detail_key": "At least one GMC device is currently connected"},
        {"key": "history", "complete": sample_count >= 10, "title_key": "History is being stored", "detail_key": "Accepted measurements are available in the database"},
        {"key": "baseline", "complete": age_days >= baseline_days, "title_key": "Local baseline available", "detail_key": "The baseline needs approximately {days} days of local history", "values": {"days": baseline_days}},
        {"key": "workflow", "complete": True, "title_key": "Workflow tools ready", "detail_key": "Comparisons, annotations, self-test, backups and APIs are available without additional hardware"},
    ]
