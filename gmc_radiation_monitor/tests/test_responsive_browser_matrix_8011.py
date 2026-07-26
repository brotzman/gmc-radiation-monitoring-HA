from __future__ import annotations

import hashlib
import os
import shutil
from pathlib import Path

import pytest
from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from PIL import Image

playwright = pytest.importorskip("playwright.sync_api")
pytestmark = pytest.mark.skipif(
    os.environ.get("GMC_RUN_BROWSER_MATRIX") != "1",
    reason="full Playwright browser matrix is opt-in; set GMC_RUN_BROWSER_MATRIX=1",
)

BROWSER_ENGINES = ("chromium", "firefox", "webkit")
VIEWPORTS = {
    "desktop": {"width": 1440, "height": 900},
    "tablet": {"width": 768, "height": 1024},
    "phone": {"width": 390, "height": 844},
    "narrow": {"width": 320, "height": 568},
}
LANGUAGES = ("en", "de", "fr", "pl")


def _dashboard_app(tmp_path: Path) -> ReportApplication:
    store = HistoryStore(tmp_path / "responsive.sqlite3")
    for serial, model, cpm in (
        ("SERIAL-320", "GMC-320", 17),
        ("SERIAL-500", "GMC-500+", 19),
    ):
        store.upsert_device_registry(
            serial,
            {
                "device_model": model,
                "configured_name": model,
                "runtime_online": True,
                "scan_interval_seconds": 60,
            },
        )
        store.insert_measurement(
            {"cpm": cpm, "temperature_c": 21.4, "voltage_v": 4.2},
            device_serial=serial,
            timestamp_utc=1_800_000_000,
        )
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="en",
        ui_mode="advanced",
    )


def _launch_browser(browser_api, engine: str):
    browser_type = getattr(browser_api, engine)
    options: dict[str, object] = {"headless": True}
    if engine == "chromium":
        options["args"] = ["--no-sandbox"]
        executable = shutil.which("chromium") or shutil.which("chromium-browser")
        if executable:
            options["executable_path"] = executable
    try:
        return browser_type.launch(**options)
    except Exception as exc:
        if os.environ.get("GMC_REQUIRE_ALL_BROWSERS") == "1":
            raise AssertionError(f"required Playwright browser {engine} could not start") from exc
        pytest.skip(f"Playwright browser {engine} is not installed in this environment")


def _boxes(page, selector: str, count: int) -> list[dict[str, float]]:
    locator = page.locator(selector)
    assert locator.count() >= count
    boxes = [locator.nth(index).bounding_box() for index in range(count)]
    assert all(box is not None for box in boxes)
    return boxes  # type: ignore[return-value]


def _assert_screenshot(path: Path, viewport: dict[str, int]) -> str:
    assert path.is_file()
    assert path.stat().st_size > 15_000
    with Image.open(path) as image:
        assert image.size == (viewport["width"], viewport["height"])
        colors = image.convert("RGB").getcolors(maxcolors=1_000_000)
        assert colors is not None and len(colors) > 100
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize("engine", BROWSER_ENGINES)
def test_dashboard_browser_language_and_viewport_matrix(tmp_path: Path, engine: str) -> None:
    app = _dashboard_app(tmp_path)
    screenshots: dict[str, str] = {}

    dashboard_css = Path("rootfs/usr/local/lib/gmc_bridge/static/dashboard.css").read_text(encoding="utf-8")
    dashboard_js = Path("rootfs/usr/local/lib/gmc_bridge/static/dashboard.js").read_text(encoding="utf-8")

    with playwright.sync_playwright() as browser_api:
        browser = _launch_browser(browser_api, engine)
        try:
            for language in LANGUAGES:
                dashboard_html = app.render_index(
                    language_override=language, mode_override="advanced"
                ).decode()
                for name, viewport in VIEWPORTS.items():
                    context = browser.new_context(
                        viewport=viewport,
                        color_scheme="light",
                        reduced_motion="reduce",
                        bypass_csp=True,
                        locale=f"{language}-{language.upper()}" if language != "en" else "en-US",
                    )
                    page = context.new_page()
                    page.set_content(dashboard_html, wait_until="domcontentloaded", timeout=15_000)
                    page.add_style_tag(content=dashboard_css)
                    page.add_script_tag(content=dashboard_js)
                    page.add_style_tag(
                        content="*{animation:none!important;transition:none!important;caret-color:transparent!important}"
                    )
                    page.wait_for_selector("#view-overview:not([hidden])", timeout=10_000)

                    overflow = page.locator(".page-scroll").evaluate(
                        "el => ({scrollWidth: el.scrollWidth, clientWidth: el.clientWidth})"
                    )
                    assert overflow["scrollWidth"] <= overflow["clientWidth"] + 1
                    assert page.locator("html").get_attribute("lang") == language
                    assert page.locator(".dashboard-view:not([hidden])").count() == 1
                    assert page.locator('.nav-item[aria-current="page"]').get_attribute("data-view") == "overview"

                    resources = _boxes(page, ".header-resource-links > *", 2)
                    levels = _boxes(page, ".analysis-level-button", 3)
                    page.locator(".system-status-panel").evaluate("el => { el.open = true; }")
                    statuses = _boxes(page, ".status-strip-item", 3)

                    if viewport["width"] >= 900:
                        assert page.locator("#app-sidebar").is_visible()
                        assert page.locator("#menu-button").is_hidden()
                        assert abs(resources[0]["y"] - resources[1]["y"]) < 2
                        assert abs(levels[0]["x"] - levels[1]["x"]) < 2
                        assert levels[1]["y"] >= levels[0]["y"] + levels[0]["height"]
                        assert abs(statuses[0]["y"] - statuses[2]["y"]) < 2
                    elif viewport["width"] <= 620:
                        assert page.locator("#menu-button").is_visible()
                        assert resources[1]["y"] > resources[0]["y"] + resources[0]["height"]
                        assert levels[1]["y"] > levels[0]["y"] + levels[0]["height"]
                        assert statuses[1]["y"] > statuses[0]["y"] + statuses[0]["height"]
                        page.locator("#menu-button").click()
                        assert "open" in (page.locator("#app-sidebar").get_attribute("class") or "")
                        page.mouse.click(viewport["width"] - 4, 20)
                        assert "open" not in (page.locator("#app-sidebar").get_attribute("class") or "")

                    if viewport["width"] <= 860:
                        page.locator("#menu-button").click()
                    page.locator('.nav-item[data-view="reports"]').click()
                    assert page.locator("#view-reports").is_visible()
                    assert page.locator("#view-overview").is_hidden()
                    assert page.evaluate("location.hash") == "#reports"
                    report_form = page.locator("#custom-report-form")
                    assert report_form.is_visible()
                    form_box = report_form.bounding_box()
                    period_box = page.locator("#custom-report-period").bounding_box()
                    assert form_box is not None and period_box is not None
                    assert period_box["x"] >= form_box["x"] - 0.5
                    assert period_box["x"] + period_box["width"] <= form_box["x"] + form_box["width"] + 0.5

                    if language == "en":
                        if viewport["width"] <= 860:
                            page.locator("#menu-button").click()
                        page.locator('.nav-item[data-view="overview"]').click()
                        screenshot = tmp_path / f"dashboard-{engine}-{name}.png"
                        page.screenshot(path=str(screenshot), full_page=False)
                        screenshots[name] = _assert_screenshot(screenshot, viewport)

                    context.close()
        finally:
            browser.close()

    assert len(set(screenshots.values())) == len(VIEWPORTS)

