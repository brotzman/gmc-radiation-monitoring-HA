from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class DeviceHealthResult:
    status: str
    reason: str
    event: dict[str, Any] | None = None


class DeviceHealthMonitor:
    """Detect likely blocked/stuck counters without rejecting measurements."""

    def __init__(self, *, window_size: int = 20, zero_limit: int = 12, constant_limit: int = 12) -> None:
        self.values: deque[int] = deque(maxlen=max(12, int(window_size)))
        self.zero_limit = max(6, int(zero_limit))
        self.constant_limit = max(6, int(constant_limit))
        self._last_status = "ok"

    def update(self, sample: dict[str, Any]) -> DeviceHealthResult:
        cpm = int(sample.get("cpm", 0))
        self.values.append(cpm)
        status = "ok"
        reason = "normal_variation"

        if len(self.values) >= self.zero_limit and all(v == 0 for v in list(self.values)[-self.zero_limit:]):
            status, reason = "warning", "prolonged_zero_cpm"
        elif len(self.values) >= self.constant_limit and len(set(list(self.values)[-self.constant_limit:])) == 1:
            status, reason = "warning", "unchanged_cpm_sequence"

        low = sample.get("tube_low_cpm")
        high = sample.get("tube_high_cpm")
        if low is not None and high is not None:
            low_i, high_i = int(low), int(high)
            total = max(1, low_i + high_i)
            if total >= 30 and (low_i == 0 or high_i == 0):
                status, reason = "warning", "dual_tube_imbalance"

        event = None
        if status != self._last_status:
            event = {
                "event_type": "device_health_changed",
                "severity": "warning" if status == "warning" else "info",
                "cpm": cpm,
                "details": {"status": status, "reason": reason},
            }
        self._last_status = status
        return DeviceHealthResult(status=status, reason=reason, event=event)
