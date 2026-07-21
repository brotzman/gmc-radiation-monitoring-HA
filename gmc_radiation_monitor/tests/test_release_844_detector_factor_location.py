from __future__ import annotations

from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def test_conversion_factor_is_rendered_per_tube_not_as_general_device_field(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    store.upsert_device_registry(
        "SERIAL-500",
        {
            "configured_name": "GMC-500+",
            "device_model": "GMC-500+",
            "runtime_online": True,
            "detector_profile": "gmc_500_plus",
            "tube_model": "M4011 + SI-3BG (Dual)",
            "cpm_per_usvh": 154.0,
            "dead_time_us": 120.0,
            "dead_time_model": "nonparalyzable",
            "dual_tube_mode": "separate",
            "dual_tube_switch_cpm": 30_000,
            "low_dose_tube_profile": {
                "tube_model": "M4011",
                "cpm_per_usvh": 154.0,
                "dead_time_us": 120.0,
                "dead_time_model": "nonparalyzable",
            },
            "high_dose_tube_profile": {
                "tube_model": "SI-3BG",
                "cpm_per_usvh": None,
                "dead_time_us": 30.0,
                "dead_time_model": "nonparalyzable",
            },
            "calibration_status": "incomplete",
            "calibration_source": "manufacturer_profile",
        },
    )
    store.insert_measurement(
        {
            "cpm": 17,
            "tube_low_cpm": 17,
            "tube_high_cpm": 0,
            "active_tube": "primary",
        },
        device_serial="SERIAL-500",
        timestamp_utc=1_800_000_000,
    )
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=120,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
        ui_mode="advanced",
    )
    page = app.render_index(
        language_override="de", mode_override="advanced", device_override="SERIAL-500"
    ).decode("utf-8")
    card = page.split('data-device-serial="SERIAL-500"', 1)[1].split("</article>", 1)[0]
    general_fields, detector_profile = card.split('class="calibration-panel', 1)

    assert "CPM je µSv/h" not in general_fields
    assert "<dt>Umrechnungsfaktor</dt>" in detector_profile
    assert "154\xa0CPM/(µSv/h)" in detector_profile
    assert "Nicht konfiguriert" in detector_profile
    assert "Teilweise kalibriert" in detector_profile
