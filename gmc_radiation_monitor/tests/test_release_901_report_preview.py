from __future__ import annotations

import json
import threading
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import yaml

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.report_web_http import ReportRequestHandler
from gmc_bridge.version import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]


def _start_server(tmp_path: Path) -> tuple[ThreadingHTTPServer, threading.Thread, str]:
    store = HistoryStore(tmp_path / "report-preview.sqlite3")
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
    )
    server = ThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
    server.app = app  # type: ignore[attr-defined]
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, thread, f"http://127.0.0.1:{server.server_port}"


def test_release_901_metadata() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "9.3.0"
    assert config["version"] == "9.3.0"
    assert (ROOT / "RELEASE_NOTES_9.3.0.md").is_file()


def test_report_preview_defaults_missing_period_to_daily(tmp_path: Path) -> None:
    server, thread, base_url = _start_server(tmp_path)
    try:
        with urllib.request.urlopen(
            f"{base_url}/api/report-preview?date=2026-07-23", timeout=5
        ) as response:
            assert response.status == 200
            payload = json.loads(response.read())
        assert payload["period_label"] == "2026-07-23"
        assert payload["samples"] == 0
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_report_preview_accepts_explicit_period(tmp_path: Path) -> None:
    server, thread, base_url = _start_server(tmp_path)
    try:
        with urllib.request.urlopen(
            f"{base_url}/api/report-preview?period=daily&date=2026-07-23", timeout=5
        ) as response:
            assert response.status == 200
            payload = json.loads(response.read())
        assert payload["period_label"] == "2026-07-23"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
