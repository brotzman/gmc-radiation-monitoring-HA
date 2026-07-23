from __future__ import annotations

import re
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication, ReportRequestHandler


def _app(tmp_path: Path, *, purge_enabled: bool = False) -> ReportApplication:
    store = HistoryStore(tmp_path / "history.sqlite3")
    for serial, model, cpm in (
        ("SERIAL-320", "GMC-320", 14),
        ("SERIAL-500", "GMC-500+", 16),
    ):
        store.upsert_device_registry(
            serial,
            {
                "device_model": model,
                "configured_name": model,
                "runtime_online": True,
                "scan_interval_seconds": 60,
                "device_health_status": "ok",
            },
        )
        store.insert_measurement(
            {"cpm": cpm, "temperature_c": 22.0, "voltage_v": 4.1},
            device_serial=serial,
            timestamp_utc=1_800_000_000 + cpm,
        )
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
        restore_enabled=False,
        purge_all_history_enabled=purge_enabled,
    )


def test_header_counters_are_consolidated_into_live_status(tmp_path: Path) -> None:
    page = _app(tmp_path).render_index(language_override="de", mode_override="advanced").decode()
    assert 'class="info-chip"' not in page
    assert '<div class="info-chips"' not in page
    status = page.split('<section class="status-strip"', 1)[1].split("</section>", 1)[0]
    assert status.count('class="status-strip-item') == 6
    assert "Gespeicherte Messwerte" in status
    assert status.index("Gespeicherte Messwerte") < status.index("Datenbank")


def test_dashboard_script_uses_nonce_and_controls_are_registered_early(tmp_path: Path) -> None:
    page = _app(tmp_path).render_index(language_override="de", mode_override="advanced").decode()
    nonce_match = re.search(r'<script nonce="([A-Za-z0-9_-]+)">', page)
    assert nonce_match is not None
    script = page.split(nonce_match.group(0), 1)[1].split("</script>", 1)[0]
    assert "function setAllCards(open)" in script
    assert "function jumpToSection(selector)" in script
    assert "event.target.closest('#toggle-all-cards')" in script
    assert "function updateToggleAllButton()" in script
    assert "preferences.groups" in script
    assert 'event.target.closest(\'.jump-links a[href^="#"], .status-strip a[href^="#"]\')' in script
    assert script.index("function setAllCards(open)") < script.index(
        "document.querySelectorAll('a[href*=\"action=download\"]')"
    )


def test_html_response_csp_authorizes_only_its_generated_script_nonce(tmp_path: Path) -> None:
    app = _app(tmp_path)
    server = ThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
    server.app = app
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{server.server_port}/?lang=de&mode=advanced", timeout=10
        ) as response:
            page = response.read().decode()
            csp = response.headers["Content-Security-Policy"]
        nonce = re.search(r'<script nonce="([A-Za-z0-9_-]+)">', page)
        assert nonce is not None
        assert f"script-src 'nonce-{nonce.group(1)}'" in csp
        assert "script-src 'unsafe-inline'" not in csp
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_analysis_and_custom_report_layout_selectors_target_card_body(tmp_path: Path) -> None:
    page = _app(tmp_path).render_index(language_override="de", mode_override="advanced").decode()
    assert "#adaptive-background .collapsible-card-body > .assessment-grid" in page
    assert "#adaptive-background .collapsible-card-body > .metrics" in page
    assert "#cosmic-influence .collapsible-card-body > .assessment-grid" in page
    assert "#cosmic-influence .collapsible-card-body > .metrics" in page
    assert "#adaptive-background > .assessment-grid" not in page
    assert "#cosmic-influence > .assessment-grid" not in page
    assert ".custom-form .form-grid { grid-template-columns:minmax(0,1.35fr) minmax(8rem,.65fr); }" in page
    assert (
        ".custom-form .form-actions { grid-column:1 / -1; display:grid; grid-template-columns:minmax(10rem,16rem);"
        in page
    )


def test_disabled_deletion_notice_occupies_the_maintenance_position(tmp_path: Path) -> None:
    page = (
        _app(tmp_path, purge_enabled=False)
        .render_index(language_override="de", mode_override="advanced")
        .decode()
    )
    maintenance = page.split('id="maintenance"', 1)[1].split("</section>", 1)[
        0
    ]
    assert "Historie wiederherstellen" in maintenance
    assert "Historie löschen" in maintenance
    assert "Das Löschen ist standardmäßig deaktiviert." in maintenance
    assert "Historienverwaltung" in maintenance
    assert "Vollständiges Löschen erlauben" not in maintenance
    assert 'action="?action=purge-all-history"' not in maintenance


def test_status_stays_at_top_and_only_navigation_is_sticky(tmp_path: Path) -> None:
    page = _app(tmp_path).render_index(language_override="de", mode_override="advanced").decode()
    assert 'id="floating-dashboard-tools"' not in page
    assert page.index('<section class="status-strip"') < page.index('<nav class="dashboard-controls"')
    assert ".status-strip { position:static;" in page
    assert ".dashboard-controls { position:sticky; top:0; z-index:50;" in page
    assert ".dashboard-controls { position:-webkit-sticky; position:sticky;" in page
    assert "top:env(safe-area-inset-top,0px)" in page
    assert "dashboardControls.getBoundingClientRect().height + 12" in page


def test_adaptive_background_values_start_on_a_new_line_after_time(tmp_path: Path) -> None:
    from gmc_bridge.translations import Translator

    app = _app(tmp_path)
    block = app._background_profile_block(
        profile={
            "available": True,
            "typical_cpm": 15.0,
            "deviation_percent": 3.0,
            "state": "Normal for this time",
            "weekday": 3,
            "hour": 13,
            "current_cpm": 16.5,
        },
        title="Device baseline",
        t=Translator("de"),
    )
    assert "Typisch für Donnerstag um 13:00 Uhr<br>" in block
    assert '<span class="background-profile-values">15.0 CPM · +3.0%</span>' in block
