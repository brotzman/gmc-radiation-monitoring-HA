from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def _app(tmp_path: Path) -> ReportApplication:
    store = HistoryStore(tmp_path / "history.sqlite3", retention_days=30)
    for serial, model, port in (
        ("SERIAL-320", "GMC-320", "/dev/ttyUSB0"),
        ("SERIAL-500", "GMC-500+", "/dev/ttyUSB1"),
    ):
        store.upsert_device_registry(
            serial,
            {
                "serial": serial,
                "device_model": model,
                "configured_name": model,
                "port": port,
                "last_seen_utc": "2099-01-01T00:00:00Z",
                "available": True,
                "connected": True,
            },
        )
    store.set_metadata({"serial": "SERIAL-320", "device_model": "GMC-320"})
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        cpm_per_usvh=154.0,
        read_gyro=False,
    )


def test_downloads_follow_displayed_analysis_without_selector(tmp_path: Path):
    page = _app(tmp_path).render_index(language_override="de", device_override="SERIAL-500").decode()
    downloads_start = page.index('<section id="reports">')
    context = page.index("Berichte für die angezeigte Analyse")
    assert context > downloads_start
    assert 'name="report_device"' not in page
    assert "GMC-500+ · SERIAL-500" in page
    assert "?device=SERIAL-500&amp;lang=de&amp;action=download&amp;period=daily" in page
    assert page.count('name="device" value="SERIAL-500"') >= 2


def test_switching_analysis_switches_all_downloads(tmp_path: Path):
    app = _app(tmp_path)
    page_320 = app.render_index(language_override="de", device_override="SERIAL-320").decode()
    page_500 = app.render_index(language_override="de", device_override="SERIAL-500").decode()
    assert "?device=SERIAL-320&amp;lang=de&amp;action=download" in page_320
    assert "?device=SERIAL-500&amp;lang=de&amp;action=download" in page_500
