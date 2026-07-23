from __future__ import annotations

from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import Translator


def _app(tmp_path: Path) -> ReportApplication:
    store = HistoryStore(tmp_path / "history.sqlite3")
    store.upsert_device_registry(
        "SERIAL-500",
        {
            "device_model": "GMC-500+ Re 2.53",
            "configured_name": "GMC-500+ Re 2.53",
            "runtime_online": True,
            "scan_interval_seconds": 60,
            "device_health_status": "ok",
        },
    )
    store.insert_measurement(
        {"cpm": 18, "temperature_c": 30.2, "voltage_v": 4.1},
        device_serial="SERIAL-500",
        timestamp_utc=1_800_000_000,
    )
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
        restore_enabled=False,
        purge_all_history_enabled=False,
    )


def test_analysis_view_no_longer_renders_duplicate_combined_interpretation(tmp_path: Path) -> None:
    page = (
        _app(tmp_path)
        .render_index(
            language_override="de",
            mode_override="advanced",
            device_override="SERIAL-500",
        )
        .decode()
    )
    analysis = page.split('<section id="analysis" class="analysis-section">', 1)[1].split("</section>", 1)[0]
    assert 'class="combined-interpretation"' not in analysis


def test_analysis_groups_use_consistent_gap_layout() -> None:
    css = (Path(__file__).resolve().parents[1] / "rootfs/usr/local/lib/gmc_bridge/static/dashboard.css").read_text(
        encoding="utf-8"
    )
    assert ".group-body { display:grid; gap:.9rem; padding: 0 1rem 1rem; }" in css
    assert ".group-body > * { min-width:0; }" in css


def test_german_baseline_wording_uses_gebildet() -> None:
    t = Translator("de")
    assert t("Baseline learning in progress") == "Baseline wird noch gebildet"
    assert "wird noch gebildet" in t(
        "The local background is still being learned, so no anomaly assessment is available yet."
    )
