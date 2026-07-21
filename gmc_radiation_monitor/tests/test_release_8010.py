from __future__ import annotations

from pathlib import Path

import yaml
from gmc_bridge.version import APP_VERSION
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent


def test_release_version_and_current_notes() -> None:
    assert APP_VERSION == "8.3.2"
    assert yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))["version"] == "8.3.2"
    assert (ROOT / "RELEASE_NOTES_8.3.2.md").is_file()


def test_only_current_release_notes_are_distributed() -> None:
    notes = sorted(path.name for path in ROOT.glob("RELEASE_NOTES_*.md"))
    assert notes == ["RELEASE_NOTES_8.3.2.md"]


def test_all_eight_manuals_and_embedded_versions_are_current() -> None:
    from gmc_bridge.report_web import USER_MANUAL_DIRECTORY, USER_MANUAL_FILENAMES

    expected_languages = {"de", "en", "es", "fr", "it", "nl", "pl", "hr"}
    assert set(USER_MANUAL_FILENAMES) == expected_languages
    packaged = sorted(USER_MANUAL_DIRECTORY.glob("*.pdf"))
    assert {path.name for path in packaged} == set(USER_MANUAL_FILENAMES.values())

    for language, filename in USER_MANUAL_FILENAMES.items():
        assert APP_VERSION in filename
        path = USER_MANUAL_DIRECTORY / filename
        reader = PdfReader(path)
        assert not reader.is_encrypted
        assert len(reader.pages) >= 15
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        assert APP_VERSION in text, f"missing {APP_VERSION} in {language} manual"
        assert "8.0.10" not in text, f"stale version in {language} manual"
        metadata = " ".join(str(value) for value in (reader.metadata or {}).values())
        assert "8.0.10" not in metadata


def test_current_version_references_are_consistent() -> None:
    current_files = (
        ROOT / "config.yaml",
        ROOT / "README.md",
        ROOT / f"RELEASE_NOTES_{APP_VERSION}.md",
        ROOT / "rootfs/usr/local/lib/gmc_bridge/version.py",
    )
    for path in current_files:
        assert APP_VERSION in path.read_text(encoding="utf-8"), path
    assert not list((ROOT / "rootfs/usr/local/share/gmc-bridge/docs").glob("*8.0.10*.pdf"))
    assert (
        (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").startswith(f"# Changelog\n\n## {APP_VERSION}\n")
    )


def test_serial_and_screenshot_test_policies_are_fixed() -> None:
    conftest = (ROOT / "tests/conftest.py").read_text(encoding="utf-8")
    workflow = (REPO_ROOT / ".github/workflows/quality.yml").read_text(encoding="utf-8")
    assert "SERIAL_TEST_TIMEOUT_SECONDS = 30" in conftest
    assert "serial test exceeded the fixed" in conftest
    assert "-name '*serial*.py' -o -name 'test_simulated_hardware_matrix_8011.py'" in workflow
    assert "timeout --signal=TERM --kill-after=10s 180s coverage run" in workflow
    assert "test_responsive_browser_matrix_8011.py" in workflow
    assert "playwright install --with-deps chromium firefox webkit" in workflow


def test_ignore_files_protect_clean_releases() -> None:
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")
    dockerignore = (ROOT / ".dockerignore").read_text(encoding="utf-8")
    assert "__pycache__/" in gitignore
    assert ".pytest_cache/" in gitignore
    assert "**/__pycache__" in dockerignore
    assert "tests" in dockerignore


def _dashboard_app(tmp_path: Path):
    from gmc_bridge.history import HistoryStore
    from gmc_bridge.report_web import ReportApplication

    store = HistoryStore(tmp_path / "history.sqlite3")
    store.upsert_device_registry(
        "SERIAL-802",
        {
            "device_model": "GMC-500+",
            "configured_name": "GMC-500+",
            "runtime_online": True,
            "scan_interval_seconds": 60,
        },
    )
    store.insert_measurement({"cpm": 17}, device_serial="SERIAL-802", timestamp_utc=1_800_000_000)
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
        ui_mode="advanced",
    )


def test_dashboard_cleanup_keeps_status_overview_and_removes_duplicate_ui(tmp_path: Path) -> None:
    app = _dashboard_app(tmp_path)
    page = app.render_index(language_override="de", mode_override="advanced").decode()

    status = page.split('<section class="status-strip"', 1)[1].split("</section>", 1)[0]
    assert status.count('class="status-strip-item') == 6
    assert "Geführter Status" not in page
    assert "Konfigurations-Vorabprüfung" not in page
    assert "JSON der Konfigurationsprüfung öffnen" not in page
    assert 'class="recommendation-card' not in page
    assert "Was sollte ich tun?" in page
    assert (
        page.count(
            "Die absolute Bewertung ist derzeit unkritisch. Für eine zuverlässige Anomalieerkennung werden mehr lokale Verlaufsdaten benötigt."
        )
        == 1
    )
    assert 'href="#history"' in page
    assert 'id="history"' in page
    assert "Ansicht" in page
    assert "Bestimmt, wie viele Details und Werkzeuge auf dieser Seite angezeigt werden." in page
    assert "Gerätestatus aktualisiert" not in page
    assert "Gerätestatus wird aktualisiert" not in page
    assert 'id="device-refresh-status"' not in page
    assert 'class="location-details external-map-link"' in page
    assert 'href="https://www.gmcmap.com/index.php"' in page
    assert 'class="location-details manual-link"' in page
    assert 'href="./docs/user-manual.pdf?lang=de"' in page
    assert "Benutzerhandbuch" in page
    assert "PDF · Version 8.3.2 · Deutsch" in page
    for language, native_name in {
        "en": "English",
        "es": "Español",
        "fr": "Français",
        "it": "Italiano",
        "nl": "Nederlands",
        "pl": "Polski",
        "hr": "Hrvatski",
    }.items():
        localized_page = app.render_index(language_override=language, mode_override="advanced").decode()
        assert f'href="./docs/user-manual.pdf?lang={language}"' in localized_page
        assert f"PDF · Version 8.3.2 · {native_name}" in localized_page
    assert page.index('class="header-resource-links"') < page.index('id="analysis-level-panel"')
    assert page.index('class="location-details external-map-link"') < page.index(
        'class="location-details manual-link"'
    )
    assert page.index('id="analysis-level-panel"') < page.index('class="status-strip"')
    assert page.index('class="status-strip"') < page.index('id="dashboard-controls"')
    assert page.index('id="history"') < page.index('id="workflow"') < page.index('id="reports"')
    assert 'id="toggle-all-cards"' in page
    assert 'id="expand-all-cards"' not in page
    assert 'id="collapse-all-cards"' not in page
    assert '<details class="analysis-group" id="workflow-notifications" open>' not in page
    assert '<details class="analysis-group" id="workflow-comparison" open>' not in page
    assert '<details class="analysis-group" id="history-explorer" open>' in page
    assert "Messwerte als CSV" in page
    assert "Original-Rohdaten als CSV" in page
    assert 'id="database-backup-link"' not in page
    assert page.index("Erzeugte Berichte") > page.index('<section id="reports">')
    maintenance = page.split('id="maintenance"', 1)[1].split("</section>", 1)[
        0
    ]
    assert "<h3>Verwaltete Sicherungen</h3>" in maintenance


def test_dashboard_cleanup_css_preserves_spacing_and_single_line_desktop_controls() -> None:
    from gmc_bridge.web_assets import DASHBOARD_CSS

    assert "grid-template-columns:minmax(270px,1.55fr) repeat(4,minmax(125px,1fr))" in DASHBOARD_CSS
    assert ".assessment-grid.baseline-grid .assessment-primary { padding-right:1.15rem; }" in DASHBOARD_CSS
    assert (
        ".dashboard-controls { position:sticky; top:0; z-index:50; display:flex; justify-content:space-between; align-items:center; gap:.75rem; flex-wrap:nowrap;"
        in DASHBOARD_CSS
    )
    assert (
        ".analysis-level-panel > div:first-child { display:grid; gap:.18rem; min-width:0; flex:1 1 22rem; }"
        in DASHBOARD_CSS
    )
    assert (
        ".analysis-level-buttons { display:flex; align-items:center; gap:.5rem; flex:0 0 auto; flex-wrap:nowrap; }"
        in DASHBOARD_CSS
    )
    assert ".refresh-indicator" not in DASHBOARD_CSS
    assert (
        ".header-resource-links { display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:.7rem; }"
        in DASHBOARD_CSS
    )
    assert "@media (max-width: 620px)" in DASHBOARD_CSS
    assert ".header-resource-links { grid-template-columns:1fr; }" in DASHBOARD_CSS
    assert ".analysis-level-panel > div:first-child { flex:0 0 auto; }" in DASHBOARD_CSS


def test_generated_report_delete_form_and_endpoint(tmp_path: Path) -> None:
    import re
    import urllib.parse
    import urllib.request
    from http.server import ThreadingHTTPServer
    from threading import Thread

    from gmc_bridge.report_web import ReportRequestHandler

    app = _dashboard_app(tmp_path)
    report = app.scheduled_report_directory / "gmc-daily-802.zip"
    report.write_bytes(b"scheduled report")
    page = app.render_index(language_override="de", mode_override="advanced").decode()
    form = re.search(
        r'action="\?action=scheduled-report-delete".*?name="csrf_token" value="([^"]+)".*?name="name" value="gmc-daily-802\.zip"',
        page,
        re.S,
    )
    assert form is not None
    assert "Diesen erzeugten Bericht löschen?" in page

    server = ThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
    server.app = app
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        body = urllib.parse.urlencode({"csrf_token": form.group(1), "name": report.name}).encode()
        request = urllib.request.Request(
            f"http://127.0.0.1:{server.server_port}/?action=scheduled-report-delete&lang=de",
            data=body,
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            assert response.status == 200
        assert not report.exists()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_scheduled_report_delete_reuses_strict_path_validation(tmp_path: Path) -> None:
    import pytest

    app = _dashboard_app(tmp_path)
    with pytest.raises(ValueError):
        app.delete_scheduled_report("../outside.zip")


def test_user_manual_pdfs_are_packaged_and_served_inline(tmp_path: Path) -> None:
    import urllib.request
    from http.server import ThreadingHTTPServer
    from threading import Thread

    from gmc_bridge.report_web import (
        USER_MANUAL_DIRECTORY,
        USER_MANUAL_FILENAMES,
        USER_MANUAL_PATH,
        ReportRequestHandler,
    )

    assert USER_MANUAL_PATH.is_file()
    assert set(USER_MANUAL_FILENAMES) == {"de", "en", "es", "fr", "it", "nl", "pl", "hr"}
    for filename in USER_MANUAL_FILENAMES.values():
        manual_path = USER_MANUAL_DIRECTORY / filename
        assert manual_path.is_file()
        assert manual_path.read_bytes().startswith(b"%PDF-")

    app = _dashboard_app(tmp_path)
    server = ThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
    server.app = app
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        for language, filename in USER_MANUAL_FILENAMES.items():
            request = urllib.request.Request(
                f"http://127.0.0.1:{server.server_port}/docs/user-manual.pdf?lang={language}"
            )
            with urllib.request.urlopen(request, timeout=5) as response:
                payload = response.read()
                assert response.status == 200
                assert response.headers.get_content_type() == "application/pdf"
                assert response.headers["Content-Disposition"].startswith("inline;")
                assert filename in response.headers["Content-Disposition"]
                assert response.headers["Cross-Origin-Resource-Policy"] == "same-origin"
                assert payload.startswith(b"%PDF-")

        # The original German URL remains available for backwards compatibility.
        with urllib.request.urlopen(
            f"http://127.0.0.1:{server.server_port}/docs/benutzerhandbuch.pdf", timeout=5
        ) as response:
            assert USER_MANUAL_FILENAMES["de"] in response.headers["Content-Disposition"]
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
