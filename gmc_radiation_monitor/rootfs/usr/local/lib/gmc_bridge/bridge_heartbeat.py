from __future__ import annotations

import json
import os
import threading
import time
from pathlib import Path
from typing import Any

from .health_settings import DEFAULT_BRIDGE_HEARTBEAT_INTERVAL_SECONDS

DEFAULT_BRIDGE_HEARTBEAT_PATH = Path("/data/gmc_bridge_heartbeat.json")
BRIDGE_HEARTBEAT_SCHEMA_VERSION = 1


class BridgeHeartbeatReporter:
    """Write an atomic liveness record for the bridge supervisor process."""

    def __init__(
        self,
        path: str | Path = DEFAULT_BRIDGE_HEARTBEAT_PATH,
        *,
        interval_seconds: float = DEFAULT_BRIDGE_HEARTBEAT_INTERVAL_SECONDS,
        configured_devices: int = 0,
    ) -> None:
        self.path = Path(path)
        self.interval_seconds = max(0.05, float(interval_seconds))
        now = int(time.time())
        self._state: dict[str, Any] = {
            "schema_version": BRIDGE_HEARTBEAT_SCHEMA_VERSION,
            "service": "gmc-bridge",
            "state": "starting",
            "started_at_utc": now,
            "updated_at_utc": now,
            "supervisor_pid": os.getpid(),
            "child_pid": None,
            "child_running": False,
            "configured_devices": max(0, int(configured_devices)),
            "assigned_devices": 0,
            "last_child_exit_code": None,
        }
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop_event.clear()
        self._try_write()
        self._thread = threading.Thread(
            target=self._run,
            name="gmc-bridge-heartbeat",
            daemon=True,
        )
        self._thread.start()

    def update(self, **values: Any) -> None:
        with self._lock:
            self._state.update(values)
            self._state["updated_at_utc"] = int(time.time())
        self._try_write()

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            state = dict(self._state)
        state["updated_at_utc"] = int(time.time())
        return state

    def write_now(self) -> None:
        payload = self.snapshot()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_name(f".{self.path.name}.{os.getpid()}.tmp")
        try:
            temporary.write_text(
                json.dumps(payload, separators=(",", ":"), sort_keys=True),
                encoding="utf-8",
            )
            os.chmod(temporary, 0o600)
            os.replace(temporary, self.path)
        finally:
            try:
                temporary.unlink(missing_ok=True)
            except OSError:
                pass

    def _try_write(self) -> None:
        try:
            self.write_now()
        except OSError:
            pass

    def stop(self, *, state: str = "stopped") -> None:
        self.update(
            state=state,
            child_running=False,
            child_pid=None,
        )
        self._stop_event.set()
        thread = self._thread
        if thread is not None and thread is not threading.current_thread():
            thread.join(timeout=max(1.0, self.interval_seconds * 2))
        self._thread = None

    def _run(self) -> None:
        while not self._stop_event.wait(self.interval_seconds):
            self._try_write()


def read_bridge_heartbeat(path: str | Path) -> dict[str, Any]:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("Bridge heartbeat must contain a JSON object")
    if int(payload.get("schema_version", 0)) != BRIDGE_HEARTBEAT_SCHEMA_VERSION:
        raise ValueError("Unsupported bridge heartbeat schema")
    updated = int(payload.get("updated_at_utc", 0))
    if updated <= 0:
        raise ValueError("Bridge heartbeat has no valid timestamp")
    return payload
