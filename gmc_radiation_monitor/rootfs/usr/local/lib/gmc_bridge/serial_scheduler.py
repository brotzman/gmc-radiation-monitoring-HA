from __future__ import annotations

import logging
import threading
import time
from collections.abc import Iterator
from contextlib import contextmanager

from .errors import GmcError

LOG = logging.getLogger("gmc_bridge")


class SerialScheduler:
    """Coordinate serial command windows across independently configured GMCs.

    The counters use separate file descriptors, but on small hosts they may still
    share one USB controller and power domain.  This scheduler prevents command
    bursts from different counters from starting at the same instant and leaves
    a configurable quiet gap between complete command windows.
    """

    def __init__(self, *, enabled: bool = True, minimum_gap_seconds: float = 2.0) -> None:
        self.enabled = bool(enabled)
        self.minimum_gap_seconds = max(0.0, float(minimum_gap_seconds))
        self._condition = threading.Condition()
        self._active_device: int | None = None
        self._next_allowed_at = 0.0

    @contextmanager
    def window(self, device_index: int, label: str, stop_event: threading.Event) -> Iterator[None]:
        if not self.enabled:
            yield
            return

        with self._condition:
            while True:
                if stop_event.is_set():
                    raise GmcError("Interrupted while waiting for serial scheduler")
                now = time.monotonic()
                delay = max(0.0, self._next_allowed_at - now)
                if self._active_device is None and delay <= 0.0:
                    self._active_device = device_index
                    break
                self._condition.wait(timeout=min(0.25, delay) if delay > 0 else 0.25)

        LOG.debug("[scheduler] device=%d state=%s entered serial window", device_index + 1, label)
        try:
            yield
        finally:
            with self._condition:
                self._active_device = None
                self._next_allowed_at = time.monotonic() + self.minimum_gap_seconds
                self._condition.notify_all()
            LOG.debug("[scheduler] device=%d state=%s left serial window", device_index + 1, label)
