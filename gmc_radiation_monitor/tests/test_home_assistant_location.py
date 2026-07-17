from __future__ import annotations

import json
import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from gmc_bridge.history import HistoryStore
from gmc_bridge.home_assistant import HomeAssistantConfigClient, HomeAssistantLocation
from gmc_bridge.report_web import ReportApplication


class _Response(BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


class _FakeLocationClient:
    def get_location(self) -> HomeAssistantLocation:
        return HomeAssistantLocation(
            available=True,
            location_name="Dom",
            latitude=45.81501,
            longitude=15.98192,
            elevation=122,
            country="HR",
            time_zone="Europe/Zagreb",
        )


def test_home_assistant_config_client_reads_and_caches_location():
    payload = json.dumps(
        {
            "location_name": "Dom",
            "latitude": 45.81501,
            "longitude": 15.98192,
            "elevation": 122,
            "country": "hr",
            "time_zone": "Europe/Zagreb",
        }
    ).encode()
    client = HomeAssistantConfigClient(token="secret", cache_seconds=300)
    with patch("gmc_bridge.home_assistant.urlopen", return_value=_Response(payload)) as call:
        first = client.get_location()
        second = client.get_location()
    assert first == second
    assert first.available is True
    assert first.location_name == "Dom"
    assert first.country == "HR"
    assert call.call_count == 1
    request = call.call_args.args[0]
    assert request.get_header("Authorization") == "Bearer secret"


def test_location_is_rendered_in_croatian_without_external_lookup():
    with tempfile.TemporaryDirectory() as temp_dir:
        store = HistoryStore(Path(temp_dir) / "history.sqlite3")
        app = ReportApplication(
            store=store,
            timezone_name="Europe/Zagreb",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
            ui_language="hr",
            home_assistant_client=_FakeLocationClient(),
        )
        rendered = app.render_index(language_override="hr").decode()
    assert "Lokacija Home Assistanta" in rendered
    assert "Dom" in rendered
    assert "Koordinate: 45.81501, 15.98192" in rendered
    assert "Nadmorska visina: 122 m" in rendered
    assert "vanjskoj usluzi za geokodiranje" in rendered


def test_missing_location_fails_closed_without_breaking_dashboard():
    class Missing:
        def get_location(self):
            return HomeAssistantLocation(available=False, error="unavailable")

    with tempfile.TemporaryDirectory() as temp_dir:
        store = HistoryStore(Path(temp_dir) / "history.sqlite3")
        app = ReportApplication(
            store=store,
            timezone_name="UTC",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
            ui_language="de",
            home_assistant_client=Missing(),
        )
        rendered = app.render_index(language_override="de").decode()
    assert "Standort nicht verfügbar" in rendered
    assert "Zeitzone: UTC" in rendered
