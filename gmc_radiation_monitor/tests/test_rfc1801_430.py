from __future__ import annotations

import sys
import types
from collections import deque

try:
    import paho.mqtt.client  # type: ignore
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

from datetime import datetime
from types import SimpleNamespace

import pytest
from gmc_bridge.config import Settings
from gmc_bridge.device_profiles import DeviceCapabilities, resolve_device_profile, split_device_version
from gmc_bridge.mqtt_pub import MqttPublisher
from gmc_bridge.serial_device import GmcProtocolError, SerialGmc
from gmc_bridge.service import STOP_EVENT, _device_clock_diagnostics, _publish_heartbeat_until


class CommandStub(SerialGmc):
    def __init__(self, responses: dict[bytes, bytes]):
        self.responses = responses
        self.rfc1801 = True
        self.heartbeat_active = False
        self.stop_event = SimpleNamespace(is_set=lambda: False, wait=lambda timeout: False)

    def request_exact(self, command: bytes, size: int) -> bytes:
        payload = self.responses[command]
        assert len(payload) == size
        return payload

    def request_until_idle(self, command: bytes, *, max_size: int = 32, idle_timeout: float = 0.05) -> bytes:
        payload = self.responses[command]
        assert len(payload) <= max_size
        return payload


def test_rfc1801_voltage_datetime_and_version_split():
    device = CommandStub(
        {
            b"<GETVOLT>>": b"3.97v",
            b"<GETDATETIME>>": bytes([26, 7, 12, 14, 35, 9, 0xAA]),
        }
    )
    assert device.get_voltage_v() == 3.97
    assert device.get_datetime() == datetime(2026, 7, 12, 14, 35, 9)
    assert split_device_version("GMC-500+ 2.20") == ("GMC-500+", "2.20")
    assert split_device_version("GMC-320Re 4.52") == ("GMC-320", "Re 4.52")


def test_rfc1801_rejects_invalid_datetime_terminator():
    device = CommandStub({b"<GETDATETIME>>": bytes([26, 7, 12, 14, 35, 9, 0])})
    with pytest.raises(GmcProtocolError):
        device.get_datetime()


def test_profiles_limit_heartbeat_and_device_clock_to_rfc1801_families():
    profile_320 = resolve_device_profile("GMC-320Re 4.52")
    profile_500 = resolve_device_profile("GMC-500+ 2.20")
    profile_600 = resolve_device_profile("GMC-600+Re 1.14")
    assert profile_320.heartbeat_hint != "yes"
    assert profile_320.device_time_hint != "yes"
    assert profile_500.heartbeat_hint == "yes"
    assert profile_500.device_time_hint == "yes"
    assert profile_600.heartbeat_hint == "yes"
    assert profile_600.device_time_hint == "yes"


def test_clock_diagnostics_uses_report_timezone_and_threshold(monkeypatch):
    settings = Settings(
        port="/dev/null",
        baudrate=19200,
        scan_interval=60,
        command_timeout=2,
        inter_command_delay_ms=150,
        high_cpm_threshold=10000,
        high_cpm_confirmations=3,
        read_gyro=False,
        mqtt_host="localhost",
        mqtt_port=1883,
        mqtt_username="",
        mqtt_password="",
        report_timezone="Europe/Berlin",
        device_clock_warning_seconds=120,
    )
    result = _device_clock_diagnostics("2026-07-12T12:00:00", settings)
    assert result["device_time"].startswith("2026-07-12T12:00:00")
    assert result["device_clock_status"] in {"ok", "warning"}
    assert isinstance(result["device_clock_offset_seconds"], int)


class HeartbeatDevice:
    def __init__(self, values: list[int]):
        self.values = iter(values)
        self.started = False
        self.stopped = False

    def start_heartbeat(self):
        self.started = True

    def read_heartbeat_cps(self):
        try:
            return next(self.values)
        except StopIteration:
            STOP_EVENT.set()
            return 0

    def stop_heartbeat(self):
        self.stopped = True


class HeartbeatPublisher:
    def __init__(self):
        self.samples: list[dict[str, object]] = []

    def publish_sample(self, sample, available):
        self.samples.append(dict(sample))
        return True


def test_heartbeat_publishes_live_cps_and_rolling_cpm(monkeypatch):
    STOP_EVENT.clear()
    device = HeartbeatDevice([2, 3])
    publisher = HeartbeatPublisher()
    times = iter([0.0, 0.1, 2.0])
    monkeypatch.setattr("gmc_bridge.service.time.monotonic", lambda: next(times, 9.0))
    last = _publish_heartbeat_until(
        device=device,
        publisher=publisher,
        base_state={"cpm": 20},
        available={"cpm": True},
        deadline_monotonic=1.0,
        rolling_cps=deque(maxlen=60),
    )
    STOP_EVENT.clear()
    assert device.started and device.stopped
    assert last == 3
    assert publisher.samples[0]["cps"] == 2
    assert publisher.samples[1]["heartbeat_cpm_60s"] == 5


def test_mqtt_heartbeat_entities_only_exist_when_enabled_and_supported():
    publisher = MqttPublisher.__new__(MqttPublisher)
    publisher.settings = SimpleNamespace(
        read_gyro=False,
        publish_advanced_sensors=True,
        heartbeat_enabled=True,
        read_device_time=True,
    )
    publisher.serial = "device-a"
    publisher.version = "GMC-500+ 2.20"
    publisher.node_id = "gmc_device_a"
    publisher.capabilities = DeviceCapabilities(
        cpm=True,
        voltage=True,
        dual_tube=True,
        device_time=True,
        heartbeat=True,
    )
    base = "gmc/device-a"
    publisher.state_topic = f"{base}/state"
    publisher.diagnostics_topic = f"{base}/diagnostics"
    publisher.device_availability_topic = f"{base}/device_availability"
    publisher.availability_topics = {
        "cpm": f"{base}/availability",
        "temperature": f"{base}/temperature_availability",
        "voltage": f"{base}/voltage_availability",
        "gyro": f"{base}/gyro_availability",
    }
    messages = dict(publisher._discovery_messages())
    assert messages[publisher._discovery_topic("cps")]
    assert messages[publisher._discovery_topic("heartbeat_cpm_60s")]
    assert messages[publisher._discovery_topic("device_time")]


def test_rfc1801_options_are_packaged_and_disabled_safely_by_default():
    from pathlib import Path

    import yaml

    root = Path(__file__).parents[1]
    config = yaml.safe_load((root / "config.yaml").read_text())
    assert config["version"] == "9.0.1"
    devices = config["options"]["devices"] + config["options"]["dual_tube_devices"]
    assert [device["name"] for device in devices] == ["GMC-320", "GMC-500+"]
    assert all(device["read_gyro"] is False for device in devices)
    assert all(device["heartbeat_enabled"] is False for device in devices)
    assert config["options"]["gmcmap"]["enabled"] is False
    assert config["options"]["gmcmap"]["privacy_confirmed"] is False
    device_schema = config["schema"]["devices"][0]
    assert {"read_device_time", "device_clock_warning_seconds", "heartbeat_enabled"} <= set(device_schema)
    runtime_options = (root / "rootfs/usr/local/lib/gmc_bridge/runtime_options.py").read_text()
    assert "READ_DEVICE_TIME" in runtime_options
    assert "DEVICE_CLOCK_WARNING_SECONDS" in runtime_options
    assert "HEARTBEAT_ENABLED" in runtime_options


class RecoveringCommandStub(CommandStub):
    def __init__(self, responses: list[bytes]):
        self.responses_sequence = iter(responses)
        self.rfc1801 = True
        self.heartbeat_active = False
        self.stop_event = SimpleNamespace(is_set=lambda: False, wait=lambda timeout: False)
        self.recoveries = 0

    def request_exact(self, command: bytes, size: int) -> bytes:
        payload = next(self.responses_sequence)
        assert len(payload) == size
        return payload

    def request_until_idle(self, command: bytes, *, max_size: int = 32, idle_timeout: float = 0.05) -> bytes:
        payload = next(self.responses_sequence)
        assert len(payload) <= max_size
        return payload

    def _recover_protocol_stream(self) -> None:
        self.recoveries += 1


def test_getver_accepts_valid_ascii_after_stale_binary_prefix():
    assert SerialGmc._decode_version_bytes(b"\xff\x00GMC-500+ 2.20") == "GMC-500+ 2.20"


def test_gyro_retries_once_after_bad_terminator_and_recovers():
    device = RecoveringCommandStub(
        [
            bytes.fromhex("001c fffa ff15 20"),
            bytes.fromhex("001c fffa ff15 aa"),
        ]
    )
    assert device.get_gyro() == (28, -6, -235)
    assert device.recoveries == 1


def test_voltage_accepts_valid_ascii_after_stale_binary_prefix():
    device = CommandStub({b"<GETVOLT>>": b"\xff\x003.97v"})
    assert device.get_voltage_v() == 3.97


def test_voltage_retries_after_malformed_response_without_leaking_unicode_error():
    device = RecoveringCommandStub([b"\xff\x00bad", b"4.01v"])
    assert device.get_voltage_v() == 4.01
    assert device.recoveries == 1


def test_voltage_invalid_binary_reply_raises_protocol_error():
    device = RecoveringCommandStub([b"\xff\x00bad", b"\xff\x01bad"])
    with pytest.raises(GmcProtocolError, match="Invalid GETVOLT response bytes"):
        device.get_voltage_v()


def test_cpm_discards_stale_prefix_and_uses_final_four_bytes():
    device = CommandStub({b"<GETCPM>>": b"\xff\x00\x00\x00\x2a"})
    device.cpm_bytes = 4
    assert device.get_cpm() == 42


def test_cpm_retries_all_ff_sentinel_then_recovers():
    device = RecoveringCommandStub([b"\xff" * 4, b"\x00\x00\x00\x11"])
    device.cpm_bytes = 4
    assert device.get_cpm() == 17
    assert device.recoveries == 1


def test_cpm_persistent_all_ff_raises_protocol_error():
    device = RecoveringCommandStub([b"\xff" * 4, b"\xff" * 4])
    device.cpm_bytes = 4
    with pytest.raises(GmcProtocolError, match="all 0xff bytes"):
        device.get_cpm()


def test_dual_tube_counter_rejects_all_ff_sentinel():
    device = RecoveringCommandStub([b"\xff" * 4, b"\xff" * 4])
    with pytest.raises(GmcProtocolError, match=r"GETCPML.*all 0xff bytes"):
        device.get_low_dose_tube_cpm()


def test_getserial_uses_final_seven_bytes_after_stale_ff_prefix():
    device = CommandStub(
        {
            b"<GETSERIAL>>": bytes.fromhex("ff 08 00 48 30 38 38 a0"),
        }
    )
    assert device.get_serial() == "080048303838a0"


def test_getserial_retries_after_short_or_sentinel_response():
    device = RecoveringCommandStub(
        [
            bytes.fromhex("ff ff ff ff ff ff ff"),
            bytes.fromhex("08 00 48 30 38 38 a0"),
        ]
    )
    assert device.get_serial() == "080048303838a0"
    assert device.recoveries == 1
