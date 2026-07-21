from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class AnalysisStatus(StrEnum):
    """Canonical presentation states shared by analyses and web views."""

    GOOD = "good"
    NOTICE = "notice"
    LEARNING = "learning"
    WARNING = "warning"
    ERROR = "error"
    UNAVAILABLE = "unavailable"
    NEUTRAL = "neutral"


class AnalysisLevel(StrEnum):
    """Stable analysis depth identifiers used by UI, reports and tests."""

    SUMMARY = "summary"
    ANALYSIS = "analysis"
    EXPERT = "expert"

    @classmethod
    def normalize(
        cls, value: str | None, *, default: AnalysisLevel | None = None
    ) -> AnalysisLevel:
        fallback = default if isinstance(default, cls) else cls.ANALYSIS
        try:
            return cls(str(value or ""))
        except ValueError:
            return fallback


@dataclass(frozen=True, slots=True)
class HistoryPeriod:
    key: str
    days: int
    label_key: str


HISTORY_PERIODS: tuple[HistoryPeriod, ...] = (
    HistoryPeriod("week", 7, "7 days"),
    HistoryPeriod("month", 30, "30 days"),
    HistoryPeriod("quarter", 90, "90 days"),
    HistoryPeriod("year", 365, "365 days"),
)


@dataclass(frozen=True, slots=True)
class AnalysisMetric:
    """A display-neutral analysis metric.

    Text is represented by translation keys and parameter mappings so the
    calculation layer does not have to produce localized prose.
    """

    key: str
    label_key: str
    value: str
    value_key: str = ""
    value_values: Mapping[str, Any] = field(default_factory=dict)
    level: AnalysisLevel = AnalysisLevel.ANALYSIS
    status: AnalysisStatus = AnalysisStatus.NEUTRAL
    note_key: str = ""
    note_values: Mapping[str, Any] = field(default_factory=dict)
    note_parts: tuple[AnalysisMessage, ...] = ()
    interpretation_key: str = ""
    interpretation_values: Mapping[str, Any] = field(default_factory=dict)
    priority: bool = False
    label_values: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AnalysisMessage:
    """One translated explanatory statement attached to an analysis."""

    key: str
    text_key: str
    values: Mapping[str, Any] = field(default_factory=dict)
    level: AnalysisLevel = AnalysisLevel.ANALYSIS
    status: AnalysisStatus = AnalysisStatus.NEUTRAL


@dataclass(frozen=True, slots=True)
class AnalysisTableColumn:
    key: str
    label_key: str


@dataclass(frozen=True, slots=True)
class AnalysisTable:
    """Small display-neutral table used by expert analysis sections."""

    key: str
    title_key: str
    columns: tuple[AnalysisTableColumn, ...]
    rows: tuple[Mapping[str, str], ...] = ()
    level: AnalysisLevel = AnalysisLevel.EXPERT
    empty_key: str = ""


@dataclass(frozen=True, slots=True)
class AnalysisEntity:
    """A repeated subject inside an analysis, for example one connected device."""

    key: str
    title: str
    status: AnalysisStatus = AnalysisStatus.NEUTRAL
    primary_value: str | None = None
    metrics: tuple[AnalysisMetric, ...] = ()
    messages: tuple[AnalysisMessage, ...] = ()
    level: AnalysisLevel = AnalysisLevel.ANALYSIS
    values: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AnalysisSection:
    """A named group of metrics, messages, entities and optional tables."""

    key: str
    title_key: str
    subtitle_key: str = ""
    level: AnalysisLevel = AnalysisLevel.ANALYSIS
    metrics: tuple[AnalysisMetric, ...] = ()
    messages: tuple[AnalysisMessage, ...] = ()
    entities: tuple[AnalysisEntity, ...] = ()
    tables: tuple[AnalysisTable, ...] = ()
    explanation_code: str | None = None
    open_by_default: bool = False
    values: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AnalysisResult:
    """Shared result contract for dashboard, reports and future APIs.

    The top-level fields cover compact summaries. ``sections`` and ``entities``
    carry the complete analysis without falling back to ad-hoc HTML-specific
    dictionaries. This lets the dashboard, JSON reports and future clients use
    the same semantic result tree.
    """

    key: str
    status: AnalysisStatus
    headline_key: str
    summary_key: str
    primary_value: str | None = None
    confidence: float | None = None
    metrics: tuple[AnalysisMetric, ...] = ()
    explanation_code: str | None = None
    action_code: str | None = None
    values: Mapping[str, Any] = field(default_factory=dict)
    messages: tuple[AnalysisMessage, ...] = ()
    sections: tuple[AnalysisSection, ...] = ()
    entities: tuple[AnalysisEntity, ...] = ()
    tables: tuple[AnalysisTable, ...] = ()
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def as_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "status": self.status.value,
            "headline_key": self.headline_key,
            "summary_key": self.summary_key,
            "primary_value": self.primary_value,
            "confidence": self.confidence,
            "explanation_code": self.explanation_code,
            "action_code": self.action_code,
            "values": dict(self.values),
            "metadata": dict(self.metadata),
            "metrics": [_metric_dict(metric) for metric in self.metrics],
            "messages": [_message_dict(message) for message in self.messages],
            "entities": [_entity_dict(entity) for entity in self.entities],
            "tables": [_table_dict(table) for table in self.tables],
            "sections": [_section_dict(section) for section in self.sections],
        }


@dataclass(frozen=True, slots=True)
class DeviceIssue:
    """One technical issue with an explicit user-facing impact contract."""

    code: str
    severity: AnalysisStatus
    affects_measurement: bool
    retryable: bool
    technical_detail: str = ""
    values: Mapping[str, Any] = field(default_factory=dict)


def _metric_dict(metric: AnalysisMetric) -> dict[str, Any]:
    return {
        "key": metric.key,
        "label_key": metric.label_key,
        "label_values": dict(metric.label_values),
        "value": metric.value,
        "value_key": metric.value_key,
        "value_values": dict(metric.value_values),
        "level": metric.level.value,
        "status": metric.status.value,
        "note_key": metric.note_key,
        "note_values": dict(metric.note_values),
        "note_parts": [_message_dict(part) for part in metric.note_parts],
        "interpretation_key": metric.interpretation_key,
        "interpretation_values": dict(metric.interpretation_values),
        "priority": metric.priority,
    }


def _message_dict(message: AnalysisMessage) -> dict[str, Any]:
    return {
        "key": message.key,
        "text_key": message.text_key,
        "values": dict(message.values),
        "level": message.level.value,
        "status": message.status.value,
    }


def _table_dict(table: AnalysisTable) -> dict[str, Any]:
    return {
        "key": table.key,
        "title_key": table.title_key,
        "level": table.level.value,
        "empty_key": table.empty_key,
        "columns": [
            {"key": column.key, "label_key": column.label_key}
            for column in table.columns
        ],
        "rows": [dict(row) for row in table.rows],
    }


def _entity_dict(entity: AnalysisEntity) -> dict[str, Any]:
    return {
        "key": entity.key,
        "title": entity.title,
        "status": entity.status.value,
        "primary_value": entity.primary_value,
        "level": entity.level.value,
        "values": dict(entity.values),
        "metrics": [_metric_dict(metric) for metric in entity.metrics],
        "messages": [_message_dict(message) for message in entity.messages],
    }


def _section_dict(section: AnalysisSection) -> dict[str, Any]:
    return {
        "key": section.key,
        "title_key": section.title_key,
        "subtitle_key": section.subtitle_key,
        "level": section.level.value,
        "explanation_code": section.explanation_code,
        "open_by_default": section.open_by_default,
        "values": dict(section.values),
        "metrics": [_metric_dict(metric) for metric in section.metrics],
        "messages": [_message_dict(message) for message in section.messages],
        "entities": [_entity_dict(entity) for entity in section.entities],
        "tables": [_table_dict(table) for table in section.tables],
    }
