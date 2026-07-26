from __future__ import annotations

import time
from pathlib import Path

import yaml

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication, _format_live_dose
from gmc_bridge.runtime_options import runtime_environment
from gmc_bridge.web_assets import DASHBOARD_CSS, render_dashboard_script
from gmc_bridge.translations import Translator


ROOT = Path(__file__).resolve().parents[1]


def test_846_configuration_and_runtime_environment() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert config["version"] == "9.3.0"
    assert config["options"]["interface"]["main_value_size"] == "large"
    assert config["options"]["interface"]["custom_value_font_size_px"] == 36
    assert config["schema"]["interface"]["main_value_size"] == "list(small|medium|large|custom)"
    assert config["schema"]["interface"]["custom_value_font_size_px"] == "int(20,64)"
    env = runtime_environment(config["options"], "reports")
    assert env["MAIN_VALUE_SIZE"] == "large"
    assert env["CUSTOM_VALUE_FONT_SIZE_PX"] == "36"


def test_846_live_dose_formatting_is_magnitude_and_locale_aware() -> None:
    assert _format_live_dose(0.0779, "de") == ("0,0779", "µSv/h")
    assert _format_live_dose(12.44, "de") == ("12,4", "µSv/h")
    assert _format_live_dose(1250.0, "en") == ("1.25", "mSv/h")
    assert _format_live_dose(None, "en") == ("—", "µSv/h")


def test_846_device_card_contains_hierarchy_and_display_controls(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite", retention_days=90)
    now = int(time.time())
    store.upsert_device_registry(
        "f488c59b0031f0",
        {
            "configured_name": "GMC-320",
            "device_model": "GMC-320 Re 4.52",
            "runtime_online": True,
            "runtime_status": "online",
            "last_seen_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(now - 7)),
            "scan_interval_seconds": 60,
            "cpm_per_usvh": 154.0,
            "tube_model": "M4011",
        },
    )
    store.insert_measurement(
        {
            "cpm": 12,
            "derived_dose_usvh": 0.0779,
            "measurement_quality_index": 100,
            "detector_type": "M4011",
            "active_tube": "M4011",
        },
        device_serial="f488c59b0031f0",
        timestamp_utc=now - 7,
    )
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
        main_value_size="large",
        custom_value_font_size_px=36,
    )
    page = app.render_index(language_override="de").decode("utf-8")
    assert 'data-main-value-size="large"' in page
    assert 'data-custom-value-font-size-px="36"' in page
    assert '<h3>GMC-320</h3>' in page
    assert 'class="device-model-line">GMC-320 Re 4.52</span>' in page
    assert 'class="device-id">ID: f488c59b0031f0</small>' in page
    assert 'class="dose-number" data-live="dose-number">0,0779</span>' in page
    assert 'class="dose-unit" data-live="dose-unit">µSv/h</span>' in page
    assert 'Hauptmesswert Schriftgröße' in page
    assert 'value="small"' in page and 'value="custom"' in page


def test_846_css_and_script_support_all_sizes() -> None:
    for size in ("small", "medium", "large", "custom"):
        assert f'body[data-main-value-size="{size}"]' in DASHBOARD_CSS
    assert "--custom-main-value-font-size" in DASHBOARD_CSS
    assert ".dose-number" in DASHBOARD_CSS and ".dose-unit" in DASHBOARD_CSS
    script = render_dashboard_script(selected_serial="abc", language="de", translator=Translator("de"))
    assert "applyMeasurementDisplayPreferences" in script
    assert "customValueFontSizePx" in script
