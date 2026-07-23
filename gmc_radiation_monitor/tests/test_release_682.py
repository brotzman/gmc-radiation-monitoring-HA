from __future__ import annotations

import re
from pathlib import Path

from gmc_bridge.filtering import HighCpmGate
from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def _insert(store: HistoryStore, serial: str, timestamp: int, cpm: int) -> None:
    sample = {"cpm": cpm, "voltage_v": 4.1}
    store.insert_raw_measurement(
        sample,
        device_serial=serial,
        timestamp_utc=timestamp,
        gate_state="accepted_normal",
        accepted=True,
    )
    store.insert_measurement(
        sample,
        device_serial=serial,
        timestamp_utc=timestamp,
        cpm_quality="normal",
        expected_interval_seconds=60,
    )


def _app(tmp_path: Path) -> ReportApplication:
    store = HistoryStore(tmp_path / "history.sqlite3")
    for serial, model, cpm in (
        ("SERIAL-320", "GMC-320 Re 4.52", 16),
        ("SERIAL-500", "GMC-500+ Re 2.53", 20),
    ):
        store.upsert_device_registry(
            serial,
            {
                "device_model": model,
                "configured_name": model,
                "runtime_online": True,
                "scan_interval_seconds": 60,
                "device_health_status": "ok",
            },
        )
        store.insert_measurement(
            {"cpm": cpm, "temperature_c": 22.0, "voltage_v": 4.1},
            device_serial=serial,
            timestamp_utc=1_800_000_000 + cpm,
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


def test_6339_cpm_is_held_from_the_first_sample() -> None:
    gate = HighCpmGate(10000, 3)
    assessment = gate.assess(6339)
    assert assessment.suspicious is True
    assert assessment.trigger == "startup_threshold"
    assert assessment.baseline_median is None
    assert assessment.adaptive_threshold == 1000
    assert gate.accept(6339, assessment=assessment) is False
    assert gate.pending == 1


def test_three_similar_high_values_can_confirm_during_cold_start() -> None:
    gate = HighCpmGate(10000, 3)
    assert gate.accept(6200) is False
    assert gate.accept(6339) is False
    assert gate.accept(6100) is True
    assert gate.just_confirmed is True
    assert gate.last_accept_reason == "consecutive_confirmed"


def test_cleanup_rechecks_after_an_earlier_run_and_removes_new_startup_peak(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    start = 1_700_000_000
    _insert(store, "GMC500", start, 15)
    first = store.purge_unconfirmed_adaptive_spikes()
    assert first["raw_deleted"] == 0

    _insert(store, "GMC500", start + 60, 6339)
    _insert(store, "GMC500", start + 120, 16)
    second = store.purge_unconfirmed_adaptive_spikes()

    assert second["previously_run"] is True
    assert second["raw_deleted"] == 1
    assert second["measurements_deleted"] == 1
    assert [
        row["cpm"] for row in store.query_raw_measurements(start, start + 300, device_serial="GMC500")
    ] == [15, 16]
    assert [row.cpm for row in store.query_range(start, start + 300, device_serial="GMC500")] == [15, 16]


def test_analysis_has_matching_device_badge_and_real_anchor(tmp_path: Path) -> None:
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
    assert 'class="analysis-device-badge device-500"' in analysis
    assert ">500+<" in analysis
    assert "Analyse für GMC-500+ Re 2.53 · SERIAL-500" in analysis
    assert '<a href="#analysis">Analyse</a>' in page
    script = Path("rootfs/usr/local/lib/gmc_bridge/static/dashboard.js").read_text(encoding="utf-8")
    assert "document.getElementById(selector.slice(1))" in script


def test_obsolete_report_history_and_presets_are_removed(tmp_path: Path) -> None:
    page = _app(tmp_path).render_index(language_override="de", mode_override="advanced").decode()
    for obsolete in (
        'id="recent-reports"',
        'id="report-presets"',
        'id="clear-recent-reports"',
        'id="clear-report-presets"',
        "gmc-recent-reports-v1",
        "gmc-report-presets-v1",
        "save-report-preset",
        "Letzte Berichte",
        "Gespeicherte Berichtsvorgaben",
    ):
        assert obsolete not in page
    assert "Schnelldownloads" in page
    assert page.count('report-preset-source unified-report-form') == 1
    assert 'id="report-generation-preview"' in page


def test_status_strip_uses_readable_responsive_grid_without_ellipsis(tmp_path: Path) -> None:
    page = _app(tmp_path).render_index(language_override="de", mode_override="advanced").decode()
    css = Path("rootfs/usr/local/lib/gmc_bridge/static/dashboard.css").read_text(encoding="utf-8")
    assert ".dashboard-controls { position:sticky; top:0; z-index:50;" in page
    assert ".status-strip { position:static; display:block; }" in page
    assert 'class="system-status-panel' in page
    assert 'class="status-details-grid"' in page
    assert (
        ".status-strip-item strong,.status-strip-item small { display:block; white-space:normal; overflow-wrap:anywhere;"
        in css
    )
    assert (
        ".status-strip-item strong,.status-strip-item small { display:block; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }"
        not in css
    )
    status = page.split('<section class="status-strip"', 1)[1].split("</section>", 1)[0]
    details = status.split('<div class="status-details-grid">', 1)[1]
    labels = re.findall(r"<strong>(.*?)</strong>", details)
    assert len(labels) == 6
    assert all("…" not in label for label in labels)
    assert "System läuft normal" in status
    assert "Statusdetails anzeigen" in status
