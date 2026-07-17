from __future__ import annotations

import statistics
import time
from collections import deque
from dataclasses import dataclass
from typing import Any


@dataclass
class SmartMonitor:
    rapid_rise_percent: float = 50.0
    rapid_rise_window_minutes: int = 10
    sustained_alert_minutes: int = 30

    def __post_init__(self) -> None:
        self.samples: deque[tuple[int, int]] = deque()
        self.alert_started_at: int | None = None
        self.last_event_key = ""

    def update(self, cpm: int, *, baseline_cpm: float | None = None, now: int | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
        timestamp = int(time.time()) if now is None else int(now)
        horizon = max(86400, self.rapid_rise_window_minutes * 60 + 60)
        self.samples.append((timestamp, int(cpm)))
        while self.samples and self.samples[0][0] < timestamp - horizon:
            self.samples.popleft()
        values = [float(value) for _, value in self.samples]
        mean_1h_values = [float(value) for ts, value in self.samples if ts > timestamp - 3600]
        mean_1h = statistics.fmean(mean_1h_values) if mean_1h_values else float(cpm)
        median_1h = statistics.median(mean_1h_values) if mean_1h_values else float(cpm)
        sd_1h = statistics.stdev(mean_1h_values) if len(mean_1h_values) > 1 else 0.0
        cutoff = timestamp - self.rapid_rise_window_minutes * 60
        old = [float(value) for ts, value in self.samples if ts <= cutoff]
        reference = old[-1] if old else (values[0] if values else float(cpm))
        rapid_change = 100.0 * (float(cpm) - reference) / reference if reference > 0 else 0.0
        deviation = 100.0 * (mean_1h - baseline_cpm) / baseline_cpm if baseline_cpm and baseline_cpm > 0 else None
        elevated = deviation is not None and deviation >= self.rapid_rise_percent
        if elevated and self.alert_started_at is None:
            self.alert_started_at = timestamp
        elif not elevated:
            self.alert_started_at = None
        sustained = bool(self.alert_started_at and timestamp - self.alert_started_at >= self.sustained_alert_minutes * 60)
        state = "sustained_high" if sustained else "rapid_rise" if rapid_change >= self.rapid_rise_percent else "elevated" if elevated else "normal"
        events: list[dict[str, Any]] = []
        event_key = state if state != "normal" else ""
        if event_key and event_key != self.last_event_key:
            events.append({"timestamp_utc": timestamp, "event_type": event_key, "severity": "warning" if state != "sustained_high" else "danger", "cpm": int(cpm), "details": {"rapid_change_percent": rapid_change, "baseline_deviation_percent": deviation}})
        if not event_key and self.last_event_key:
            events.append({"timestamp_utc": timestamp, "event_type": "returned_to_normal", "severity": "info", "cpm": int(cpm), "details": {}})
        self.last_event_key = event_key
        return ({"smart_alert_state": state, "mean_1h_cpm": round(mean_1h, 3), "median_1h_cpm": round(median_1h, 3), "sd_1h_cpm": round(sd_1h, 3), "rapid_change_percent": round(rapid_change, 2), "baseline_cpm": round(baseline_cpm, 3) if baseline_cpm is not None else None, "baseline_deviation_percent": round(deviation, 2) if deviation is not None else None, "sustained_alert": sustained}, events)
