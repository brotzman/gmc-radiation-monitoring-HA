import importlib.util
import os
import pty
import random
import select
import sys
import threading
import time
import unittest
from contextlib import suppress
from pathlib import Path
from unittest import mock

try:
    import paho.mqtt.client  # type: ignore[import-not-found]
except ImportError:
    import types

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
spec = importlib.util.spec_from_file_location("gmc_bridge_pty_launcher", MODULE_PATH)
mod = importlib.util.module_from_spec(spec)
assert spec and spec.loader
sys.modules["gmc_bridge_pty_launcher"] = mod
spec.loader.exec_module(mod)


class GmcSimulator:
    def __init__(self, responses, *, chunk_plans=None, close_on=None):
        self.master_fd, slave_fd = pty.openpty()
        self.slave_path = os.ttyname(slave_fd)
        os.close(slave_fd)
        self.responses = responses
        self.chunk_plans = chunk_plans or {}
        self.close_on = close_on or set()
        self.commands = []
        self._stop = threading.Event()
        self.thread = threading.Thread(target=self._run, daemon=True)

    def start(self):
        self.thread.start()
        return self

    def close(self):
        self._stop.set()
        if self.master_fd is not None:
            with suppress(OSError):
                os.close(self.master_fd)
            self.master_fd = None
        self.thread.join(timeout=2.0)
        if self.thread.is_alive():
            raise TimeoutError("serial PTY simulator did not stop within 2 seconds")

    def _write_chunks(self, response, plan):
        offset = 0
        for size in plan:
            if offset >= len(response) or self.master_fd is None:
                break
            os.write(self.master_fd, response[offset : offset + size])
            offset += size
            time.sleep(0.003)
        if offset < len(response) and self.master_fd is not None:
            os.write(self.master_fd, response[offset:])

    def _run(self):
        buffer = bytearray()
        while not self._stop.is_set():
            try:
                fd = self.master_fd
                if fd is None:
                    break
                readable, _, _ = select.select([fd], [], [], 0.1)
                if not readable:
                    continue
                chunk = os.read(fd, 256)
            except OSError:
                time.sleep(0.01)
                continue
            if not chunk:
                continue
            buffer.extend(chunk)
            while b">>" in buffer:
                end = buffer.index(b">>") + 2
                command = bytes(buffer[:end])
                del buffer[:end]
                self.commands.append(command)
                if command in self.close_on:
                    with suppress(OSError):
                        os.close(self.master_fd)
                    self.master_fd = None
                    return
                response = self.responses.get(command)
                if response is None:
                    continue
                self._write_chunks(response, self.chunk_plans.get(command, [len(response)]))


class SerialPtyTests(unittest.TestCase):
    def setUp(self):
        mod.STOP_EVENT.clear()

    def _device(self, sim, timeout=0.5):
        return mod.SerialGmc(sim.slave_path, 19200, timeout=timeout, delay_ms=1, stop_event=mod.STOP_EVENT)

    def test_full_identity_and_sample_with_partial_cpm_reply(self):
        responses = {
            b"<GETVER>>": b"GMC-320Re 4.52",
            b"<GETSERIAL>>": bytes.fromhex("f488c59b0031f0"),
            b"<GETCPM>>": (17).to_bytes(2, "big"),
            b"<GETTEMP>>": bytes([26, 8, 0, 0xAA]),
            b"<GETVOLT>>": bytes([42]),
            b"<GETGYRO>>": bytes.fromhex("001c fffa ff15 aa"),
        }
        sim = GmcSimulator(responses, chunk_plans={b"<GETCPM>>": [1, 1]}).start()
        device = self._device(sim)
        try:
            with mock.patch("termios.tcflush", return_value=None):
                device.open()
            self.assertEqual(mod.read_identity(device), ("GMC-320Re 4.52", "f488c59b0031f0"))
            result = mod.read_sample(device, True)
            self.assertEqual(result.state["cpm"], 17)
            self.assertEqual(result.state["temperature_c"], 26.8)
            self.assertEqual(result.state["voltage_v"], 4.2)
            self.assertEqual(
                (result.state["gyro_x"], result.state["gyro_y"], result.state["gyro_z"]), (28, -6, -235)
            )
        finally:
            device.close()
            sim.close()

    def test_getgyro_with_stale_prefix_reads_through_real_terminator(self):
        responses = {
            b"<GETGYRO>>": bytes.fromhex("ff 00 70 01 10 c1 40 aa"),
        }
        sim = GmcSimulator(responses, chunk_plans={b"<GETGYRO>>": [1, 3, 4]}).start()
        device = self._device(sim)
        try:
            with mock.patch("termios.tcflush", return_value=None):
                device.open()
            self.assertEqual(device.get_gyro(), (112, 272, -16064))
        finally:
            device.close()
            sim.close()

    def test_randomized_chunk_boundaries(self):
        rng = random.Random(42)
        response = b"GMC-320Re 4.52"
        for _ in range(12):
            remaining = len(response)
            plan = []
            while remaining:
                size = rng.randint(1, min(4, remaining))
                plan.append(size)
                remaining -= size
            sim = GmcSimulator({b"<GETVER>>": response}, chunk_plans={b"<GETVER>>": plan}).start()
            device = self._device(sim)
            try:
                with mock.patch("termios.tcflush", return_value=None):
                    device.open()
                self.assertEqual(device.get_version(), "GMC-320Re 4.52")
            finally:
                device.close()
                sim.close()

    def test_timeout_on_missing_second_cpm_byte(self):
        sim = GmcSimulator({b"<GETCPM>>": b"\x00"}).start()
        device = self._device(sim, timeout=0.15)
        try:
            with mock.patch("termios.tcflush", return_value=None):
                device.open()
            with self.assertRaises(mod.GmcTimeout):
                device.get_cpm()
        finally:
            device.close()
            sim.close()

    def test_invalid_temperature_terminator_is_preserved_as_optional_failure(self):
        responses = {
            b"<GETCPM>>": (17).to_bytes(2, "big"),
            b"<GETTEMP>>": bytes([26, 8, 0, 0x00]),
        }
        sim = GmcSimulator(responses).start()
        device = self._device(sim)
        try:
            with mock.patch("termios.tcflush", return_value=None):
                device.open()
            result = mod.read_sample(device, True)
            self.assertEqual(result.state, {"cpm": 17})
            self.assertTrue(result.reconnect_required)
            self.assertEqual(result.optional_errors[0].sensor, "temperature")
        finally:
            device.close()
            sim.close()

    def test_disconnect_at_each_measurement_command_is_detected(self):
        commands = [b"<GETCPM>>", b"<GETTEMP>>", b"<GETVOLT>>", b"<GETGYRO>>"]
        base = {
            b"<GETCPM>>": (17).to_bytes(2, "big"),
            b"<GETTEMP>>": bytes([26, 8, 0, 0xAA]),
            b"<GETVOLT>>": bytes([42]),
            b"<GETGYRO>>": bytes.fromhex("001c fffa ff15 aa"),
        }
        for command in commands:
            sim = GmcSimulator(base, close_on={command}).start()
            device = self._device(sim, timeout=0.25)
            try:
                with mock.patch("termios.tcflush", return_value=None):
                    device.open()
                if command == b"<GETCPM>>":
                    with self.assertRaises(mod.GmcError):
                        mod.read_sample(device, True)
                else:
                    result = mod.read_sample(device, True)
                    self.assertEqual(result.state["cpm"], 17)
                    self.assertTrue(result.reconnect_required)
            finally:
                device.close()
                sim.close()

    def test_different_serial_after_reconnect_is_rejected(self):
        with self.assertRaises(mod.DeviceIdentityChanged):
            mod.ensure_same_serial("f488c59b0031f0", "aaaaaaaaaaaaaa")


if __name__ == "__main__":
    unittest.main()
