from __future__ import annotations

import json
import time
from pathlib import Path

import yaml

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import Translator
from gmc_bridge.web_assets import DASHBOARD_CSS, render_dashboard_script
from gmc_bridge.workflow import run_self_test, validate_candidate_options


ROOT = Path(__file__).resolve().parents[1]


def _base_device(name: str, *, delay: int) -> dict[str, object]:
    return {"name": name, "scan_interval": 60, "serial_startup_delay": delay}


def test_847_dual_tube_devices_are_independent_physical_devices() -> None:
    options = {
        "devices": [_base_device("GMC-320", delay=0)],
        "dual_tube_devices": [
            {
                **_base_device("GMC-500+", delay=15),
                "dual_tube_mode": "separate",
                "dual_tube_switch_cpm": 30000,
            }
        ],
        "history": {"retention_days": 90, "report_timezone": "Europe/Berlin"},
    }
    problems = validate_candidate_options(options)
    assert problems == []
    assert not any("references unknown device name" in item for item in problems)

    only_dual = {**options, "devices": []}
    only_dual["dual_tube_devices"] = [
        {
            **_base_device("GMC-500+", delay=0),
            "dual_tube_mode": "separate",
            "dual_tube_switch_cpm": 30000,
        }
    ]
    assert validate_candidate_options(only_dual) == []


def test_847_validator_requires_one_device_and_cross_list_unique_names() -> None:
    empty = {"devices": [], "dual_tube_devices": []}
    assert validate_candidate_options(empty) == [
        "At least one device configuration is required across devices and dual_tube_devices"
    ]

    duplicate = {
        "devices": [_base_device("GMC-500+", delay=0)],
        "dual_tube_devices": [
            {
                **_base_device("gmc-500+", delay=15),
                "dual_tube_mode": "separate",
            }
        ],
    }
    problems = validate_candidate_options(duplicate)
    assert any("Duplicate device name across devices and dual_tube_devices" in item for item in problems)


def test_847_self_test_exposes_configuration_problem_details(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite", retention_days=90)
    now = int(time.time())
    store.upsert_device_registry(
        "SERIAL-1",
        {
            "configured_name": "GMC-320",
            "runtime_online": True,
            "timestamp_utc": now,
            "last_timestamp_utc": now,
        },
    )
    options_path = tmp_path / "options.json"
    options_path.write_text(
        json.dumps(
            {
                "devices": [_base_device("GMC-320", delay=0)],
                "dual_tube_devices": [
                    {
                        **_base_device("GMC-320", delay=15),
                        "dual_tube_mode": "separate",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    checks = run_self_test(
        store=store,
        timezone_name="Europe/Berlin",
        devices=store.list_devices(),
        home_assistant_available=True,
        options_path=options_path,
        backup_directory=tmp_path / "backups",
        now_utc=now,
    )
    configuration = next(item for item in checks if item.key == "configuration")
    assert configuration.status == "error"
    assert configuration.values["count"] == 1
    assert configuration.values["problems"]
    assert "Duplicate device name" in configuration.values["problems"][0]


def test_847_warning_state_remains_healthy(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite", retention_days=90)
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
    )
    result = app.api_self_test()
    assert result["status"] == "warning"
    assert result["healthy"] is True
    assert result["ok"] is True


def test_847_browser_override_and_expert_measurement_markup(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite", retention_days=90)
    now = int(time.time())
    store.upsert_device_registry(
        "f488c59b0031f0",
        {
            "configured_name": "GMC-320",
            "device_model": "GMC-320 Re 4.52",
            "runtime_online": True,
            "runtime_status": "online",
            "timestamp_utc": now,
            "last_timestamp_utc": now,
            "scan_interval_seconds": 60,
            "cpm_per_usvh": 154.0,
            "tube_model": "M4011",
            "detector_profile": "gmc_320_plus_v4",
        },
    )
    store.insert_measurement(
        {
            "cpm": 8,
            "derived_dose_usvh": 0.0519,
            "measurement_quality_index": 100,
            "measurement_quality_stars": "★★★★★",
            "corrected_cpm": 8.0,
            "dead_time_loss_percent": 0.0,
            "dead_time_correction_factor": 1.0,
            "detector_type": "M4011",
            "active_tube": "M4011",
        },
        device_serial="f488c59b0031f0",
        timestamp_utc=now,
    )
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
        ui_mode="advanced",
    )
    page = app.render_index(language_override="de", mode_override="advanced").decode("utf-8")
    assert 'id="measurement-override-status" hidden' in page
    assert "Lokale Browser-Einstellung aktiv" in page
    assert 'id="reset-main-value-size"' in page
    assert "Auf App-Standard zurücksetzen" in page
    assert '<section class="measurement-details" data-analysis-tier="expert">' in page
    assert '<details class="tube-profile-grid" data-analysis-tier="expert">' not in page
    assert 'class="measurement-details-body"' in page
    assert "Messdetails" in page
    assert '<summary>' not in page.split('class="measurement-details"', 1)[1].split('</section>', 1)[0]

    script = render_dashboard_script(
        selected_serial="f488c59b0031f0", language="de", translator=Translator("de")
    )
    assert "hasLocalMeasurementDisplayOverride" in script
    assert "reset-main-value-size" in script
    assert "delete preferences.mainValueSize" in script
    assert ".measurement-details-header" in DASHBOARD_CSS
    assert ".expert-details > summary::after" not in DASHBOARD_CSS
    assert ".measurement-override-row[hidden]" in DASHBOARD_CSS


def test_847_public_defaults_are_installation_neutral() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert config["version"] == "9.0.0"
    analysis = config["options"]["analysis"]
    assert analysis["external_temperature_entity"] == ""
    assert analysis["external_temperature_name"] == ""
    assert analysis["pressure_weather_entity_primary"] == ""
    assert analysis["pressure_weather_entity_secondary"] == ""
    assert analysis["cosmic_hint_enabled"] is False
