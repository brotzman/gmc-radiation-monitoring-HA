from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any, Protocol

from .presentation_models import AnalysisStatus, DeviceIssue


class TranslatorLike(Protocol):
    def __call__(self, text: str, **values: object) -> str: ...


@dataclass(frozen=True, slots=True)
class Explanation:
    title_key: str
    body_key: str
    action_key: str = ""


EXPLANATIONS: dict[str, Explanation] = {
    "radiation_intelligence": Explanation(
        "Why is this assessment shown?",
        "The app combines the recent trend, robust statistics, agreement between connected counters and the learned local background. The result is a statistical aid and does not identify a physical cause.",
        "No action is required while the result remains normal. Investigate persistent changes by checking the measurement location and comparing both devices.",
    ),
    "adaptive_background": Explanation(
        "How is the background profile calculated?",
        "The app compares quality-filtered measurements from the same weekday and hour. Robust medians reduce the influence of isolated spikes and regular daily patterns are kept separate from unusual changes.",
        "During the learning phase, leave the counters in a stable location and allow additional measurements to accumulate.",
    ),
    "historical_development": Explanation(
        "What does the historical trend mean?",
        "Daily quality-filtered medians are smoothed over seven days. The period cards compare the recent part of each period with the preceding part; detected jumps are statistical changes and do not determine their cause.",
        "Check location, orientation and environmental conditions when a persistent jump appears.",
    ),
    "cosmic_influence": Explanation(
        "How is the pressure relationship assessed?",
        "The app compares quality-filtered radiation measurements with available air-pressure data. A statistical relationship can support interpretation, but correlation alone does not prove a cosmic or environmental cause.",
        "Use this as context only and review longer periods before drawing conclusions.",
    ),
    "fleet_intelligence": Explanation(
        "How are connected counters compared?",
        "Only quality-filtered, one-to-one time-matched measurements are compared. Agreement, correlation, relative bias and stability are evaluated separately so one faulty counter does not automatically define the site result.",
        "Keep both counters close together and similarly oriented when using the comparison as a reference.",
    ),
    "counting_statistics": Explanation(
        "Why are Poisson values shown?",
        "Radiation counts fluctuate naturally. The Fano factor and Poisson spread ratio compare the observed variation with a simple counting-statistics model; they describe distribution shape but not a physical cause or calibration state.",
        "Interpret these values together with coverage, device stability and the historical background.",
    ),
    "data_quality": Explanation(
        "How is data quality evaluated?",
        "The score combines time-window coverage, missing or irregular intervals, duplicate timestamps and optional-sensor coverage. It indicates how strongly the analysis can rely on the stored series.",
        "Resolve persistent connection gaps before relying on long-term comparisons.",
    ),
}


ACTION_MESSAGES: dict[str, str] = {
    "analysis_learning": "No action is required. The assessment becomes more reliable as additional measurements are collected.",
    "analysis_review_events": "Review the recent trend and event timing. Check both counters and the measurement location if the change persists.",
    "analysis_improve_coverage": "Resolve persistent connection gaps before relying on long-term comparisons.",
    "analysis_continue_monitoring": "No action is required. Continue normal monitoring.",
}


ISSUE_MESSAGES: dict[str, tuple[str, str]] = {
    "orientation_frame_invalid": (
        "Orientation data is temporarily unavailable.",
        "Radiation measurement continues; only the optional orientation value is affected.",
    ),
    "temperature_unavailable": (
        "Device temperature is unavailable.",
        "Radiation measurement continues. An external Home Assistant temperature may be used when configured.",
    ),
    "serial_connection_unstable": (
        "The serial connection is unstable.",
        "Check the USB cable and power supply if this continues for more than 15 minutes.",
    ),
}


def translate_explanation(
    code: str | None,
    translator: TranslatorLike,
    *,
    values: Mapping[str, Any] | None = None,
) -> tuple[str, str, str] | None:
    if not code or code not in EXPLANATIONS:
        return None
    entry = EXPLANATIONS[code]
    params = dict(values or {})
    return (
        translator(entry.title_key, **params),
        translator(entry.body_key, **params),
        translator(entry.action_key, **params) if entry.action_key else "",
    )


def translate_issue(issue: DeviceIssue, translator: TranslatorLike) -> tuple[str, str]:
    title_key, impact_key = ISSUE_MESSAGES.get(
        issue.code,
        ("A device function is temporarily unavailable.", "Radiation measurement continues unless the device status says otherwise."),
    )
    values = dict(issue.values)
    return translator(title_key, **values), translator(impact_key, **values)


def issue_status_class(status: AnalysisStatus) -> str:
    return {
        AnalysisStatus.GOOD: "good",
        AnalysisStatus.NOTICE: "notice",
        AnalysisStatus.LEARNING: "notice",
        AnalysisStatus.WARNING: "alert",
        AnalysisStatus.ERROR: "alert",
        AnalysisStatus.UNAVAILABLE: "neutral",
        AnalysisStatus.NEUTRAL: "neutral",
    }[status]


def translate_action(code: str | None, translator: TranslatorLike) -> str:
    if not code:
        return ""
    key = ACTION_MESSAGES.get(code, "")
    return translator(key) if key else ""
