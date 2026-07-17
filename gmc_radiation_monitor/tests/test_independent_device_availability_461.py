from __future__ import annotations

import tempfile
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def _app(store: HistoryStore) -> ReportApplication:
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
    )


def test_analysis_selection_does_not_change_other_device_online_state():
    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        for serial, model, port in (
            ("SERIAL-320", "GMC-320Re 4.52", "/dev/ttyUSB0"),
            ("SERIAL-500", "GMC-500+ 2.20", "/dev/ttyUSB1"),
        ):
            store.upsert_device_registry(
                serial,
                {
                    "device_model": model,
                    "port": port,
                    "runtime_online": True,
                    "runtime_status": "online",
                    "last_seen_utc": "2000-01-01T00:00:00Z",
                },
            )
            store.insert_measurement({"cpm": 10}, device_serial=serial, timestamp_utc=946684800)

        page = (
            _app(store)
            .render_index(
                language_override="de",
                device_override="SERIAL-500",
                report_device_override="all",
            )
            .decode("utf-8")
        )

        assert page.count('<span class="device-status online">Online</span>') == 2
        assert "Analyse wird angezeigt" in page
        assert "Analyse anzeigen" in page


def test_explicit_runtime_offline_state_hides_device_from_live_view():
    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        store.upsert_device_registry(
            "SERIAL-OFF",
            {
                "device_model": "GMC-500+",
                "port": "/dev/ttyUSB1",
                "runtime_online": False,
                "runtime_status": "offline",
                "last_seen_utc": "2099-01-01T00:00:00Z",
            },
        )
        store.insert_measurement({"cpm": 20}, device_serial="SERIAL-OFF", timestamp_utc=4_000_000_000)
        page = (
            _app(store)
            .render_index(language_override="de", device_override="SERIAL-OFF", report_device_override="all")
            .decode("utf-8")
        )
        assert 'data-connected-count="0"' in page
        assert "SERIAL-OFF" not in page
        assert '<span class="device-status offline">Offline</span>' not in page
