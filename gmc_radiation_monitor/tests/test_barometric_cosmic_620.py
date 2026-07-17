from __future__ import annotations

import json
import math
from datetime import UTC, datetime, timedelta
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from gmc_bridge.barometric_background import build_barometric_cosmic_hint
from gmc_bridge.history import HistoryRow, HistoryStore
from gmc_bridge.home_assistant import (
    HomeAssistantPressure,
    HomeAssistantPressureClient,
    HomeAssistantPressureSource,
)
from gmc_bridge.report_web import ReportApplication


class _Response(BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        self.close()
        return False


def _weather_payload(entity_id: str, name: str, pressure: float, unit: str = "hPa") -> bytes:
    return json.dumps(
        {
            "entity_id": entity_id,
            "state": "sunny",
            "attributes": {
                "friendly_name": name,
                "pressure": pressure,
                "pressure_unit": unit,
            },
            "last_updated": datetime.now(UTC).isoformat(),
        }
    ).encode()


def test_pressure_client_plausibilizes_forecast_home_and_balkon() -> None:
    payloads = {
        "weather.forecast_home_2": _weather_payload("weather.forecast_home_2", "Forecast Home 2", 1012.4),
        "weather.forecast_balkon": _weather_payload("weather.forecast_balkon", "Forecast Balkon", 1013.0),
    }

    def fake_urlopen(request, timeout):
        entity_id = request.full_url.rsplit("/", 1)[-1]
        return _Response(payloads[entity_id])

    client = HomeAssistantPressureClient(
        entity_ids=("weather.forecast_home_2", "weather.forecast_balkon"),
        provider_name="Meteorologisk institutt (Met.no)",
        token="secret",
        max_difference_hpa=5.0,
    )
    with patch("gmc_bridge.home_assistant.urlopen", side_effect=fake_urlopen):
        result = client.get_pressure()
    assert result.available is True
    assert result.source_mode == "plausibilized"
    assert result.source_count == 2
    assert result.pressure_hpa == 1012.7
    assert [source.friendly_name for source in result.sources] == ["Forecast Home 2", "Forecast Balkon"]


def test_pressure_client_rejects_disagreeing_sources() -> None:
    payloads = [
        _weather_payload("weather.forecast_home_2", "Forecast Home 2", 1000.0),
        _weather_payload("weather.forecast_balkon", "Forecast Balkon", 1010.0),
    ]
    client = HomeAssistantPressureClient(
        entity_ids=("weather.forecast_home_2", "weather.forecast_balkon"),
        token="secret",
        max_difference_hpa=5.0,
    )
    with patch("gmc_bridge.home_assistant.urlopen", side_effect=[_Response(value) for value in payloads]):
        result = client.get_pressure()
    assert result.available is False
    assert result.source_mode == "disagreement"
    assert result.source_spread_hpa == 10.0


def test_pressure_is_stored_in_schema_v7(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    store.insert_measurement(
        {"cpm": 16, "pressure_hpa": 1014.2},
        device_serial="abc",
        timestamp_utc=1_700_000_000,
    )
    row = store.query_all(device_serial="abc")[0]
    assert store.schema_version() == 8
    assert row.pressure_hpa == 1014.2


def test_barometric_model_learns_negative_pressure_signature() -> None:
    start = datetime(2026, 1, 1, tzinfo=UTC)
    count = 24 * 40
    rows: dict[str, list[HistoryRow]] = {"a": [], "b": []}
    for index in range(count):
        timestamp = start + timedelta(hours=index)
        phase = (index % 240) / 240.0 * 2.0 * math.pi
        pressure = 1010.0 + 10.0 * math.sin(phase)
        time_profile = 100.0 + 2.0 * math.sin((timestamp.hour / 24.0) * 2.0 * math.pi)
        cpm = time_profile * (1.0 - 0.004 * (pressure - 1010.0))
        rows["a"].append(
            HistoryRow(
                "a",
                int(timestamp.timestamp()),
                round(cpm),
                None,
                None,
                None,
                None,
                None,
                "normal",
                pressure_hpa=pressure,
            )
        )
        rows["b"].append(
            HistoryRow(
                "b",
                int(timestamp.timestamp()),
                round(cpm + 1.0),
                None,
                None,
                None,
                None,
                None,
                "normal",
                pressure_hpa=pressure,
            )
        )
    now = int((start + timedelta(hours=count - 1)).timestamp())
    snapshot = HomeAssistantPressure(
        True,
        pressure_hpa=float(rows["a"][-1].pressure_hpa),
        provider_name="Meteorologisk institutt (Met.no)",
        source_mode="plausibilized",
        source_count=2,
        sources=(
            HomeAssistantPressureSource(
                True, "weather.forecast_home_2", "Forecast Home 2", float(rows["a"][-1].pressure_hpa)
            ),
            HomeAssistantPressureSource(
                True, "weather.forecast_balkon", "Forecast Balkon", float(rows["a"][-1].pressure_hpa)
            ),
        ),
    )
    result = build_barometric_cosmic_hint(
        rows,
        timezone_name="UTC",
        device_weights={"a": 1.0, "b": 0.95},
        tolerance_seconds=60,
        pressure_snapshot=snapshot,
        now_utc=now,
        minimum_days=30,
        minimum_hourly_samples=500,
        minimum_pressure_span_hpa=10.0,
    )
    assert result["learning"] is False
    assert result["pressure_coefficient_percent_per_hpa"] < 0
    assert result["correlation"] < -0.5
    assert result["state"] in {
        "Cosmic influence is possible",
        "Pressure-typical signature is pronounced",
        "No pressure-typical signature",
    }
    assert result["hourly_sample_count"] >= 900


def test_german_dashboard_shows_clean_cosmic_hint_panel(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    now = int(datetime.now(UTC).timestamp())
    store.insert_measurement(
        {"cpm": 16, "pressure_hpa": 1012.7},
        device_serial="abc",
        timestamp_utc=now,
    )

    class PressureClient:
        def get_pressure(self):
            return HomeAssistantPressure(
                True,
                pressure_hpa=1012.7,
                provider_name="Meteorologisk institutt (Met.no)",
                source_mode="plausibilized",
                source_count=2,
                sources=(
                    HomeAssistantPressureSource(True, "weather.forecast_home_2", "Forecast Home 2", 1012.4),
                    HomeAssistantPressureSource(True, "weather.forecast_balkon", "Forecast Balkon", 1013.0),
                ),
            )

    app = ReportApplication(
        store=store,
        timezone_name="UTC",
        scan_interval_seconds=120,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
        pressure_client=PressureClient(),
        cosmic_hint_enabled=True,
    )
    rendered = app.render_index(language_override="de").decode()
    assert "Kosmischer Einfluss – statistischer Hinweis" in rendered
    assert "Luftdruckquelle" not in rendered
    assert "Nur statistischer Hinweis" not in rendered
    assert (
        "Sinkender Luftdruck ist häufig mit einer leicht höheren Intensität kosmisch erzeugter Sekundärstrahlung am Boden verbunden"
        in rendered
    )
