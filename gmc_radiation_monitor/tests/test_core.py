import importlib.util
import json
import sys
import threading
import types
import unittest
from pathlib import Path
from unittest import mock

try:
    import paho.mqtt.client
except ImportError:
    paho = types.ModuleType("paho")
    paho_mqtt = types.ModuleType("paho.mqtt")
    paho_client = types.ModuleType("paho.mqtt.client")
    paho_client.MQTT_ERR_SUCCESS = 0
    paho_mqtt.client = paho_client
    paho.mqtt = paho_mqtt
    sys.modules["paho"] = paho
    sys.modules["paho.mqtt"] = paho_mqtt
    sys.modules["paho.mqtt.client"] = paho_client

MODULE_PATH = Path(__file__).parents[1] / "rootfs/usr/local/bin/gmc_bridge.py"
spec = importlib.util.spec_from_file_location("gmc_bridge_launcher", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules["gmc_bridge_launcher"] = mod
spec.loader.exec_module(mod)


class CoreTests(unittest.TestCase):
    def setUp(self):
        mod.STOP_EVENT.clear()

    def test_high_cpm_gate_requires_consecutive_confirmations(self):
        gate = mod.HighCpmGate(10000, 3)
        self.assertFalse(gate.accept(12000))
        self.assertFalse(gate.accept(13000))
        self.assertTrue(gate.accept(14000))
        self.assertTrue(gate.just_confirmed)
        self.assertTrue(gate.accept(15000))
        self.assertFalse(gate.just_confirmed)
        self.assertEqual(gate.pending, 3)

    def test_high_cpm_gate_resets_on_normal_value(self):
        gate = mod.HighCpmGate(10000, 3)
        self.assertFalse(gate.accept(12000))
        self.assertTrue(gate.accept(100))
        self.assertEqual(gate.state, mod.HighCpmGate.NORMAL)

    def test_slugify_is_safe_for_mqtt_ids(self):
        self.assertEqual(mod.slugify("AB:CD / 12"), "ab_cd_12")

    def test_parse_bool_is_strict(self):
        self.assertTrue(mod.parse_bool("READ_GYRO", "true"))
        self.assertFalse(mod.parse_bool("READ_GYRO", "FALSE"))
        with self.assertRaises(ValueError):
            mod.parse_bool("READ_GYRO", "banana")

    def test_settings_validation_matches_schema_minimum(self):
        settings = self._settings(scan_interval=4)
        with self.assertRaises(ValueError):
            settings.validate()
        self._settings(scan_interval=5).validate()

    def test_gyro_values_are_decoded_as_signed_int16(self):
        device = mod.SerialGmc.__new__(mod.SerialGmc)
        device.port = "/dev/test-gmc"
        device.heartbeat_active = False
        device._discard_pending_input = lambda: None
        device.request_until_idle = lambda command, max_size=32, idle_timeout=0.05: bytes.fromhex(
            "001b fffb ff14 aa"
        )
        self.assertEqual(device.get_gyro(), (27, -5, -236))

    def test_format_published_sample_handles_full_sample(self):
        sample = {
            "cpm": 12,
            "temperature_c": 31.1,
            "voltage_v": 4.0,
            "gyro_x": 27,
            "gyro_y": -5,
            "gyro_z": -236,
        }
        self.assertEqual(
            mod.format_published_sample(sample),
            "Published CPM=12 temperature=31.1°C voltage=4.0V gyro=(27, -5, -236)",
        )

    def test_identity_change_has_dedicated_fatal_exception(self):
        with self.assertRaises(mod.DeviceIdentityChanged):
            mod.ensure_same_serial("aaaa", "bbbb")

    def test_read_sample_keeps_cpm_when_gyro_fails(self):
        device = types.SimpleNamespace(
            get_cpm=lambda: 17,
            get_temperature_c=lambda: 26.8,
            get_voltage_v=lambda: 4.2,
            get_gyro=mock.Mock(side_effect=mod.GmcTimeout("gyro timeout")),
        )
        result = mod.read_sample(device, True)
        self.assertEqual(result.state["cpm"], 17)
        self.assertEqual(result.state["temperature_c"], 26.8)
        self.assertEqual(result.state["voltage_v"], 4.2)
        self.assertFalse(result.available["gyro"])
        self.assertTrue(result.reconnect_required)
        self.assertEqual(result.optional_errors[0].sensor, "gyro")

    def test_read_sample_stops_after_first_optional_failure(self):
        voltage = mock.Mock(return_value=4.2)
        gyro = mock.Mock(return_value=(1, 2, 3))
        device = types.SimpleNamespace(
            get_cpm=lambda: 17,
            get_temperature_c=mock.Mock(side_effect=mod.GmcTimeout("temp timeout")),
            get_voltage_v=voltage,
            get_gyro=gyro,
        )
        result = mod.read_sample(device, True)
        voltage.assert_not_called()
        gyro.assert_not_called()
        self.assertEqual(result.state, {"cpm": 17})

    def test_cpm_failure_remains_fatal_for_cycle(self):
        device = types.SimpleNamespace(get_cpm=mock.Mock(side_effect=mod.GmcTimeout("cpm")))
        with self.assertRaises(mod.GmcTimeout):
            mod.read_sample(device, False)

    def _settings(self, **overrides):
        values = dict(
            port="/dev/null",
            baudrate=19200,
            scan_interval=60,
            command_timeout=2.0,
            inter_command_delay_ms=150,
            high_cpm_threshold=10000,
            high_cpm_confirmations=3,
            read_gyro=False,
            mqtt_host="localhost",
            mqtt_port=1883,
            mqtt_username="",
            mqtt_password="",
        )
        values.update(overrides)
        return mod.Settings(**values)


class FakePublishInfo:
    def __init__(self, rc=0, published=True):
        self.rc = rc
        self._published = published

    def wait_for_publish(self, timeout=None):
        return self._published

    def is_published(self):
        return self._published


class FakeMqttClient:
    def __init__(self):
        self.published = []
        self.fail_positions = set()
        self._publish_calls = 0
        self.disconnected = False
        self.loop_stopped = False

    def publish(self, topic, payload=None, qos=0, retain=False):
        self._publish_calls += 1
        self.published.append((topic, payload, qos, retain))
        rc = 1 if self._publish_calls in self.fail_positions else 0
        return FakePublishInfo(rc=rc)

    def disconnect(self):
        self.disconnected = True

    def loop_stop(self):
        self.loop_stopped = True


class PublisherBehaviorTests(unittest.TestCase):
    def setUp(self):
        mod.STOP_EVENT.clear()

    def _settings(self, read_gyro=False):
        return mod.Settings(
            port="/dev/null",
            baudrate=19200,
            scan_interval=60,
            command_timeout=2.0,
            inter_command_delay_ms=150,
            high_cpm_threshold=10000,
            high_cpm_confirmations=3,
            read_gyro=read_gyro,
            mqtt_host="localhost",
            mqtt_port=1883,
            mqtt_username="",
            mqtt_password="",
        )

    def _publisher_shell(self, read_gyro=False, connected=True):
        publisher = mod.MqttPublisher.__new__(mod.MqttPublisher)
        publisher.settings = self._settings(read_gyro)
        publisher.serial = "f488c59b0031f0"
        publisher.version = "GMC-320Re 4.52"
        publisher.node_id = "gmc_f488c59b0031f0"
        base = "gmc/f488c59b0031f0"
        publisher.state_topic = f"{base}/state"
        publisher.diagnostics_topic = f"{base}/diagnostics"
        publisher.device_availability_topic = f"{base}/device_availability"
        publisher.availability_topics = {
            "cpm": f"{base}/availability",
            "temperature": f"{base}/temperature_availability",
            "voltage": f"{base}/voltage_availability",
            "gyro": f"{base}/gyro_availability",
        }
        publisher.availability_topic = publisher.availability_topics["cpm"]
        publisher.measurement_availability_topic = publisher.availability_topic
        publisher.gyro_availability_topic = publisher.availability_topics["gyro"]
        publisher._state_lock = threading.RLock()
        publisher._sync_lock = threading.Lock()
        publisher._stopping = threading.Event()
        publisher._connected_event = threading.Event()
        publisher._sync_worker_running = False
        publisher._connected = connected
        publisher._device_online = False
        publisher._channel_ready = {channel: False for channel in publisher.CHANNELS}
        publisher._pending_state_payload = None
        publisher._pending_diagnostics_payload = None
        publisher._discovery_dirty = False
        publisher._published_device_online = None
        publisher._published_channel_online = {channel: None for channel in publisher.CHANNELS}
        publisher._generation = 0
        publisher._synced_generation = -1
        publisher.client = FakeMqttClient()
        return publisher

    def test_disconnect_callback_accepts_paho_v1_and_v2(self):
        for args in [(0,), ({}, 0, None)]:
            publisher = self._publisher_shell()
            publisher._on_disconnect(None, None, *args)
            self.assertFalse(publisher._connected)

    def test_disabling_gyro_removes_retained_discovery_topics(self):
        publisher = self._publisher_shell(read_gyro=False)
        publisher.publish_discovery()
        cleared = {
            topic for topic, payload, qos, retain in publisher.client.published if payload == "" and retain
        }
        expected = set(publisher.GYRO_OBJECT_IDS) | {
            "cps",
            "heartbeat_cpm_60s",
            "heartbeat_enabled",
            "heartbeat_error_count",
            "device_time",
            "device_clock_offset_seconds",
            "device_clock_status",
            "device_time_error_count",
            "gmcmap_upload_status",
            "gmcmap_last_attempt_utc",
            "gmcmap_last_upload_utc",
            "gmcmap_next_upload_utc",
            "gmcmap_last_cpm",
            "gmcmap_upload_success_count",
            "gmcmap_upload_error_count",
            "gmcmap_consecutive_error_count",
            "gmcmap_last_error_utc",
            "gmcmap_last_error",
            "gmcmap_last_http_status",
            "gmcmap_last_response",
            "gmcmap_counter_id_masked",
        }
        self.assertEqual(cleared, {publisher._discovery_topic(x) for x in expected})

    def test_each_measurement_channel_has_own_availability(self):
        publisher = self._publisher_shell(read_gyro=True)
        messages = dict(publisher._discovery_messages())
        for object_id, channel in [
            ("cpm", "cpm"),
            ("temperature", "temperature"),
            ("voltage", "voltage"),
            ("gyro_x", "gyro"),
        ]:
            payload = json.loads(messages[publisher._discovery_topic(object_id)])
            topics = {item["topic"] for item in payload["availability"]}
            self.assertEqual(
                topics, {publisher.device_availability_topic, publisher.availability_topics[channel]}
            )

    def test_optional_gyro_unavailable_does_not_hide_cpm(self):
        publisher = self._publisher_shell(read_gyro=True)
        publisher.set_device_online(True)
        publisher._published_channel_online["gyro"] = True
        publisher.client.published.clear()
        publisher.publish_sample(
            {"cpm": 20, "temperature_c": 26.8, "voltage_v": 4.2},
            {"cpm": True, "temperature": True, "voltage": True, "gyro": False},
        )
        payloads = {(topic, payload) for topic, payload, _, _ in publisher.client.published}
        self.assertIn((publisher.availability_topics["cpm"], "online"), payloads)
        self.assertIn((publisher.availability_topics["gyro"], "offline"), payloads)

    def test_state_is_published_before_channel_online(self):
        publisher = self._publisher_shell()
        publisher.set_device_online(True)
        publisher.client.published.clear()
        publisher.publish_sample({"cpm": 20}, {"cpm": True})
        topics = [item[0] for item in publisher.client.published]
        self.assertLess(
            topics.index(publisher.state_topic), topics.index(publisher.availability_topics["cpm"])
        )

    def test_latest_state_only_is_kept_while_offline(self):
        publisher = self._publisher_shell(connected=False)
        publisher.publish_state({"cpm": 10})
        publisher.publish_state({"cpm": 20})
        self.assertIn('"cpm":20', publisher._pending_state_payload)

    def test_generation_advances_on_state_changes(self):
        publisher = self._publisher_shell(connected=False)
        before = publisher._generation
        publisher.publish_state({"cpm": 10})
        self.assertGreater(publisher._generation, before)

    def test_partial_discovery_failure_is_retried(self):
        publisher = self._publisher_shell(read_gyro=True)
        publisher._discovery_dirty = True
        publisher.client.fail_positions = {4}
        self.assertFalse(publisher.sync_mqtt_state())
        self.assertTrue(publisher._discovery_dirty)
        publisher.client.fail_positions.clear()
        self.assertTrue(publisher.sync_mqtt_state())
        self.assertFalse(publisher._discovery_dirty)

    def test_fault_injection_at_every_sync_publish_position_recovers(self):
        baseline = self._publisher_shell(read_gyro=True)
        baseline._discovery_dirty = True
        baseline._device_online = True
        baseline._channel_ready = {channel: True for channel in baseline.CHANNELS}
        baseline._pending_state_payload = json.dumps(
            {"cpm": 20, "temperature_c": 26.8, "voltage_v": 4.2, "gyro_x": 1, "gyro_y": 2, "gyro_z": 3}
        )
        baseline._pending_diagnostics_payload = json.dumps({"serial_error_count": 0})
        baseline.sync_mqtt_state()
        total_calls = baseline.client._publish_calls
        self.assertGreater(total_calls, 12)

        for fail_position in range(1, total_calls + 1):
            publisher = self._publisher_shell(read_gyro=True)
            publisher._discovery_dirty = True
            publisher._device_online = True
            publisher._channel_ready = {channel: True for channel in publisher.CHANNELS}
            publisher._pending_state_payload = (
                baseline.client.published[-5][1] if False else json.dumps({"cpm": 20})
            )
            publisher._pending_diagnostics_payload = json.dumps({"serial_error_count": 0})
            publisher.client.fail_positions = {fail_position}
            publisher.sync_mqtt_state()
            publisher.client.fail_positions.clear()
            for _ in range(3):
                publisher.sync_mqtt_state()
            self.assertFalse(publisher._discovery_dirty, fail_position)
            self.assertIsNone(publisher._pending_state_payload, fail_position)
            self.assertIsNone(publisher._pending_diagnostics_payload, fail_position)

    def test_shutdown_blocks_new_non_offline_publishes(self):
        publisher = self._publisher_shell()
        publisher._stopping.set()
        with self.assertRaises(mod.MqttError):
            publisher._publish_async("topic", "online", retain=True, qos=1)

    def test_queue_has_sync_headroom(self):
        self.assertGreaterEqual(mod.MQTT_MAX_QUEUED_MESSAGES, 100)


if __name__ == "__main__":
    unittest.main()
