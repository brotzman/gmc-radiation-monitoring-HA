from __future__ import annotations

import io
import json
from unittest.mock import patch
from urllib.error import HTTPError

from gmc_bridge.home_assistant import HomeAssistantPressureClient, HomeAssistantTemperatureClient


class Response(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def response(payload):
    return Response(json.dumps(payload).encode())


def test_pressure_client_falls_back_to_weather_entity_aliases_after_404():
    states = [
        {
            "entity_id": "weather.forecast_home_2",
            "state": "sunny",
            "attributes": {"friendly_name": "Forecast Home", "pressure": 1021.0, "pressure_unit": "hPa"},
        },
        {
            "entity_id": "weather.forecast_balkon",
            "state": "sunny",
            "attributes": {"friendly_name": "Forecast Balkon", "pressure": 1020.8, "pressure_unit": "hPa"},
        },
    ]

    def fake_urlopen(request, timeout):
        if request.full_url.endswith("/states/weather.forecast_home"):
            raise HTTPError(request.full_url, 404, "Not Found", hdrs=None, fp=None)
        if request.full_url.endswith("/states"):
            return response(states)
        if request.full_url.endswith("/states/weather.forecast_balkon"):
            return response(states[1])
        raise AssertionError(request.full_url)

    client = HomeAssistantPressureClient(
        entity_ids=("weather.forecast_home", "weather.forecast_balkon"), token="x"
    )
    with patch("gmc_bridge.home_assistant.urlopen", side_effect=fake_urlopen):
        result = client.get_pressure()
    assert result.available
    assert result.source_count == 2
    assert result.sources[0].friendly_name == "Forecast Home"


def test_temperature_client_accepts_stale_explicit_sensor_value():
    payload = {
        "entity_id": "sensor.arbeitszimmer_temperatur",
        "state": "22.4",
        "attributes": {
            "friendly_name": "Arbeitszimmer Temperatur",
            "device_class": "temperature",
            "unit_of_measurement": "°C",
        },
        "last_updated": "2026-07-15T00:00:00+00:00",
    }
    with patch("gmc_bridge.home_assistant.urlopen", return_value=response(payload)):
        result = HomeAssistantTemperatureClient(
            entity_id="sensor.arbeitszimmer_temperatur", token="x", max_age_seconds=30
        ).get_temperature()
    assert result.available
    assert result.temperature_c == 22.4
    assert result.error == "Temperature entity state is stale"
