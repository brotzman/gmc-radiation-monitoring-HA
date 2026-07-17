from __future__ import annotations

import time
from pathlib import Path

from gmc_bridge.fleet_analytics import build_fleet_snapshot, measurement_gap_status
from gmc_bridge.history import HistoryStore
from gmc_bridge.translations import Translator


def test_measurement_gap_thresholds_follow_configured_interval() -> None:
    assert measurement_gap_status(359, 240) is None
    assert measurement_gap_status(360, 240) == "Warning"
    assert measurement_gap_status(599, 240) == "Warning"
    assert measurement_gap_status(600, 240) == "Critical"
    assert measurement_gap_status(382, 255) is None
    assert measurement_gap_status(383, 255) == "Warning"
    assert measurement_gap_status(638, 255) == "Critical"


def test_fleet_snapshot_uses_device_specific_interval_for_gap_status(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    now = int(time.time())
    store.upsert_device_registry(
        "a",
        {
            "device_model": "GMC-320",
            "runtime_online": True,
            "scan_interval_seconds": 240,
            "serial_error_count": 0,
            "serial_reconnect_count": 0,
        },
    )
    for timestamp in (now - 1000, now - 640, now - 40):
        store.insert_measurement(
            {"cpm": 15},
            device_serial="a",
            timestamp_utc=timestamp,
            expected_interval_seconds=240,
        )
    item = build_fleet_snapshot(store)["stability"][0]
    assert item.scan_interval_seconds == 240
    assert item.longest_gap_seconds == 600
    assert item.gap_status == "Critical"


def test_german_gap_status_translation() -> None:
    t = Translator("de")
    assert t("Warning") == "Warnung"
    assert t("Critical") == "Kritisch"
    assert (
        t("Warning from {warning} s; critical from {critical} s", warning="360", critical="600")
        == "Warnung ab 360 s; kritisch ab 600 s"
    )


def test_gap_status_is_rendered_after_longest_gap() -> None:
    root = Path("rootfs/usr/local/lib/gmc_bridge")
    source = "\n".join((root / name).read_text() for name in ("web_analysis_views.py", "web_assets.py"))
    assert "{html.escape(value)}{gap_status_html}</span>" in source
    assert 'class="gap-status {gap_class}"' in source
    assert ".gap-status.warning" in source
    assert ".gap-status.critical" in source
