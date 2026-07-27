from __future__ import annotations

import importlib
import sys
import types
import unittest
from types import SimpleNamespace

from gmc_bridge.device_profiles import DeviceCapabilities
from gmc_bridge.errors import GmcTimeout
from gmc_bridge.serial_device import read_sample


class FakeSerialDevice:
    def __init__(self, *, fail_temperature: bool = False) -> None:
        self.fail_temperature = fail_temperature
        self.calls: list[str] = []

    def get_cpm(self) -> int:
        self.calls.append("cpm")
        return 37

    def get_temperature_c(self) -> float:
        self.calls.append("temperature")
        if self.fail_temperature:
            raise GmcTimeout("simulated temperature timeout")
        return 22.5

    def get_voltage_v(self) -> float:
        self.calls.append("voltage")
        return 3.2

    def get_gyro(self) -> tuple[int, int, int]:
        self.calls.append("gyro")
        return (1, 2, 3)


class FakePublishInfo:
    rc = 0

    def wait_for_publish(self, timeout: float | None = None) -> bool:
        return True


class FakeMqttClient:
    def __init__(self, *args: object, **kwargs: object) -> None:
        self.published: list[tuple[str, str, int, bool]] = []

    def username_pw_set(self, *args: object, **kwargs: object) -> None: pass
    def enable_logger(self, *args: object, **kwargs: object) -> None: pass
    def will_set(self, *args: object, **kwargs: object) -> None: pass
    def reconnect_delay_set(self, *args: object, **kwargs: object) -> None: pass
    def max_queued_messages_set(self, *args: object, **kwargs: object) -> None: pass
    def max_inflight_messages_set(self, *args: object, **kwargs: object) -> None: pass
    def connect_async(self, *args: object, **kwargs: object) -> None: pass
    def loop_start(self) -> None: pass
    def loop_stop(self) -> None: pass
    def disconnect(self) -> None: pass

    def publish(self, topic: str, payload: str, qos: int, retain: bool) -> FakePublishInfo:
        self.published.append((topic, payload, qos, retain))
        return FakePublishInfo()


def _load_mqtt_module():
    mqtt_client = types.ModuleType("paho.mqtt.client")
    mqtt_client.CallbackAPIVersion = SimpleNamespace(VERSION2=2)
    mqtt_client.MQTT_ERR_SUCCESS = 0
    mqtt_client.Client = FakeMqttClient
    mqtt_pkg = types.ModuleType("paho.mqtt")
    mqtt_pkg.client = mqtt_client
    paho_pkg = types.ModuleType("paho")
    paho_pkg.mqtt = mqtt_pkg
    sys.modules.setdefault("paho", paho_pkg)
    sys.modules.setdefault("paho.mqtt", mqtt_pkg)
    sys.modules.setdefault("paho.mqtt.client", mqtt_client)
    sys.modules.pop("gmc_bridge.mqtt_pub", None)
    return importlib.import_module("gmc_bridge.mqtt_pub")


class SerialAndMqttIntegrationTests(unittest.TestCase):
    def test_optional_serial_failure_keeps_valid_cpm_and_stops_command_chain(self) -> None:
        device = FakeSerialDevice(fail_temperature=True)
        result = read_sample(
            device,
            read_gyro=True,
            capabilities=DeviceCapabilities(cpm=True, temperature=True, voltage=True, gyro=True, gyro_probe_requested=True),
        )
        self.assertEqual(result.state, {"cpm": 37})
        self.assertTrue(result.available["cpm"])
        self.assertEqual(result.optional_errors[0].sensor, "temperature")
        self.assertTrue(result.reconnect_required)
        self.assertEqual(device.calls, ["cpm", "temperature"])

    def test_complete_serial_sample_and_mqtt_retained_state_sync(self) -> None:
        device = FakeSerialDevice()
        sample = read_sample(
            device,
            read_gyro=True,
            capabilities=DeviceCapabilities(cpm=True, temperature=True, voltage=True, gyro=True, gyro_probe_requested=True),
        )
        self.assertEqual(sample.state["gyro_z"], 3)
        mqtt_pub = _load_mqtt_module()
        settings = SimpleNamespace(
            ui_language="de", read_gyro=True, mqtt_username="", mqtt_password="",
            mqtt_host="localhost", mqtt_port=1883, publish_advanced_sensors=False,
            heartbeat_enabled=False, read_device_time=False, gmcmap_enabled=False,
        )
        publisher = mqtt_pub.MqttPublisher(settings, "SERIAL-A", "GMC-500+")
        publisher._connected = True
        publisher._discovery_dirty = False
        publisher._device_online = True
        ok = publisher.publish_sample(sample.state, sample.available)
        self.assertTrue(ok)
        published = publisher.client.published
        self.assertTrue(any(topic == publisher.state_topic and '"cpm":37' in payload for topic, payload, _qos, _retain in published))
        self.assertTrue(any(topic == publisher.availability_topic and payload == "online" for topic, payload, _qos, _retain in published))


if __name__ == "__main__":
    unittest.main()
