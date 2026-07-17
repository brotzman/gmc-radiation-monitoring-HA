from __future__ import annotations

import tempfile
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.reports import build_live_analysis


def _app(store: HistoryStore) -> ReportApplication:
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
    )


def test_learned_baseline_is_reloaded_per_device_from_sqlite_after_switching():
    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        store.upsert_device_registry("SERIAL-A", {"device_model": "GMC-320Re", "scan_interval_seconds": 60})
        store.upsert_device_registry("SERIAL-B", {"device_model": "GMC-500+", "scan_interval_seconds": 60})

        # Device A has more than six hours of accepted history, but only one sample in
        # the latest hour. Its baseline is learned; only the current comparison must wait.
        start = 1_800_000_000
        for index in range(360):
            store.insert_measurement(
                {"cpm": 12 + (index % 3)},
                device_serial="SERIAL-A",
                timestamp_utc=start + index * 60,
            )
        store.insert_measurement({"cpm": 14}, device_serial="SERIAL-A", timestamp_utc=start + 8 * 3600)

        # Device B is genuinely new and must learn its own, separate baseline.
        for index in range(10):
            store.insert_measurement(
                {"cpm": 25},
                device_serial="SERIAL-B",
                timestamp_utc=start + index * 60,
            )

        analysis_a = build_live_analysis(store, scan_interval_seconds=60, device_serial="SERIAL-A")
        analysis_b = build_live_analysis(store, scan_interval_seconds=60, device_serial="SERIAL-B")
        assert analysis_a["baseline_ready"] is True
        assert analysis_a["recent_window_ready"] is False
        assert analysis_b["baseline_ready"] is False

        page_a_before = (
            _app(store)
            .render_index(language_override="de", device_override="SERIAL-A", report_device_override="all")
            .decode("utf-8")
        )
        page_b = (
            _app(store)
            .render_index(language_override="de", device_override="SERIAL-B", report_device_override="all")
            .decode("utf-8")
        )
        page_a_after = (
            _app(store)
            .render_index(language_override="de", device_override="SERIAL-A", report_device_override="all")
            .decode("utf-8")
        )

        assert "Baseline verfügbar" in page_a_before
        assert "Wartet auf genügend aktuelle Messwerte" in page_a_before
        assert "Baseline wird gebildet" not in page_a_before
        assert "Baseline wird gebildet" in page_b
        assert "Baseline verfügbar" in page_a_after
        assert "Baseline wird gebildet" not in page_a_after
