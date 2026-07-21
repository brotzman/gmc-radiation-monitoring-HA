from __future__ import annotations

from pathlib import Path

from gmc_bridge.analysis_presentation import (
    AnalysisPresentationConfig,
    build_absolute_safety_result,
    build_adaptive_background_result,
    build_combined_interpretation_result,
    build_cosmic_influence_result,
    build_detailed_analysis_result,
    build_fleet_intelligence_result,
    build_local_background_result,
    build_radiation_intelligence_result,
    build_recommendation_result,
)
from gmc_bridge.presentation_models import AnalysisResult
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import Translator
from gmc_bridge.version import APP_VERSION

ROOT = Path(__file__).parents[1]
LIB = ROOT / "rootfs/usr/local/lib/gmc_bridge"


def _analysis() -> dict[str, object]:
    return {
        "available": True,
        "latest_cpm": 16.0,
        "mean_1h": 15.5,
        "mean_24h": 15.0,
        "mean_7d": 14.8,
        "sd_24h": 3.0,
        "median_24h": 15.0,
        "p95_24h": 20.0,
        "p99_24h": 23.0,
        "min_24h": 8.0,
        "max_24h": 24.0,
        "z_score_24h": 0.33,
        "samples_1h": 60,
        "samples_24h": 1440,
        "samples_7d": 10080,
        "coverage_1h_percent": 100.0,
        "coverage_24h_percent": 100.0,
        "coverage_7d_percent": 100.0,
        "baseline_ready": True,
        "recent_window_ready": True,
        "baseline_readiness_percent": 100.0,
        "baseline_deviation_cpm": 0.7,
        "baseline_deviation_percent": 4.7,
        "background_index_percent": 104.7,
        "data_quality_label_24h": "Excellent",
        "data_quality_score_24h": 99.0,
        "events_24h": 0,
        "scan_interval_seconds": 60,
        "cpm_per_usvh": 154.0,
        "counting_uncertainty_latest": {"lower_cpm": 9.0, "upper_cpm": 25.0},
        "counting_uncertainty_1h": {"lower_cpm": 14.5, "upper_cpm": 16.5},
        "counting_uncertainty_24h": {"lower_cpm": 14.8, "upper_cpm": 15.2},
        "counting_uncertainty_7d": {"lower_cpm": 14.7, "upper_cpm": 14.9},
        "temperature_bins_24h": [],
    }


def _profile() -> dict[str, object]:
    return {
        "available": True,
        "current_cpm": 16.0,
        "typical_cpm": 15.0,
        "deviation_percent": 6.7,
        "state": "Normal",
        "weekday": 3,
        "hour": 13,
        "confidence": "High",
        "drift": {},
        "historical_development": {},
    }


def test_release_version_is_710() -> None:
    assert APP_VERSION == "8.3.2"
    assert "version: 8.3.2" in (ROOT / "config.yaml").read_text(encoding="utf-8")
    assert (ROOT / "RELEASE_NOTES_8.3.2.md").is_file()


def test_every_dashboard_analysis_builder_returns_the_shared_model() -> None:
    analysis = _analysis()
    config = AnalysisPresentationConfig()
    results = (
        build_detailed_analysis_result(analysis, config=config),
        build_absolute_safety_result(analysis, config=config),
        build_local_background_result(analysis, config=config),
        build_combined_interpretation_result(analysis, config=config),
        build_recommendation_result(analysis, config=config),
        build_radiation_intelligence_result(
            {
                "available": True,
                "state": "No statistically unusual signal",
                "probability_percent": 12.0,
                "confidence": "High",
                "reasons": [],
            },
            collected=1440,
            needed=0,
        ),
        build_adaptive_background_result(_profile(), _profile()),
        build_cosmic_influence_result({"enabled": False}),
        build_fleet_intelligence_result({}),
    )
    assert all(isinstance(result, AnalysisResult) for result in results)
    assert {result.key for result in results} == {
        "device_analysis",
        "absolute_safety",
        "local_background",
        "combined_interpretation",
        "recommendation",
        "radiation_intelligence",
        "adaptive_background",
        "cosmic_influence",
        "fleet_intelligence",
    }


def test_detailed_analysis_contains_all_semantic_sections() -> None:
    result = build_detailed_analysis_result(_analysis(), config=AnalysisPresentationConfig())
    assert [section.key for section in result.sections] == [
        "status-summary",
        "overview",
        "statistics",
        "counting-statistics",
        "environment",
        "long-term-context",
        "advanced-diagnostics",
    ]
    payload = result.as_dict()
    assert payload["sections"]
    assert payload["sections"][0]["metrics"]
    assert {"messages", "entities", "tables"}.issubset(payload["sections"][0])


def test_analysis_calculation_module_contains_no_html_templates() -> None:
    source = (LIB / "analysis_presentation.py").read_text(encoding="utf-8")
    assert "<article" not in source
    assert "<section" not in source
    assert 'class="' not in source


def test_web_orchestrator_is_smaller_and_delegates_analysis_rendering() -> None:
    report_source = (LIB / "report_web.py").read_text(encoding="utf-8")
    report_lines = report_source.count("\n") + 1
    assert report_lines < 2500
    assert (LIB / "web_analysis_views.py").is_file()
    assert "render_device_analysis(" in report_source
    assert (LIB / "workflow_controller.py").is_file()
    assert (LIB / "report_web_support.py").is_file()
    assert "from .report_web_support import (" in report_source
    assert "WorkflowApplicationMixin" in report_source
    assert "render_adaptive_background(" in report_source
    assert "render_fleet_intelligence(" in report_source
    assert 'class="assessment-grid stability-grid"' not in report_source


def test_background_profile_compatibility_wrapper_uses_shared_model() -> None:
    html = ReportApplication._background_profile_block(
        _profile(), title="Device baseline", t=Translator("de")
    )
    assert "Typisch für Donnerstag um 13:00 Uhr<br>" in html
    assert "15.0 CPM · +6.7%" in html
