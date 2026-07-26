from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from gmc_bridge.config import DeviceConfig, TubeCalibrationConfig
from gmc_bridge.history import HistoryRow, HistoryStore
from gmc_bridge.metrology import (
    DualTubeMetrologyConfig,
    TubeMetrologyProfile,
    derived_dual_tube_dose_estimate,
)
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.reports import ReportPeriod, analysis_document
from gmc_bridge.version import APP_VERSION


def _low_profile() -> TubeMetrologyProfile:
    return TubeMetrologyProfile(
        tube_model="M4011",
        cpm_per_usvh=154.0,
        dead_time_us=120.0,
        reliable_max_cpm=30_000,
        dead_time_model="nonparalyzable",
        conversion_factor_uncertainty_percent=20.0,
        calibration_reference="M4011 working values",
    )


def _high_profile(*, calibrated: bool) -> TubeMetrologyProfile:
    return TubeMetrologyProfile(
        tube_model="SI-3BG",
        cpm_per_usvh=5.15 if calibrated else None,
        dead_time_us=30.0 if calibrated else None,
        reliable_max_cpm=200_000 if calibrated else None,
        dead_time_model="nonparalyzable" if calibrated else "none",
        calibration_reference="Individual high-dose calibration" if calibrated else "",
    )


def test_legacy_values_migrate_to_effective_low_dose_profile() -> None:
    device = DeviceConfig(
        port="/dev/ttyUSB0",
        name="GMC-500+",
        cpm_per_usvh=154.0,
        dead_time_us=120.0,
        reliable_max_cpm=30_000,
        dead_time_model="nonparalyzable",
        tube_model="M4011 + SI-3BG (Dual)",
        dual_tube_mode="separate",
        dual_tube_switch_cpm=30_000,
        high_dose_tube=TubeCalibrationConfig(tube_model="SI-3BG"),
    )
    device.validate()

    low = device.effective_low_dose_tube()
    registry = device.calibration_registry_values()
    assert low.tube_model == "M4011 + SI-3BG (Dual)"
    assert low.cpm_per_usvh == 154.0
    assert low.dead_time_us == 120.0
    assert registry["low_dose_tube_profile"]["reliable_max_cpm"] == 30_000
    assert registry["calibration_status"] == "incomplete"


def test_separate_profiles_never_apply_m4011_factor_to_uncalibrated_high_tube() -> None:
    config = DualTubeMetrologyConfig(
        mode="separate",
        switch_cpm=30_000,
        low_dose=_low_profile(),
        high_dose=_high_profile(calibrated=False),
    )

    normal = derived_dual_tube_dose_estimate(
        primary_cpm=100,
        low_cpm=100,
        high_cpm=2,
        counting_relative_percent=None,
        config=config,
    )
    high_range = derived_dual_tube_dose_estimate(
        primary_cpm=35_000,
        low_cpm=35_000,
        high_cpm=80,
        counting_relative_percent=None,
        config=config,
    )

    assert normal["selected_tube"] == "low"
    assert normal["available"] is True
    assert high_range["selected_tube"] == "high"
    assert high_range["available"] is False
    assert high_range["reason"] == "tube conversion factor is not configured"


def test_configured_high_tube_and_piecewise_curve_are_supported() -> None:
    separate = DualTubeMetrologyConfig(
        mode="separate",
        switch_cpm=30_000,
        low_dose=_low_profile(),
        high_dose=_high_profile(calibrated=True),
    )
    high_result = derived_dual_tube_dose_estimate(
        primary_cpm=40_000,
        low_cpm=40_000,
        high_cpm=515,
        counting_relative_percent=None,
        config=separate,
    )
    assert high_result["selected_tube"] == "high"
    assert high_result["available"] is True
    assert high_result["value_usvh"] > 100.0

    curve = DualTubeMetrologyConfig(
        mode="curve",
        switch_cpm=30_000,
        low_dose=_low_profile(),
        high_dose=_high_profile(calibrated=True),
    )
    curve_result = derived_dual_tube_dose_estimate(
        primary_cpm=31_000,
        low_cpm=None,
        high_cpm=None,
        counting_relative_percent=None,
        config=curve,
    )
    assert curve_result["selected_tube"] == "high"
    assert curve_result["available"] is True


def test_main_device_card_exposes_calibration_in_analysis_and_expert_tiers(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    store.upsert_device_registry(
        "SERIAL-500",
        {
            "configured_name": "GMC-500+",
            "device_model": "GMC-500+",
            "port": "/dev/ttyUSB1",
            "runtime_online": True,
            "runtime_status": "online",
            "scan_interval_seconds": 60,
            "cpm_per_usvh": 154.0,
            "dead_time_us": 120.0,
            "reliable_max_cpm": 30_000,
            "dead_time_model": "nonparalyzable",
            "conversion_factor_uncertainty_percent": 20.0,
            "tube_model": "M4011 + SI-3BG (Dual)",
            "dual_tube_mode": "separate",
            "dual_tube_switch_cpm": 30_000,
            "low_dose_tube_profile": _low_profile().as_dict(),
            "high_dose_tube_profile": _high_profile(calibrated=False).as_dict(),
            "calibration_status": "incomplete",
        },
    )
    store.insert_measurement(
        {"cpm": 20, "tube_low_cpm": 20, "tube_high_cpm": 1},
        device_serial="SERIAL-500",
        timestamp_utc=1_800_000_000,
    )
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
    )

    page = app.render_index(
        language_override="de",
        mode_override="advanced",
        device_override="SERIAL-500",
    ).decode("utf-8")

    assert "Detektorprofil" in page
    assert "Zwei physische Zählrohre" in page
    assert "M4011 + SI-3BG" in page
    assert "Unvollständige Kalibrierung" in page
    assert 'class="calibration-grid" data-analysis-tier="analysis"' in page
    assert 'class="measurement-details" data-analysis-tier="expert"' in page
    assert "SI-3BG" in page
    css = Path("rootfs/usr/local/lib/gmc_bridge/static/dashboard.css").read_text()
    assert ".calibration-panel" in css
    assert "@media(max-width:700px)" in css.replace(" ", "")


def test_analysis_json_records_dual_tube_configuration_and_selected_profile() -> None:
    start = datetime(2026, 7, 21, tzinfo=UTC)
    period = ReportPeriod(
        kind="daily",
        label="2026-07-21",
        start_local=start,
        end_local=start + timedelta(days=1),
    )
    rows = [
        HistoryRow("SERIAL-500", int(start.timestamp()), 100, None, None, None, None, None, "accepted", 100, 2),
        HistoryRow("SERIAL-500", int(start.timestamp()) + 60, 110, None, None, None, None, None, "accepted", 110, 2),
    ]
    metadata = {
        "serial": "SERIAL-500",
        "device_model": "GMC-500+",
        "dual_tube_mode": "separate",
        "dual_tube_switch_cpm": 30_000,
        "low_dose_tube_profile": _low_profile().as_dict(),
        "high_dose_tube_profile": _high_profile(calibrated=False).as_dict(),
        "app_version": APP_VERSION,
    }

    document = analysis_document(
        period=period,
        timezone_name="UTC",
        scan_interval_seconds=60,
        rows=rows,
        baseline_rows=[],
        device_metadata=metadata,
        cpm_per_usvh=154.0,
        yellow_percent=150.0,
        red_percent=200.0,
        language="de",
    )

    assert document["app_version"] == "9.3.0"
    assert document["dual_tube_configuration"]["mode"] == "separate"
    assert document["dual_tube_configuration"]["low_dose"]["tube_model"] == "M4011"
    assert document["derived_dose_estimate"]["selected_tube"] == "low"
    assert document["derived_dose_estimate"]["available"] is True
