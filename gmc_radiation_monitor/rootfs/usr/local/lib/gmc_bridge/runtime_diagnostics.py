from __future__ import annotations

import threading
import time
from dataclasses import dataclass
from typing import Any


@dataclass
class _Issue:
    count: int = 0
    first_timestamp_utc: int = 0
    last_timestamp_utc: int = 0
    last_message: str = ""
    last_log_monotonic: float = 0.0


class RuntimeDiagnosticTracker:
    """Rate-limited counters for recoverable failures that must not stay invisible."""

    def __init__(self, *, log_interval_seconds: float = 300.0) -> None:
        self.log_interval_seconds = max(10.0, float(log_interval_seconds))
        self._issues: dict[str, _Issue] = {}
        self._lock = threading.Lock()

    def record(self, name: str, error: BaseException | str) -> tuple[dict[str, Any], bool]:
        now_utc = int(time.time())
        now_monotonic = time.monotonic()
        message = str(error).strip().replace("\n", " ")[:300]
        with self._lock:
            issue = self._issues.setdefault(str(name), _Issue())
            issue.count += 1
            if issue.first_timestamp_utc == 0:
                issue.first_timestamp_utc = now_utc
            issue.last_timestamp_utc = now_utc
            issue.last_message = message
            should_log = now_monotonic - issue.last_log_monotonic >= self.log_interval_seconds
            if should_log:
                issue.last_log_monotonic = now_monotonic
            return self._as_dict(name, issue), should_log

    def recover(self, name: str) -> dict[str, Any] | None:
        with self._lock:
            issue = self._issues.pop(str(name), None)
            return self._as_dict(name, issue) if issue else None

    def snapshot(self) -> dict[str, dict[str, Any]]:
        with self._lock:
            return {name: self._as_dict(name, issue) for name, issue in self._issues.items()}

    @staticmethod
    def _as_dict(name: str, issue: _Issue) -> dict[str, Any]:
        return {
            "name": name,
            "count": issue.count,
            "first_timestamp_utc": issue.first_timestamp_utc,
            "last_timestamp_utc": issue.last_timestamp_utc,
            "last_message": issue.last_message,
        }
