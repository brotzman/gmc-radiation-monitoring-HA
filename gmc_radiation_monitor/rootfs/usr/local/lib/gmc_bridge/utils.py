from __future__ import annotations

import re
from datetime import UTC, datetime
from threading import Event


def slugify(value: str) -> str:
    result = re.sub(r"[^a-zA-Z0-9_-]+", "_", value).strip("_").lower()
    return result or "unknown"


def utc_timestamp() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")


def interruptible_sleep(seconds: float, stop_event: Event, poll_interval: float = 0.25) -> bool:
    """Sleep up to seconds and return False when interrupted by stop_event."""
    return not stop_event.wait(timeout=max(0.0, seconds))
