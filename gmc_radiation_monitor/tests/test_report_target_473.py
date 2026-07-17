from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def _app(tmp_path: Path) -> ReportApplication:
    store = HistoryStore(tmp_path / "history.sqlite")
    for serial, model, cpm, port in (
        ("SERIAL-320", "GMC-320", 20, "/dev/a"),
        ("SERIAL-500", "GMC-500+", 30, "/dev/b"),
    ):
        store.upsert_device_registry(
            serial,
            {
                "device_model": model,
                "configured_name": model,
                "port": port,
                "last_seen_utc": "2099-01-01T00:00:00Z",
                "available": True,
                "connected": True,
                "scan_interval_seconds": 60,
                "cpm_per_usvh": 154.0,
            },
        )
        store.set_device_capabilities(serial, {"cpm": True})
        store.insert_measurement({"cpm": cpm}, device_serial=serial, timestamp_utc=1_800_000_000)
    store.set_metadata({"serial": "SERIAL-320", "device_model": "GMC-320"})
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
    )


def test_report_target_is_bound_server_side_to_quick_links(tmp_path: Path):
    page = (
        _app(tmp_path)
        .render_index(
            language_override="de",
            device_override="SERIAL-500",
        )
        .decode()
    )
    assert "?device=SERIAL-500&amp;lang=de&amp;action=download&amp;period=daily" in page
    assert 'href="?action=download&amp;period=daily' not in page


def test_report_target_is_bound_to_custom_download_forms(tmp_path: Path):
    page = _app(tmp_path).render_index(language_override="de", device_override="SERIAL-500").decode()
    assert page.count('name="device" value="SERIAL-500"') >= 2
    assert 'name="report_device"' not in page
