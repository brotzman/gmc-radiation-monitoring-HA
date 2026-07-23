from __future__ import annotations

import json
import re
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication, ReportRequestHandler


def _store(path: Path) -> HistoryStore:
    store = HistoryStore(path)
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
                "cpm_discarded_peak_samples": 1 if "500" in serial else 0,
                "device_health_status": "ok",
            },
        )
        store.insert_measurement(
            {"cpm": cpm, "temperature_c": 22.0, "voltage_v": 4.1},
            device_serial=serial,
            timestamp_utc=1_800_000_000 + cpm,
        )
    return store


def _app(tmp_path: Path, *, restore_enabled: bool = True) -> ReportApplication:
    return ReportApplication(
        store=_store(tmp_path / "history.sqlite3"),
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
        restore_enabled=restore_enabled,
        purge_all_history_enabled=True,
    )


def test_dashboard_contains_persistent_usability_controls(tmp_path: Path) -> None:
    page = _app(tmp_path).render_index(language_override="de", mode_override="advanced").decode()
    assert 'class="status-strip"' in page
    assert 'id="dashboard-controls"' in page
    assert 'id="toggle-all-cards"' in page
    assert 'id="expand-all-cards"' not in page
    assert 'id="collapse-all-cards"' not in page
    assert 'id="preview-restore"' in page
    script = Path("rootfs/usr/local/lib/gmc_bridge/static/dashboard.js").read_text(encoding="utf-8")
    assert "gmc-dashboard-usability-v1" in script
    assert "gmc-last-backup-request-v1" not in page
    assert 'id="database-backup-link"' not in page
    assert 'id="device-refresh-status"' not in page
    assert "Gerätestatus aktualisiert" not in page
    assert "Gerätestatus wird aktualisiert" not in page
    assert 'id="recent-reports"' not in page
    assert 'id="report-presets"' not in page
    assert "gmc-recent-reports-v1" not in page
    assert "gmc-report-presets-v1" not in page
    assert "Letzte in diesem Browser angeforderte Sicherung" not in page
    assert "IntersectionObserver" in script
    assert "localStorage" in script
    assert "applyCardPreferences" in script
    assert 'class="device-card device-320' in page
    assert 'class="device-card device-500' in page
    assert "Keine aktiven Gerätewarnungen" in page


def test_backup_inspection_is_read_only_and_reports_period(tmp_path: Path) -> None:
    source = _store(tmp_path / "source.sqlite3")
    backup = source.backup_to_path(tmp_path / "backup.sqlite3")
    destination = HistoryStore(tmp_path / "destination.sqlite3")
    before = destination.count(all_devices=True)
    preview = destination.inspect_backup_path(backup)
    assert preview["integrity"] == "ok"
    assert preview["measurements"] == 2
    assert preview["first_timestamp_utc"] is not None
    assert preview["last_timestamp_utc"] is not None
    assert preview["device_serials"] == ["SERIAL-320", "SERIAL-500"]
    assert preview["size_bytes"] > 0
    assert destination.count(all_devices=True) == before


def test_restore_preview_endpoint_validates_uploaded_sqlite_without_merging(tmp_path: Path) -> None:
    app = _app(tmp_path / "app")
    backup_store = _store(tmp_path / "backup-source.sqlite3")
    backup_path = backup_store.backup_to_path(tmp_path / "preview.sqlite3")
    page = app.render_index(language_override="en", mode_override="advanced").decode()
    token = re.search(r'name="preview_csrf_token" value="([^"]+)"', page)
    assert token is not None

    boundary = "----gmc680preview"
    payload = backup_path.read_bytes()
    body = (
        (
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="preview_csrf_token"\r\n\r\n'
            f"{token.group(1)}\r\n"
            f"--{boundary}\r\n"
            'Content-Disposition: form-data; name="backup"; filename="preview.sqlite3"\r\n'
            "Content-Type: application/vnd.sqlite3\r\n\r\n"
        ).encode()
        + payload
        + f"\r\n--{boundary}--\r\n".encode()
    )

    before = app.store.count(all_devices=True)
    server = ThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
    server.app = app
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_port}/?action=restore-preview&lang=en"
        request = urllib.request.Request(
            url,
            data=body,
            method="POST",
            headers={
                "Content-Type": f"multipart/form-data; boundary={boundary}",
                "Origin": f"http://127.0.0.1:{server.server_port}",
                "Sec-Fetch-Site": "same-origin",
                "Accept": "application/json",
            },
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            result = json.loads(response.read())
        assert result["integrity"] == "ok"
        assert result["measurements"] == 2
        assert result["next_csrf_token"]
        assert app.store.count(all_devices=True) == before
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_bridge_persists_device_warning_summary_for_dashboard() -> None:
    source = (Path(__file__).parents[1] / "rootfs/usr/local/lib/gmc_bridge/service.py").read_text()
    assert '"cpm_discarded_peak_samples": discarded_peak_sample_count' in source
    assert '"device_health_status"' in source
    assert '"serial_reconnect_count": serial_reconnect_count' in source
