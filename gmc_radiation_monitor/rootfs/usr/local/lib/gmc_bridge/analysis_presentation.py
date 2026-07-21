from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from .device_profiles import normalize_device_version_display
from .presentation_models import (
    HISTORY_PERIODS,
    AnalysisEntity,
    AnalysisLevel,
    AnalysisMessage,
    AnalysisMetric,
    AnalysisResult,
    AnalysisSection,
    AnalysisStatus,
    AnalysisTable,
    AnalysisTableColumn,
)
from .utils import slugify


@dataclass(frozen=True, slots=True)
class AnalysisPresentationConfig:
    """Configuration values needed to turn calculations into semantic results."""

    scan_interval_seconds: int = 60
    cpm_per_usvh: float = 154.0
    traffic_light_yellow_percent: float = 125.0
    traffic_light_red_percent: float = 175.0
    safety_profile: str = "gq"
    safety_threshold_basis: str = "either"
    safety_warning_cpm: int = 51
    safety_danger_cpm: int = 100
    safety_warning_usvh: float = 0.326
    safety_danger_usvh: float = 0.651


def _quality_status(label: str) -> AnalysisStatus:
    return {
        "Excellent": AnalysisStatus.GOOD,
        "Good": AnalysisStatus.GOOD,
        "Limited": AnalysisStatus.NOTICE,
        "Poor": AnalysisStatus.WARNING,
    }.get(label, AnalysisStatus.UNAVAILABLE)


def _metric(
    label: str,
    value: str,
    *,
    key: str | None = None,
    level: AnalysisLevel = AnalysisLevel.ANALYSIS,
    status: AnalysisStatus = AnalysisStatus.NEUTRAL,
    note_key: str = "",
    note_values: Mapping[str, Any] | None = None,
    note_parts: tuple[AnalysisMessage, ...] = (),
    interpretation_key: str = "",
    interpretation_values: Mapping[str, Any] | None = None,
    priority: bool = False,
    value_key: str = "",
    value_values: Mapping[str, Any] | None = None,
    label_values: Mapping[str, Any] | None = None,
) -> AnalysisMetric:
    return AnalysisMetric(
        key=key or slugify(label),
        label_key=label,
        label_values=dict(label_values or {}),
        value=value,
        value_key=value_key,
        value_values=dict(value_values or {}),
        level=level,
        status=status,
        note_key=note_key,
        note_values=dict(note_values or {}),
        note_parts=note_parts,
        interpretation_key=interpretation_key,
        interpretation_values=dict(interpretation_values or {}),
        priority=priority,
    )


def _message(
    key: str,
    text_key: str,
    *,
    values: Mapping[str, Any] | None = None,
    level: AnalysisLevel = AnalysisLevel.ANALYSIS,
    status: AnalysisStatus = AnalysisStatus.NEUTRAL,
) -> AnalysisMessage:
    return AnalysisMessage(
        key=key,
        text_key=text_key,
        values=dict(values or {}),
        level=level,
        status=status,
    )


def _analysis_scan_interval(analysis: Mapping[str, Any], config: AnalysisPresentationConfig) -> int:
    return max(1, int(analysis.get("_scan_interval_seconds") or config.scan_interval_seconds))


def _analysis_cpm_per_usvh(analysis: Mapping[str, Any], config: AnalysisPresentationConfig) -> float:
    return max(0.001, float(analysis.get("_cpm_per_usvh") or config.cpm_per_usvh))


def _value(analysis: Mapping[str, Any], name: str, decimals: int = 2, suffix: str = "") -> str:
    raw = analysis.get(name)
    if raw is None:
        return "—"
    return f"{float(raw):.{decimals}f}{suffix}"


def _signed_value(analysis: Mapping[str, Any], name: str, decimals: int = 2, suffix: str = "") -> str:
    raw = analysis.get(name)
    if raw is None:
        return "—"
    return f"{float(raw):+.{decimals}f}{suffix}"


def _dose_value(analysis: Mapping[str, Any], name: str, config: AnalysisPresentationConfig) -> str:
    raw = analysis.get(name)
    if raw is None:
        return "—"
    return f"{float(raw) / _analysis_cpm_per_usvh(analysis, config):.3f} µSv/h"


def _coverage_note(count: int, coverage_percent: float) -> tuple[str, dict[str, Any]]:
    return "n={count} · {coverage:.1f}% coverage", {
        "count": count,
        "coverage": coverage_percent,
    }


def _uncertainty_text(analysis: Mapping[str, Any], name: str) -> str:
    item = analysis.get(name) or {}
    if not item.get("available"):
        return "Counting uncertainty not available"
    duration_seconds = int(item.get("duration_seconds") or 0)
    if duration_seconds >= 3600 and duration_seconds % 3600 == 0:
        duration = f"{duration_seconds / 3600:g} h"
    else:
        duration = f"{duration_seconds / 60:g} min"
    return (
        f"−{float(item.get('minus_cpm') or 0.0):.2f}/"
        f"+{float(item.get('plus_cpm') or 0.0):.2f} CPM · "
        f"{int(item.get('impulses') or 0)} impulses in {duration}"
    )



def _uncertainty_message(
    analysis: Mapping[str, Any], name: str, *, key: str
) -> AnalysisMessage:
    item = analysis.get(name) or {}
    if not item.get("available"):
        return _message(key, "Counting uncertainty not available")
    duration_seconds = int(item.get("duration_seconds") or 0)
    if duration_seconds >= 3600 and duration_seconds % 3600 == 0:
        duration = f"{duration_seconds / 3600:g} h"
    else:
        duration = f"{duration_seconds / 60:g} min"
    return _message(
        key,
        "Counting uncertainty (68%): −{minus:.2f}/+{plus:.2f} CPM · {impulses} impulses in {duration}",
        values={
            "minus": float(item.get("minus_cpm") or 0.0),
            "plus": float(item.get("plus_cpm") or 0.0),
            "impulses": int(item.get("impulses") or 0),
            "duration": duration,
        },
    )

def _z_interpretation(analysis: Mapping[str, Any]) -> tuple[str, AnalysisStatus]:
    raw = analysis.get("z_score_24h")
    if raw is None:
        return "Not available yet — the 24 h CPM series needs variation and at least two samples", AnalysisStatus.NEUTRAL
    magnitude = abs(float(raw))
    if magnitude < 2:
        return "Within normal statistical variation", AnalysisStatus.GOOD
    if magnitude < 3:
        return "Noticeable statistical deviation", AnalysisStatus.NOTICE
    return "Strong statistical deviation", AnalysisStatus.WARNING


def _fano_interpretation(analysis: Mapping[str, Any]) -> tuple[str, AnalysisStatus]:
    raw = analysis.get("fano_factor_24h")
    if raw is None:
        return "Not available yet — at least two CPM samples are required", AnalysisStatus.NEUTRAL
    number = float(raw)
    if 0.8 <= number <= 1.2:
        return "Close to Poisson expectation", AnalysisStatus.GOOD
    if number < 0.8:
        return "Less variable than Poisson expectation", AnalysisStatus.NOTICE
    return "More variable than Poisson expectation", AnalysisStatus.NOTICE


def _poisson_interpretation(analysis: Mapping[str, Any]) -> tuple[str, AnalysisStatus]:
    raw = analysis.get("poisson_sd_ratio_24h")
    if raw is None:
        return "Not available yet — the 24 h mean and spread are still insufficient", AnalysisStatus.NEUTRAL
    number = float(raw)
    if 0.9 <= number <= 1.1:
        return "Very close to Poisson-like spread", AnalysisStatus.GOOD
    if 0.75 <= number <= 1.25:
        return "Broadly compatible with Poisson-like spread", AnalysisStatus.GOOD
    return "Noticeable difference from Poisson-like spread", AnalysisStatus.NOTICE


def _correlation_details(analysis: Mapping[str, Any], prefix: str) -> tuple[str, str, dict[str, Any], str]:
    count = int(analysis.get(f"{prefix}_pairs_24h", 0))
    status = str(analysis.get(f"{prefix}_correlation_status_24h", ""))
    raw = analysis.get(f"{prefix}_correlation_24h")
    if status == "ok" and raw is not None:
        number = float(raw)
        magnitude = abs(number)
        if magnitude < 0.1:
            interpretation = "Very weak linear relationship"
        elif magnitude < 0.3:
            interpretation = "Weak linear relationship"
        elif magnitude < 0.5:
            interpretation = "Moderate linear relationship"
        elif magnitude < 0.7:
            interpretation = "Strong linear relationship"
        else:
            interpretation = "Very strong linear relationship"
        return f"{number:.3f}", "Pearson r · n={count} paired samples", {"count": count}, interpretation
    if status == "no sensor variation":
        reason = "Not available — the sensor value did not vary during this period"
    elif status == "no CPM variation":
        reason = "Not available — CPM did not vary during this period"
    else:
        reason = "Not available yet — more paired samples are required"
    return "—", "n={count} paired samples", {"count": count}, reason


def _drift_interpretation(analysis: Mapping[str, Any]) -> tuple[str, AnalysisStatus]:
    raw = analysis.get("baseline_drift_percent")
    if raw is None:
        return "Not available yet — more baseline history is required", AnalysisStatus.NEUTRAL
    magnitude = abs(float(raw))
    if magnitude < 5:
        return "Baseline currently stable", AnalysisStatus.GOOD
    if magnitude < 10:
        return "Small baseline drift", AnalysisStatus.NOTICE
    return "Noticeable baseline drift", AnalysisStatus.NOTICE


def _quality_interpretation_key(label: str) -> str:
    return {
        "Excellent": "Very complete 24 h data window",
        "Good": "Suitable for most trend analysis",
        "Limited": "Interpret statistics with coverage in mind",
        "Poor": "Too little or too fragmented for strong conclusions",
    }.get(label, "Data quality status unavailable")


def _quality_reason_message(reason: str, index: int) -> AnalysisMessage:
    patterns = (
        (r"^(\d+(?:\.\d+)?)% time-window coverage$", "{value}% time-window coverage", float),
        (r"^longest gap (\d+) s$", "longest gap {value} s", int),
        (r"^(\d+) unusually short intervals$", "{value} unusually short intervals", int),
        (r"^(\d+) long intervals$", "{value} long intervals", int),
        (r"^(\d+) duplicate timestamps observed$", "{value} duplicate timestamps observed", int),
        (r"^(\d+) clock regressions observed$", "{value} clock regressions observed", int),
        (r"^temperature coverage (\d+(?:\.\d+)?)%$", "temperature coverage {value}%", float),
        (r"^voltage coverage (\d+(?:\.\d+)?)%$", "voltage coverage {value}%", float),
    )
    for pattern, key, converter in patterns:
        match = re.fullmatch(pattern, reason)
        if match:
            raw = match.group(1)
            converted = converter(raw)
            value: Any = f"{converted:.1f}" if converter is float else converted
            return _message(f"quality-reason-{index}", key, values={"value": value}, level=AnalysisLevel.EXPERT)
    return _message(f"quality-reason-{index}", reason, level=AnalysisLevel.EXPERT)


def build_primary_analysis_result(analysis: dict[str, Any]) -> AnalysisResult:
    """Build the compact shared summary of one live analysis."""
    if not analysis.get("available"):
        return AnalysisResult(
            key="primary_analysis",
            status=AnalysisStatus.UNAVAILABLE,
            headline_key="No measurements yet.",
            summary_key="Analysis, the traffic light and downloads will become meaningful after the first stored samples arrive.",
            explanation_code="data_quality",
        )

    quality_label = str(analysis.get("data_quality_label_24h") or "Poor")
    quality_score = float(analysis.get("data_quality_score_24h") or 0.0)
    baseline_ready = bool(analysis.get("baseline_ready"))
    background_index = analysis.get("background_index_percent")
    events = int(analysis.get("events_24h") or 0)

    if not baseline_ready:
        status = AnalysisStatus.LEARNING
        headline = "Baseline learning in progress"
        summary = "The absolute level is currently uncritical. More local history is required before anomaly detection becomes reliable."
        action = "analysis_learning"
    elif events > 0 or (background_index is not None and float(background_index) >= 175.0):
        status = AnalysisStatus.WARNING
        headline = "Continue observing"
        summary = "The absolute level is currently uncritical, but the local comparison or short-term trend deserves continued observation."
        action = "analysis_review_events"
    elif _quality_status(quality_label) == AnalysisStatus.WARNING:
        status = AnalysisStatus.NOTICE
        headline = "Interpret statistics with coverage in mind"
        summary = "Too little or too fragmented for strong conclusions"
        action = "analysis_improve_coverage"
    else:
        status = AnalysisStatus.GOOD
        headline = "No action required"
        summary = "The current value is below the configured warning threshold and within the usual local range."
        action = "analysis_continue_monitoring"

    metrics = (
        _metric(
            "Latest CPM",
            f"{float(analysis.get('latest_cpm') or 0.0):.0f} CPM",
            key="latest_cpm",
            level=AnalysisLevel.SUMMARY,
            status=status,
            priority=True,
        ),
        _metric(
            "Background index",
            "—" if background_index is None else f"{float(background_index):.1f}%",
            key="background_index",
            level=AnalysisLevel.SUMMARY,
            status=status,
            note_key="1 h mean / 7 d mean × 100",
            priority=True,
        ),
        _metric(
            "Data quality",
            quality_label,
            value_key=quality_label,
            key="data_quality",
            status=_quality_status(quality_label),
            note_key="score {score:.1f}/100 · coverage {coverage:.1f}% · longest gap {gap} s",
            note_values={
                "score": quality_score,
                "coverage": float(analysis.get("coverage_24h_percent") or 0.0),
                "gap": int(analysis.get("longest_gap_24h_seconds") or 0),
            },
        ),
    )
    return AnalysisResult(
        key="primary_analysis",
        status=status,
        headline_key=headline,
        summary_key=summary,
        primary_value=f"{float(analysis.get('latest_cpm') or 0.0):.0f} CPM",
        confidence=max(0.0, min(1.0, quality_score / 100.0)),
        metrics=metrics,
        explanation_code="data_quality",
        action_code=action,
    )


def build_detailed_analysis_result(
    analysis: dict[str, Any],
    *,
    config: AnalysisPresentationConfig,
    latest_local: datetime | None = None,
) -> AnalysisResult:
    """Build every detailed device-analysis section as one shared result tree."""
    primary = build_primary_analysis_result(analysis)
    if not analysis.get("available"):
        return primary

    quality_label = str(analysis.get("data_quality_label_24h") or "Poor")
    quality_status = _quality_status(quality_label)
    coverage_1h_key, coverage_1h_values = _coverage_note(
        int(analysis.get("samples_1h") or 0), float(analysis.get("coverage_1h_percent") or 0.0)
    )
    coverage_24h_key, coverage_24h_values = _coverage_note(
        int(analysis.get("samples_24h") or 0), float(analysis.get("coverage_24h_percent") or 0.0)
    )
    coverage_7d_key, coverage_7d_values = _coverage_note(
        int(analysis.get("samples_7d") or 0), float(analysis.get("coverage_7d_percent") or 0.0)
    )
    overview = AnalysisSection(
        key="overview",
        title_key="Overview",
        subtitle_key="The values most users need first",
        level=AnalysisLevel.ANALYSIS,
        open_by_default=True,
        metrics=(
            _metric(
                "Latest CPM",
                _value(analysis, "latest_cpm", 0, " CPM"),
                key="overview-latest",
                note_parts=(
                    _message("overview-latest-time", "{content}", values={"content": latest_local.strftime("%Y-%m-%d %H:%M:%S %Z") if latest_local is not None else ""}),
                    _uncertainty_message(analysis, "counting_uncertainty_latest", key="overview-latest-uncertainty"),
                ),
                priority=True,
            ),
            _metric(
                "24 h mean",
                _value(analysis, "mean_24h", 2, " CPM"),
                key="overview-mean-24h",
                note_parts=(
                    _message("overview-24h-coverage", coverage_24h_key, values=coverage_24h_values),
                    _uncertainty_message(analysis, "counting_uncertainty_24h", key="overview-24h-uncertainty"),
                ),
                priority=True,
            ),
            _metric(
                "Events last 24 h",
                _value(analysis, "events_24h", 0),
                key="overview-events",
                note_key="Sustained yellow/red relative anomaly events",
                interpretation_key=("No sustained relative anomaly events detected" if int(analysis.get("events_24h") or 0) == 0 else "Review the event export for timing and severity"),
                status=(AnalysisStatus.GOOD if int(analysis.get("events_24h") or 0) == 0 else AnalysisStatus.NOTICE),
                priority=True,
            ),
            _metric("Background index", _value(analysis, "background_index_percent", 1, "%"), key="overview-background-index", note_key="1 h mean / 7 d mean × 100", priority=True),
            _metric("Latest dose rate", _dose_value(analysis, "latest_cpm", config), key="overview-latest-dose", note_key="Derived from latest CPM"),
            _metric("1 h mean dose rate", _dose_value(analysis, "mean_1h", config), key="overview-mean-dose", note_key="Derived from 1 h mean CPM"),
        ),
    )

    z_text, z_status = _z_interpretation(analysis)
    statistics = AnalysisSection(
        key="statistics",
        title_key="Statistics",
        subtitle_key="24 h distribution, percentiles and latest-value deviation",
        level=AnalysisLevel.EXPERT,
        metrics=(
            _metric(
                "24 h mean",
                _value(analysis, "mean_24h", 2, " CPM"),
                key="statistics-mean",
                note_parts=(
                    _message("statistics-24h-coverage", coverage_24h_key, values=coverage_24h_values, level=AnalysisLevel.EXPERT),
                    _uncertainty_message(analysis, "counting_uncertainty_24h", key="statistics-24h-uncertainty"),
                ),
                level=AnalysisLevel.EXPERT,
            ),
            _metric("24 h standard deviation", _value(analysis, "sd_24h", 2, " CPM"), note_key="Sample standard deviation", level=AnalysisLevel.EXPERT),
            _metric("24 h median", _value(analysis, "median_24h", 2, " CPM"), note_key="50th percentile", level=AnalysisLevel.EXPERT),
            _metric("24 h P95", _value(analysis, "p95_24h", 2, " CPM"), note_key="95th percentile", level=AnalysisLevel.EXPERT),
            _metric("24 h P99", _value(analysis, "p99_24h", 2, " CPM"), note_key="99th percentile", level=AnalysisLevel.EXPERT),
            _metric("24 h minimum", _value(analysis, "min_24h", 2, " CPM"), note_key="Lowest stored 24 h value", level=AnalysisLevel.EXPERT),
            _metric("24 h maximum", _value(analysis, "max_24h", 2, " CPM"), note_key="Highest stored 24 h value", level=AnalysisLevel.EXPERT),
            _metric("24 h Z-score", _value(analysis, "z_score_24h", 2), note_key="Latest CPM vs 24 h distribution", interpretation_key=z_text, status=z_status, level=AnalysisLevel.EXPERT),
        ),
    )

    fano_text, fano_status = _fano_interpretation(analysis)
    poisson_text, poisson_status = _poisson_interpretation(analysis)
    counting = AnalysisSection(
        key="counting-statistics",
        title_key="Counting statistics",
        subtitle_key="How closely the observed spread resembles Poisson-like counting",
        level=AnalysisLevel.EXPERT,
        metrics=(
            _metric("Latest CPM uncertainty", _uncertainty_text(analysis, "counting_uncertainty_latest"), note_key="Poisson counting interval from the observed impulse count", level=AnalysisLevel.EXPERT),
            _metric("1 h counting uncertainty", _uncertainty_text(analysis, "counting_uncertainty_1h"), note_key="Gaps are excluded from effective counting time", level=AnalysisLevel.EXPERT),
            _metric("24 h counting uncertainty", _uncertainty_text(analysis, "counting_uncertainty_24h"), note_key="Gaps are excluded from effective counting time", level=AnalysisLevel.EXPERT),
            _metric("7 d counting uncertainty", _uncertainty_text(analysis, "counting_uncertainty_7d"), note_key="Gaps are excluded from effective counting time", level=AnalysisLevel.EXPERT),
            _metric("24 h Fano factor", _value(analysis, "fano_factor_24h", 3), note_key="Variance / mean", interpretation_key=fano_text, status=fano_status, level=AnalysisLevel.EXPERT),
            _metric("Poisson SD ratio", _value(analysis, "poisson_sd_ratio_24h", 3), note_key="Observed SD / √mean", interpretation_key=poisson_text, status=poisson_status, level=AnalysisLevel.EXPERT),
        ),
        messages=(
            _message("counting-shape", "These values describe the shape of the count distribution. They do not by themselves prove a physical cause or a calibration state.", level=AnalysisLevel.EXPERT),
            _message("counting-cause", "Spread above the Poisson expectation can be caused by environmental changes, device instability or changing interference; the metric does not identify which cause applies.", level=AnalysisLevel.EXPERT),
        ),
        explanation_code="counting_statistics",
    )

    temp_value, temp_note, temp_values, temp_interpretation = _correlation_details(analysis, "temperature")
    voltage_value, voltage_note, voltage_values, voltage_interpretation = _correlation_details(analysis, "voltage")
    temperature_rows = tuple(
        {
            "temperature": f"{float(item['lower_c']):.1f}–{float(item['upper_c']):.1f} °C",
            "samples": str(int(item["samples"])),
            "mean": f"{float(item['mean_cpm']):.2f} CPM",
            "median": f"{float(item['median_cpm']):.2f} CPM",
        }
        for item in analysis.get("temperature_bins_24h", [])
    )
    environment = AnalysisSection(
        key="environment",
        title_key="Environment",
        subtitle_key="Temperature and voltage relationships",
        level=AnalysisLevel.EXPERT,
        metrics=(
            _metric("CPM–temperature correlation", temp_value, note_key=temp_note, note_values=temp_values, interpretation_key=temp_interpretation, level=AnalysisLevel.EXPERT),
            _metric("CPM–voltage correlation", voltage_value, note_key=voltage_note, note_values=voltage_values, interpretation_key=voltage_interpretation, level=AnalysisLevel.EXPERT),
        ),
        tables=(
            AnalysisTable(
                key="temperature-bins-24h",
                title_key="Temperature bins (24 h)",
                columns=(
                    AnalysisTableColumn("temperature", "Temperature"),
                    AnalysisTableColumn("samples", "Samples"),
                    AnalysisTableColumn("mean", "Mean"),
                    AnalysisTableColumn("median", "Median"),
                ),
                rows=temperature_rows,
                level=AnalysisLevel.EXPERT,
                empty_key="Not available yet — no temperature samples were stored in the current 24 h window.",
            ),
        ),
        messages=(
            _message("correlation-caution", "Correlation does not imply causation. Strong values should be investigated over longer periods before drawing conclusions.", level=AnalysisLevel.EXPERT),
        ),
    )

    drift_text, drift_status = _drift_interpretation(analysis)
    level_shift = analysis.get("level_shift") or {}
    level_state = str(level_shift.get("state") or "Insufficient history for level-shift detection")
    if level_shift.get("available"):
        level_value = f"{float(level_shift.get('change_percent') or 0.0):+.1f}%"
        level_note = "{before:.2f} → {after:.2f} CPM · {sigma:.1f}σ · {hours} h persistent"
        level_values = {
            "before": float(level_shift.get("before_cpm") or 0.0),
            "after": float(level_shift.get("after_cpm") or 0.0),
            "sigma": float(level_shift.get("significance_sigma") or 0.0),
            "hours": int(level_shift.get("post_hours") or 0),
        }
        level_status = AnalysisStatus.NOTICE if level_shift.get("detected") else AnalysisStatus.GOOD
    else:
        level_value = "—"
        level_note = "At least 24 h reference and 6 h persistence are required"
        level_values = {}
        level_status = AnalysisStatus.NEUTRAL
    long_term = AnalysisSection(
        key="long-term-context",
        title_key="Long-term context",
        subtitle_key="Baseline deviation, drift and sustained relative events",
        level=AnalysisLevel.EXPERT,
        metrics=(
            _metric("7 d baseline", _value(analysis, "mean_7d", 2, " CPM"), key="long-term-baseline", note_key=coverage_7d_key, note_values=coverage_7d_values, level=AnalysisLevel.EXPERT),
            _metric("Baseline deviation", _signed_value(analysis, "baseline_deviation_cpm", 2, " CPM"), key="long-term-deviation-cpm", note_key="1 h mean minus 7 d baseline", level=AnalysisLevel.EXPERT),
            _metric("Baseline deviation", _signed_value(analysis, "baseline_deviation_percent", 1, "%"), key="long-term-deviation-percent", note_key="Relative to 7 d baseline", level=AnalysisLevel.EXPERT),
            _metric("7 d baseline drift", _signed_value(analysis, "baseline_drift_percent", 1, "%"), key="long-term-drift", note_key="Second half vs first half of available 7 d window", interpretation_key=drift_text, status=drift_status, level=AnalysisLevel.EXPERT),
            _metric("Statistical level shift", level_value, key="long-term-level-shift", note_key=level_note, note_values=level_values, interpretation_key=level_state, status=level_status, level=AnalysisLevel.EXPERT),
            _metric("Events last 24 h", _value(analysis, "events_24h", 0), key="long-term-events", note_key="Sustained relative anomaly events", level=AnalysisLevel.EXPERT),
            _metric("Background index", _value(analysis, "background_index_percent", 1, "%"), key="long-term-background-index", note_key="1 h mean / 7 d mean × 100", level=AnalysisLevel.EXPERT),
        ),
        messages=(
            _message("level-shift-caution", "The level-shift detector looks for persistent statistical changes and does not alter radiation warnings.", level=AnalysisLevel.EXPERT),
        ),
    )

    diagnostics = AnalysisSection(
        key="advanced-diagnostics",
        title_key="Advanced diagnostics",
        subtitle_key="Coverage, gaps, runtime counters and derived dose-rate values",
        level=AnalysisLevel.EXPERT,
        metrics=(
            _metric(
                "Data quality",
                quality_label,
                value_key=quality_label,
                key="diagnostics-quality",
                note_key="score {score:.1f}/100 · coverage {coverage:.1f}% · longest gap {gap} s",
                note_values={
                    "score": float(analysis.get("data_quality_score_24h") or 0.0),
                    "coverage": float(analysis.get("coverage_24h_percent") or 0.0),
                    "gap": int(analysis.get("longest_gap_24h_seconds") or 0),
                },
                interpretation_key=_quality_interpretation_key(quality_label),
                status=quality_status,
                level=AnalysisLevel.EXPERT,
            ),
            _metric(
                "Raw-data archive",
                str(int(analysis.get("raw_archive_samples_24h") or 0)),
                note_key="Confirmed original samples in 24 h · {accepted} stored",
                note_values={"accepted": int(analysis.get("raw_archive_accepted_24h") or 0)},
                interpretation_key="Accepted device values are stored separately after live CPM plausibility confirmation",
                status=AnalysisStatus.GOOD if analysis.get("raw_archive_available") else AnalysisStatus.NEUTRAL,
                level=AnalysisLevel.EXPERT,
            ),
            _metric("Timestamp diagnostics", f"{analysis.get('duplicate_timestamps_24h', 0)} / {analysis.get('clock_regressions_since_start', 0)}", note_key="duplicates / clock regressions", level=AnalysisLevel.EXPERT),
            _metric("Interval diagnostics", f"{analysis.get('short_intervals_24h', 0)} / {analysis.get('long_intervals_24h', 0)}", note_key="short / long intervals", level=AnalysisLevel.EXPERT),
            _metric("Serial errors / reconnects", f"{analysis.get('serial_error_count_since_start', 0)} / {analysis.get('serial_reconnect_count_since_start', 0)}", note_key="Since app start", level=AnalysisLevel.EXPERT),
            _metric("Temperature / voltage errors", f"{analysis.get('temperature_error_count_since_start', 0)} / {analysis.get('voltage_error_count_since_start', 0)}", note_key="Since app start", level=AnalysisLevel.EXPERT),
            _metric("Gyro errors", str(analysis.get("gyro_error_count_since_start", 0)), note_key="Since app start", level=AnalysisLevel.EXPERT),
            _metric("24 h mean dose rate", _dose_value(analysis, "mean_24h", config), note_key="Derived from 24 h mean CPM", level=AnalysisLevel.EXPERT),
            _metric("7 d baseline dose rate", _dose_value(analysis, "mean_7d", config), note_key="Derived from 7 d mean CPM", level=AnalysisLevel.EXPERT),
        ),
        messages=(*tuple(_quality_reason_message(str(reason), index) for index, reason in enumerate(analysis.get("data_quality_reasons_24h", []))), _message("formula-z", "Z-score = (latest CPM − 24 h mean) / 24 h standard deviation.", level=AnalysisLevel.EXPERT), _message("formula-fano", "Fano factor = variance / mean; a value near 1 is consistent with Poisson-like counting statistics.", level=AnalysisLevel.EXPERT), _message("formula-poisson", "Poisson SD ratio = observed standard deviation / √mean; a value near 1 indicates Poisson-like spread.", level=AnalysisLevel.EXPERT), _message("formula-background", "Background index compares the rolling 1 h mean with the available 7 d baseline.", level=AnalysisLevel.EXPERT), _message("formula-hysteresis", "Radiation traffic light uses hysteresis: it enters yellow at {yellow_enter:g}% and clears below {yellow_clear:g}%; it enters red at {red_enter:g}% and clears below {red_clear:g}%.", values={"yellow_enter": config.traffic_light_yellow_percent, "yellow_clear": max(100.0, config.traffic_light_yellow_percent - 10.0), "red_enter": config.traffic_light_red_percent, "red_clear": max(config.traffic_light_yellow_percent, config.traffic_light_red_percent - 15.0)}, level=AnalysisLevel.EXPERT), _message("formula-dose", "Dose rate = CPM / configured conversion factor ({factor:g} CPM per µSv/h).", values={"factor": _analysis_cpm_per_usvh(analysis, config)}, level=AnalysisLevel.EXPERT), _message("diagnostic-context", "Rolling windows end at the latest stored measurement. Dose-rate values are derived from CPM using the configured factor and are not independently measured. CPM remains the primary measurement. The traffic light is a relative background-anomaly indicator, not an emergency, health, or radiation-safety classification.", level=AnalysisLevel.EXPERT)),
        explanation_code="data_quality",
    )

    baseline_color, _, _ = baseline_state(analysis, config=config)
    status_summary = AnalysisSection(
        key="status-summary",
        title_key="",
        level=AnalysisLevel.SUMMARY,
        metrics=(
            _metric(
                "1 h mean",
                _value(analysis, "mean_1h", 2, " CPM"),
                key="status-mean-1h",
                level=AnalysisLevel.SUMMARY,
                note_parts=(
                    _message("status-1h-coverage", coverage_1h_key, values=coverage_1h_values, level=AnalysisLevel.SUMMARY),
                    _uncertainty_message(analysis, "counting_uncertainty_1h", key="status-1h-uncertainty"),
                ),
            ),
            _metric(
                "7 d baseline",
                _value(analysis, "mean_7d", 2, " CPM"),
                key="status-mean-7d",
                level=AnalysisLevel.SUMMARY,
                note_parts=(
                    _message("status-7d-coverage", coverage_7d_key, values=coverage_7d_values, level=AnalysisLevel.SUMMARY),
                    _uncertainty_message(analysis, "counting_uncertainty_7d", key="status-7d-uncertainty"),
                ),
            ),
            _metric(
                "Baseline deviation",
                _signed_value(analysis, "baseline_deviation_percent", 1, "%"),
                key="status-deviation",
                level=AnalysisLevel.SUMMARY,
                note_key="{value} vs local baseline",
                note_values={"value": _signed_value(analysis, "baseline_deviation_cpm", 2, " CPM")},
                status=_state_status(baseline_color),
            ),
            _metric(
                "Data quality",
                quality_label,
                value_key=quality_label,
                key="status-quality",
                level=AnalysisLevel.SUMMARY,
                interpretation_key=_quality_interpretation_key(quality_label),
                status=quality_status,
            ),
        ),
    )

    return AnalysisResult(
        key="device_analysis",
        status=primary.status,
        headline_key=primary.headline_key,
        summary_key=primary.summary_key,
        primary_value=primary.primary_value,
        confidence=primary.confidence,
        metrics=primary.metrics,
        explanation_code=primary.explanation_code,
        action_code=primary.action_code,
        values=primary.values,
        sections=(status_summary, overview, statistics, counting, environment, long_term, diagnostics),
    )


def effective_safety_thresholds(
    config: AnalysisPresentationConfig, *, cpm_per_usvh: float | None = None
) -> dict[str, Any]:
    factor = cpm_per_usvh or config.cpm_per_usvh
    if config.safety_profile == "gq":
        return {
            "profile": "gq",
            "basis": "either",
            "warning_cpm": 51,
            "danger_cpm": 100,
            "warning_usvh": 0.326,
            "danger_usvh": 0.651,
            "label": "GQ GMC-500+ manufacturer bands",
            "reference": "Manufacturer display guidance; not an official regulatory limit.",
        }
    if config.safety_profile in {"bfs_reference", "icrp_reference"}:
        source = "German Strahlenschutz reference" if config.safety_profile == "bfs_reference" else "ICRP reference"
        return {
            "profile": config.safety_profile,
            "basis": "dose_rate",
            "warning_cpm": round(0.114 * factor),
            "danger_cpm": round(2.283 * factor),
            "warning_usvh": 0.114,
            "danger_usvh": 2.283,
            "label": source + " (annualised projection)",
            "reference": (
                "0.114 µSv/h and 2.283 µSv/h are mathematical continuous-rate equivalents of "
                "1 mSv/year and 20 mSv/year. They are context only, include no background subtraction, "
                "and are not official instantaneous alarm thresholds."
            ),
        }
    return {
        "profile": "custom",
        "basis": config.safety_threshold_basis,
        "warning_cpm": config.safety_warning_cpm,
        "danger_cpm": config.safety_danger_cpm,
        "warning_usvh": config.safety_warning_usvh,
        "danger_usvh": config.safety_danger_usvh,
        "label": "Custom thresholds",
        "reference": "User-defined values; verify them for the detector tube, calibration and intended use.",
    }


def safety_state(
    analysis: Mapping[str, Any], *, config: AnalysisPresentationConfig
) -> tuple[str, dict[str, Any], float, float]:
    raw_cpm = analysis.get("latest_cpm")
    factor = _analysis_cpm_per_usvh(analysis, config)
    effective = effective_safety_thresholds(config, cpm_per_usvh=factor)
    if raw_cpm is None:
        return "blue", effective, 0.0, 0.0
    cpm = float(raw_cpm)
    dose = cpm / factor
    cpm_state = "red" if cpm >= effective["danger_cpm"] else "yellow" if cpm >= effective["warning_cpm"] else "green"
    dose_state = "red" if dose >= effective["danger_usvh"] else "yellow" if dose >= effective["warning_usvh"] else "green"
    if effective["basis"] == "cpm":
        state = cpm_state
    elif effective["basis"] == "dose_rate":
        state = dose_state
    else:
        state = "red" if "red" in {cpm_state, dose_state} else "yellow" if "yellow" in {cpm_state, dose_state} else "green"
    return state, effective, cpm, dose


def baseline_state(
    analysis: Mapping[str, Any], *, config: AnalysisPresentationConfig
) -> tuple[str, float | None, float]:
    background_index = analysis.get("background_index_percent")
    samples_7d = int(analysis.get("samples_7d", 0))
    coverage_1h = float(analysis.get("coverage_1h_percent", 0.0))
    minimum_baseline_samples = int(
        analysis.get("baseline_minimum_samples")
        or max(6, round(21600 / _analysis_scan_interval(analysis, config)))
    )
    baseline_ready = bool(analysis.get("baseline_ready", samples_7d >= minimum_baseline_samples))
    recent_window_ready = bool(analysis.get("recent_window_ready", coverage_1h >= 50.0))
    readiness = float(
        analysis.get(
            "baseline_readiness_percent",
            min(100.0, 100.0 * samples_7d / minimum_baseline_samples),
        )
    )
    if not baseline_ready:
        return "blue", None, readiness
    if background_index is None or not recent_window_ready:
        return "blue", None, 100.0
    index = float(background_index)
    if index >= config.traffic_light_red_percent:
        return "red", index, 100.0
    orange_threshold = max(config.traffic_light_yellow_percent + 25.0, config.traffic_light_red_percent - 25.0)
    if index >= orange_threshold:
        return "orange", index, 100.0
    if index >= config.traffic_light_yellow_percent:
        return "yellow", index, 100.0
    return "green", index, 100.0


def _state_status(state: str) -> AnalysisStatus:
    return {
        "green": AnalysisStatus.GOOD,
        "yellow": AnalysisStatus.NOTICE,
        "orange": AnalysisStatus.WARNING,
        "red": AnalysisStatus.ERROR,
        "blue": AnalysisStatus.LEARNING,
    }.get(state, AnalysisStatus.NEUTRAL)


def build_absolute_safety_result(
    analysis: dict[str, Any], *, config: AnalysisPresentationConfig
) -> AnalysisResult:
    state, effective, cpm, dose = safety_state(analysis, config=config)
    if analysis.get("latest_cpm") is None:
        headline = "No measurement yet"
        summary = "The absolute assessment starts after the first measurement."
    else:
        headline = {"green": "Uncritical", "yellow": "Elevated", "red": "Critical"}[state]
        summary = {"green": "Below warning threshold", "yellow": "Within warning range", "red": "Danger threshold exceeded"}[state]
    basis_key = {"cpm": "CPM", "dose_rate": "Derived dose rate", "either": "CPM and derived dose rate"}[effective["basis"]]
    profile_key = {
        "gq": "GQ manufacturer recommendation",
        "bfs_reference": "BfS reference projection",
        "icrp_reference": "ICRP reference projection",
        "custom": "Custom thresholds",
    }.get(effective["profile"], effective["label"])
    return AnalysisResult(
        key="absolute_safety",
        status=_state_status(state),
        headline_key=headline,
        summary_key=summary,
        primary_value=f"{cpm:.0f} CPM · {dose:.3f} µSv/h",
        metrics=(
            _metric("Active threshold profile", profile_key, value_key=profile_key, key="safety-profile", level=AnalysisLevel.SUMMARY),
            _metric("Warning thresholds", f"{effective['warning_cpm']:g} CPM", key="safety-warning", note_key="{value:g} µSv/h", note_values={"value": effective["warning_usvh"]}, level=AnalysisLevel.SUMMARY),
            _metric("Danger thresholds", f"{effective['danger_cpm']:g} CPM", key="safety-danger", note_key="{value:g} µSv/h", note_values={"value": effective["danger_usvh"]}, level=AnalysisLevel.SUMMARY),
        ),
        messages=(
            _message("safety-meaning", "This classification only compares the current measurement with the selected thresholds. It does not compare the value with the usual background at this location.", level=AnalysisLevel.SUMMARY),
        ),
        metadata={
            "state_color": state,
            "icon": "🛡️",
            "title_key": "Absolute radiation assessment",
            "subtitle_key": "Evaluates the current value using the configured thresholds.",
            "basis_key": basis_key,
            "profile_key": profile_key,
            "effective": effective,
        },
    )


def build_local_background_result(
    analysis: dict[str, Any], *, config: AnalysisPresentationConfig
) -> AnalysisResult:
    state, _, readiness = baseline_state(analysis, config=config)
    latest = float(analysis.get("latest_cpm") or 0.0)
    baseline = analysis.get("mean_7d")
    deviation = analysis.get("baseline_deviation_percent")
    trend = float(analysis.get("trend_30m_cpm") or 0.0)
    trend_key = "Rising" if trend > 1 else "Falling" if trend < -1 else "Stable"
    baseline_ready = bool(analysis.get("baseline_ready", False))
    if state == "blue" and baseline_ready:
        headline, summary = "Baseline available", "Waiting for enough recent measurements"
    elif state == "blue":
        headline, summary = "Learning baseline", "Not enough local history yet"
    elif state == "green":
        headline, summary = "Normal", "Within the usual local range"
    elif state == "yellow":
        headline, summary = "Noticeable", "Above the usual local range"
    elif state == "orange":
        headline, summary = "Clearly elevated", "Clearly above the usual local range"
    else:
        headline, summary = "Extremely elevated", "Far above the usual local range"
    baseline_text = "—" if baseline is None else f"{float(baseline):.1f} CPM"
    deviation_text = "—" if deviation is None else f"{float(deviation):+.0f}%"
    collected_seconds = int(analysis.get("samples_7d", 0)) * _analysis_scan_interval(analysis, config)
    return AnalysisResult(
        key="local_background",
        status=_state_status(state),
        headline_key=headline,
        summary_key=summary,
        primary_value=deviation_text,
        metrics=(
            _metric("Local baseline", baseline_text, key="background-local-baseline", note_key="Learned from local history", level=AnalysisLevel.SUMMARY),
            _metric("Current value", f"{latest:.0f} CPM", key="background-current", note_key="{dose:.3f} µSv/h", note_values={"dose": latest / _analysis_cpm_per_usvh(analysis, config)}, level=AnalysisLevel.SUMMARY),
            _metric("Deviation", deviation_text, key="background-deviation", note_key="Compared with local baseline", level=AnalysisLevel.SUMMARY),
            _metric("Trend (30 min)", trend_key, value_key=trend_key, key="background-trend", note_key="{trend:+.1f} CPM", note_values={"trend": trend}, level=AnalysisLevel.SUMMARY),
        ),
        messages=(
            _message("background-meaning", "This analysis detects unusual changes compared with the normal background at this location. It is not a danger classification; an unusual value can still be below the absolute warning threshold.", level=AnalysisLevel.SUMMARY),
        ),
        metadata={
            "state_color": state,
            "data_state": "learning" if state == "blue" else state,
            "icon": "📈",
            "title_key": "Local background analysis",
            "subtitle_key": "Compares the current value with the usual background at this location.",
            "readiness": readiness,
            "baseline_ready": baseline_ready,
            "collected_hours": collected_seconds // 3600,
            "collected_minutes": (collected_seconds % 3600) // 60,
            "coverage_1h_percent": float(analysis.get("coverage_1h_percent") or 0.0),
        },
    )


def build_combined_interpretation_result(
    analysis: dict[str, Any], *, config: AnalysisPresentationConfig
) -> AnalysisResult:
    safety, _, _, _ = safety_state(analysis, config=config)
    background, _, _ = baseline_state(analysis, config=config)
    if safety == "red":
        first = "The configured danger threshold is exceeded."
    elif safety == "yellow":
        first = "The current value is within the configured warning range."
    else:
        first = "The current radiation level is uncritical according to the selected thresholds."
    if background == "blue" and bool(analysis.get("baseline_ready", False)):
        second = "The device baseline is available, but there are not enough recent measurements for a current comparison."
    elif background == "blue":
        second = "The local background is still being learned, so no anomaly assessment is available yet."
    elif background == "green":
        second = "The value is also within the usual range for this location."
    elif background == "yellow":
        second = "However, the value is noticeably above the usual local background. Observe the trend."
    else:
        second = "At the same time, the value is clearly above the usual local background. Review the trend and measurement conditions."
    return AnalysisResult(
        key="combined_interpretation",
        status=max_status(_state_status(safety), _state_status(background)),
        headline_key="Interpretation",
        summary_key="{first} {second}",
        values={"first": first, "second": second},
        messages=(
            _message("combined-first", first),
            _message("combined-second", second),
        ),
        metadata={"icon": "💡"},
    )


def build_recommendation_result(
    analysis: dict[str, Any], *, config: AnalysisPresentationConfig
) -> AnalysisResult:
    safety, _, _, _ = safety_state(analysis, config=config)
    background, _, _ = baseline_state(analysis, config=config)
    trend = float(analysis.get("trend_30m_cpm") or 0.0)
    if safety == "red":
        state, icon = AnalysisStatus.ERROR, "🚨"
        headline = "Danger threshold exceeded"
        detail = "Move away from the suspected source if safe to do so, avoid unnecessary exposure and seek qualified radiation-protection advice."
    elif safety == "yellow":
        state, icon = AnalysisStatus.WARNING, "⚠️"
        headline = "Warning threshold exceeded"
        detail = "Check the measurement conditions, observe the trend and verify the reading with an appropriate instrument if it persists."
    elif background in {"red", "orange"}:
        state, icon = AnalysisStatus.WARNING, "🔎"
        headline = "Check the measurement location"
        detail = "The absolute level is below the configured warning threshold, but the value is far above the learned local background."
    elif background == "yellow" or trend > 1:
        state, icon = AnalysisStatus.NOTICE, "👁️"
        headline = "Continue observing"
        detail = "The absolute level is currently uncritical, but the local comparison or short-term trend deserves continued observation."
    elif background == "blue" and bool(analysis.get("baseline_ready", False)):
        state, icon = AnalysisStatus.LEARNING, "⏱️"
        headline = "Waiting for recent measurements"
        detail = "The learned baseline remains available. More current samples are required before the local comparison can be updated."
    elif background == "blue":
        state, icon = AnalysisStatus.LEARNING, "⏳"
        headline = "Baseline learning in progress"
        detail = "The absolute level is currently uncritical. More local history is required before anomaly detection becomes reliable."
    else:
        state, icon = AnalysisStatus.GOOD, "✓"
        headline = "No action required"
        detail = "The current value is below the configured warning threshold and within the usual local range."
    return AnalysisResult(
        key="recommendation",
        status=state,
        headline_key=headline,
        summary_key=detail,
        metadata={"icon": icon, "title_key": "Recommendation"},
    )


def max_status(*statuses: AnalysisStatus) -> AnalysisStatus:
    order = {
        AnalysisStatus.UNAVAILABLE: 0,
        AnalysisStatus.NEUTRAL: 1,
        AnalysisStatus.GOOD: 2,
        AnalysisStatus.LEARNING: 3,
        AnalysisStatus.NOTICE: 4,
        AnalysisStatus.WARNING: 5,
        AnalysisStatus.ERROR: 6,
    }
    return max(statuses, key=lambda item: order[item]) if statuses else AnalysisStatus.NEUTRAL


def build_radiation_intelligence_result(
    result: dict[str, Any], *, collected: int = 0, needed: int = 0
) -> AnalysisResult:
    if not result.get("available"):
        progress_key = (
            "Waiting for the first accepted measurement"
            if collected <= 0
            else "More history is needed; approximately {count} additional measurements are required."
        )
        progress_values = {} if collected <= 0 else {"count": needed}
        return AnalysisResult(
            key="radiation_intelligence",
            status=AnalysisStatus.LEARNING,
            headline_key="Analysis is still being prepared",
            summary_key=progress_key,
            values=progress_values,
            explanation_code="radiation_intelligence",
            metadata={"title_key": "Intelligent radiation analysis", "icon": "⏳"},
        )
    probability = float(result.get("probability_percent") or 0.0)
    if probability < 20:
        status = AnalysisStatus.GOOD
    elif probability < 50:
        status = AnalysisStatus.NOTICE
    elif probability < 75:
        status = AnalysisStatus.WARNING
    else:
        status = AnalysisStatus.ERROR
    confidence = str(result.get("confidence") or "Low")
    confidence_value = {"Low": 0.33, "Medium": 0.66, "High": 1.0}.get(confidence)
    reasons = tuple(
        _message(
            f"radiation-reason-{index}",
            str(reason.get("key") or "") if isinstance(reason, dict) else str(reason),
            values=dict(reason.get("params") or {}) if isinstance(reason, dict) else {},
            level=AnalysisLevel.ANALYSIS,
        )
        for index, reason in enumerate(result.get("reasons") or [])
    )
    return AnalysisResult(
        key="radiation_intelligence",
        status=status,
        headline_key=str(result.get("state") or "No data"),
        summary_key="{probability:.0f}% estimated signal probability",
        values={"probability": probability},
        primary_value=f"{probability:.0f}%",
        confidence=confidence_value,
        metrics=(
            _metric("Confidence", confidence, value_key=confidence, key="radiation-confidence", status=status, level=AnalysisLevel.SUMMARY),
        ),
        messages=(*reasons, _message("radiation-disclaimer", str(result.get("disclaimer") or "Heuristic statistical assessment; not a radiation-protection classification."), level=AnalysisLevel.EXPERT)),
        explanation_code="radiation_intelligence",
        metadata={"title_key": "Intelligent radiation analysis", "classification": result.get("classification")},
    )


def build_background_profile_entity(
    profile: Mapping[str, Any], *, key: str, title: str
) -> AnalysisEntity:
    """Build the shared presentation model for one adaptive background profile."""
    if not profile.get("available"):
        return AnalysisEntity(
            key=key,
            title=title,
            status=AnalysisStatus.UNAVAILABLE,
            messages=(_message(f"{key}-empty", "No measurement yet"),),
        )
    typical = profile.get("typical_cpm")
    deviation = profile.get("deviation_percent")
    if typical is None:
        status = AnalysisStatus.LEARNING
        headline = "Daily and weekly profile is still being formed"
        detail = "More measurements are needed for this weekday and hour."
        detail_values: dict[str, Any] = {}
    else:
        state = str(profile.get("state") or "Normal")
        status = {
            "Normal": AnalysisStatus.GOOD,
            "Noticeable": AnalysisStatus.NOTICE,
            "Clearly elevated": AnalysisStatus.WARNING,
            "Extremely elevated": AnalysisStatus.ERROR,
        }.get(state, AnalysisStatus.GOOD)
        headline = state
        weekday_names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        detail = "Typical for {weekday} at {hour}:00"
        detail_values = {
            "weekday": weekday_names[int(profile.get("weekday") or 0)],
            "hour": int(profile.get("hour") or 0),
        }
    excluded = int(profile.get("excluded_sample_count") or profile.get("fusion_rejected_samples") or 0)
    metrics: list[AnalysisMetric] = [
        _metric("Current", f"{float(profile.get('current_cpm') or 0.0):.1f} CPM", key=f"{key}-current", status=status)
    ]
    if typical is not None:
        metrics.append(
            _metric(
                "Typical background",
                f"{float(typical):.1f} CPM · {float(deviation or 0.0):+.1f}%",
                key=f"{key}-typical",
                status=status,
                level=AnalysisLevel.SUMMARY,
            )
        )
    if profile.get("confidence"):
        confidence = str(profile.get("confidence"))
        metrics.append(_metric("Confidence", confidence, value_key=confidence, key=f"{key}-confidence", status=status))
    if excluded:
        metrics.append(_metric("Excluded measurements", str(excluded), key=f"{key}-excluded", level=AnalysisLevel.EXPERT))
    if profile.get("paired_samples") is not None:
        metrics.append(_metric("Valid paired samples", str(int(profile.get("paired_samples") or 0)), key=f"{key}-pairs", level=AnalysisLevel.EXPERT))
    return AnalysisEntity(
        key=key,
        title=title,
        status=status,
        primary_value=None if typical is None else f"{float(typical):.1f} CPM",
        metrics=tuple(metrics),
        messages=(
            _message(f"{key}-headline", headline, level=AnalysisLevel.SUMMARY, status=status),
            _message(f"{key}-detail", detail, values=detail_values, level=AnalysisLevel.SUMMARY),
        ),
        level=AnalysisLevel.SUMMARY,
    )


def _trend_symbol(value: float | None) -> str:
    if value is None:
        return "—"
    if value > 1.0:
        return "↗"
    if value < -1.0:
        return "↘"
    return "→"


def build_historical_section(profile: Mapping[str, Any]) -> AnalysisSection:
    history = profile.get("historical_development") or {}
    drift = profile.get("drift") or {}
    trend_metrics = tuple(
        _metric(
            "{days} days",
            "—" if (value := (drift.get(str(period.days), {}) or {}).get("change_percent")) is None else f"{_trend_symbol(float(value))} {float(value):+.1f}%",
            key=f"historical-{period.key}",
            note_key="Recent period compared with the preceding period",
            note_values={"days": period.days},
            level=AnalysisLevel.ANALYSIS,
        )
        for period in HISTORY_PERIODS
    )
    environmental: list[AnalysisMetric] = []
    for key, label, unit, item in (
        ("temperature-trend", "Temperature trend", "°C", history.get("temperature_trend") or {}),
        ("pressure-trend", "Air-pressure trend", "hPa", history.get("pressure_trend") or {}),
    ):
        change = item.get("change")
        shown = "—" if change is None else f"{_trend_symbol(float(change))} {float(change):+.1f} {unit}"
        note_key = "Insufficient paired daily values" if change is None else "Recent 30 days compared with the preceding 30 days"
        environmental.append(
            _metric(
                label,
                shown,
                key=key,
                note_key="{note} · n={samples}",
                note_values={"note": note_key, "samples": int(item.get("samples") or 0)},
                level=AnalysisLevel.EXPERT,
            )
        )
    jump_count = int(history.get("jump_count") or 0)
    environmental.append(
        _metric(
            "Detected baseline jumps",
            str(jump_count),
            key="baseline-jumps",
            note_key="{span:.0f} {days_label} · {count} {daily_label}",
            note_values={
                "span": float(history.get("span_days") or 0.0),
                "days_label": "days",
                "count": int(history.get("daily_points") or 0),
                "daily_label": "daily values",
            },
            level=AnalysisLevel.EXPERT,
        )
    )
    jump_messages = tuple(
        _message(
            f"baseline-jump-{index}",
            "{date}: {from_cpm:.1f} → {to_cpm:.1f} CPM ({change_percent:+.1f}%)",
            values={
                "date": str(item.get("date") or ""),
                "from_cpm": float(item.get("from_cpm") or 0.0),
                "to_cpm": float(item.get("to_cpm") or 0.0),
                "change_percent": float(item.get("change_percent") or 0.0),
            },
            level=AnalysisLevel.EXPERT,
            status=AnalysisStatus.NOTICE,
        )
        for index, item in enumerate(history.get("jumps") or [])
    )
    if jump_messages:
        jump_messages += (
            _message("jump-cause-caution", "These are statistical changes. They can indicate a location, geometry or environmental change, but do not identify the cause.", level=AnalysisLevel.EXPERT),
        )
    else:
        jump_messages = (_message("no-baseline-jumps", "No pronounced baseline jumps detected.", level=AnalysisLevel.EXPERT, status=AnalysisStatus.GOOD),)
    return AnalysisSection(
        key="historical-development",
        title_key="Historical development",
        subtitle_key="Background trend over days and months",
        level=AnalysisLevel.ANALYSIS,
        metrics=trend_metrics + tuple(environmental),
        messages=jump_messages,
        explanation_code="historical_development",
        values={
            "points": tuple(dict(point) for point in history.get("points") or []),
            "jump_count": jump_count,
        },
    )


def build_adaptive_background_result(
    device_profile: dict[str, Any], site_profile: dict[str, Any]
) -> AnalysisResult:
    entities = (
        build_background_profile_entity(device_profile, key="device-baseline", title="Device baseline"),
        build_background_profile_entity(site_profile, key="site-baseline", title="Measurement-site baseline"),
    )
    metrics: list[AnalysisMetric] = []
    if device_profile.get("temperature_typical_cpm") is not None:
        start = int(device_profile.get("temperature_bin_start_c") or 0)
        metrics.append(
            _metric(
                "Temperature-specific background",
                f"{float(device_profile['temperature_typical_cpm']):.1f} CPM",
                key="temperature-specific-background",
                note_key="{start}–{end} °C · {samples} Samples",
                note_values={
                    "start": start,
                    "end": start + 2,
                    "samples": int(device_profile.get("temperature_samples") or 0),
                },
            )
        )
    else:
        metrics.append(
            _metric(
                "Temperature-specific background",
                "—",
                key="temperature-specific-background",
                note_key="Temperature profile is still being formed",
                status=AnalysisStatus.LEARNING,
            )
        )
    for period in HISTORY_PERIODS:
        if period.days > 90:
            continue
        item = (device_profile.get("drift") or {}).get(str(period.days), {})
        change = item.get("change_percent")
        shown = "—" if change is None else f"{_trend_symbol(float(change))} {float(change):+.1f}%"
        metrics.append(
            _metric(
                "{days} days",
                shown,
                key=f"quick-drift-{period.days}",
                note_key="Long-term drift",
                note_values={"days": period.days},
            )
        )
    status = max_status(*(entity.status for entity in entities))
    return AnalysisResult(
        key="adaptive_background",
        status=status,
        headline_key="Adaptive background profile",
        summary_key="Learns typical values for the current hour, weekday and temperature range and shows long-term drift.",
        entities=entities,
        sections=(
            AnalysisSection(
                key="adaptive-supporting-values",
                title_key="Adaptive background profile",
                level=AnalysisLevel.ANALYSIS,
                metrics=tuple(metrics),
            ),
            build_historical_section(device_profile),
        ),
        explanation_code="adaptive_background",
        metadata={"title_key": "Adaptive background profile"},
    )


def build_cosmic_influence_result(model: dict[str, Any]) -> AnalysisResult:
    if not model.get("enabled"):
        return AnalysisResult(
            key="cosmic_influence",
            status=AnalysisStatus.UNAVAILABLE,
            headline_key="Pressure model is still being formed",
            summary_key="Compares pressure changes with quality-filtered counts. The result is only a statistical hint and never changes warning thresholds.",
            metadata={"hidden": True, "title_key": "Cosmic influence – statistical indication"},
        )
    snapshot = model.get("pressure_snapshot") or {}
    pressure = model.get("current_pressure_hpa")
    if pressure is None and snapshot.get("available"):
        pressure = snapshot.get("pressure_hpa")
    state = str(model.get("state") or "Pressure model is still being formed")
    status = {
        "Pressure-typical signature is pronounced": AnalysisStatus.NOTICE,
        "Cosmic influence is possible": AnalysisStatus.NOTICE,
        "No pressure-typical signature": AnalysisStatus.GOOD,
        "Pressure model is still being formed": AnalysisStatus.LEARNING,
    }.get(state, AnalysisStatus.LEARNING)
    confidence = str(model.get("confidence") or "Insufficient")
    reasons = tuple(
        _message(
            f"pressure-reason-{index}",
            str(reason.get("key") or "") if isinstance(reason, dict) else str(reason),
            values=dict(reason.get("params") or {}) if isinstance(reason, dict) else {},
        )
        for index, reason in enumerate(model.get("reasons") or [])
    )
    return AnalysisResult(
        key="cosmic_influence",
        status=status,
        headline_key=state,
        summary_key="Confidence: {confidence}",
        values={"confidence": confidence},
        confidence={"Insufficient": 0.0, "Low": 0.33, "Medium": 0.66, "High": 1.0}.get(confidence),
        metrics=(
            _metric("Current air pressure", "—" if pressure is None else f"{float(pressure):.1f} hPa", key="pressure-current"),
            _metric("Estimated pressure influence", "—" if model.get("estimated_pressure_effect_percent") is None else f"{float(model['estimated_pressure_effect_percent']):+.1f}%", key="pressure-effect"),
            _metric("Remaining deviation", "—" if model.get("remaining_deviation_percent") is None else f"{float(model['remaining_deviation_percent']):+.1f}%", key="pressure-remaining"),
            _metric("Learned pressure coefficient", "—" if model.get("pressure_coefficient_percent_per_hpa") is None else f"{float(model['pressure_coefficient_percent_per_hpa']):+.3f} %/hPa", key="pressure-coefficient", level=AnalysisLevel.EXPERT),
            _metric("CPM–pressure correlation", "—" if model.get("correlation") is None else f"{float(model['correlation']):+.2f}", key="pressure-correlation", level=AnalysisLevel.EXPERT),
            _metric("Learning basis", str(int(model.get("hourly_sample_count") or 0)), key="pressure-learning-basis", note_key="valid hourly values · {days:.1f} days · {span:.1f} hPa", note_values={"days": float(model.get("data_span_days") or 0.0), "span": float(model.get("pressure_span_hpa") or 0.0)}, level=AnalysisLevel.EXPERT),
        ),
        messages=(*reasons, _message("pressure-explanation", "Falling air pressure is often associated with a slightly higher intensity of cosmically generated secondary radiation at ground level, while rising air pressure is associated with a slightly lower intensity. The strength of this relationship depends on detector, location and atmosphere; the cause cannot be determined unambiguously from total counts.", level=AnalysisLevel.ANALYSIS), _message("pressure-statistical-only", "The pressure model cannot prove cosmic radiation and never suppresses radiation warnings.", level=AnalysisLevel.EXPERT)),
        explanation_code="cosmic_influence",
        metadata={"title_key": "Cosmic influence – statistical indication"},
    )


def _stability_status(status: str) -> AnalysisStatus:
    return {
        "Stable": AnalysisStatus.GOOD,
        "Slightly noticeable": AnalysisStatus.NOTICE,
        "Unstable": AnalysisStatus.WARNING,
        "Critical": AnalysisStatus.ERROR,
    }.get(status, AnalysisStatus.NEUTRAL)


def fleet_stability_display_key(item: Any) -> tuple[int, str, str]:
    """Return the stable dashboard order for counter stability cards."""
    label = normalize_device_version_display(str(getattr(item, "label", "")))
    compact = label.casefold().replace(" ", "")
    if "320" in compact:
        rank = 0
    elif "500" in compact:
        rank = 1
    else:
        rank = 2
    return rank, label.casefold(), str(getattr(item, "serial", ""))


def build_fleet_intelligence_result(snapshot: dict[str, Any]) -> AnalysisResult:
    stability_items = sorted(
        list(snapshot.get("stability") or []), key=fleet_stability_display_key
    )
    entities: list[AnalysisEntity] = []
    for item in stability_items:
        age = "—" if item.last_sample_age_seconds is None else f"{item.last_sample_age_seconds} s"
        entities.append(
            AnalysisEntity(
                key=f"stability-{item.serial}",
                title=normalize_device_version_display(item.label),
                status=_stability_status(item.status),
                primary_value=f"{item.score:.0f}/100",
                metrics=(
                    _metric("Status", item.status, value_key=item.status, key=f"{item.serial}-status", status=_stability_status(item.status)),
                    _metric("Availability", f"{item.availability_percent:.1f}%", key=f"{item.serial}-availability"),
                    _metric("Largest measurement interval", f"{item.longest_gap_seconds} s", key=f"{item.serial}-gap", note_key="Warning from {warning:g} s; critical from {critical:g} s", note_values={"warning": item.scan_interval_seconds * 1.5, "critical": item.scan_interval_seconds * 2.5}, status=(AnalysisStatus.WARNING if item.gap_status == "Critical" else AnalysisStatus.NOTICE if item.gap_status == "Warning" else AnalysisStatus.NEUTRAL)),
                    _metric("Expected measurement interval", f"{item.scan_interval_seconds} s", key=f"{item.serial}-expected-interval"),
                    _metric("Maximum interval deviation", "—" if item.interval_deviation_seconds is None else f"{item.interval_deviation_seconds:+d} s", key=f"{item.serial}-interval-deviation"),
                    _metric("Reconnects", str(item.reconnects), key=f"{item.serial}-reconnects"),
                    _metric("Last sample age", age, key=f"{item.serial}-age"),
                    _metric("Valid measurements ({hours:g} h)", f"{item.valid_samples} / {item.expected_samples}", key=f"{item.serial}-valid", label_values={"hours": item.analysis_window_seconds / 3600.0}, level=AnalysisLevel.EXPERT),
                    _metric("Total stored measurements", str(item.total_stored_samples), key=f"{item.serial}-stored", level=AnalysisLevel.EXPERT),
                    _metric("Excluded measurements", str(item.excluded_samples), key=f"{item.serial}-excluded", level=AnalysisLevel.EXPERT),
                    _metric("Quality weight", f"{item.quality_weight:.0%}", key=f"{item.serial}-weight", level=AnalysisLevel.EXPERT),
                ),
            )
        )
    comparison = snapshot.get("comparison")
    comparison_metrics: tuple[AnalysisMetric, ...]
    comparison_messages: tuple[AnalysisMessage, ...] = ()
    if comparison:
        correlation = "—" if comparison.get("correlation") is None else f"{float(comparison['correlation']):.2f}"
        current_difference = comparison.get("current_difference")
        current_shown = "—" if current_difference is None else f"{float(current_difference):+.1f} CPM"
        a_hour = comparison.get("a_mean_1h")
        b_hour = comparison.get("b_mean_1h")
        hour_shown = "—" if a_hour is None or b_hour is None else f"{float(a_hour):.1f} / {float(b_hour):.1f}"
        correlation_note = (
            "At least {count} valid pairs are required"
            if comparison.get("correlation") is None
            else "Quality-filtered correlation"
        )
        correlation_values = {"count": int(comparison.get("minimum_pairs_for_correlation", 10))}
        confidence = str(comparison.get("confidence") or "Insufficient")
        comparison_metrics = (
            _metric("Agreement", f"{float(comparison.get('agreement_percent') or 0.0):.1f}%", key="fleet-agreement", note_key="{pairs} valid paired samples", note_values={"pairs": int(comparison.get("pairs") or 0)}, priority=True),
            _metric("Excluded pairs", str(int(comparison.get("excluded_pairs") or 0)), key="fleet-excluded-pairs", note_key="Pair-level disagreement"),
            _metric("Excluded measurements", str(int(comparison.get("excluded_measurements") or 0)), key="fleet-excluded-measurements", note_key="Outliers and invalid measurements"),
            _metric("Comparison confidence", confidence, value_key=confidence, key="fleet-comparison-confidence"),
            _metric("Correlation", correlation, key="fleet-correlation", note_key=correlation_note, note_values=correlation_values),
            _metric("Mean absolute difference", f"{float(comparison.get('mean_difference') or 0.0):.2f} CPM", key="fleet-mean-difference"),
            _metric("Current difference", current_shown, key="fleet-current-difference"),
            _metric("Robust one-hour values", hour_shown, key="fleet-hour-values", note_key="CPM"),
        )
    else:
        comparison_metrics = ()
        comparison_messages = (_message("fleet-comparison-empty", "Connect two devices to enable comparison."),)

    relative = snapshot.get("relative_calibration")
    relative_metrics: tuple[AnalysisMetric, ...] = ()
    relative_messages: tuple[AnalysisMessage, ...]
    if relative and relative.get("available"):
        factor = relative.get("factor_right_to_left")
        spread = relative.get("relative_spread_percent")
        if relative.get("orientation_verified"):
            orientation_key = "Orientation stable" if relative.get("orientation_stable") else "Orientation changes detected"
        else:
            orientation_key = "Orientation cannot be verified automatically"
        learning_key = (
            "Learning: {pairs}/{minimum} pairs · {days:.1f}/{minimum_days:g} days"
            if relative.get("learning")
            else "Long-term relative factor available"
        )
        learning_values = {
            "pairs": int(relative.get("pairs") or 0),
            "minimum": int(relative.get("minimum_pairs") or 0),
            "days": float(relative.get("span_days") or 0.0),
            "minimum_days": float(relative.get("minimum_span_days") or 0.0),
        }
        relative_metrics = (
            _metric("Relative correction factor", "—" if factor is None else f"×{float(factor):.4f}", key="relative-factor", note_key="{b} × factor → {a}", note_values={"b": normalize_device_version_display(str(relative.get("b_label") or "B")), "a": normalize_device_version_display(str(relative.get("a_label") or "A"))}, level=AnalysisLevel.EXPERT),
            _metric("Relative-factor confidence", str(relative.get("confidence") or "Insufficient"), value_key=str(relative.get("confidence") or "Insufficient"), key="relative-confidence", note_key=learning_key, note_values=learning_values, level=AnalysisLevel.EXPERT),
            _metric("Relative spread", "—" if spread is None else f"{float(spread):.1f}%", key="relative-spread", note_key="{pairs} valid paired samples · counting uncertainty {value:.2f}%", note_values={"pairs": int(relative.get("pairs") or 0), "value": float(relative.get("counting_uncertainty_percent") or 0.0)}, level=AnalysisLevel.EXPERT),
            _metric("Orientation qualification", orientation_key, value_key=orientation_key, key="relative-orientation", note_key="Co-location and equal geometry must be ensured by the user", level=AnalysisLevel.EXPERT),
        )
        relative_messages = (_message("relative-caution", "This factor is only a relative device comparison and is not an absolute radiation calibration.", level=AnalysisLevel.EXPERT),)
    else:
        relative_messages = (_message("relative-empty", "Connect two devices to learn a relative response factor.", level=AnalysisLevel.EXPERT),)

    shared = snapshot.get("shared_event")
    if shared and shared.get("active"):
        shared_messages = (
            _message("shared-rise", "Shared CPM rise", status=AnalysisStatus.ERROR),
            _message("shared-rise-values", "{a:+.1f}% / {b:+.1f}%", values={"a": float(shared.get("a_change_percent") or 0.0), "b": float(shared.get("b_change_percent") or 0.0)}, status=AnalysisStatus.ERROR),
            _message("shared-rise-confidence", "Confidence: {confidence}", values={"confidence": str(shared.get("confidence") or "Low")}, status=AnalysisStatus.ERROR),
        )
        shared_status = AnalysisStatus.ERROR
    else:
        shared_messages = (_message("shared-empty", "No shared rise detected.", status=AnalysisStatus.GOOD),)
        shared_status = AnalysisStatus.GOOD

    movement_entities = tuple(
        AnalysisEntity(
            key=f"movement-{index}",
            title=normalize_device_version_display(str(event.get("label") or "")),
            status=AnalysisStatus.NOTICE,
            messages=(
                _message(
                    f"movement-{index}-change",
                    "{from_value} → {to_value}",
                    values={
                        "from_value": str((event.get("details") or {}).get("from", "—")),
                        "to_value": str((event.get("details") or {}).get("to", "—")),
                    },
                    level=AnalysisLevel.EXPERT,
                ),
            ),
            level=AnalysisLevel.EXPERT,
        )
        for index, event in enumerate((snapshot.get("orientation_events") or [])[:6])
    )
    movement_messages = () if movement_entities else (_message("movement-empty", "No position changes recorded.", level=AnalysisLevel.EXPERT),)

    stable_count = sum(1 for item in stability_items if item.status == "Stable")
    agreement = "—" if not comparison else f"{float(comparison.get('agreement_percent') or 0.0):.1f}%"
    confidence = "Insufficient" if not comparison else str(comparison.get("confidence") or "Insufficient")
    overall = max_status(*(_stability_status(item.status) for item in stability_items), shared_status)
    return AnalysisResult(
        key="fleet_intelligence",
        status=overall,
        headline_key="Fleet intelligence",
        summary_key="Compares connected counters, device stability, shared events and the long-term relative response.",
        metrics=(
            _metric("Stable devices", f"{stable_count}/{len(stability_items)}", key="fleet-stable-devices", note_key="Connected counters without an active stability warning", priority=True),
            _metric("Agreement", agreement, key="fleet-summary-agreement", note_key="Comparison confidence: {confidence}", note_values={"confidence": confidence}, priority=True),
        ),
        entities=tuple(entities),
        sections=(
            AnalysisSection("fleet-stability", "Stability and device health", level=AnalysisLevel.ANALYSIS, entities=tuple(entities)),
            AnalysisSection("fleet-comparison", "Device comparison", level=AnalysisLevel.ANALYSIS, metrics=comparison_metrics, messages=comparison_messages),
            AnalysisSection("relative-response", "Long-term relative response", level=AnalysisLevel.EXPERT, metrics=relative_metrics, messages=relative_messages),
            AnalysisSection("shared-event", "Shared event detector", level=AnalysisLevel.EXPERT, messages=shared_messages),
            AnalysisSection("movement-log", "Position change log", level=AnalysisLevel.EXPERT, entities=movement_entities, messages=movement_messages),
        ),
        explanation_code="fleet_intelligence",
        metadata={"title_key": "Fleet intelligence"},
    )


def build_period_analysis_result(analysis: dict[str, Any]) -> AnalysisResult:
    samples = int(analysis.get("samples") or 0)
    if samples <= 0:
        return AnalysisResult(
            key="period_analysis",
            status=AnalysisStatus.UNAVAILABLE,
            headline_key="No measurements yet.",
            summary_key="No data",
            explanation_code="data_quality",
        )
    quality = analysis.get("data_quality") or {}
    label = str(quality.get("label") or "Poor")
    score = float(quality.get("score") or 0.0)
    event_count = int(analysis.get("event_count") or 0)
    deviation = analysis.get("baseline_deviation_percent")
    if event_count > 0:
        status = AnalysisStatus.WARNING
        headline = "Continue observing"
        summary = "Review the event export for timing and severity"
        action = "analysis_review_events"
    elif _quality_status(label) == AnalysisStatus.WARNING:
        status = AnalysisStatus.NOTICE
        headline = "Interpret statistics with coverage in mind"
        summary = "Too little or too fragmented for strong conclusions"
        action = "analysis_improve_coverage"
    else:
        status = AnalysisStatus.GOOD
        headline = "No action required"
        summary = "Within normal statistical variation"
        action = "analysis_continue_monitoring"
    metrics = (
        _metric("Mean", "—" if analysis.get("cpm_mean") is None else f"{float(analysis['cpm_mean']):.2f} CPM", key="period-mean", level=AnalysisLevel.SUMMARY, status=status),
        _metric(
            "Data quality",
            label,
            value_key=label,
            key="period-quality",
            status=_quality_status(label),
            note_key="score {score:.1f}/100 · coverage {coverage:.1f}% · longest gap {gap} s",
            note_values={
                "score": score,
                "coverage": float(quality.get("completeness_percent") or 0.0),
                "gap": int(quality.get("longest_gap_seconds") or 0),
            },
        ),
        _metric("Baseline deviation", "—" if deviation is None else f"{float(deviation):+.1f}%", key="period-baseline-deviation", status=status, note_key="Relative to 7 d baseline"),
    )
    return AnalysisResult(
        key="period_analysis",
        status=status,
        headline_key=headline,
        summary_key=summary,
        primary_value="—" if analysis.get("cpm_mean") is None else f"{float(analysis['cpm_mean']):.2f} CPM",
        confidence=max(0.0, min(1.0, score / 100.0)),
        metrics=metrics,
        explanation_code="data_quality",
        action_code=action,
    )
