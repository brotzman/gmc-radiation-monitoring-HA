from __future__ import annotations

import io
import json
from unittest.mock import patch

from gmc_bridge.home_assistant import HomeAssistantTemperatureClient


class Response(io.BytesIO):
    status = 200

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def response(payload):
    return Response(json.dumps(payload).encode())


def test_reads_configured_celsius_entity():
    payload = {
        "entity_id": "sensor.room_temperature",
        "state": "21.7",
        "attributes": {
            "friendly_name": "Raumklima (Arbeitszimmer) Temperatur",
            "device_class": "temperature",
            "unit_of_measurement": "°C",
        },
    }
    with patch("gmc_bridge.home_assistant.urlopen", return_value=response(payload)):
        result = HomeAssistantTemperatureClient(
            entity_id="sensor.room_temperature", token="x"
        ).get_temperature()
    assert result.available
    assert result.temperature_c == 21.7


def test_converts_fahrenheit():
    payload = {
        "entity_id": "sensor.room_temperature",
        "state": "68",
        "attributes": {"friendly_name": "Room", "device_class": "temperature", "unit_of_measurement": "°F"},
    }
    with patch("gmc_bridge.home_assistant.urlopen", return_value=response(payload)):
        result = HomeAssistantTemperatureClient(
            entity_id="sensor.room_temperature", token="x"
        ).get_temperature()
    assert result.available
    assert result.temperature_c == 20.0


def test_discovers_by_friendly_name():
    payload = [
        {"entity_id": "sensor.other", "state": "45", "attributes": {"device_class": "humidity"}},
        {
            "entity_id": "sensor.real_temp",
            "state": "22.2",
            "attributes": {
                "friendly_name": "Raumklima (Arbeitszimmer) Temperatur",
                "device_class": "temperature",
                "unit_of_measurement": "°C",
            },
        },
    ]
    with patch("gmc_bridge.home_assistant.urlopen", return_value=response(payload)):
        result = HomeAssistantTemperatureClient(
            friendly_name="Raumklima (Arbeitszimmer)", token="x"
        ).get_temperature()
    assert result.available
    assert result.entity_id == "sensor.real_temp"
