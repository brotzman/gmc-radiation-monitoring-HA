from __future__ import annotations

import io
import json
import threading
import time
import zipfile
from datetime import UTC, datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from gmc_bridge.automation import WorkflowAutomationService
from gmc_bridge.backup_manager import ManagedBackupManager
from gmc_bridge.history import HistoryStore
from gmc_bridge.migrations import SCHEMA_VERSION
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.reports import build_report, resolve_period
from gmc_bridge.workflow import (
    WorkflowSettings,
    compare_periods,
    load_workflow_settings,
    run_self_test,
    save_workflow_settings,
    validate_candidate_options,
)


def _store(tmp_path: Path) -> HistoryStore:
    store = HistoryStore(tmp_path / "history.sqlite3")
    now = int(time.time())
    store.upsert_device_registry(
        "SERIAL-1",
        {
            "device_model": "GMC-500+ Re 2.53",
            "configured_name": "GMC-500+",
            "runtime_online": True,
            "runtime_status_updated_utc": datetime.now(UTC).isoformat(),
            "scan_interval_seconds": 60,
            "device_health_status": "ok",
        },
    )
    for index, cpm in enumerate([10, 11, 12, 13, 14, 20, 21, 22, 23, 24]):
        store.insert_measurement(
            {"cpm": cpm, "voltage_v": 4.1},
            device_serial="SERIAL-1",
            timestamp_utc=now - 600 + index * 60,
            expected_interval_seconds=60,
        )
    return store


def _app(store: HistoryStore) -> ReportApplication:
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
        restore_enabled=False,
        purge_all_history_enabled=False,
    )


def test_schema_8_and_event_annotation_crud(tmp_path: Path) -> None:
    store = _store(tmp_path)
    assert SCHEMA_VERSION == 8
    assert store.schema_version() == 8
    annotation_id = store.add_event_annotation(
        start_timestamp_utc=1_700_000_000,
        end_timestamp_utc=1_700_000_120,
        category="ventilation",
        status="note",
        note="Window and ventilation test",
        device_serial="SERIAL-1",
    )
    rows = store.list_event_annotations(device_serial="SERIAL-1")
    assert rows[0]["id"] == annotation_id
    assert rows[0]["note"] == "Window and ventilation test"
    store.update_event_annotation_status(annotation_id, "confirmed")
    assert store.list_event_annotations(device_serial="SERIAL-1")[0]["status"] == "confirmed"
    store.delete_event_annotation(annotation_id)
    assert store.list_event_annotations(device_serial="SERIAL-1") == []


def test_annotations_survive_backup_restore_and_are_exported(tmp_path: Path) -> None:
    store = _store(tmp_path)
    now = int(time.time())
    store.add_event_annotation(
        start_timestamp_utc=now - 300,
        end_timestamp_utc=now - 120,
        category="maintenance",
        status="confirmed",
        note="Battery and cable check",
        device_serial="SERIAL-1",
    )
    backup = tmp_path / "backup.sqlite3"
    store.backup_to_path(backup)
    restored = HistoryStore(tmp_path / "restored.sqlite3")
    result = restored.restore_backup_path(backup)
    assert result["annotations_merged"] == 1
    assert restored.list_event_annotations(device_serial="SERIAL-1")[0]["note"] == "Battery and cable check"
    second_restore = restored.restore_backup_path(backup)
    assert second_restore["annotations_merged"] == 0
    assert len(restored.list_event_annotations(device_serial="SERIAL-1")) == 1

    period = resolve_period(
        kind="daily",
        selection="specific",
        tz=ZoneInfo("UTC"),
        date_value=datetime.fromtimestamp(now, UTC).date().isoformat(),
    )
    _filename, _content_type, payload = build_report(
        store,
        period=period,
        timezone_name="UTC",
        scan_interval_seconds=60,
        output_format="zip",
        device_serial="SERIAL-1",
    )
    with zipfile.ZipFile(io.BytesIO(payload)) as archive:
        annotation_name = next(name for name in archive.namelist() if name.endswith("annotations.csv"))
        assert "Battery and cable check" in archive.read(annotation_name).decode("utf-8")
        analysis_name = next(name for name in archive.namelist() if name.endswith("analysis.json"))
        analysis = json.loads(archive.read(analysis_name))
        assert analysis["annotations"][0]["category"] == "maintenance"


def test_period_comparison_and_workflow_settings(tmp_path: Path) -> None:
    store = _store(tmp_path)
    rows = store.query_range(0, int(time.time()) + 10, device_serial="SERIAL-1")
    first = rows[:5]
    second = rows[5:]
    comparison = compare_periods(
        store,
        device_serial="SERIAL-1",
        first_start_utc=first[0].timestamp_utc,
        first_end_utc=first[-1].timestamp_utc + 60,
        second_start_utc=second[0].timestamp_utc,
        second_end_utc=second[-1].timestamp_utc + 60,
        scan_interval_seconds=60,
    )
    assert comparison.first.samples == 5
    assert comparison.second.samples == 5
    assert comparison.mean_difference_cpm == 10.0
    assert comparison.interpretation in {"possible_difference", "clear_statistical_difference"}

    settings = WorkflowSettings.from_mapping(
        {
            "notifications_enabled": "true",
            "offline_minutes": 1,
            "report_hour": 99,
            "managed_backup_retention": 100,
        }
    )
    assert settings.notifications_enabled is True
    assert settings.offline_minutes == 2
    assert settings.report_hour == 23
    assert settings.managed_backup_retention == 50
    save_workflow_settings(store, settings)
    assert load_workflow_settings(store) == settings


def test_managed_backup_create_compare_and_prune(tmp_path: Path) -> None:
    store = _store(tmp_path)
    manager = ManagedBackupManager(store, tmp_path / "managed")
    first = manager.create(label="manual")
    store.insert_measurement({"cpm": 33}, device_serial="SERIAL-1", timestamp_utc=int(time.time()) + 30)
    second = manager.create(label="manual")
    comparison = manager.compare(first.name, second.name)
    assert comparison["measurement_difference"] == 1
    assert comparison["schema_equal"] is True
    assert manager.resolve(second.name).is_file()
    removed = manager.prune(1)
    assert len(removed) == 1
    assert len(manager.list()) == 1


def test_self_test_and_candidate_config_validation(tmp_path: Path) -> None:
    store = _store(tmp_path)
    checks = run_self_test(
        store=store,
        timezone_name="Europe/Berlin",
        devices=store.list_devices(),
        home_assistant_available=True,
        options_path=tmp_path / "missing-options.json",
        backup_directory=tmp_path / "managed",
    )
    keys = {item.key for item in checks}
    assert {
        "database",
        "schema",
        "devices",
        "connections",
        "freshness",
        "home_assistant",
        "timezone",
        "storage",
        "translations",
        "configuration",
        "backups",
    } <= keys
    assert next(item for item in checks if item.key == "database").status == "ok"
    good = {
        "devices": [{"name": "GMC", "scan_interval": 60}],
        "history": {"retention_days": 90, "report_timezone": "Europe/Berlin"},
        "analysis": {"traffic_light_yellow_percent": 125, "traffic_light_red_percent": 175},
        "safety": {"warning_cpm": 51, "danger_cpm": 100, "warning_usvh": 0.326, "danger_usvh": 0.651},
    }
    assert validate_candidate_options(good) == []
    bad = {**good, "safety": {"warning_cpm": 100, "danger_cpm": 50, "warning_usvh": 1, "danger_usvh": 0.5}}
    assert len(validate_candidate_options(bad)) == 2


def test_dashboard_and_machine_readable_workflow_apis(tmp_path: Path) -> None:
    store = _store(tmp_path)
    app = _app(store)
    page = app.render_index(
        language_override="de", mode_override="advanced", device_override="SERIAL-1"
    ).decode()
    for visible in (
        "Arbeitsabläufe und Betrieb",
        "Benachrichtigungen und geplante Berichte",
        "Zeiträume vergleichen",
        "Ereignisnotizen",
        "Verlaufsnavigation",
        "System-Selbsttest",
        "Verwaltete Sicherungen",
        "Maschinenlesbare APIs",
    ):
        assert visible in page
    assert 'id="workflow"' in page
    assert "Konfigurations-Vorabprüfung" not in page
    assert "JSON der Konfigurationsprüfung öffnen" not in page
    assert "/api/v1/analysis" in page
    assert app.api_analysis("SERIAL-1")["device_serial"] == "SERIAL-1"
    assert app.api_history(device_serial="SERIAL-1")["accepted"]
    assert "comparison" in app.api_comparison(device_serial="SERIAL-1")
    assert len(app.api_self_test()["checks"]) == 11


class _FakeHomeAssistant:
    def __init__(self) -> None:
        self.notifications: list[dict[str, str]] = []

    def create_persistent_notification(self, *, title: str, message: str, notification_id: str) -> None:
        self.notifications.append({"title": title, "message": message, "notification_id": notification_id})


def test_notification_rule_uses_cooldown_and_scheduled_file_pruning(tmp_path: Path) -> None:
    store = _store(tmp_path)
    fake = _FakeHomeAssistant()
    service = WorkflowAutomationService(
        store=store,
        timezone=ZoneInfo("UTC"),
        timezone_name="UTC",
        scan_interval_seconds=60,
        cpm_per_usvh=154.0,
        traffic_light_yellow_percent=125.0,
        traffic_light_red_percent=175.0,
        home_assistant_client=fake,  # type: ignore[arg-type]
        ui_language="en",
        report_slot=threading.BoundedSemaphore(1),
        report_directory=tmp_path / "scheduled",
        backup_manager=ManagedBackupManager(store, tmp_path / "managed"),
    )
    now = int(time.time())
    # Mark the device offline long enough to trigger exactly one notification.
    store.upsert_device_registry(
        "SERIAL-1",
        {
            "runtime_online": False,
            "runtime_status_updated_utc": datetime.fromtimestamp(now - 3600, UTC).isoformat(),
        },
    )
    settings = WorkflowSettings(notifications_enabled=True, offline_minutes=15, cooldown_minutes=180)
    assert "device_offline" in service.evaluate_notifications(settings, now_utc=now)
    assert service.evaluate_notifications(settings, now_utc=now + 60) == []
    assert any(item["notification_id"] == "gmc_device_offline" for item in fake.notifications)

    service.report_directory.mkdir(parents=True, exist_ok=True)
    for index in range(12):
        path = service.report_directory / f"gmc-old-{index}.json"
        path.write_text("{}", encoding="utf-8")
        path.touch()
        time.sleep(0.001)
    removed = service._prune_scheduled_reports(10)
    assert len(removed) == 2
    assert len(list(service.report_directory.glob("gmc-*.json"))) == 10


def test_monthly_scheduled_summary_creates_backup_and_downloadable_file(tmp_path: Path) -> None:
    store = _store(tmp_path)
    service = WorkflowAutomationService(
        store=store,
        timezone=ZoneInfo("UTC"),
        timezone_name="UTC",
        scan_interval_seconds=60,
        cpm_per_usvh=154.0,
        traffic_light_yellow_percent=125.0,
        traffic_light_red_percent=175.0,
        home_assistant_client=None,
        ui_language="en",
        report_slot=threading.BoundedSemaphore(1),
        report_directory=tmp_path / "scheduled",
        backup_manager=ManagedBackupManager(store, tmp_path / "managed"),
    )
    settings = WorkflowSettings(
        scheduled_reports_enabled=True,
        daily_report=False,
        weekly_report=False,
        monthly_summary=True,
        report_hour=6,
        managed_backup_retention=3,
    )
    completed = service.run_scheduled_tasks(settings, now=datetime(2026, 7, 1, 8, 0, tzinfo=UTC))
    assert completed == ["monthly"]
    summaries = list((tmp_path / "scheduled").glob("gmc-monthly-summary-2026-06.json"))
    assert len(summaries) == 1
    payload = json.loads(summaries[0].read_text(encoding="utf-8"))
    assert payload["period"] == "2026-06"
    assert "SERIAL-1" in payload["devices"]
    assert len(list((tmp_path / "managed").glob("gmc-managed-*.sqlite3"))) == 1
