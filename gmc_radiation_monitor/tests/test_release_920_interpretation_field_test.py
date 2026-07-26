from __future__ import annotations

import json
import math
import shutil
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

from gmc_bridge.field_test_protocol import build_field_test_protocol, field_test_protocol_json
from gmc_bridge.history import HistoryStore
from gmc_bridge.long_term_analysis import MINIMUM_REQUIREMENTS, WINDOW_MINIMUM_COVERAGE, build_long_term_analysis
from gmc_bridge.long_term_web import render_long_term_analysis
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.report_web_http import ReportRequestHandler
from gmc_bridge.translations import Translator, validate_catalogs

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "rootfs/usr/local/lib/gmc_bridge"


def _store(tmp_path: Path, *, days: int, missing_every: int = 0) -> HistoryStore:
    store = HistoryStore(tmp_path / f"history-{days}-{missing_every}.sqlite3", retention_days=730)
    start = 1_760_000_000
    rows = []
    for hour in range(days * 24):
        if missing_every and hour % missing_every == 0:
            continue
        rows.append((
            "SERIAL-920",
            start + hour * 3600,
            18.0 + 2.0 * math.sin(2.0 * math.pi * (hour % 24) / 24.0) + hour / (365 * 24),
            19.0 + 4.0 * math.sin(2.0 * math.pi * (hour % 24) / 24.0),
            1012.0 + 7.0 * math.sin(2.0 * math.pi * hour / (24.0 * 6.0)),
            "normal",
        ))
    with store._connect() as connection:
        connection.executemany(
            "INSERT INTO measurements(device_serial,timestamp_utc,cpm,temperature_c,pressure_hpa,cpm_quality) VALUES(?,?,?,?,?,?)",
            rows,
        )
        connection.commit()
    store.upsert_device_registry(
        "SERIAL-920",
        {
            "configured_name": "Long-term reference counter",
            "device_model": "GMC-500+",
            "device_version": "2.20",
            "runtime_online": True,
            "scan_interval_seconds": 3600,
            "stored_samples": len(rows),
            "app_started_at": start,
            "serial_error_count": 2,
            "serial_reconnect_count": 3,
            "history_write_error_count": 1,
            "gmcmap_enabled": True,
            "gmcmap_upload_status": "ok",
            "gmcmap_upload_success_count": 17,
            "gmcmap_upload_error_count": 2,
            "gmcmap_consecutive_error_count": 0,
        },
    )
    return store


def _analysis(store: HistoryStore) -> dict:
    return build_long_term_analysis(
        store,
        device_serial="SERIAL-920",
        scan_interval_seconds=3600,
        cpm_per_usvh=154.0,
        timezone_name="Europe/Berlin",
        warning_cpm=51.0,
        danger_cpm=100.0,
        minimum_coverage_percent=80.0,
        maximum_days=730,
    )


def test_920_conservative_minimum_requirements_and_annual_projection(tmp_path: Path) -> None:
    short = _analysis(_store(tmp_path / "short", days=20))
    assert WINDOW_MINIMUM_COVERAGE["24h"] == 90.0
    assert MINIMUM_REQUIREMENTS["trend"]["days"] == 30.0
    assert MINIMUM_REQUIREMENTS["annual_projection"]["days"] == 90.0
    assert short["trend"]["evidence"]["level"] == "not_evaluable"
    assert short["dose"]["annual_projection_usv"] is None

    long = _analysis(_store(tmp_path / "long", days=100))
    assert long["windows"]["90d"]["ready"] is True
    assert long["dose"]["annual_projection_usv"] is not None
    assert long["dose"]["projection_basis_days"] == 90
    assert long["trend"]["evidence"]["level"] in {
        "not_evaluable", "exploratory", "preliminary", "supported", "well_supported"
    }
    if long["trend"]["evidence"]["level"] == "not_evaluable":
        assert "effective_sample_size" in long["trend"]["evidence"]["reasons"]
    assert long["trend"]["effect"]["percent_per_month"] is not None


def test_920_environment_requires_pairs_and_uses_fdr(tmp_path: Path) -> None:
    short = _analysis(_store(tmp_path / "short-env", days=3))
    temperature = short["environment"]["temperature"]
    assert temperature["available"] is False
    assert temperature["minimum_pairs"] == 100
    assert temperature["evidence"]["level"] == "not_evaluable"

    sufficient = _analysis(_store(tmp_path / "long-env", days=8))
    temperature = sufficient["environment"]["temperature"]
    assert temperature["available"] is True
    assert temperature["fdr_method"] == "Benjamini-Hochberg"
    assert temperature["best"]["pairs"] >= 100
    assert "p_value_fdr" in temperature["best"]
    assert temperature["causal"] is False


def test_920_field_test_protocol_contains_endurance_counters_and_serialises(tmp_path: Path) -> None:
    store = _store(tmp_path, days=4, missing_every=11)
    protocol = build_field_test_protocol(
        store, device_serial="SERIAL-920", timezone_name="Europe/Berlin"
    )
    assert protocol["schema"] == "gmc-field-test-protocol-v1"
    assert protocol["runtime"]["serial_reconnect_count"] == 3
    assert protocol["runtime"]["history_write_error_count"] == 1
    assert protocol["history"]["gap_count"] > 0
    assert protocol["history"]["longest_gap_seconds"] >= 7200
    assert protocol["gmcmap"]["successful_uploads"] == 17
    assert "continuous_30_day_operation" in protocol["field_test_checklist"]
    assert protocol["interpretation"]["does_not_certify_measurement_accuracy"] is True
    decoded = json.loads(field_test_protocol_json(
        store, device_serial="SERIAL-920", timezone_name="Europe/Berlin"
    ))
    assert decoded["device"]["serial"] == "SERIAL-920"


def test_920_field_test_http_download(tmp_path: Path) -> None:
    store = _store(tmp_path, days=2)
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=3600,
        read_gyro=False,
        cpm_per_usvh=154.0,
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
    server.app = app  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{server.server_port}/api/v1/field-test-protocol?device=SERIAL-920",
            timeout=5,
        ) as response:
            payload = json.loads(response.read())
            disposition = response.headers.get("Content-Disposition", "")
        assert payload["device"]["serial"] == "SERIAL-920"
        assert disposition.startswith('attachment; filename="gmc-field-test-')
        assert disposition.endswith('.json"')
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_920_presentation_is_plain_first_collapsible_and_not_duplicated(tmp_path: Path) -> None:
    result = _analysis(_store(tmp_path, days=100))
    page = render_long_term_analysis(
        result,
        timezone=ZoneInfo("Europe/Berlin"),
        t=Translator("de"),
        device_label="Sehr langer GMC Referenzzählername · SERIAL-920",
    )
    assert page.count('id="long-term-analysis"') == 1
    assert "Verständliche Zusammenfassung" in page
    assert "Feldtestprotokoll exportieren" in page
    assert page.count("<details") >= 7
    # Only the overview is expanded by default; methodological groups remain collapsed.
    assert page.count("<details class=\"analysis-group long-term-group\" open>") == 1
    assert "Benjamini-Hochberg" in page
    assert "Korrelation beweist keine Kausalität" in page
    assert validate_catalogs() == []


@pytest.mark.skipif(shutil.which("chromium") is None, reason="Chromium is not installed")
def test_920_all_languages_and_responsive_layout_without_overlap(tmp_path: Path) -> None:
    playwright = pytest.importorskip("playwright.sync_api")
    result = _analysis(_store(tmp_path, days=100))
    css = (LIB / "static/dashboard.css").read_text(encoding="utf-8")
    with playwright.sync_playwright() as api:
        browser = api.chromium.launch(
            headless=True,
            executable_path=shutil.which("chromium"),
            args=["--no-sandbox", "--disable-dev-shm-usage"],
        )
        page = browser.new_page()
        try:
            for language in ("de", "en", "es", "fr", "hr", "it", "nl", "pl"):
                section = render_long_term_analysis(
                    result,
                    timezone=ZoneInfo("Europe/Berlin"),
                    t=Translator(language),
                    device_label="GMC-500+ · Very long physical reference counter identifier SERIAL-920-123456789",
                )
                for width, height, zoom in ((320, 700, "100%"), (390, 844, "200%"), (768, 1024, "100%"), (1440, 1000, "100%")):
                    page.set_viewport_size({"width": width, "height": height})
                    page.set_content(
                        f"<!doctype html><html lang='{language}'><meta charset='utf-8'><style>{css} html{{font-size:{zoom}}}</style><main>{section}</main></html>",
                        wait_until="domcontentloaded",
                    )
                    page.locator("details").evaluate_all("els => els.forEach(el => { el.open = true; })")
                    layout = page.evaluate(
                        """() => {
                          const known = '.calendar-scroll,.long-term-table-wrap';
                          const leaks = [...document.querySelectorAll('.plain-assessment,.long-term-card,.analysis-group')]
                            .filter(el => !el.closest(known))
                            .filter(el => el.scrollWidth > el.clientWidth + 2)
                            .map(el => ({cls: el.className, excess: el.scrollWidth - el.clientWidth}));
                          const overlaps = [...document.querySelectorAll('.long-term-card,.plain-assessment article')]
                            .filter(el => {
                              const children=[...el.children].filter(x => getComputedStyle(x).position !== 'absolute');
                              return children.some((a,i) => children.slice(i+1).some(b => {
                                const ar=a.getBoundingClientRect(), br=b.getBoundingClientRect();
                                return Math.min(ar.right,br.right)-Math.max(ar.left,br.left)>2 && Math.min(ar.bottom,br.bottom)-Math.max(ar.top,br.top)>2;
                              }));
                            }).length;
                          return {pageExcess: document.documentElement.scrollWidth-document.documentElement.clientWidth, leaks, overlaps};
                        }"""
                    )
                    assert layout["pageExcess"] <= 1, (language, width, zoom, layout)
                    assert layout["leaks"] == [], (language, width, zoom, layout)
                    assert layout["overlaps"] == 0, (language, width, zoom, layout)
        finally:
            page.close()
            browser.close()
