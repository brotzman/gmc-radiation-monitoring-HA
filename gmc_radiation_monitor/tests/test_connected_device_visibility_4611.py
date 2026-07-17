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


def _register(
    store: HistoryStore,
    *,
    serial: str,
    model: str,
    port: str,
    online: bool,
    cpm: int,
    timestamp: int,
) -> None:
    store.upsert_device_registry(
        serial,
        {
            "configured_name": model,
            "device_model": model,
            "port": port,
            "scan_interval_seconds": 60,
            "runtime_online": online,
            "runtime_status": "online" if online else "offline",
            "last_seen_utc": "2099-01-01T00:00:00Z",
        },
    )
    store.insert_measurement({"cpm": cpm}, device_serial=serial, timestamp_utc=timestamp)


def test_only_connected_device_is_shown_and_used_for_analysis() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        _register(
            store,
            serial="SERIAL-320",
            model="GMC-320",
            port="/dev/ttyUSB0",
            online=False,
            cpm=12,
            timestamp=1_800_000_000,
        )
        _register(
            store,
            serial="SERIAL-500",
            model="GMC-500+",
            port="/dev/ttyUSB1",
            online=True,
            cpm=34,
            timestamp=1_800_000_060,
        )

        page = (
            _app(store)
            .render_index(
                language_override="de",
                device_override="SERIAL-320",
                report_device_override="all",
            )
            .decode("utf-8")
        )

        assert 'data-connected-count="1"' in page
        assert 'data-selected-serial="SERIAL-500"' in page
        assert "GMC-500+ · SERIAL-500" in page
        assert "Analyse für GMC-500+ · SERIAL-500" in page
        assert "34 CPM" in page
        assert "SERIAL-320" not in page


def test_both_connected_devices_remain_visible() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        _register(
            store,
            serial="SERIAL-320",
            model="GMC-320",
            port="/dev/ttyUSB0",
            online=True,
            cpm=12,
            timestamp=1_800_000_000,
        )
        _register(
            store,
            serial="SERIAL-500",
            model="GMC-500+",
            port="/dev/ttyUSB1",
            online=True,
            cpm=34,
            timestamp=1_800_000_060,
        )

        page = (
            _app(store)
            .render_index(
                language_override="de",
                device_override="SERIAL-500",
                report_device_override="all",
            )
            .decode("utf-8")
        )

        assert 'data-connected-count="2"' in page
        assert "SERIAL-320" in page
        assert "SERIAL-500" in page
        assert page.count('<span class="device-status online">Online</span>') == 2
        assert "Analyse für GMC-500+ · SERIAL-500" in page


def test_no_connected_device_does_not_reuse_historical_analysis() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        _register(
            store,
            serial="SERIAL-OFF",
            model="GMC-500+",
            port="/dev/ttyUSB1",
            online=False,
            cpm=99,
            timestamp=1_800_000_000,
        )

        page = _app(store).render_index(language_override="de").decode("utf-8")

        assert 'data-connected-count="0"' in page
        assert 'data-selected-serial=""' in page
        assert "SERIAL-OFF" not in page
        assert "Noch keine Messwerte." in page
        assert "99 CPM" not in page


def test_bridge_start_resets_stale_online_registry_state() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        store = HistoryStore(Path(tmp) / "history.sqlite3")
        _register(
            store,
            serial="SERIAL-STALE",
            model="GMC-500+",
            port="/dev/ttyUSB1",
            online=True,
            cpm=42,
            timestamp=1_800_000_000,
        )

        store.reset_device_runtime_states()
        item = store.list_devices()[0]

        assert item["runtime_online"] is False
        assert item["runtime_status"] == "offline"
        assert item["runtime_status_reason"] == "service_starting"
