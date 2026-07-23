from __future__ import annotations

from pathlib import Path

from gmc_bridge.analysis_presentation import build_primary_analysis_result
from gmc_bridge.errors import GmcProtocolError, classify_optional_issue
from gmc_bridge.explanations import translate_explanation
from gmc_bridge.historical_presentation import trend_symbol
from gmc_bridge.history import HistoryStore
from gmc_bridge.presentation_models import (
    HISTORY_PERIODS,
    AnalysisLevel,
    AnalysisMetric,
    AnalysisStatus,
)
from gmc_bridge.reports import build_live_analysis
from gmc_bridge.translations import Translator, validate_catalogs
from gmc_bridge.version import APP_VERSION
from gmc_bridge.web_components import render_metric_card

ROOT = Path(__file__).parents[1]
LIB = ROOT / "rootfs/usr/local/lib/gmc_bridge"


def test_current_release_version() -> None:
    assert APP_VERSION == "9.0.2"
    assert "version: 9.0.2" in (ROOT / "config.yaml").read_text(encoding="utf-8")
    assert (ROOT / "RELEASE_NOTES_9.0.2.md").is_file()


def test_large_web_and_translation_modules_are_split_by_responsibility() -> None:
    report_lines = (LIB / "report_web.py").read_text(encoding="utf-8").count("\n") + 1
    translation_lines = (LIB / "translations.py").read_text(encoding="utf-8").count("\n") + 1
    assert report_lines < 3300
    assert translation_lines < 100
    assert (LIB / "web_assets.py").is_file()
    assert (LIB / "web_components.py").is_file()
    assert (LIB / "analysis_presentation.py").is_file()
    assert (LIB / "historical_presentation.py").is_file()
    assert (LIB / "report_web_support.py").is_file()
    for language in ("en", "de", "fr", "es", "it", "nl", "pl", "hr"):
        assert (LIB / "i18n" / f"{language}.py").is_file()


def test_catalogues_are_complete_and_placeholder_safe() -> None:
    assert validate_catalogs() == []


def test_analysis_level_normalization_always_returns_enum_member() -> None:
    assert AnalysisLevel.normalize(None) is AnalysisLevel.ANALYSIS
    assert AnalysisLevel.normalize("invalid") is AnalysisLevel.ANALYSIS
    assert AnalysisLevel.normalize("summary") is AnalysisLevel.SUMMARY


def test_history_periods_have_one_shared_definition() -> None:
    assert [(period.key, period.days) for period in HISTORY_PERIODS] == [
        ("week", 7),
        ("month", 30),
        ("quarter", 90),
        ("year", 365),
    ]
    assert trend_symbol(2.0) == "↗"
    assert trend_symbol(-2.0) == "↘"
    assert trend_symbol(0.5) == "→"


def test_metric_component_uses_display_neutral_model() -> None:
    metric = AnalysisMetric(
        key="quality",
        label_key="Data quality",
        value="Gut",
        level=AnalysisLevel.ANALYSIS,
        status=AnalysisStatus.GOOD,
        note_key="Suitable for most trend analysis",
    )
    html = render_metric_card(metric, Translator("de"))
    assert 'data-metric-key="quality"' in html
    assert 'data-analysis-tier="analysis"' in html
    assert "Datenqualität" in html
    assert "Für die meisten Trendanalysen geeignet" in html


def test_live_analysis_serializes_shared_presentation_result(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    store.set_metadata({"serial": "SERIAL-A"})
    store.insert_measurement({"cpm": 15}, device_serial="SERIAL-A", timestamp_utc=1_800_000_000)
    analysis = build_live_analysis(store, scan_interval_seconds=60, device_serial="SERIAL-A")
    expected = build_primary_analysis_result(analysis).as_dict()
    assert analysis["presentation"]["key"] == "primary_analysis"
    assert analysis["presentation"]["status"] == expected["status"]
    assert analysis["presentation"]["metrics"]


def test_explanation_codes_are_localized_at_the_presentation_boundary() -> None:
    explanation = translate_explanation("adaptive_background", Translator("de"))
    assert explanation is not None
    title, body, action = explanation
    assert title == "Wie wird das Hintergrundprofil berechnet?"
    assert "Wochentags" in body
    assert "Lernphase" in action


def test_new_explanation_titles_are_localized_in_every_non_english_catalogue() -> None:
    english = "Why is this assessment shown?"
    for language in ("de", "fr", "es", "it", "nl", "pl", "hr"):
        translated = Translator(language)(english)
        assert translated
        assert translated != english


def test_optional_device_errors_have_stable_issue_contract() -> None:
    issue = classify_optional_issue("gyro", GmcProtocolError("expected terminator 0xaa, received 0x40"))
    assert issue.code == "orientation_frame_invalid"
    assert issue.affects_measurement is False
    assert issue.retryable is True
    assert "0x40" in issue.technical_detail
