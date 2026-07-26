from __future__ import annotations

from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest
import yaml

from gmc_bridge.device_card_display import measurement_freshness
from gmc_bridge.maintenance import support_diagnostics_text
from gmc_bridge.reports import resolve_period
from gmc_bridge.version import APP_VERSION
from gmc_bridge.workflow_web import _history_chart

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "rootfs/usr/local/lib/gmc_bridge/static"


def _t(text: str, **values: object) -> str:
    return text.format(**values)


def test_release_902_metadata_and_notes_are_current() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "9.1.1"
    assert config["version"] == "9.1.1"
    assert sorted(path.name for path in ROOT.glob("RELEASE_NOTES_*.md")) == [
        "RELEASE_NOTES_9.1.1.md"
    ]
    assert (ROOT / "CHANGELOG.md").read_text(encoding="utf-8").startswith(
        "# Changelog\n\n## 9.1.1\n"
    )


def test_report_periods_cover_month_rolling_and_inclusive_custom_dates() -> None:
    tz = ZoneInfo("UTC")
    now = datetime(2026, 7, 23, 12, 30, tzinfo=tz)

    monthly = resolve_period(
        kind="monthly", selection="specific", month_value="2026-02", tz=tz, now=now
    )
    assert monthly.start_local == datetime(2026, 2, 1, tzinfo=tz)
    assert monthly.end_local == datetime(2026, 3, 1, tzinfo=tz)
    assert monthly.filename_label == "2026-02"

    rolling = resolve_period(kind="rolling24", selection="specific", tz=tz, now=now)
    assert rolling.end_local == now
    assert rolling.start_local == now - timedelta(hours=24)

    custom = resolve_period(
        kind="custom",
        selection="specific",
        start_value="2026-07-01",
        end_value="2026-07-03",
        tz=tz,
        now=now,
    )
    assert custom.start_local == datetime(2026, 7, 1, tzinfo=tz)
    assert custom.end_local == datetime(2026, 7, 4, tzinfo=tz)

    with pytest.raises(ValueError, match="must not be before"):
        resolve_period(
            kind="custom",
            selection="specific",
            start_value="2026-07-03",
            end_value="2026-07-01",
            tz=tz,
            now=now,
        )


def test_measurement_freshness_is_independent_from_connection_state() -> None:
    current = measurement_freshness(
        online=True, age_seconds=10, scan_interval_seconds=15, t=_t
    )
    delayed = measurement_freshness(
        online=True, age_seconds=90, scan_interval_seconds=15, t=_t
    )
    stale = measurement_freshness(
        online=True, age_seconds=600, scan_interval_seconds=15, t=_t
    )
    reconnecting = measurement_freshness(
        online=False,
        age_seconds=None,
        scan_interval_seconds=15,
        runtime_reason="serial_error",
        t=_t,
    )

    assert current["state"] == "current"
    assert delayed["state"] == "delayed"
    assert stale["state"] == "stale"
    assert reconnecting["state"] == "reconnecting"
    assert "10 s" in current["label"]


class _SupportStore:
    def get_metadata(self) -> dict[str, object]:
        return {
            "app_version": "9.1.1",
            "report_timezone": "Europe/Berlin",
            "configured_ports": "/dev/ttyUSB0,/dev/serial/by-id/private-device",
            "mqtt_password": "top-secret",
            "api_token": "private-token",
        }

    def list_devices(self) -> list[dict[str, object]]:
        return [
            {
                "configured_name": "Office counter",
                "device_model": "GMC-500+",
                "serial": "ABCDEF123456",
                "runtime_online": True,
                "runtime_status": "online",
                "runtime_status_reason": "measurement_ok",
                "timestamp_utc": 1_721_735_000,
                "scan_interval_seconds": 15,
                "serial_error_count": 2,
                "serial_reconnect_count": 1,
                "stored_samples": 1234,
            }
        ]

    def schema_version(self) -> int:
        return 8

    def cached_quick_check(self, *, max_age_seconds: int) -> str:
        assert max_age_seconds == 60
        return "ok"

    def database_stats(self) -> dict[str, object]:
        return {
            "measurements": 1234,
            "raw_measurements": 1300,
            "size_bytes": 4096,
            "first_timestamp_utc": 1,
            "last_timestamp_utc": 2,
            "path": "/config/private/gmc.sqlite3",
        }


def test_support_diagnostics_are_copy_safe() -> None:
    text = support_diagnostics_text(_SupportStore())
    assert "serial …3456" in text
    assert "ABCDEF123456" not in text
    assert "/dev/ttyUSB0" not in text
    assert "top-secret" not in text
    assert "private-token" not in text
    assert "/config/private" not in text
    assert "Schema: 8" in text


def test_history_chart_marks_and_breaks_real_data_gaps() -> None:
    points = [
        {"timestamp_utc": 0, "cpm": 10.0, "raw_cpm": 10.0, "corrected_cpm": 10.0},
        {"timestamp_utc": 60, "cpm": 11.0, "raw_cpm": 11.0, "corrected_cpm": 11.0},
        {"timestamp_utc": 660, "cpm": 12.0, "raw_cpm": 12.0, "corrected_cpm": 12.0},
        {"timestamp_utc": 720, "cpm": 13.0, "raw_cpm": 13.0, "corrected_cpm": 13.0},
    ]
    output = _history_chart(points, [], [], ZoneInfo("UTC"), _t)
    assert 'class="history-gap-band"' in output
    assert output.count("history-accepted-line") == 2
    assert "No measurement data between" in output
    assert "data-chart-reset" in output
    assert "data-chart-download" in output


def test_release_902_ui_contains_presets_diagnostics_and_mobile_touch_targets() -> None:
    report_web = (ROOT / "rootfs/usr/local/lib/gmc_bridge/report_web.py").read_text(
        encoding="utf-8"
    )
    http = (ROOT / "rootfs/usr/local/lib/gmc_bridge/report_web_http.py").read_text(
        encoding="utf-8"
    )
    js = (ASSETS / "dashboard.js").read_text(encoding="utf-8")
    css = (ASSETS / "dashboard.css").read_text(encoding="utf-8")
    automation = (ROOT / "rootfs/usr/local/lib/gmc_bridge/automation.py").read_text(
        encoding="utf-8"
    )

    for preset in ("today", "yesterday", "rolling24", "rolling7", "month", "custom"):
        assert f'data-report-preset="{preset}"' in report_web
    assert "/api/support-diagnostics" in http
    assert "REPORT-PREVIEW-01" in js
    assert "DIAGNOSTICS-COPY-01" in js
    assert "min-height:2.75rem" in css
    assert "env(safe-area-inset" in css
    assert "active_since_utc" in automation
    assert "_resolved" in automation
