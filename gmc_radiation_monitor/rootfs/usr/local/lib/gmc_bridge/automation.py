from __future__ import annotations

import json
import logging
import threading
import time
from collections.abc import Callable
from contextlib import suppress
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any

from .backup_manager import ManagedBackupManager
from .history import HistoryStore
from .home_assistant import HomeAssistantConfigClient
from .reports import build_report_to_path, resolve_period
from .translations import SUPPORTED_UI_LANGUAGES, Translator
from .workflow import WorkflowSettings, load_workflow_settings, summarize_period

LOG = logging.getLogger("gmc_workflow")
_NOTIFICATION_STATE_KEY = "workflow_notification_state_v1"
_SCHEDULER_STATE_KEY = "workflow_scheduler_state_v1"


class WorkflowAutomationService:
    """Run optional notifications, managed backups and scheduled reports.

    The service is deliberately started only by the report-server process. Unit
    tests and library consumers can instantiate ReportApplication without
    creating background threads.
    """

    def __init__(
        self,
        *,
        store: HistoryStore,
        timezone,
        timezone_name: str,
        scan_interval_seconds: int,
        cpm_per_usvh: float,
        traffic_light_yellow_percent: float,
        traffic_light_red_percent: float,
        home_assistant_client: HomeAssistantConfigClient | None,
        ui_language: str,
        report_slot: threading.BoundedSemaphore,
        report_directory: str | Path | None = None,
        backup_manager: ManagedBackupManager | None = None,
        analysis_provider: Callable[[str, int, float], dict[str, Any]] | None = None,
    ) -> None:
        self.store = store
        self.timezone = timezone
        self.timezone_name = timezone_name
        self.scan_interval_seconds = max(5, int(scan_interval_seconds))
        self.cpm_per_usvh = float(cpm_per_usvh)
        self.traffic_light_yellow_percent = float(traffic_light_yellow_percent)
        self.traffic_light_red_percent = float(traffic_light_red_percent)
        self.home_assistant_client = home_assistant_client
        language = ui_language if ui_language in SUPPORTED_UI_LANGUAGES else "en"
        self.t = Translator(language)
        self.report_slot = report_slot
        self.report_directory = Path(report_directory or store.path.parent / "scheduled_reports")
        self.report_directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.backup_manager = backup_manager or ManagedBackupManager(store)
        self.analysis_provider = analysis_provider
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread and self._thread.is_alive():
            return
        self._thread = threading.Thread(target=self._run, name="gmc-workflow-automation", daemon=True)
        self._thread.start()

    def stop(self) -> None:
        self._stop.set()
        if self._thread:
            self._thread.join(timeout=5)

    def _run(self) -> None:
        while not self._stop.is_set():
            try:
                settings = load_workflow_settings(self.store)
                self.evaluate_notifications(settings)
                self.run_scheduled_tasks(settings)
            except Exception as exc:  # pragma: no cover - defensive daemon boundary
                LOG.exception("Workflow automation iteration failed: %s", exc)
            self._stop.wait(60.0)

    def _load_state(self, key: str) -> dict[str, Any]:
        raw = self.store.get_metadata().get(key, "")
        try:
            value = json.loads(raw) if raw else {}
        except (TypeError, ValueError, json.JSONDecodeError):
            value = {}
        return value if isinstance(value, dict) else {}

    def _save_state(self, key: str, state: dict[str, Any]) -> None:
        self.store.set_metadata({key: json.dumps(state, sort_keys=True, separators=(",", ":"))})

    def evaluate_notifications(self, settings: WorkflowSettings, *, now_utc: int | None = None) -> list[str]:
        if not settings.notifications_enabled or self.home_assistant_client is None:
            return []
        now = int(time.time()) if now_utc is None else int(now_utc)
        state = self._load_state(_NOTIFICATION_STATE_KEY)
        sent: list[str] = []
        conditions: dict[str, tuple[bool, str, str]] = {}
        devices = self.store.list_devices()

        if settings.notify_device_offline:
            offline = []
            threshold = settings.offline_minutes * 60
            for item in devices:
                if bool(item.get("runtime_online")):
                    continue
                updated = str(item.get("runtime_status_updated_utc") or "")
                updated_epoch = 0
                if updated:
                    try:
                        updated_epoch = int(
                            datetime.fromisoformat(updated.replace("Z", "+00:00")).timestamp()
                        )
                    except ValueError:
                        updated_epoch = 0
                if updated_epoch and now - updated_epoch >= threshold:
                    offline.append(
                        str(
                            item.get("configured_name")
                            or item.get("device_model")
                            or item.get("serial")
                            or "GMC"
                        )
                    )
            conditions["device_offline"] = (
                bool(offline),
                self.t("GMC device offline"),
                self.t(
                    "The following devices have been offline for at least {minutes} minutes: {devices}",
                    minutes=settings.offline_minutes,
                    devices=", ".join(offline),
                ),
            )

        if settings.notify_data_stale:
            latest = max(
                (int(item.get("timestamp_utc") or item.get("last_timestamp_utc") or 0) for item in devices),
                default=0,
            )
            stale = bool(latest and now - latest >= settings.stale_minutes * 60)
            conditions["data_stale"] = (
                stale,
                self.t("GMC measurements are stale"),
                self.t(
                    "No accepted GMC measurement has been stored for at least {minutes} minutes.",
                    minutes=settings.stale_minutes,
                ),
            )

        if settings.notify_database_problem:
            integrity = self.store.cached_quick_check(max_age_seconds=60)
            conditions["database_problem"] = (
                integrity != "ok",
                self.t("GMC database problem"),
                self.t("The SQLite quick check returned: {result}", result=integrity),
            )

        if settings.notify_confirmed_event:
            newest_event = 0
            newest_serial = ""
            newest_severity = ""
            newest_cpm: Any = None
            for item in devices:
                serial = str(item.get("serial") or "")
                for event in self.store.recent_operational_events(limit=20, device_serial=serial):
                    severity = str(event.get("severity") or "").lower()
                    if severity not in {"warning", "error", "red", "critical"}:
                        continue
                    timestamp = int(event.get("timestamp_utc") or 0)
                    if timestamp > newest_event:
                        newest_event = timestamp
                        newest_serial = serial
                        newest_severity = severity
                        newest_cpm = event.get("cpm")
            last_seen = int(state.get("confirmed_event_timestamp") or 0)
            active = newest_event > last_seen and newest_event >= now - 3600
            conditions["confirmed_event"] = (
                active,
                self.t("Confirmed GMC event"),
                self.t(
                    "A confirmed {severity} event was recorded for {device} at {time}{cpm}.",
                    severity=newest_severity or "warning",
                    device=newest_serial or "GMC",
                    time=datetime.fromtimestamp(newest_event or now, UTC)
                    .astimezone(self.timezone)
                    .strftime("%Y-%m-%d %H:%M %Z"),
                    cpm=(f" · {int(newest_cpm)} CPM" if newest_cpm is not None else ""),
                ),
            )
            if active:
                state["confirmed_event_timestamp"] = newest_event

        cooldown = settings.cooldown_minutes * 60
        recoverable_conditions = {"device_offline", "data_stale", "database_problem"}
        for key, (active, title, message) in conditions.items():
            item = state.get(key) if isinstance(state.get(key), dict) else {}
            last_notified = int(item.get("last_notified_utc") or 0)
            was_active = bool(item.get("active"))
            active_since = int(item.get("active_since_utc") or 0)
            if active and not was_active:
                active_since = now
            should_send = active and (not was_active or now - last_notified >= cooldown)
            if should_send:
                try:
                    self.home_assistant_client.create_persistent_notification(
                        title=title,
                        message=message,
                        notification_id=f"gmc_{key}",
                    )
                    sent.append(key)
                    last_notified = now
                except Exception as exc:
                    LOG.warning("Could not create Home Assistant notification %s: %s", key, exc)
                    state["last_notification_error"] = str(exc)[:500]
            elif was_active and not active and key in recoverable_conditions:
                duration_seconds = max(0, now - active_since) if active_since else 0
                duration_minutes = max(1, round(duration_seconds / 60)) if duration_seconds else 1
                try:
                    self.home_assistant_client.create_persistent_notification(
                        title=self.t("GMC condition resolved"),
                        message=self.t(
                            "{condition} is no longer active. Duration: about {minutes} minutes.",
                            condition=title,
                            minutes=duration_minutes,
                        ),
                        notification_id=f"gmc_{key}",
                    )
                    sent.append(f"{key}_resolved")
                except Exception as exc:
                    LOG.warning("Could not create Home Assistant recovery notification %s: %s", key, exc)
                    state["last_notification_error"] = str(exc)[:500]
                active_since = 0
            state[key] = {
                "active": active,
                "active_since_utc": active_since,
                "last_notified_utc": last_notified,
                "updated_utc": now,
            }
        if sent:
            state["last_notification_success_utc"] = now
        self._save_state(_NOTIFICATION_STATE_KEY, state)
        return sent

    def run_scheduled_tasks(self, settings: WorkflowSettings, *, now: datetime | None = None) -> list[str]:
        if not settings.scheduled_reports_enabled:
            return []
        current = (now or datetime.now(self.timezone)).astimezone(self.timezone)
        if current.hour < settings.report_hour:
            return []
        state = self._load_state(_SCHEDULER_STATE_KEY)
        completed: list[str] = []
        jobs: list[tuple[str, str]] = []
        if settings.daily_report:
            jobs.append(("daily", (current.date() - timedelta(days=1)).isoformat()))
        if settings.weekly_report and current.weekday() == 0:
            previous_monday = current.date() - timedelta(days=7)
            iso = previous_monday.isocalendar()
            jobs.append(("weekly", f"{iso.year}-W{iso.week:02d}"))
        if settings.monthly_summary and current.day == 1:
            previous_month_end = current.date().replace(day=1) - timedelta(days=1)
            jobs.append(("monthly", previous_month_end.strftime("%Y-%m")))

        for kind, label in jobs:
            state_key = f"last_{kind}_label"
            if state.get(state_key) == label:
                continue
            if not self.report_slot.acquire(blocking=False):
                continue
            try:
                backup = self.backup_manager.create(label=f"scheduled-{kind}")
                self.backup_manager.prune(settings.managed_backup_retention)
                files = self._generate_scheduled_report(kind, label, current)
                self._prune_scheduled_reports(max(10, settings.managed_backup_retention * 4))
                state[state_key] = label
                state[f"last_{kind}_utc"] = int(time.time())
                state[f"last_{kind}_files"] = files
                state["last_backup"] = backup.name
                state.pop("last_error", None)
                completed.append(kind)
                if self.home_assistant_client is not None:
                    try:
                        self.home_assistant_client.create_persistent_notification(
                            title=self.t("GMC scheduled report ready"),
                            message=self.t(
                                "The {kind} report for {period} was created successfully. Files: {count}",
                                kind=self.t(kind.capitalize()),
                                period=label,
                                count=len(files),
                            ),
                            notification_id=f"gmc_scheduled_{kind}",
                        )
                    except Exception as exc:
                        LOG.warning("Could not announce scheduled report: %s", exc)
            except Exception as exc:
                LOG.exception("Scheduled %s report failed: %s", kind, exc)
                state["last_error"] = str(exc)[:500]
                state["last_error_utc"] = int(time.time())
                if self.home_assistant_client is not None:
                    # Notification failure must not abort scheduling.
                    with suppress(Exception):  # nosec B110
                        self.home_assistant_client.create_persistent_notification(
                            title=self.t("GMC scheduled report failed"),
                            message=self.t(
                                "The {kind} report for {period} could not be created: {error}",
                                kind=self.t(kind.capitalize()),
                                period=label,
                                error=str(exc),
                            ),
                            notification_id=f"gmc_scheduled_{kind}_failed",
                        )
            finally:
                self.report_slot.release()
        self._save_state(_SCHEDULER_STATE_KEY, state)
        return completed

    def _prune_scheduled_reports(self, keep: int) -> list[str]:
        candidates: list[Path] = []
        for path in self.report_directory.iterdir():
            if path.is_file() and path.name.startswith("gmc-") and path.suffix.lower() in {".zip", ".json"}:
                candidates.append(path)
        candidates.sort(key=lambda item: item.stat().st_mtime, reverse=True)
        deleted: list[str] = []
        for path in candidates[max(1, int(keep)) :]:
            try:
                path.unlink()
                deleted.append(path.name)
            except OSError as exc:
                LOG.warning("Could not prune scheduled report %s: %s", path, exc)
        return deleted

    def _generate_scheduled_report(self, kind: str, label: str, current: datetime) -> list[str]:
        files: list[str] = []
        devices = [item for item in self.store.list_devices() if str(item.get("serial") or "").strip()]
        if kind in {"daily", "weekly"}:
            if kind == "daily":
                period = resolve_period(
                    kind="daily", selection="specific", tz=self.timezone, date_value=label
                )
            else:
                period = resolve_period(
                    kind="weekly", selection="specific", tz=self.timezone, week_value=label
                )
            for item in devices:
                serial = str(item.get("serial"))
                scan = int(item.get("scan_interval_seconds") or self.scan_interval_seconds)
                factor = float(item.get("cpm_per_usvh") or self.cpm_per_usvh)
                safe_serial = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in serial)
                output = self.report_directory / f"gmc-{kind}-{label}-{safe_serial}.zip"
                build_report_to_path(
                    self.store,
                    output,
                    period=period,
                    timezone_name=self.timezone_name,
                    scan_interval_seconds=scan,
                    output_format="zip",
                    cpm_per_usvh=factor,
                    traffic_light_yellow_percent=self.traffic_light_yellow_percent,
                    traffic_light_red_percent=self.traffic_light_red_percent,
                    device_serial=serial,
                    all_devices=False,
                    language=self.t.language,
                )
                files.append(output.name)
            return files

        # Monthly summaries are compact JSON files so they remain inexpensive
        # even with multi-year histories.
        year, month = (int(value) for value in label.split("-", 1))
        start_local = datetime(year, month, 1, tzinfo=self.timezone)
        if month == 12:
            end_local = datetime(year + 1, 1, 1, tzinfo=self.timezone)
        else:
            end_local = datetime(year, month + 1, 1, tzinfo=self.timezone)
        start_utc = int(start_local.astimezone(UTC).timestamp())
        end_utc = int(end_local.astimezone(UTC).timestamp())
        payload: dict[str, Any] = {
            "period": label,
            "generated_at_utc": datetime.now(UTC).isoformat(),
            "timezone": self.timezone_name,
            "devices": {},
        }
        for item in devices:
            serial = str(item.get("serial"))
            scan = int(item.get("scan_interval_seconds") or self.scan_interval_seconds)
            rows = self.store.query_range(start_utc, end_utc, device_serial=serial)
            payload["devices"][serial] = summarize_period(
                rows,
                start_utc=start_utc,
                end_utc=end_utc,
                scan_interval_seconds=scan,
            ).as_dict()
        output = self.report_directory / f"gmc-monthly-summary-{label}.json"
        output.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        files.append(output.name)
        return files


def automation_status(store: HistoryStore) -> dict[str, Any]:
    metadata = store.get_metadata()
    result: dict[str, Any] = {}
    for key, output_key in ((_NOTIFICATION_STATE_KEY, "notifications"), (_SCHEDULER_STATE_KEY, "scheduler")):
        try:
            value = json.loads(metadata.get(key, "{}"))
        except (TypeError, ValueError, json.JSONDecodeError):
            value = {}
        result[output_key] = value if isinstance(value, dict) else {}
    return result
