from __future__ import annotations

from datetime import UTC, datetime, timedelta
from io import BytesIO
from pathlib import Path

import yaml
from gmc_bridge.calibration_presets import PRESETS, detect_profile_id
from gmc_bridge.history import HistoryStore
from gmc_bridge.metrology import MetrologyConfig, live_measurement_metrology
from gmc_bridge.migrations import SCHEMA_VERSION
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.reports import build_report, load_timezone, resolve_period
from gmc_bridge.version import APP_VERSION
from pypdf import PdfReader


def test_automatic_detector_profile_detection_covers_supported_families() -> None:
    assert detect_profile_id("GMC-300E Plus") == "gmc_300"
    assert detect_profile_id("GMC-320 Plus V4") == "gmc_320_plus_v4"
    assert detect_profile_id("GMC-500+") == "gmc_500_plus"
    assert detect_profile_id("GMC-600+") == "gmc_600_plus"
    assert PRESETS["gmc_320_plus_v4"].dual_tube_mode == "single"
    assert PRESETS["gmc_500_plus"].dual_tube_mode == "separate"
    assert PRESETS["gmc_500_plus"].high_dose_tube_model == "SI-3BG"
    assert PRESETS["gmc_500_plus"].cpm_per_usvh == 154.0
    assert PRESETS["gmc_600_plus"].tube_model == "LND 7317"


def test_live_metrology_exposes_quality_load_losses_and_correction() -> None:
    result = live_measurement_metrology(
        cpm=8_000,
        cpm_per_usvh=154.0,
        config=MetrologyConfig(
            tube_model="M4011",
            dead_time_us=120.0,
            dead_time_model="nonparalyzable",
            reliable_max_cpm=50_000,
        ),
        calibration_status="predefined",
        calibration_source="manufacturer_profile",
    )
    assert result["raw_cpm"] == 8_000
    assert result["corrected_cpm"] > 8_000
    assert result["detector_load_percent"] > 0
    assert result["dead_time_loss_percent"] > 0
    assert result["correction_factor"] > 1
    assert 1 <= result["measurement_quality_stars"] <= 5
    assert 0 <= result["measurement_quality_index"] <= 100
    assert result["dose_quality"] in {"high", "medium", "low"}


def _store_with_devices(tmp_path: Path) -> HistoryStore:
    store = HistoryStore(tmp_path / "history.sqlite3")
    now = int(datetime.now(UTC).timestamp())
    low_profile = {
        "tube_model": "M4011",
        "cpm_per_usvh": 154.0,
        "dead_time_us": 120.0,
        "reliable_max_cpm": 30_000,
        "dead_time_model": "nonparalyzable",
        "conversion_factor_uncertainty_percent": 20.0,
        "calibration_uncertainty_percent": None,
        "calibration_reference": "GMC-500+ primary working profile",
    }
    high_profile = {
        "tube_model": "SI-3BG",
        "cpm_per_usvh": None,
        "dead_time_us": 30.0,
        "reliable_max_cpm": None,
        "dead_time_model": "nonparalyzable",
        "conversion_factor_uncertainty_percent": None,
        "calibration_uncertainty_percent": None,
        "calibration_reference": "No verified dose factor",
    }
    store.upsert_device_registry(
        "SERIAL-320",
        {
            "configured_name": "GMC-320",
            "device_model": "GMC-320 Plus V4",
            "runtime_online": True,
            "detector_profile": "gmc_320_plus_v4",
            "tube_model": "M4011",
            "cpm_per_usvh": 154.0,
            "dead_time_us": 120.0,
            "dead_time_model": "nonparalyzable",
            "reliable_max_cpm": 50_000,
            "dual_tube_mode": "single",
            "calibration_status": "predefined",
            "calibration_source": "manufacturer_profile",
        },
    )
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
            "reliable_max_cpm": 30_000,
            "dual_tube_mode": "separate",
            "dual_tube_switch_cpm": 30_000,
            "low_dose_tube_profile": low_profile,
            "high_dose_tube_profile": high_profile,
            "calibration_status": "incomplete",
            "calibration_source": "manufacturer_profile",
        },
    )
    store.insert_measurement(
        {
            "cpm": 18,
            "raw_cpm": 18,
            "corrected_cpm": 18.01,
            "detector_type": "M4011",
            "dual_tube_mode": "single",
            "active_tube": "primary",
            "dead_time_model": "nonparalyzable",
            "dead_time_us": 120,
            "dead_time_loss_percent": 0.036,
            "detector_load_percent": 0.0036,
            "correction_factor": 1.00036,
            "calibration_status": "predefined",
            "calibration_source": "manufacturer_profile",
            "measurement_quality_index": 99,
            "dose_quality": "high",
            "derived_dose_usvh": 18.01 / 154.0,
        },
        device_serial="SERIAL-320",
        timestamp_utc=now,
    )
    store.insert_measurement(
        {
            "cpm": 17,
            "tube_low_cpm": 17,
            "tube_high_cpm": 0,
            "raw_cpm": 17,
            "corrected_cpm": 17.01,
            "detector_type": "M4011",
            "dual_tube_mode": "separate",
            "active_tube": "primary",
            "dead_time_model": "nonparalyzable",
            "dead_time_us": 120,
            "dead_time_loss_percent": 0.034,
            "detector_load_percent": 0.0034,
            "correction_factor": 1.00034,
            "calibration_status": "incomplete",
            "calibration_source": "manufacturer_profile",
            "measurement_quality_index": 60,
            "dose_quality": "medium",
            "derived_dose_usvh": 17.01 / 154.0,
        },
        device_serial="SERIAL-500",
        timestamp_utc=now,
    )
    return store


def test_schema_and_calibration_audit_storage(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    assert SCHEMA_VERSION == 8
    assert store.schema_version() == 8
    values = {
        "tube_model": "Test tube",
        "cpm_per_usvh": 100.0,
        "dead_time_us": 100.0,
        "dead_time_model": "nonparalyzable",
        "reliable_max_cpm": 20_000,
    }
    store.save_custom_calibration_profile(
        profile_id="test_profile",
        display_name="Test profile",
        detector_type="single",
        values=values,
        source="user",
        comment="Release 8.4 test",
    )
    store.assign_custom_calibration_profile(
        device_serial="SERIAL-X", profile_id="test_profile", values=values
    )
    store.record_calibration_change(
        device_serial="SERIAL-X",
        profile_id="test_profile",
        detector_type="single",
        values=values,
        changed_fields=["cpm_per_usvh", "dead_time_us"],
        source="user",
        comment="Release 8.4 test",
    )
    assert store.list_custom_calibration_profiles()[0]["profile_id"] == "test_profile"
    assert store.get_custom_calibration_assignment("SERIAL-X")["profile_id"] == "test_profile"
    history = store.list_calibration_history(device_serial="SERIAL-X")
    assert history[0]["changed_fields"] == ["cpm_per_usvh", "dead_time_us"]
    assert history[0]["source"] == "user"


def test_advanced_dashboard_contains_release_840_controls(tmp_path: Path) -> None:
    store = _store_with_devices(tmp_path)
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
    for text in (
        "Detektorprofil",
        "Messqualität",
        "Detektorauslastung",
        "Kalibrierungsprofile",
        "Kalibrierungsassistent",
        "Rohdaten",
        "Totzeitkorrigiert",
        "Vergleichsansicht",
        "Roh-CPM",
        "Korrigierte CPM",
        "SI-3BG",
    ):
        assert text in page
    assert "SERIAL-320" in page
    assert "SERIAL-500" in page
    assert 'data_mode=comparison' in page
    assert 'id="device-comparison"' not in page
    assert 'class="device-comparison-section"' not in page
    assert "measurement-quality-card" not in page
    assert "Teilweise kalibriert" in page
    assert "154\xa0CPM/(µSv/h)" in page
    assert "Nicht konfiguriert" in page


def test_scientific_pdf_adds_sixth_page_and_comparison_mode(tmp_path: Path) -> None:
    store = _store_with_devices(tmp_path)
    tz = load_timezone("Europe/Berlin")
    local_now = datetime.now(tz)
    period = resolve_period(
        kind="daily",
        selection="specific",
        tz=tz,
        date_value=local_now.date().isoformat(),
        now=local_now + timedelta(minutes=1),
    )
    filename, content_type, payload = build_report(
        store,
        period=period,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=120,
        output_format="pdf",
        cpm_per_usvh=154.0,
        device_serial="SERIAL-320",
        language="de",
        data_mode="comparison",
        scientific_page=True,
    )
    assert filename.endswith(".analysis.pdf")
    assert content_type == "application/pdf"
    reader = PdfReader(BytesIO(payload))
    assert len(reader.pages) == 6
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    assert "Messqualität" in text
    assert "Wissenschaftliche Detektor- und Korrekturdokumentation" in text
    assert "Vergleich" in text or "Datenmodus" in text


def test_release_metadata_and_supervisor_schema_are_840() -> None:
    config = yaml.safe_load(Path("config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "8.4.4"
    assert config["version"] == "8.4.4"
    profile_schema = config["schema"]["devices"][0]["detector_profile"]
    for profile in ("gmc_300", "gmc_320_plus_v4", "gmc_500_plus", "gmc_600_plus"):
        assert profile in profile_schema
