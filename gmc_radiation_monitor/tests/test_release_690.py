from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from gmc_bridge.adaptive_background import build_adaptive_background
from gmc_bridge.history import HistoryRow, HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.version import APP_VERSION


def _row(ts: datetime, cpm: int, *, temperature: float = 20.0, pressure: float = 1013.0) -> HistoryRow:
    return HistoryRow(
        "SERIAL-320",
        int(ts.timestamp()),
        cpm,
        temperature,
        4.1,
        None,
        None,
        None,
        "accepted",
        pressure_hpa=pressure,
    )


def _app_with_history(tmp_path: Path) -> ReportApplication:
    store = HistoryStore(tmp_path / "history.sqlite3", retention_days=800)
    store.upsert_device_registry(
        "SERIAL-320",
        {
            "device_model": "GMC-320 Re 4.52",
            "configured_name": "GMC-320",
            "runtime_online": True,
            "scan_interval_seconds": 60,
            "device_health_status": "ok",
        },
    )
    now = datetime(2026, 7, 16, 12, 0, tzinfo=UTC)
    for day in range(100):
        ts = now - timedelta(days=99 - day)
        store.insert_measurement(
            {
                "cpm": 12 + day // 30,
                "temperature_c": 18.0 + day * 0.02,
                "voltage_v": 4.1,
                "pressure_hpa": 1015.0 - day * 0.03,
            },
            device_serial="SERIAL-320",
            timestamp_utc=int(ts.timestamp()),
        )
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
        restore_enabled=False,
        purge_all_history_enabled=False,
    )


def test_adaptive_background_includes_365_day_trend_and_compact_daily_chart() -> None:
    now = datetime(2026, 7, 16, 12, 0, tzinfo=UTC)
    rows = [
        _row(
            now - timedelta(days=729 - day),
            12 if day < 365 else 15,
            temperature=18.0 + day / 500,
            pressure=1018.0 - day / 600,
        )
        for day in range(730)
    ]
    result = build_adaptive_background(rows, timezone_name="UTC", now_utc=int(now.timestamp()))
    assert "365" in result["drift"]
    assert result["drift"]["365"]["change_percent"] is not None
    history = result["historical_development"]
    assert history["available"] is True
    assert 2 <= len(history["points"]) <= 121
    assert history["daily_points"] == 366
    assert history["temperature_trend"]["samples"] > 0
    assert history["pressure_trend"]["samples"] > 0


def test_dashboard_has_three_neutral_symbol_analysis_levels_and_persists_choice(tmp_path: Path) -> None:
    page = _app_with_history(tmp_path).render_index(language_override="de").decode()
    panel = page.split('<section class="analysis-level-panel"', 1)[1].split("</section>", 1)[0]
    assert "◉" in panel and "▤" in panel and "∑" in panel
    assert "Zusammenfassung" in panel
    assert "Expertenansicht" in panel
    assert "🟢" not in panel and "🟡" not in panel and "🔵" not in panel
    assert 'data-analysis-level="summary"' in panel
    assert 'data-analysis-level="analysis"' in panel
    assert 'data-analysis-level="expert"' in panel
    assert "preferences.analysisLevel" in page
    assert "document.body.dataset.analysisLevel = level" in page


def test_analysis_cards_are_progressively_grouped_and_history_is_integrated(tmp_path: Path) -> None:
    page = _app_with_history(tmp_path).render_index(language_override="de").decode()
    assert 'data-analysis-tier="summary"' in page
    assert 'data-analysis-tier="analysis"' in page
    assert 'data-analysis-tier="expert"' in page
    assert "Historische Entwicklung" in page
    assert 'class="historical-chart"' in page
    assert "Tagesmedian, über 7 Tage geglättet" in page
    assert "Erkannte Baseline-Sprünge" in page
    assert "Warum wird das so bewertet?" in page
    assert "Wie wird das Hintergrundprofil berechnet?" in page
    assert 'body[data-analysis-level="summary"] [data-analysis-tier="analysis"]' in page
    assert 'body[data-analysis-level="analysis"] [data-analysis-tier="expert"]' in page


def test_release_version_is_690() -> None:
    assert APP_VERSION == "8.3.1"
