from __future__ import annotations

import tempfile
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.home_assistant import HomeAssistantLocation
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import SUPPORTED_UI_LANGUAGES


class _LocationClient:
    def get_location(self) -> HomeAssistantLocation:
        return HomeAssistantLocation(
            available=True,
            location_name="Home",
            latitude=51.60176,
            longitude=7.45410,
            elevation=0,
            country="DE",
            time_zone="Europe/Berlin",
        )


def _render(language: str = "de") -> str:
    with tempfile.TemporaryDirectory() as temp_dir:
        store = HistoryStore(Path(temp_dir) / "history.sqlite3")
        app = ReportApplication(
            store=store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
            ui_language=language,
            home_assistant_client=_LocationClient(),
        )
        return app.render_index(language_override=language).decode("utf-8")


def test_global_report_header_uses_status_strip_and_collapsible_location():
    rendered = _render("de")
    assert '<header class="report-header">' in rendered
    assert '<div class="info-chips"' not in rendered
    assert 'class="info-chip"' not in rendered
    assert "Gespeicherte Messwerte" in rendered
    assert 'class="status-strip"' in rendered
    assert '<nav class="control-toolbar"' not in rendered
    assert 'class="analysis-control"' not in rendered
    assert 'class="language-control"' not in rendered
    assert '<details class="location-details">' in rendered
    assert 'class="global-settings"' not in rendered
    assert 'class="global-setting"' not in rendered
    assert "Koordinaten: 51.60176, 7.45410" in rendered
    assert "Zeitzone: Europe/Berlin" in rendered
    assert "Die Standortdaten stammen" in rendered


def test_header_css_no_longer_contains_in_page_mode_or_language_controls():
    rendered = _render("de")
    assert ".control-toolbar" not in rendered
    assert ".analysis-control" not in rendered
    assert ".language-control" not in rendered
    assert ".mode-link" not in rendered
    assert ".lang-link" not in rendered
    assert ".info-chips" not in rendered
    assert "grid-template-columns:repeat(3,minmax(0,1fr))" in rendered


def test_new_header_renders_for_every_supported_language():
    for language in SUPPORTED_UI_LANGUAGES:
        rendered = _render(language)
        assert '<div class="info-chips"' not in rendered
        assert 'class="info-chip"' not in rendered
        assert 'class="status-strip"' in rendered
        assert '<nav class="control-toolbar"' not in rendered
        assert '<details class="location-details">' in rendered
        assert "Europe/Berlin" in rendered
        assert "Home" in rendered
