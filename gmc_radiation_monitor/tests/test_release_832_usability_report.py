from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.reports import (
    _PAGE1_ASSESSMENT_RECT,
    _PAGE1_CHART_RECT,
    _PAGE1_STATS_HEADING_Y,
    _report_display_end,
    load_timezone,
    resolve_period,
)


def _app(tmp_path: Path) -> ReportApplication:
    store = HistoryStore(tmp_path / "history.sqlite3")
    serial = "SERIAL-320"
    store.upsert_device_registry(
        serial,
        {
            "device_model": "GMC-320 Re 4.52",
            "configured_name": "Arbeitszimmer",
            "runtime_online": True,
            "scan_interval_seconds": 120,
            "device_health_status": "ok",
        },
    )
    store.insert_measurement(
        {"cpm": 14, "temperature_c": 22.0, "voltage_v": 4.1},
        device_serial=serial,
        timestamp_utc=int(datetime.now(UTC).timestamp()),
    )
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=120,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
    )


def test_page_one_layout_reserves_a_clear_gap_between_chart_and_assessment() -> None:
    _chart_x, chart_bottom, _chart_width, _chart_height = _PAGE1_CHART_RECT
    _panel_x, panel_bottom, _panel_width, panel_height = _PAGE1_ASSESSMENT_RECT
    panel_top = panel_bottom + panel_height

    # The chart's bottom is above the assessment panel, leaving enough room
    # for tick labels and the x-axis label instead of overlapping the heading.
    assert chart_bottom - panel_top >= 0.05
    assert panel_bottom > _PAGE1_STATS_HEADING_Y


def test_current_period_chart_ends_at_generation_time() -> None:
    tz = load_timezone("Europe/Berlin")
    generated = datetime(2026, 7, 21, 5, 0, tzinfo=tz)
    period = resolve_period(
        kind="daily",
        selection="specific",
        tz=tz,
        date_value="2026-07-21",
        now=generated,
    )
    assert _report_display_end(period, generated.astimezone(UTC)) == generated


def test_completed_period_chart_keeps_full_calendar_end() -> None:
    tz = load_timezone("Europe/Berlin")
    period = resolve_period(
        kind="daily",
        selection="specific",
        tz=tz,
        date_value="2026-07-20",
        now=datetime(2026, 7, 21, 5, 0, tzinfo=tz),
    )
    generated = datetime(2026, 7, 21, 3, 0, tzinfo=UTC)
    assert _report_display_end(period, generated) == period.end_local


def test_dashboard_explains_view_level_and_report_formats(tmp_path: Path) -> None:
    page = _app(tmp_path).render_index(language_override="de", mode_override="advanced").decode()

    assert 'id="analysis-level-description"' in page
    assert 'data-analysis-description="Ausführliche Einordnung und die wichtigsten unterstützenden Werte"' in page
    assert "description.textContent = selectedDescription" in page
    assert 'class="report-format-guide"' in page
    assert "Am besten zum Lesen, Drucken und Weitergeben" in page
    assert "Enthält Rohdaten, Prüfsummen und Angaben zur Reproduzierbarkeit" in page
    assert "Für Tabellenprogramme und weiterführende Auswertungen" in page
    assert "@media (max-width:620px) { .report-format-guide { grid-template-columns:1fr; } }" in page
    assert ".analysis-level-button, a.button, button { min-height:2.75rem; }" in page
    assert ".header-intro h1 { font-size:1.5rem; overflow-wrap:normal; word-break:normal; hyphens:auto; }" in page
