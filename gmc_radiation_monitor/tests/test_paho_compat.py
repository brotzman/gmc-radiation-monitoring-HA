import importlib.util
import sys
import threading
import unittest
import warnings
from pathlib import Path

try:
    import paho.mqtt.client as mqtt
except ImportError:
    mqtt = None

MODULE_PATH = Path(__file__).parents[1] / "rootfs/usr/local/bin/gmc_bridge.py"
mod = None
if mqtt is not None:
    spec = importlib.util.spec_from_file_location("gmc_bridge_paho_launcher", MODULE_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    sys.modules["gmc_bridge_paho_launcher"] = mod
    spec.loader.exec_module(mod)


@unittest.skipIf(mqtt is None or not hasattr(mqtt, "Client"), "real paho-mqtt is not installed")
class RealPahoCompatibilityTests(unittest.TestCase):
    def _publisher_shell(self):
        publisher = mod.MqttPublisher.__new__(mod.MqttPublisher)
        publisher._state_lock = threading.RLock()
        publisher._connected = True
        publisher._published_device_online = True
        publisher._published_channel_online = {channel: True for channel in publisher.CHANNELS}
        publisher._connected_event = threading.Event()
        publisher._connected_event.set()
        publisher._stopping = threading.Event()
        publisher._generation = 0
        publisher._schedule_sync = lambda: None
        return publisher

    def test_real_paho_v1_internal_disconnect_dispatch(self):
        publisher = self._publisher_shell()
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1)
        client.on_disconnect = publisher._on_disconnect
        client._do_on_disconnect(False, mqtt.MQTT_ERR_SUCCESS)
        self.assertFalse(publisher._connected)

    def test_real_paho_v2_internal_disconnect_dispatch(self):
        publisher = self._publisher_shell()
        client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        client.on_disconnect = publisher._on_disconnect
        client._do_on_disconnect(False, mqtt.MQTT_ERR_SUCCESS)
        self.assertFalse(publisher._connected)

    def test_real_paho_v2_reason_code_is_accepted_on_connect(self):
        from paho.mqtt.reasoncodes import ReasonCode

        publisher = self._publisher_shell()
        publisher._discovery_dirty = False
        publisher._published_device_online = None
        publisher._published_channel_online = {channel: None for channel in publisher.CHANNELS}
        reason = ReasonCode(mqtt.PacketTypes.CONNACK, identifier=0)
        publisher._on_connect(None, None, {}, reason, None)
        self.assertTrue(publisher._connected)


if __name__ == "__main__":
    unittest.main()
