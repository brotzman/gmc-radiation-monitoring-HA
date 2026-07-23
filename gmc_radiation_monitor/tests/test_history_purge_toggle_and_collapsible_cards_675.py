from __future__ import annotations

import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication, ReportRequestHandler
from gmc_bridge.runtime_options import runtime_environment


def _app(tmp_path: Path, *, purge_enabled: bool) -> ReportApplication:
    store = HistoryStore(tmp_path / "history.sqlite3")
    store.upsert_device_registry(
        "SERIAL-A",
        {
            "device_model": "GMC-320",
            "configured_name": "GMC-320",
            "runtime_online": True,
            "scan_interval_seconds": 60,
        },
    )
    store.insert_measurement(
        {"cpm": 12, "temperature_c": 21.0, "voltage_v": 4.2},
        device_serial="SERIAL-A",
        timestamp_utc=1_800_000_000,
    )
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
        history_management_enabled=purge_enabled,
    )


def test_purge_controls_are_replaced_by_disabled_notice_and_no_token_is_issued(tmp_path: Path) -> None:
    app = _app(tmp_path, purge_enabled=False)
    page = app.render_index(language_override="de", mode_override="advanced").decode()
    assert "Gesamten GMC-Verlauf löschen" not in page
    assert "Gefahrenbereich" not in page
    assert 'action="?action=purge-all-history"' not in page
    assert "Historie löschen" in page
    assert "Das Löschen ist standardmäßig deaktiviert." in page
    assert "Historienverwaltung" in page
    assert app.csrf_tokens.consume("", "purge-all-history").valid is False


def test_direct_purge_request_is_forbidden_when_disabled(tmp_path: Path) -> None:
    app = _app(tmp_path, purge_enabled=False)
    server = ThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
    server.app = app
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        request = urllib.request.Request(
            f"http://127.0.0.1:{server.server_port}/?action=purge-all-history",
            data=b"confirm=DELETE+ALL+GMC+HISTORY&csrf_token=not-issued",
            method="POST",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
        try:
            urllib.request.urlopen(request, timeout=5)
        except urllib.error.HTTPError as exc:
            assert exc.code == 403
            assert "disabled" in exc.read().decode().lower()
        else:
            raise AssertionError("disabled purge route unexpectedly accepted the request")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_purge_card_is_rendered_when_enabled(tmp_path: Path) -> None:
    page = (
        _app(tmp_path, purge_enabled=True)
        .render_index(language_override="de", mode_override="advanced")
        .decode()
    )
    assert "Gesamten GMC-Verlauf löschen" in page
    assert "Gefahrenbereich" in page
    assert 'action="?action=purge-all-history"' in page


def test_runtime_option_controls_purge_feature() -> None:
    disabled = runtime_environment({"devices": [{}], "history": {}}, "reports")
    enabled = runtime_environment({"devices": [{}], "history": {"history_management_enabled": True}}, "reports")
    assert disabled["HISTORY_MANAGEMENT_ENABLED"] == "false"
    assert enabled["HISTORY_MANAGEMENT_ENABLED"] == "true"
    assert enabled["ENABLE_RESTORE"] == "true"
    assert enabled["ENABLE_PURGE_ALL_HISTORY"] == "true"


def test_requested_main_cards_are_collapsible(tmp_path: Path) -> None:
    page = (
        _app(tmp_path, purge_enabled=False)
        .render_index(language_override="de", mode_override="advanced", device_override="SERIAL-A")
        .decode()
    )
    expected = {
        "devices": "Verbundene GMC-Geräte",
        "radiation-intelligence": "Intelligente Strahlungsanalyse",
        "adaptive-background": "Adaptives Hintergrundprofil",
        "cosmic-influence": "Kosmischer Einfluss – statistischer Hinweis",
        "fleet-intelligence": "Geräteverbund-Auswertung",
    }
    for card_id, title in expected.items():
        marker = f'<details class="card collapsible-card" id="{card_id}"'
        assert marker in page
        card = page.split(marker, 1)[1].split("</details>", 1)[0]
        assert " open>" in card[:250]
        assert f"<h2>{title}</h2>" in card


def test_device_live_refresh_updates_fields_without_replacing_details() -> None:
    source = (Path(__file__).parents[1] / "rootfs/usr/local/lib/gmc_bridge/static/dashboard.js").read_text()
    assert "./api/live-devices" in source
    assert "updateLiveCard" in source
    assert "replaceWith" not in source
