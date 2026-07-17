from __future__ import annotations

import statistics
from collections import deque
from dataclasses import dataclass


@dataclass(frozen=True)
class CpmAssessment:
    """Explain why one CPM value is normal or requires confirmation."""

    cpm: int
    suspicious: bool
    trigger: str
    baseline_median: float | None
    adaptive_threshold: int | None


class HighCpmGate:
    """Hold back fixed-limit and extreme adaptive CPM spikes until confirmed.

    The fixed 10,000 CPM safety limit remains active. Before a per-device
    baseline exists, a conservative 1,000 CPM startup threshold prevents a
    single corrupt reading from bypassing plausibility checks. Once a short
    baseline exists, values far above the recent median are treated as
    suspicious even when they are below the fixed limit. Suspicious values must
    occur three times consecutively at a closely similar magnitude before they
    are released. Normal accepted readings feed the rolling baseline; held-back
    and confirmed-high readings do not.
    """

    NORMAL = "normal"
    PENDING = "pending"
    CONFIRMED = "confirmed"

    def __init__(
        self,
        threshold: int = 10000,
        confirmations: int = 3,
        *,
        adaptive_window: int = 12,
        adaptive_min_samples: int = 5,
        adaptive_multiplier: float = 20.0,
        adaptive_minimum_cpm: int = 1000,
        adaptive_minimum_delta: int = 500,
        pending_consistency_ratio: float = 1.25,
    ) -> None:
        self.threshold = int(threshold)
        self.confirmations = int(confirmations)
        self.adaptive_min_samples = max(3, int(adaptive_min_samples))
        self.adaptive_multiplier = max(2.0, float(adaptive_multiplier))
        self.adaptive_minimum_cpm = max(1, int(adaptive_minimum_cpm))
        self.adaptive_minimum_delta = max(1, int(adaptive_minimum_delta))
        self.pending_consistency_ratio = max(1.1, float(pending_consistency_ratio))
        self._recent_normal: deque[int] = deque(
            maxlen=max(self.adaptive_min_samples, int(adaptive_window))
        )
        self._count = 0
        self._state = self.NORMAL
        self._just_confirmed = False
        self._pending_reference: float | None = None
        self._last_assessment = CpmAssessment(0, False, "normal", None, None)
        self._last_accept_reason = "normal"

    def seed(self, values: list[int] | tuple[int, ...]) -> None:
        """Warm the adaptive baseline from previously accepted measurements.

        Older releases may have stored a one-off spike as ``normal``. The
        median of the seed batch is used to reject legacy contamination before
        values reach the live rolling baseline.
        """
        prepared = [int(value) for value in values if 0 <= int(value) <= self.threshold]
        if len(prepared) >= self.adaptive_min_samples:
            center = float(statistics.median(prepared))
            seed_limit = min(
                self.threshold,
                max(
                    self.adaptive_minimum_cpm,
                    round(center * self.adaptive_multiplier),
                    round(center + self.adaptive_minimum_delta),
                ),
            )
        else:
            # A short history cannot establish a trustworthy median. Keep only
            # values that would pass the conservative cold-start gate.
            seed_limit = min(self.threshold, self.adaptive_minimum_cpm)
        prepared = [value for value in prepared if value <= seed_limit]
        for cpm in prepared:
            self._recent_normal.append(cpm)

    def assess(self, cpm: int) -> CpmAssessment:
        value = int(cpm)
        baseline = self.baseline_median
        adaptive_threshold = self.adaptive_threshold
        effective_threshold = (
            adaptive_threshold
            if adaptive_threshold is not None
            else min(self.threshold, self.adaptive_minimum_cpm)
        )
        if value > self.threshold:
            return CpmAssessment(value, True, "fixed_threshold", baseline, effective_threshold)
        if value > effective_threshold:
            trigger = "adaptive_threshold" if adaptive_threshold is not None else "startup_threshold"
            return CpmAssessment(value, True, trigger, baseline, effective_threshold)
        return CpmAssessment(value, False, "normal", baseline, effective_threshold)

    def accept(self, cpm: int, *, assessment: CpmAssessment | None = None) -> bool:
        self._just_confirmed = False
        current = assessment or self.assess(cpm)
        self._last_assessment = current

        if not current.suspicious:
            self.reset()
            self._recent_normal.append(int(cpm))
            self._last_accept_reason = "normal"
            return True

        if self._state == self.CONFIRMED:
            self._last_accept_reason = "confirmed_high"
            return True

        self._state = self.PENDING
        if not self._is_consistent_pending_value(int(cpm)):
            self._count = 0
            self._pending_reference = float(cpm)
        self._count = min(self._count + 1, self.confirmations)
        if self._pending_reference is None:
            self._pending_reference = float(cpm)
        else:
            self._pending_reference = statistics.median(
                (self._pending_reference, float(cpm))
            )
        if self._count >= self.confirmations:
            self._state = self.CONFIRMED
            self._just_confirmed = True
            self._last_accept_reason = "consecutive_confirmed"
            return True
        self._last_accept_reason = "pending_confirmation"
        return False

    def _is_consistent_pending_value(self, cpm: int) -> bool:
        if self._pending_reference is None or self._count == 0:
            return True
        low = min(float(cpm), self._pending_reference)
        high = max(float(cpm), self._pending_reference)
        if low <= 0:
            return high <= 0
        return high / low <= self.pending_consistency_ratio

    def reset(self, *, clear_history: bool = False) -> None:
        self._count = 0
        self._state = self.NORMAL
        self._just_confirmed = False
        self._pending_reference = None
        if clear_history:
            self._recent_normal.clear()

    @property
    def baseline_median(self) -> float | None:
        if len(self._recent_normal) < self.adaptive_min_samples:
            return None
        return float(statistics.median(self._recent_normal))

    @property
    def adaptive_threshold(self) -> int | None:
        baseline = self.baseline_median
        if baseline is None:
            return None
        calculated = max(
            self.adaptive_minimum_cpm,
            round(baseline * self.adaptive_multiplier),
            round(baseline + self.adaptive_minimum_delta),
        )
        return min(self.threshold, calculated)

    @property
    def pending(self) -> int:
        return self._count

    @property
    def state(self) -> str:
        return self._state

    @property
    def just_confirmed(self) -> bool:
        return self._just_confirmed

    @property
    def last_assessment(self) -> CpmAssessment:
        return self._last_assessment

    @property
    def last_accept_reason(self) -> str:
        return self._last_accept_reason
