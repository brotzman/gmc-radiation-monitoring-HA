import tempfile
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def make_app(profile: str, **kwargs):
    tmp = tempfile.TemporaryDirectory()
    store = HistoryStore(Path(tmp.name) / "history.sqlite", retention_days=30)
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        safety_profile=profile,
        **kwargs,
    )
    app._tmp = tmp
    return app


def test_gq_profile_uses_fixed_manufacturer_bands():
    app = make_app("gq", safety_warning_cpm=999, safety_danger_cpm=1000)
    thresholds = app._effective_safety_thresholds()
    assert thresholds["basis"] == "either"
    assert thresholds["warning_cpm"] == 51
    assert thresholds["danger_cpm"] == 100
    assert thresholds["warning_usvh"] == 0.326
    assert thresholds["danger_usvh"] == 0.651


def test_official_reference_profiles_are_annualised_context_only():
    for profile in ("bfs_reference", "icrp_reference"):
        app = make_app(profile)
        thresholds = app._effective_safety_thresholds()
        assert thresholds["basis"] == "dose_rate"
        assert thresholds["warning_usvh"] == 0.114
        assert thresholds["danger_usvh"] == 2.283
        assert "not official instantaneous alarm thresholds" in thresholds["reference"]


def test_custom_profile_uses_all_configured_values():
    app = make_app(
        "custom",
        safety_threshold_basis="cpm",
        safety_warning_cpm=12,
        safety_danger_cpm=34,
        safety_warning_usvh=0.2,
        safety_danger_usvh=0.9,
    )
    thresholds = app._effective_safety_thresholds()
    assert thresholds == {
        "profile": "custom",
        "basis": "cpm",
        "warning_cpm": 12,
        "danger_cpm": 34,
        "warning_usvh": 0.2,
        "danger_usvh": 0.9,
        "label": "Custom thresholds",
        "reference": "User-defined values; verify them for the detector tube, calibration and intended use.",
    }


def _recommendation_analysis(*, cpm: float, index: float | None = 100.0, trend: float = 0.0):
    return {
        "latest_cpm": cpm,
        "background_index_percent": index,
        "samples_7d": 400,
        "coverage_1h_percent": 100.0,
        "trend_30m_cpm": trend,
    }


def test_recommendation_combines_absolute_and_local_states():
    app = make_app("gq")
    normal = app._render_recommendation(_recommendation_analysis(cpm=20))
    assert "No action required" in normal

    local_anomaly = app._render_recommendation(_recommendation_analysis(cpm=20, index=190.0))
    assert "Check the measurement location" in local_anomaly

    warning = app._render_recommendation(_recommendation_analysis(cpm=60))
    assert "Warning threshold exceeded" in warning

    danger = app._render_recommendation(_recommendation_analysis(cpm=120))
    assert "Danger threshold exceeded" in danger


def test_recommendation_is_translated_to_german():
    from gmc_bridge.translations import Translator

    app = make_app("gq")
    rendered = app._render_recommendation(_recommendation_analysis(cpm=20), t=Translator("de"))
    assert "Empfehlung" in rendered
    assert "Keine Maßnahmen erforderlich" in rendered
