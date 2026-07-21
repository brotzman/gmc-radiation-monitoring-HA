from __future__ import annotations

import json
import sys
import threading
import time
from pathlib import Path

import yaml

from gmc_bridge.bridge_heartbeat import BridgeHeartbeatReporter, read_bridge_heartbeat
from gmc_bridge.config_validation import validate_options
from gmc_bridge.health import assess_health
from gmc_bridge.history import HistoryStore
from gmc_bridge.runtime_options import runtime_environment
from gmc_bridge.serial_autoconfig import AutomaticSerialBridge
from gmc_bridge.serial_discovery import SerialPortInfo
from gmc_bridge.version import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]


def _options(path: Path, *, system: dict[str, int] | None = None) -> Path:
    payload = {
        "devices": [
            {
                "name": "GMC-320",
                "scan_interval": 60,
                "serial_startup_delay": 0,
            }
        ],
        "dual_tube_devices": [],
        "history": {"retention_days": 90, "report_timezone": "Europe/Berlin"},
        "system": system or {},
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def _store(tmp_path: Path, *, timestamp: int) -> HistoryStore:
    store = HistoryStore(tmp_path / "history.sqlite", retention_days=90)
    store.upsert_device_registry(
        "SERIAL-1",
        {
            "configured_name": "GMC-320",
            "runtime_online": True,
            "runtime_status": "online",
            "scan_interval_seconds": 60,
            "timestamp_utc": timestamp,
            "last_timestamp_utc": timestamp,
        },
    )
    store.insert_measurement(
        {"cpm": 8, "derived_dose_usvh": 0.0519},
        device_serial="SERIAL-1",
        timestamp_utc=timestamp,
    )
    return store


def test_849_bridge_heartbeat_reporter_writes_atomic_liveness_record(tmp_path: Path) -> None:
    path = tmp_path / "bridge-heartbeat.json"
    reporter = BridgeHeartbeatReporter(
        path,
        interval_seconds=0.05,
        configured_devices=2,
    )
    reporter.start()
    reporter.update(
        state="running",
        child_running=True,
        child_pid=1234,
        assigned_devices=2,
    )
    try:
        payload = read_bridge_heartbeat(path)
        assert payload["service"] == "gmc-bridge"
        assert payload["state"] == "running"
        assert payload["child_running"] is True
        assert payload["child_pid"] == 1234
        assert payload["configured_devices"] == 2
        assert payload["assigned_devices"] == 2
        assert not list(tmp_path.glob(".*.tmp"))
    finally:
        reporter.stop()



def test_849_automatic_bridge_reports_runtime_state_transitions() -> None:
    class FakeDiscovery:
        def discover(self, **_kwargs: object) -> list[SerialPortInfo]:
            return [
                SerialPortInfo(
                    path="/dev/null",
                    resolved_path="/dev/null",
                    display_name="GMC-320",
                    detail="test",
                    category="serial",
                    suitable=True,
                    exists=True,
                    stable_path=True,
                    detected_model="GMC-320",
                    detected_serial="SERIAL-1",
                    detected_baudrate=19200,
                    status="detected",
                )
            ]

    class RecordingHeartbeat:
        def __init__(self) -> None:
            self.events: list[tuple[str, dict[str, object]]] = []

        def start(self) -> None:
            self.events.append(("start", {}))

        def update(self, **values: object) -> None:
            self.events.append(("update", values))

        def stop(self, *, state: str = "stopped") -> None:
            self.events.append(("stop", {"state": state}))

    heartbeat = RecordingHeartbeat()
    bridge = AutomaticSerialBridge(
        [{"name": "GMC-320", "scan_interval": 60}],
        child_command=[sys.executable, "-c", "import time; time.sleep(60)"],
        discovery_factory=FakeDiscovery,
        heartbeat_reporter=heartbeat,  # type: ignore[arg-type]
    )
    stopper = threading.Timer(0.2, bridge.request_stop)
    stopper.start()
    try:
        assert bridge.run() == 0
    finally:
        stopper.cancel()
    updates = [values for event, values in heartbeat.events if event == "update"]
    assert any(values.get("state") == "discovering" for values in updates)
    assert any(
        values.get("state") == "running"
        and values.get("child_running") is True
        and values.get("assigned_devices") == 1
        for values in updates
    )
    assert heartbeat.events[-1] == ("stop", {"state": "stopped"})

def test_849_health_distinguishes_bridge_liveness_from_measurement_freshness(tmp_path: Path) -> None:
    now = int(time.time())
    system = {
        "bridge_heartbeat_interval_seconds": 5,
        "health_startup_grace_seconds": 60,
        "health_bridge_warning_seconds": 10,
        "health_bridge_error_seconds": 20,
        "health_measurement_warning_seconds": 30,
        "health_measurement_error_seconds": 60,
    }
    options_path = _options(tmp_path / "options.json", system=system)
    store = _store(tmp_path, timestamp=now)
    devices = [dict(item, health_connected=True) for item in store.list_devices()]
    heartbeat_path = tmp_path / "heartbeat.json"
    heartbeat_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "service": "gmc-bridge",
                "state": "running",
                "started_at_utc": now - 100,
                "updated_at_utc": now - 5,
                "supervisor_pid": 100,
                "child_pid": 101,
                "child_running": True,
                "configured_devices": 1,
                "assigned_devices": 1,
                "last_child_exit_code": None,
            }
        ),
        encoding="utf-8",
    )
    healthy = assess_health(
        store=store,
        devices=devices,
        options_path=options_path,
        scan_interval_seconds=60,
        started_at_utc=now - 100,
        now_utc=now,
        bridge_heartbeat_path=heartbeat_path,
    )
    checks = {item.key: item for item in healthy.checks}
    assert healthy.healthy is True
    assert checks["bridge_heartbeat"].status == "ok"
    assert checks["freshness"].status == "ok"
    assert checks["configuration"].values["health_thresholds"] == {
        "startup_grace_seconds": 60,
        "bridge_warning_seconds": 10,
        "bridge_error_seconds": 20,
        "measurement_warning_seconds": 30,
        "measurement_error_seconds": 60,
    }

    stale_payload = json.loads(heartbeat_path.read_text(encoding="utf-8"))
    stale_payload["updated_at_utc"] = now - 25
    heartbeat_path.write_text(json.dumps(stale_payload), encoding="utf-8")
    unhealthy = assess_health(
        store=store,
        devices=devices,
        options_path=options_path,
        scan_interval_seconds=60,
        started_at_utc=now - 100,
        now_utc=now,
        bridge_heartbeat_path=heartbeat_path,
    )
    stale_checks = {item.key: item for item in unhealthy.checks}
    assert unhealthy.healthy is False
    assert stale_checks["bridge_heartbeat"].status == "error"
    assert stale_checks["freshness"].status == "ok"


def test_849_health_limits_are_validated_and_exported_to_bridge(tmp_path: Path) -> None:
    payload = json.loads(_options(tmp_path / "options.json").read_text(encoding="utf-8"))
    payload["system"] = {
        "bridge_heartbeat_interval_seconds": 15,
        "health_startup_grace_seconds": 900,
        "health_bridge_warning_seconds": 45,
        "health_bridge_error_seconds": 120,
        "health_measurement_warning_seconds": 600,
        "health_measurement_error_seconds": 1200,
    }
    assert validate_options(payload).clean is True
    bridge_env = runtime_environment(payload, "bridge")
    reports_env = runtime_environment(payload, "reports")
    assert bridge_env["BRIDGE_HEARTBEAT_INTERVAL_SECONDS"] == "15"
    assert bridge_env["BRIDGE_HEARTBEAT_PATH"] == "/data/gmc_bridge_heartbeat.json"
    assert reports_env["BRIDGE_HEARTBEAT_PATH"] == "/data/gmc_bridge_heartbeat.json"

    payload["system"]["health_bridge_error_seconds"] = 40
    payload["system"]["health_bridge_warning_seconds"] = 45
    result = validate_options(payload)
    assert any(issue.code == "bridge_health_threshold_order" for issue in result.errors)


def test_849_release_metadata_and_public_defaults() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "8.4.9"
    assert config["version"] == "8.4.9"
    assert (ROOT / "RELEASE_NOTES_8.4.9.md").is_file()
    system = config["options"]["system"]
    assert system["bridge_heartbeat_interval_seconds"] == 15
    assert system["health_startup_grace_seconds"] == 900
    assert system["health_bridge_warning_seconds"] == 45
    assert system["health_bridge_error_seconds"] == 120
    assert system["health_measurement_warning_seconds"] == 600
    assert system["health_measurement_error_seconds"] == 1200
