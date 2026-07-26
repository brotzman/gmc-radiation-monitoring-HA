from __future__ import annotations

import json
from pathlib import Path

import yaml
from gmc_bridge.calibration_http import persist_calibration_profile
from gmc_bridge.gmcmap import AcpmAccumulator
from gmc_bridge.history import HistoryRow, HistoryStore
from gmc_bridge.report_statistics import build_statistics
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.scientific_analysis import counting_uncertainty
from gmc_bridge.time_series import independent_count_windows, time_weighted_summary
from gmc_bridge.translations import validate_catalogs
from gmc_bridge.version import APP_VERSION
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "rootfs/usr/local/lib/gmc_bridge"
DOCS = ROOT / "rootfs/usr/local/share/gmc-bridge/docs"


def _row(timestamp: int, cpm: int) -> HistoryRow:
    return HistoryRow("SERIAL", timestamp, cpm, None, None, None, None, None, "accepted")


def test_900_release_metadata_and_single_release_notes() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "9.2.0"
    assert config["version"] == "9.2.0"
    notes = sorted(path.name for path in ROOT.glob("RELEASE_NOTES_*.md"))
    assert notes == ["RELEASE_NOTES_9.2.0.md"]
    text = (ROOT / notes[0]).read_text(encoding="utf-8")
    for phrase in (
        "measurement freshness",
        "report presets",
        "copy-safe support-diagnostics",
        "database schema 8",
    ):
        assert phrase in text


def test_fast_cpm_polls_are_not_treated_as_independent_minutes() -> None:
    rows = [_row(1_800_000_000 + offset, 60) for offset in range(0, 121, 5)]
    selected = independent_count_windows(
        rows, timestamp=lambda row: row.timestamp_utc, minimum_separation_seconds=60
    )
    result = counting_uncertainty(rows)
    assert [row.timestamp_utc for row in selected] == [1_800_000_000, 1_800_000_060, 1_800_000_120]
    assert result["raw_sample_count"] == 25
    assert result["independent_sample_count"] == 3
    assert result["overlap_excluded_count"] == 22
    assert result["duration_seconds"] == 180


def test_time_weighting_does_not_let_dense_bursts_hide_long_gaps() -> None:
    start = 1_800_000_000
    rows = [
        _row(start, 10),
        _row(start + 60, 10),
        _row(start + 3_500, 100),
        _row(start + 3_560, 100),
    ]
    summary = time_weighted_summary(
        rows,
        timestamp=lambda row: row.timestamp_utc,
        value=lambda row: row.cpm,
        start_utc=start,
        end_utc=start + 3_600,
        expected_interval_seconds=60,
    )
    assert summary.available is True
    assert summary.gap_count == 1
    assert summary.coverage_percent < 10.0
    assert summary.mean == 64.0


def test_report_statistics_separate_sample_and_time_coverage() -> None:
    start = 1_800_000_000
    rows = [_row(start + offset, 20) for offset in (0, 5, 10, 15, 20, 25, 30)]
    stats = build_statistics(
        rows,
        expected_count=60,
        start_utc=start,
        end_utc=start + 3_600,
        scan_interval_seconds=60,
    )
    assert stats["sample_completeness_percent"] > stats["time_coverage_percent"]
    assert stats["time_coverage_percent"] < 2.0
    assert stats["cpm_mean"] == 20.0


def test_gmcmap_acpm_is_rolling_time_weighted_and_gap_aware() -> None:
    accumulator = AcpmAccumulator(window_seconds=3_600, expected_interval_seconds=60)
    assert accumulator.add(10, timestamp_utc=0) == 10.0
    assert accumulator.add(20, timestamp_utc=60) == 15.0
    # A long gap is not integrated; the fallback remains finite and bounded.
    value = accumulator.add(100, timestamp_utc=3_000)
    assert 10.0 <= value <= 100.0
    accumulator.add(80, timestamp_utc=3_060)
    assert accumulator.window_minutes == 60.0
    assert accumulator.sample_count <= 4


def test_calibration_dossier_is_persisted_with_traceability(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "calibration.sqlite3")
    store.upsert_device_registry("SERIAL", {"device_model": "GMC-320"})
    checksum = "a" * 64
    payload = {
        "profile_id": ["lab_profile"],
        "display_name": ["Lab profile"],
        "detector_type": ["M4011"],
        "device_serial": ["SERIAL"],
        "cpm_per_usvh": ["154"],
        "dead_time_model": ["nonparalyzable"],
        "source": ["laboratory"],
        "calibration_type": ["traceable_laboratory"],
        "device_model": ["GMC-320 Re 4.52"],
        "device_serial_number": ["SERIAL"],
        "firmware_version": ["4.52"],
        "laboratory": ["Reference laboratory"],
        "accreditation": ["ISO/IEC 17025"],
        "certificate_number": ["CERT-900"],
        "calibration_date": ["2026-07-01"],
        "valid_until": ["2027-07-01"],
        "measurement_geometry": ["Documented fixed geometry"],
        "environment_conditions": ["20 C; 1013 hPa"],
        "operator_name": ["Operator"],
        "certificate_sha256": [checksum],
        "calibration_uncertainty_percent": ["5"],
        "conversion_factor_uncertainty_percent": ["3"],
        "comment": ["Traceable comparison"],
    }
    persist_calibration_profile(store, payload, translate=lambda text: text)
    device = next(item for item in store.list_devices() if item["serial"] == "SERIAL")
    dossier = device["calibration_dossier"]
    assert dossier["calibration_type"] == "traceable_laboratory"
    assert dossier["certificate_sha256"] == checksum
    assert dossier["laboratory"] == "Reference laboratory"


def test_dashboard_uses_versioned_assets_compact_live_api_and_unified_report_form(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "dashboard.sqlite3")
    store.upsert_device_registry(
        "SERIAL", {"device_model": "GMC-320", "runtime_online": True, "scan_interval_seconds": 60}
    )
    store.insert_measurement({"cpm": 14}, device_serial="SERIAL", timestamp_utc=1_800_000_000)
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
    )
    page = app.render_index(language_override="de", mode_override="advanced").decode()
    assert './assets/dashboard.css?v=9.2.0' in page
    assert './assets/dashboard.js?v=9.2.0' in page
    assert page.count('id="custom-report-form"') == 1
    assert 'id="report-generation-preview"' in page
    payload = app.live_devices_payload(language_override="de", device_override="SERIAL")
    assert payload["connected_count"] == 1
    assert payload["devices"][0]["latest_value"] == "14 CPM"
    json.dumps(payload)


def test_static_assets_include_mobile_accessibility_and_retry_behaviour() -> None:
    css = (LIB / "static/dashboard.css").read_text(encoding="utf-8")
    script = (LIB / "static/dashboard.js").read_text(encoding="utf-8")
    compact_css = "".join(css.split())
    for selector in (
        "@media(prefers-reduced-motion:reduce)",
        "@media(forced-colors:active)",
        ".unified-report-form.form-grid",
        'input[type="date"]',
    ):
        assert selector in compact_css
    for phrase in (
        "resolveDashboardUrl",
        "liveRefreshDelayMs",
        "Math.min(120000",
        "setAttribute('role','tooltip')",
        "Escape",
        "refreshReportPreview",
    ):
        assert phrase in script


def test_architecture_modules_and_size_limits_are_enforced() -> None:
    expected = (
        "time_series.py",
        "report_statistics.py",
        "baseline_cache.py",
        "runtime_diagnostics.py",
        "interfaces.py",
        "report_server.py",
        "report_http_responses.py",
        "report_http_utils.py",
    )
    assert all((LIB / name).is_file() for name in expected)
    assert len((LIB / "report_web.py").read_text(encoding="utf-8").splitlines()) < 1_800
    assert len((LIB / "report_web_http.py").read_text(encoding="utf-8").splitlines()) < 1_000


def test_translation_catalogues_are_complete_and_not_likely_untranslated() -> None:
    assert validate_catalogs() == []


def test_all_eight_manuals_are_current_and_describe_version_900() -> None:
    manuals = sorted(DOCS.glob("*.pdf"))
    assert len(manuals) == 8
    assert all("9.2.0" in path.name for path in manuals)
    for manual in manuals:
        reader = PdfReader(str(manual))
        text = "\n".join((page.extract_text() or "") for page in (reader.pages[0], reader.pages[-1]))
        assert "9.2.0" in text
        assert len(reader.pages) >= 15
