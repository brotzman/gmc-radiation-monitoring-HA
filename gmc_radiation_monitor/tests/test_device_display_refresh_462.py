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


def _store_with_two_devices(path: Path) -> HistoryStore:
    store = HistoryStore(path)
    for serial, model, port, cpm in (
        ("SERIAL-320", "GMC-320Re 4.52", "/dev/ttyUSB0", 13),
        ("SERIAL-500", "GMC-500+ 2.20", "/dev/ttyUSB1", 21),
    ):
        store.upsert_device_registry(
            serial,
            {
                "device_model": model,
                "port": port,
                "runtime_online": True,
                "runtime_status": "online",
                "scan_interval_seconds": 60,
            },
        )
        store.insert_measurement(
            {"cpm": cpm},
            device_serial=serial,
            timestamp_utc=1_800_000_000,
        )
    return store


def test_device_cards_refresh_without_reloading_analysis_or_losing_scroll():
    with tempfile.TemporaryDirectory() as tmp:
        store = _store_with_two_devices(Path(tmp) / "history.sqlite3")
        page = (
            _app(store)
            .render_index(
                language_override="de",
                device_override="SERIAL-500",
                report_device_override="all",
            )
            .decode("utf-8")
        )

        assert "const deviceRefreshIntervalMs = 20000;" in page
        assert "new URL('./api/device-cards', currentUrl)" in page
        assert "currentSection.replaceWith(nextSection)" in page
        assert "window.location.replace(currentUrl.toString())" in page
        assert "pageScroll.scrollTop = savedScrollTop" in page
        assert "window.location.reload" not in page
        assert "location.reload" not in page
        assert "['mode', 'lang', 'device']" in page


def test_device_fragment_keeps_selected_analysis_device_and_contains_only_cards_section():
    with tempfile.TemporaryDirectory() as tmp:
        store = _store_with_two_devices(Path(tmp) / "history.sqlite3")
        fragment = (
            _app(store)
            .render_devices_fragment(
                mode_override="advanced",
                language_override="de",
                device_override="SERIAL-500",
                report_device_override="all",
            )
            .decode("utf-8")
        )

        assert fragment.startswith('<details class="card collapsible-card" id="devices"')
        assert fragment.endswith("</details>")
        assert "Verbundene GMC-Geräte" in fragment
        assert fragment.count('<span class="device-status online">Online</span>') == 2
        assert "SERIAL-500" in fragment
        assert "Analyse wird angezeigt" in fragment
        assert "<html" not in fragment
        assert "<script" not in fragment
