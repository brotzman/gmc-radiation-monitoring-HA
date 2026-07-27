from __future__ import annotations

import json
import logging
import os
import tempfile
import threading
import time
from pathlib import Path
from typing import Any

from .health_settings import DEFAULT_BRIDGE_HEARTBEAT_INTERVAL_SECONDS

LOG = logging.getLogger("gmc_bridge")

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
            "write_error_count": 0,
            "last_write_error_utc": None,
            "last_write_error": "",
        }
        self._lock = threading.Lock()
        self._write_lock = threading.Lock()
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
        # update() and the periodic heartbeat thread may request a write at the
        # same time. Serialize the complete snapshot/write/replace sequence so
        # an older snapshot cannot overwrite a newer state. Each write also
        # receives its own temporary file; a PID-only name is shared by all
        # threads and allowed one writer to replace another writer's source.
        with self._write_lock:
            payload = self.snapshot()
            self.path.parent.mkdir(parents=True, exist_ok=True)
            descriptor = -1
            temporary: Path | None = None
            try:
                descriptor, temporary_name = tempfile.mkstemp(
                    prefix=f".{self.path.name}.{os.getpid()}.",
                    suffix=".tmp",
                    dir=self.path.parent,
                )
                temporary = Path(temporary_name)
                with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
                    descriptor = -1
                    handle.write(json.dumps(payload, separators=(",", ":"), sort_keys=True))
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, self.path)
            finally:
                if descriptor >= 0:
                    try:
                        os.close(descriptor)
                    except OSError as exc:
                        self._record_write_error(exc)
                if temporary is not None:
                    try:
                        temporary.unlink(missing_ok=True)
                    except OSError as exc:
                        self._record_write_error(exc)

    def _record_write_error(self, error: OSError) -> None:
        now = int(time.time())
        with self._lock:
            count = int(self._state.get("write_error_count") or 0) + 1
            self._state.update({
                "write_error_count": count,
                "last_write_error_utc": now,
                "last_write_error": str(error).replace("\n", " ")[:240],
            })
        if count == 1 or count % 20 == 0:
            LOG.warning("Bridge heartbeat write failed (%d): %s", count, error)

    def _try_write(self) -> None:
        try:
            self.write_now()
        except OSError as exc:
            self._record_write_error(exc)

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
