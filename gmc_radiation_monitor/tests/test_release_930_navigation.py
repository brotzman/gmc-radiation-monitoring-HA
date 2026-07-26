from __future__ import annotations

import shutil
from pathlib import Path

import pytest
from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import Translator, validate_catalogs

LIB = Path(__file__).parents[1] / "rootfs/usr/local/lib/gmc_bridge"


def _app(tmp_path: Path) -> ReportApplication:
    store = HistoryStore(tmp_path / "navigation.sqlite3")
    for index, (serial, model, cpm) in enumerate(
        (("SERIAL-NAV-320", "GMC-320", 14), ("SERIAL-NAV-500", "GMC-500+", 18))
    ):
        store.upsert_device_registry(
            serial,
            {
                "device_model": model,
                "configured_name": f"{model} navigation reference device {index + 1}",
                "runtime_online": True,
                "scan_interval_seconds": 60,
            },
        )
        store.insert_measurement(
            {"cpm": cpm, "temperature_c": 21.5, "voltage_v": 4.1},
            device_serial=serial,
            timestamp_utc=1_800_000_000 + index,
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


def test_930_sidebar_navigation_structure_and_translations(tmp_path: Path) -> None:
    app = _app(tmp_path)
    view_ids = (
        "overview",
        "analysis",
        "long-term",
        "history",
        "workflow",
        "calibration",
        "reports",
        "maintenance",
    )
    for language in ("de", "en", "es", "fr", "hr", "it", "nl", "pl"):
        page = app.render_index(language_override=language, mode_override="advanced").decode()
        assert page.count('id="app-sidebar"') == 1
        assert page.count('id="sidebar-backdrop"') == 1
        assert page.count('id="menu-button"') == 1
        assert page.count('class="app-topbar"') == 1
        for view in view_ids:
            assert page.count(f'id="view-{view}"') == 1
            assert page.count(f'data-view="{view}"') >= 2  # navigation item and view section
        t = Translator(language)
        for label in ("Main navigation", "Monitoring", "Evaluation", "Documentation", "Administration"):
            assert t(label) in page
        assert t("Refresh") in page
        assert t("Skip to content") in page
        assert 'id="dashboard-controls"' not in page
        assert page.count('id="toggle-all-cards"') == 1
    assert validate_catalogs() == []


def test_930_navigation_assets_keep_views_persistent_and_mobile_safe() -> None:
    script = (LIB / "static/dashboard.js").read_text(encoding="utf-8")
    css = (LIB / "static/dashboard.css").read_text(encoding="utf-8")
    for phrase in (
        "function setDashboardView",
        "function setSidebar",
        "function closeSidebar",
        "preferences.view = view",
        "history.replaceState",
        "window.addEventListener('hashchange'",
        "sidebarBackdrop?.setAttribute('aria-hidden'",
    ):
        assert phrase in script
    for phrase in (
        ".app-layout {",
        ".app-sidebar {",
        ".nav-item.active {",
        ".app-topbar {",
        "body.sidebar-open::after",
        "body.sidebar-open { overflow: hidden; }",
        "@media (max-width: 860px)",
        "@media (max-width: 390px)",
    ):
        assert phrase in css


@pytest.mark.skipif(shutil.which("chromium") is None, reason="Chromium is not installed")
def test_930_navigation_browser_desktop_mobile_persistence_and_overflow(tmp_path: Path) -> None:
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
            for width, height, text_size in (
                (1440, 1000, "100%"),
                (768, 1024, "100%"),
                (390, 844, "100%"),
                (390, 844, "200%"),
                (320, 700, "100%"),
            ):
                context = browser.new_context(
                    viewport={"width": width, "height": height},
                    reduced_motion="reduce",
                    bypass_csp=True,
                )
                page = context.new_page()
                page.set_content(html, wait_until="domcontentloaded")
                page.add_style_tag(content=css + f"\nhtml{{font-size:{text_size};}}")
                page.add_script_tag(content=script)
                page.wait_for_selector("#view-overview:not([hidden])")

                state = page.evaluate(
                    """() => ({
                      visibleViews: [...document.querySelectorAll('.dashboard-view')].filter(el => !el.hidden && getComputedStyle(el).display !== 'none').length,
                      pageExcess: document.querySelector('#page-scroll').scrollWidth - document.querySelector('#page-scroll').clientWidth,
                      bodyExcess: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                      active: document.querySelector('.nav-item[aria-current="page"]')?.dataset.view,
                    })"""
                )
                assert state["visibleViews"] == 1
                assert state["active"] == "overview"
                assert state["pageExcess"] <= 1, (width, text_size, state)
                assert state["bodyExcess"] <= 1, (width, text_size, state)

                if width <= 860:
                    page.locator("#menu-button").click()
                page.locator('.nav-item[data-view="analysis"]').click()
                assert page.locator("#view-analysis").is_visible()
                assert page.locator("#view-overview").is_hidden()
                assert page.locator('.nav-item[data-view="analysis"]').get_attribute("aria-current") == "page"
                assert page.evaluate("location.hash") == "#analysis"

                if width <= 860:
                    page.locator("#menu-button").click()
                    assert page.locator("#app-sidebar").get_attribute("class") is not None
                    assert "open" in (page.locator("#app-sidebar").get_attribute("class") or "")
                    assert page.locator("#sidebar-backdrop").get_attribute("aria-hidden") == "false"
                    page.keyboard.press("Escape")
                    assert "open" not in (page.locator("#app-sidebar").get_attribute("class") or "")
                    assert page.locator("#sidebar-backdrop").get_attribute("aria-hidden") == "true"
                    page.locator("#menu-button").click()
                    page.mouse.click(width - 4, 20)
                    assert "open" not in (page.locator("#app-sidebar").get_attribute("class") or "")
                    page.locator("#menu-button").click()
                    page.locator('.nav-item[data-view="long-term"]').click()
                    assert page.locator("#view-long-term").is_visible()
                    assert "open" not in (page.locator("#app-sidebar").get_attribute("class") or "")

                overflow_after = page.evaluate(
                    """() => ({
                      pageExcess: document.querySelector('#page-scroll').scrollWidth - document.querySelector('#page-scroll').clientWidth,
                      bodyExcess: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                      visibleViews: [...document.querySelectorAll('.dashboard-view')].filter(el => !el.hidden && getComputedStyle(el).display !== 'none').length,
                    })"""
                )
                assert overflow_after["visibleViews"] == 1
                assert overflow_after["pageExcess"] <= 1, (width, text_size, overflow_after)
                assert overflow_after["bodyExcess"] <= 1, (width, text_size, overflow_after)
                context.close()
        finally:
            browser.close()
