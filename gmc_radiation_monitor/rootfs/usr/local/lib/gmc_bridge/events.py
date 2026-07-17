from __future__ import annotations

import statistics
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from .history import HistoryRow


@dataclass(frozen=True)
class AnomalyThresholds:
    yellow_enter: float
    red_enter: float
    yellow_clear: float
    red_clear: float

    @classmethod
    def from_enter_thresholds(cls, yellow: float, red: float) -> AnomalyThresholds:
        if yellow < 100 or red <= yellow:
            raise ValueError("red threshold must be greater than yellow threshold")
        return cls(
            yellow_enter=yellow,
            red_enter=red,
            yellow_clear=max(100.0, yellow - 10.0),
            red_clear=max(yellow, red - 15.0),
        )


class EventStateMachine:
    """Small hysteretic state machine for relative-background anomalies."""

    def __init__(self, thresholds: AnomalyThresholds) -> None:
        self.thresholds = thresholds
        self.state = "normal"

    def update(self, index_percent: float) -> str:
        if self.state == "normal":
            if index_percent >= self.thresholds.red_enter:
                self.state = "red"
            elif index_percent >= self.thresholds.yellow_enter:
                self.state = "yellow"
        elif self.state == "yellow":
            if index_percent >= self.thresholds.red_enter:
                self.state = "red"
            elif index_percent < self.thresholds.yellow_clear:
                self.state = "normal"
        elif self.state == "red":
            if index_percent < self.thresholds.yellow_clear:
                self.state = "normal"
            elif index_percent < self.thresholds.red_clear:
                self.state = "yellow"
        return self.state


def current_hysteretic_state(indices: Iterable[float], *, yellow: float, red: float) -> str:
    machine = EventStateMachine(AnomalyThresholds.from_enter_thresholds(yellow, red))
    seen = False
    for value in indices:
        seen = True
        machine.update(float(value))
    return machine.state if seen else "learning"


def rolling_background_states(
    rows: list[HistoryRow],
    *,
    baseline_mean: float | None,
    yellow_percent: float,
    red_percent: float,
    window_seconds: int = 15 * 60,
) -> list[tuple[HistoryRow, float, float, str]]:
    if not rows or baseline_mean is None or baseline_mean <= 0:
        return []
    thresholds = AnomalyThresholds.from_enter_thresholds(yellow_percent, red_percent)
    machine = EventStateMachine(thresholds)
    ordered = sorted(rows, key=lambda row: row.timestamp_utc)
    rolling: list[HistoryRow] = []
    states: list[tuple[HistoryRow, float, float, str]] = []
    for row in ordered:
        rolling.append(row)
        cutoff = row.timestamp_utc - window_seconds
        while rolling and rolling[0].timestamp_utc <= cutoff:
            rolling.pop(0)
        rolling_mean = statistics.fmean(float(item.cpm) for item in rolling)
        index = 100.0 * rolling_mean / baseline_mean
        states.append((row, rolling_mean, index, machine.update(index)))
    return states


def detect_events(
    rows: list[HistoryRow],
    *,
    baseline_mean: float | None,
    yellow_percent: float,
    red_percent: float,
    scan_interval_seconds: int,
) -> list[dict[str, Any]]:
    states = rolling_background_states(
        rows,
        baseline_mean=baseline_mean,
        yellow_percent=yellow_percent,
        red_percent=red_percent,
    )
    if not states:
        return []

    events: list[dict[str, Any]] = []
    current: list[tuple[HistoryRow, float, float, str]] = []
    for state in [*states, (None, 0.0, 0.0, "normal")]:  # type: ignore[list-item]
        row, _, _, severity = state
        if row is not None and severity in {"yellow", "red"}:
            current.append(state)
            continue
        if not current:
            continue
        start = current[0][0].timestamp_utc
        end = current[-1][0].timestamp_utc
        max_index = max(item[2] for item in current)
        event_severity = "red" if any(item[3] == "red" for item in current) else "yellow"
        minimum_duration = 5 * 60 if event_severity == "red" else 10 * 60
        duration = max(scan_interval_seconds, end - start + scan_interval_seconds)
        if duration >= minimum_duration:
            cpms = [float(item[0].cpm) for item in current]
            events.append(
                {
                    "start_timestamp_utc": start,
                    "end_timestamp_utc": end,
                    "duration_seconds": duration,
                    "severity": event_severity,
                    "max_cpm": max(cpms),
                    "mean_cpm": statistics.fmean(cpms),
                    "max_background_index_percent": max_index,
                    "hysteresis_yellow_clear_percent": max(100.0, yellow_percent - 10.0),
                    "hysteresis_red_clear_percent": max(yellow_percent, red_percent - 15.0),
                }
            )
        current = []
    return events
