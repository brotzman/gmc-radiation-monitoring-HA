from __future__ import annotations

import re
import time
from pathlib import Path

import yaml

from gmc_bridge.history import HistoryStore
from gmc_bridge.number_format import format_number, localize_numeric_text
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import Translator
from gmc_bridge.version import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "rootfs/usr/local/lib/gmc_bridge"


def _app(tmp_path: Path) -> ReportApplication:
    store = HistoryStore(tmp_path / "history.sqlite3")
    now = int(time.time())
    store.upsert_device_registry(
        "SERIAL-LOCAL",
        {
            "device_model": "GMC-500+",
            "configured_name": "Test counter",
            "runtime_online": True,
            "scan_interval_seconds": 15,
            "voltage_v": 4.25,
            "serial_error_count": 1234,
            "serial_reconnect_count": 2345,
            "cpm_discarded_peak_samples": 0,
        },
    )
    for index in range(1234):
        store.insert_measurement(
            {"cpm": 20, "voltage_v": 4.25},
            device_serial="SERIAL-LOCAL",
            timestamp_utc=now - 1233 + index,
            cpm_quality="normal",
            expected_interval_seconds=15,
        )
    return ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=15,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
    )


def test_release_903_metadata_and_manuals_are_current() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "9.3.0"
    assert config["version"] == "9.3.0"
    assert sorted(path.name for path in ROOT.glob("RELEASE_NOTES_*.md")) == [
        "RELEASE_NOTES_9.3.0.md"
    ]
    manuals = sorted((ROOT / "rootfs/usr/local/share/gmc-bridge/docs").glob("*.pdf"))
    assert len(manuals) == 8
    assert all("9.3.0" in path.name for path in manuals)


def test_german_number_formatter_preserves_identifiers() -> None:
    assert format_number(1234567.89, "de", decimals=2, grouping=True) == "1.234.567,89"
    assert format_number(1234567.89, "en", decimals=2, grouping=True) == "1,234,567.89"
    assert localize_numeric_text("20.99 CPM · 1,364 samples", "de", group_plain_integers=True) == (
        "20,99 CPM · 1.364 samples"
    )
    assert localize_numeric_text("9.3.0 · GMC-500+ Re 2.53", "de", group_plain_integers=True) == (
        "9.3.0 · GMC-500+ Re 2.53"
    )
    assert Translator("de")("Completeness: {value:.2f}%", value=12.5) == "Vollständigkeit: 12,50 %"


def test_compact_status_and_german_dashboard_numbers(tmp_path: Path) -> None:
    app = _app(tmp_path)
    german = app.render_index(language_override="de", mode_override="advanced").decode()
    status = german.split('<section class="status-strip"', 1)[1].split("</section>", 1)[0]
    assert '<details class="system-status-panel ok">' in status
    assert "System läuft normal" in status
    assert "Statusdetails anzeigen" in status
    assert 'class="status-details-grid"' in status
    assert status.count('class="status-strip-item') == 6
    assert "Gespeicherte Messwerte: 1.234" in status
    assert "4,25 V" in german
    assert "1.234 Fehler" in german
    assert "2.345 Wiederverbindungen" in german
    assert re.search(r"Datenbank: ok</strong><small>\d+,\d{2} MiB", status)

    english = app.render_index(language_override="en", mode_override="advanced").decode()
    assert "Stored samples: 1,234" in english
    assert "4.25 V" in english
    assert "1,234 errors" in english
    assert "2,345 reconnects" in english


def test_browser_updated_values_use_selected_ui_locale() -> None:
    script = (LIB / "static/dashboard.js").read_text(encoding="utf-8")
    assert "new Intl.NumberFormat(uiLocale" in script
    assert "toLocaleString(uiLocale)" in script
    assert ".toFixed(" not in script
    assert ".toLocaleString()" not in script
