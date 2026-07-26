from __future__ import annotations

import math
import shutil
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
import yaml
from gmc_bridge.history import HistoryStore
from gmc_bridge.long_term_analysis import _aggregate_daily, build_long_term_analysis
from gmc_bridge.long_term_web import render_long_term_analysis
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import Translator, validate_catalogs
from gmc_bridge.version import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "rootfs/usr/local/lib/gmc_bridge"
DOCS = ROOT / "rootfs/usr/local/share/gmc-bridge/docs"


def _store_with_history(tmp_path: Path, *, days: int = 400, missing_every: int = 0) -> HistoryStore:
    store = HistoryStore(tmp_path / "long-term.sqlite3", retention_days=730)
    start = 1_760_000_000
    rows = []
    for hour in range(days * 24):
        if missing_every and hour % missing_every == 0:
            continue
        cpm = 20 + int(4 * math.sin(2 * math.pi * (hour % 24) / 24)) + hour // (180 * 24)
        rows.append((
            "SERIAL-LT",
            start + hour * 3600,
            cpm,
            18 + 5 * math.sin(2 * math.pi * (hour % 24) / 24),
            1013 + 8 * math.sin(2 * math.pi * hour / (24 * 8)),
            "normal",
        ))
    with store._connect() as connection:
        connection.executemany(
            "INSERT INTO measurements(device_serial,timestamp_utc,cpm,temperature_c,pressure_hpa,cpm_quality) VALUES(?,?,?,?,?,?)",
            rows,
        )
        connection.commit()
    return store


def _analysis(store: HistoryStore) -> dict:
    return build_long_term_analysis(
        store,
        device_serial="SERIAL-LT",
        scan_interval_seconds=3600,
        cpm_per_usvh=154.0,
        timezone_name="Europe/Berlin",
        warning_cpm=51.0,
        danger_cpm=100.0,
        minimum_coverage_percent=80.0,
        maximum_days=730,
    )


def test_910_release_metadata_retention_and_manual_names() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "9.3.0"
    assert config["version"] == "9.3.0"
    assert config["options"]["history"]["retention_days"] == 730
    assert sorted(path.name for path in ROOT.glob("RELEASE_NOTES_*.md")) == [
        "RELEASE_NOTES_9.3.0.md"
    ]
    manuals = sorted(DOCS.glob("*.pdf"))
    assert len(manuals) == 8
    assert all("9.3.0" in path.name for path in manuals)


def test_manuals_are_clean_current_editions() -> None:
    pypdf = pytest.importorskip("pypdf")
    for path in sorted(DOCS.glob("*.pdf")):
        reader = pypdf.PdfReader(str(path))
        text = "\n".join((page.extract_text() or "") for page in reader.pages)
        assert len(reader.pages) >= 15
        first_pages = "\n".join((page.extract_text() or "") for page in reader.pages[:9])
        assert "9.3.0" in first_pages
        for stale in ("8.0.10", "8.3.2", "9.0.2", "9.0.3"):
            assert stale not in text
        assert "Bland-Altman" in text

def test_real_windows_require_duration_and_coverage(tmp_path: Path) -> None:
    store = _store_with_history(tmp_path, days=20)
    result = _analysis(store)
    assert result["windows"]["24h"]["ready"] is True
    assert result["windows"]["7d"]["ready"] is True
    assert result["windows"]["30d"]["ready"] is False
    assert result["windows"]["30d"]["reason"] == "insufficient_duration"
    assert result["windows"]["30d"]["minimum_coverage_percent"] == 80.0


def test_long_term_statistics_dose_trend_and_episodes(tmp_path: Path) -> None:
    result = _analysis(_store_with_history(tmp_path, days=400))
    assert result["available"] is True
    assert all(result["windows"][name]["ready"] for name in ("24h", "7d", "30d", "90d", "365d"))
    assert result["dose"]["total_usv"] is not None
    assert result["dose"]["annual_projection_usv"] is not None
    assert result["effective_sample_size"]["available"] is True
    assert result["bootstrap"]["available"] is True
    assert result["trend"]["available"] is True
    assert result["trend"]["direction"] == "increasing"
    assert result["control_chart"]["statistical_only"] is True
    assert result["environment"]["temperature"]["causal"] is False
    assert len(result["calendar"]) <= 366
    assert len(result["daily"]) <= 730


def test_gaps_are_not_interpolated_and_can_block_readiness(tmp_path: Path) -> None:
    result = _analysis(_store_with_history(tmp_path, days=40, missing_every=3))
    thirty = result["windows"]["30d"]
    assert thirty["coverage_percent"] < 80.0
    assert thirty["ready"] is False
    assert thirty["reason"] == "insufficient_coverage"
    assert result["notes"]["no_interpolation"] is True


def test_daily_coverage_uses_actual_dst_day_length() -> None:
    timezone = ZoneInfo("Europe/Berlin")
    spring_start = 1_774_738_800  # 2026-03-28 23:00 UTC / local midnight
    spring_points = [
        {
            "timestamp_utc": spring_start + hour * 3600,
            "mean_cpm": 20.0,
            "covered_seconds": 3600.0,
            "dose_usv": 0.1,
        }
        for hour in range(23)
    ]
    fall_start = 1_792_879_200  # 2026-10-24 22:00 UTC / local midnight
    fall_points = [
        {
            "timestamp_utc": fall_start + hour * 3600,
            "mean_cpm": 20.0,
            "covered_seconds": 3600.0,
            "dose_usv": 0.1,
        }
        for hour in range(25)
    ]
    spring = _aggregate_daily(spring_points, timezone)
    fall = _aggregate_daily(fall_points, timezone)
    assert len(spring) == 1
    assert len(fall) == 1
    assert spring[0]["expected_hours"] == 23.0
    assert fall[0]["expected_hours"] == 25.0
    assert spring[0]["coverage_percent"] == pytest.approx(100.0)
    assert fall[0]["coverage_percent"] == pytest.approx(100.0)


def test_long_term_html_is_localised_and_separate_from_recent_baseline(tmp_path: Path) -> None:
    result = _analysis(_store_with_history(tmp_path, days=40))
    for language, marker in {
        "en": "Long-term analysis",
        "de": "Langzeitanalyse",
        "fr": "Analyse à long terme",
        "es": "Análisis a largo plazo",
        "it": "Analisi a lungo termine",
        "nl": "Langetermijnanalyse",
        "pl": "Analiza długoterminowa",
        "hr": "Dugoročna analiza",
    }.items():
        page = render_long_term_analysis(
            result,
            timezone=ZoneInfo("Europe/Berlin"),
            t=Translator(language),
            device_label="GMC-320 · SERIAL-LT",
        )
        assert marker in page
        assert 'id="long-term-analysis"' in page
        assert "Long-term analysis for {device}" not in page
        assert Translator(language)("Seasonal month-of-year profile") in page
    presentation = (LIB / "analysis_presentation.py").read_text(encoding="utf-8")
    assert 'title_key="Recent baseline context"' in presentation
    assert 'title_key="Long-term context"' not in presentation
    assert validate_catalogs() == []


def test_long_term_css_has_mobile_wrapping_and_internal_scroll() -> None:
    css = (LIB / "static/dashboard.css").read_text(encoding="utf-8")
    compact = "".join(css.split())
    for phrase in (
        ".long-term-card{min-width:0",
        ".calendar-scroll{max-width:100%;overflow-x:auto",
        ".long-term-table-wrap{max-width:100%",
        "@media(max-width:430px)",
        ".long-term-window-grid,.long-term-grid{grid-template-columns:1fr",
        ".long-term-value{font-size:clamp(1.05rem,1.6vw,1.34rem)",
        ".long-term-card.window-card.pending.long-term-value{font-size:clamp(1rem,1.45vw,1.18rem)",
    ):
        assert phrase in compact


@pytest.mark.skipif(shutil.which("chromium") is None, reason="Chromium is not installed")
def test_long_term_section_has_no_page_overflow_at_mobile_and_desktop(tmp_path: Path) -> None:
    playwright = pytest.importorskip("playwright.sync_api")
    result = _analysis(_store_with_history(tmp_path, days=40))
    section = render_long_term_analysis(
        result,
        timezone=ZoneInfo("Europe/Berlin"),
        t=Translator("de"),
        device_label="Sehr langer Geräteanzeigename GMC-500+ · SERIAL-LT-0123456789",
    )
    css = (LIB / "static/dashboard.css").read_text(encoding="utf-8")
    document = f"<!doctype html><meta charset='utf-8'><style>{css}</style><main>{section}</main>"
    with playwright.sync_playwright() as api:
        browser = api.chromium.launch(headless=True, executable_path=shutil.which("chromium"))
        page = browser.new_page()
        for width, height in ((320, 700), (390, 844), (768, 1024), (1440, 1000)):
            page.set_viewport_size({"width": width, "height": height})
            page.set_content(document, wait_until="domcontentloaded")
            sizes = page.evaluate(
                """() => ({
                    regular: parseFloat(getComputedStyle(document.querySelector('.window-card.good .long-term-value')).fontSize),
                    pending: parseFloat(getComputedStyle(document.querySelector('.window-card.pending .long-term-value')).fontSize),
                    standard: parseFloat(getComputedStyle(document.querySelector('.metric .value') || document.documentElement).fontSize)
                })"""
            )
            assert sizes["regular"] <= 21.5
            assert sizes["pending"] <= 18.9
            assert sizes["pending"] <= sizes["regular"]
            overflow = page.evaluate(
                """() => ({
                    body: document.documentElement.scrollWidth - document.documentElement.clientWidth,
                    cards: [...document.querySelectorAll('.long-term-card')].filter(el => el.scrollWidth > el.clientWidth + 1).length,
                    internalScrollers: [...document.querySelectorAll('.calendar-scroll,.long-term-table-wrap')].filter(el => el.scrollWidth > el.clientWidth + 1).length
                })"""
            )
            assert overflow["body"] <= 1
            assert overflow["cards"] == 0
            if width <= 390:
                assert overflow["internalScrollers"] >= 1
        browser.close()


@pytest.mark.skipif(shutil.which("chromium") is None, reason="Chromium is not installed")
def test_full_dashboard_all_languages_mobile_desktop_and_large_text(tmp_path: Path) -> None:
    playwright = pytest.importorskip("playwright.sync_api")
    store = _store_with_history(tmp_path, days=40)
    store.upsert_device_registry(
        "SERIAL-LT",
        {
            "device_model": "GMC-500+",
            "configured_name": "Very long reference monitor name / Sehr langer Referenzmonitorname",
            "runtime_online": True,
            "scan_interval_seconds": 3600,
        },
    )
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=3600,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="en",
        ui_mode="advanced",
    )
    css = (LIB / "static/dashboard.css").read_text(encoding="utf-8")
    languages = ("de", "en", "es", "fr", "hr", "it", "nl", "pl")
    # Test every language at the narrowest supported width, then exercise
    # large text and desktop layouts in both primary manual languages.
    cases = [(language, 320, 700, "100%") for language in languages]
    cases.extend(
        (language, width, height, font_size)
        for language in ("de", "en")
        for width, height, font_size in ((390, 844, "200%"), (1440, 1000, "100%"))
    )
    with playwright.sync_playwright() as api:
        browser = api.chromium.launch(
            headless=True,
            executable_path=shutil.which("chromium"),
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = browser.new_page()
        try:
            for language, width, height, font_size in cases:
                document = app.render_index(
                    language_override=language,
                    mode_override="advanced",
                ).decode()
                page.set_viewport_size({"width": width, "height": height})
                page.set_content(document, wait_until="domcontentloaded")
                page.add_style_tag(content=css)
                page.add_style_tag(
                    content=(
                        f"html{{font-size:{font_size};}}"
                        "*{animation:none!important;transition:none!important;}"
                    )
                )
                page.locator("details").evaluate_all("els => els.forEach(el => { el.open = true; })")
                layout = page.evaluate(
                    """() => {
                        const root = document.querySelector('.page-scroll');
                        const knownScrollers = '.jump-links,.language-switcher,.table-scroll,.calendar-scroll,.long-term-table-wrap';
                        const leaking = [...document.querySelectorAll('main section, main details, .card, .long-term-card')]
                          .filter(el => !el.closest(knownScrollers))
                          .filter(el => el.scrollWidth > el.clientWidth + 12)
                          .map(el => ({id: el.id, cls: el.className, excess: el.scrollWidth - el.clientWidth}));
                        return {
                          pageExcess: root.scrollWidth - root.clientWidth,
                          leaking,
                          emptyText: [...document.querySelectorAll('button,a,summary,label')]
                            .filter(el => !el.textContent.trim() && !el.getAttribute('aria-label')).length,
                        };
                    }"""
                )
                assert page.locator("html").get_attribute("lang") == language
                assert layout["pageExcess"] <= 1, (language, width, font_size, layout)
                assert layout["leaking"] == [], (language, width, font_size, layout)
                assert layout["emptyText"] == 0
        finally:
            page.close()
            browser.close()

