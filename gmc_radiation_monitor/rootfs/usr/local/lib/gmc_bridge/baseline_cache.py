from __future__ import annotations

import statistics
import threading
from collections import deque
from dataclasses import dataclass
from typing import Iterable

from .history import HistoryRow


@dataclass(frozen=True)
class BaselineSnapshot:
    value_cpm: float | None
    samples: int
    start_timestamp_utc: int | None
    end_timestamp_utc: int | None


class RollingBaselineCache:
    """Per-device rolling baseline that avoids a full SQLite scan every cycle."""

    def __init__(self, *, window_seconds: int) -> None:
        self.window_seconds = max(3600, int(window_seconds))
        self._rows: deque[tuple[int, float]] = deque()
        self._lock = threading.RLock()

    def seed(self, rows: Iterable[HistoryRow], *, now_utc: int) -> None:
        with self._lock:
            self._rows.clear()
            cutoff = int(now_utc) - self.window_seconds
            for row in sorted(rows, key=lambda item: item.timestamp_utc):
                if int(row.timestamp_utc) >= cutoff:
                    self._rows.append((int(row.timestamp_utc), float(row.cpm)))
            self._expire(now_utc)

    def add(self, timestamp_utc: int, cpm: int | float) -> None:
        with self._lock:
            timestamp = int(timestamp_utc)
            if self._rows and timestamp < self._rows[-1][0]:
                self._rows.append((timestamp, max(0.0, float(cpm))))
                self._rows = deque(sorted(self._rows, key=lambda item: item[0]))
            else:
                self._rows.append((timestamp, max(0.0, float(cpm))))
            self._expire(timestamp)

    def _expire(self, now_utc: int) -> None:
        cutoff = int(now_utc) - self.window_seconds
        while self._rows and self._rows[0][0] < cutoff:
            self._rows.popleft()

    def snapshot(self, *, now_utc: int) -> BaselineSnapshot:
        with self._lock:
            self._expire(now_utc)
            values = [value for _timestamp, value in self._rows]
            return BaselineSnapshot(
                value_cpm=float(statistics.median(values)) if values else None,
                samples=len(values),
                start_timestamp_utc=self._rows[0][0] if self._rows else None,
                end_timestamp_utc=self._rows[-1][0] if self._rows else None,
            )
