from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import Translator, validate_catalogs
from gmc_bridge.version import APP_VERSION

LIB = Path(__file__).parents[1] / "rootfs/usr/local/lib/gmc_bridge"


def _app(tmp_path: Path) -> ReportApplication:
    store = HistoryStore(tmp_path / "release-940.sqlite3")
    store.upsert_device_registry(
        "SERIAL-940",
        {
            "device_model": "GMC-500+",
            "configured_name": "GMC-500+ long navigation reference detector",
            "runtime_online": True,
            "scan_interval_seconds": 60,
        },
    )
    for offset in range(180):
        store.insert_measurement(
            {
                "cpm": 15 + (offset % 4),
                "temperature_c": 20.5 + (offset % 3) * 0.2,
                "pressure_hpa": 1012.0 - (offset % 5),
                "voltage_v": 4.1,
            },
            device_serial="SERIAL-940",
            timestamp_utc=1_800_000_000 + offset * 60,
        )
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
        ui_mode="advanced",
        restore_enabled=True,
        purge_all_history_enabled=True,
    )


def test_940_version_sidebar_category_and_long_term_placement(tmp_path: Path) -> None:
    assert APP_VERSION == "9.4.0"
    page = _app(tmp_path).render_index(language_override="de", mode_override="advanced").decode()

    sidebar_start = page.index('id="app-sidebar"')
    sidebar_end = page.index('</aside>', sidebar_start)
    sidebar = page[sidebar_start:sidebar_end]
    assert sidebar.count('id="analysis-level-panel"') == 1
    assert sidebar.index('id="analysis-level-panel"') < sidebar.index('class="side-nav"')
    assert "Ansicht" in sidebar
    assert "in allen Bereichen" in sidebar

    overview_start = page.index('id="view-overview"')
    analysis_start = page.index('id="view-analysis"')
    overview = page[overview_start:analysis_start]
    long_term_start = page.index('id="view-long-term"')
    history_start = page.index('id="view-history"')
    long_term = page[long_term_start:history_start]
    for card_id in ("radiation-intelligence", "adaptive-background", "cosmic-influence"):
        assert f'id="{card_id}"' not in overview
        assert f'id="{card_id}"' in long_term
    assert 'id="long-term-context"' in long_term
    assert "Kosmischer Einfluss" in long_term


def test_940_assets_use_global_level_and_blue_sidebar_accent() -> None:
    script = (LIB / "static/dashboard.js").read_text(encoding="utf-8")
    css = (LIB / "static/dashboard.css").read_text(encoding="utf-8")
    for phrase in (
        "document.body.dataset.analysisLevel = level",
        "preferences.analysisLevel = level",
        "setAnalysisLevel(preferences.analysisLevel",
        "'radiation-intelligence': 'long-term'",
        "'adaptive-background': 'long-term'",
        "'cosmic-influence': 'long-term'",
    ):
        assert phrase in script
    assert "setAnalysisLevel('analysis')" not in script
    for phrase in (
        "--app-accent: var(--blue)",
        ".app-sidebar .analysis-level-panel",
        ".app-sidebar .analysis-level-button[aria-pressed=\"true\"]",
        ".long-term-context-stack",
    ):
        assert phrase in css


def test_940_new_copy_is_localised_in_all_catalogs() -> None:
    source_keys = (
        "Choose how many details and tools are shown across all sections. The selection is stored in this browser.",
        "Long-term interpretation context",
        "Intelligent analysis, adaptive background and cosmic-influence context for the selected detector.",
    )
    for language in ("de", "en", "es", "fr", "hr", "it", "nl", "pl"):
        translator = Translator(language)
        for key in source_keys:
            translated = translator(key)
            assert translated
            if language != "en":
                assert translated != key
    assert validate_catalogs() == []


@pytest.mark.skipif(shutil.which("chromium") is None, reason="Chromium is not installed")
def test_940_browser_global_level_persists_across_views_and_mobile_has_no_overflow(tmp_path: Path) -> None:
    playwright = pytest.importorskip("playwright.sync_api")
    app = _app(tmp_path)
    css = (LIB / "static/dashboard.css").read_text(encoding="utf-8")
    script = (LIB / "static/dashboard.js").read_text(encoding="utf-8")
    html = app.render_index(language_override="de", mode_override="advanced").decode()

    with playwright.sync_playwright() as api:
        browser = api.chromium.launch(
            headless=True,
            executable_path=shutil.which("chromium"),
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        try:
            for width, height in ((1440, 1000), (390, 844), (320, 700)):
                context = browser.new_context(viewport={"width": width, "height": height}, bypass_csp=True)
                page = context.new_page()
                page.set_content(html, wait_until="domcontentloaded")
                page.add_style_tag(content=css)
                page.add_script_tag(content=script)
                page.wait_for_selector("#view-overview:not([hidden])")

                if width <= 860:
                    page.locator("#menu-button").click()
                page.locator('.analysis-level-button[data-analysis-level="expert"]').click()
                assert page.locator("body").get_attribute("data-analysis-level") == "expert"

                for view in ("analysis", "long-term", "reports", "overview"):
                    if width <= 860 and "open" not in (page.locator("#app-sidebar").get_attribute("class") or ""):
                        page.locator("#menu-button").click()
                    page.locator(f'.nav-item[data-view="{view}"]').click()
                    assert page.locator(f"#view-{view}").is_visible()
                    assert page.locator("body").get_attribute("data-analysis-level") == "expert"

                if width <= 860 and "open" not in (page.locator("#app-sidebar").get_attribute("class") or ""):
                    page.locator("#menu-button").click()
                page.locator('.analysis-level-button[data-analysis-level="summary"]').click()
                assert page.locator("body").get_attribute("data-analysis-level") == "summary"
                if width <= 860 and "open" not in (page.locator("#app-sidebar").get_attribute("class") or ""):
                    page.locator("#menu-button").click()
                page.locator('.nav-item[data-view="long-term"]').click()
                assert page.locator("body").get_attribute("data-analysis-level") == "summary"
                assert page.locator("#long-term-context").is_visible()

                overflow = page.evaluate(
                    """() => ({
                      root: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                      page: document.querySelector('#page-scroll').scrollWidth - document.querySelector('#page-scroll').clientWidth,
                      sidebar: document.querySelector('#app-sidebar').scrollWidth - document.querySelector('#app-sidebar').clientWidth,
                    })"""
                )
                assert overflow["root"] <= 1, (width, overflow)
                assert overflow["page"] <= 1, (width, overflow)
                assert overflow["sidebar"] <= 1, (width, overflow)
                context.close()
        finally:
            browser.close()
