from __future__ import annotations

import json
import logging
import os
import signal

# Invokes fixed internal system commands only.
import subprocess  # nosec B404
import sys
import threading
import time
from collections.abc import Callable, Iterable, Sequence
from copy import deepcopy
from typing import Any

from .serial_discovery import SerialDiscoveryService, SerialPortInfo

LOG = logging.getLogger("gmc_serial_autoconfig")
MINIMUM_SERIAL_STARTUP_STAGGER_SECONDS = 15.0
AUTO_RESCAN_SECONDS = 15.0


ALL_DEVICES_MISSING_RESCAN_SECONDS = 30.0


def effective_serial_startup_delays(
    configured_delays: Sequence[float | None],
) -> tuple[float, ...]:
    """Return ordered startup offsets with a minimum 15-second device gap."""
    effective: list[float] = []
    previous = -MINIMUM_SERIAL_STARTUP_STAGGER_SECONDS
    for index, configured_delay in enumerate(configured_delays):
        requested = (
            float(configured_delay)
            if configured_delay is not None
            else index * MINIMUM_SERIAL_STARTUP_STAGGER_SECONDS
        )
        current = max(0.0, requested, previous + MINIMUM_SERIAL_STARTUP_STAGGER_SECONDS)
        effective.append(current)
        previous = current
    return tuple(effective)


def effective_serial_startup_delay(
    configured_delay: float | None,
    device_index: int,
) -> float:
    """Compatibility helper for one device using the default ordered offsets."""
    delays = [None] * max(0, int(device_index)) + [configured_delay]
    return effective_serial_startup_delays(delays)[-1]


def _normalized_serial(value: object) -> str:
    return "".join(character for character in str(value or "").casefold() if character.isalnum())


def _model_token(value: object) -> str:
    return "".join(character for character in str(value or "").casefold() if character.isalnum() or character == "+")


def model_matches(configured_name: object, detected_model: object) -> bool:
    expected = _model_token(configured_name)
    detected = _model_token(detected_model)
    if not expected or not detected:
        return False
    if "gmc320" in expected or "gmc300" in expected:
        return "gmc320" in detected or "gmc300" in detected
    if "gmc500" in expected:
        return "gmc500" in detected
    if "gmc600" in expected:
        return "gmc600" in detected
    return expected in detected or detected in expected


def _identity_hint(device: dict[str, Any]) -> str:
    # The calibration serial is already a stable per-device identity in existing
    # installations and keeps per-device settings attached to the right counter.
    return _normalized_serial(device.get("orientation_calibration_serial"))


def _detected_identity(port: SerialPortInfo) -> str:
    return _normalized_serial(port.detected_serial)


def _unique_device_name(base: str, serial: str, used: set[str]) -> str:
    base = str(base or "GMC").strip() or "GMC"
    candidate = base
    if candidate.casefold() in used:
        suffix = serial[-6:] if serial else str(len(used) + 1)
        candidate = f"{base} {suffix}"
    counter = 2
    while candidate.casefold() in used:
        candidate = f"{base} {counter}"
        counter += 1
    used.add(candidate.casefold())
    return candidate


def resolve_automatic_devices(
    configured_devices: Sequence[dict[str, Any]],
    detected_ports: Sequence[SerialPortInfo],
) -> list[dict[str, Any]]:
    """Match detected GMC counters to logical device settings.

    Stable serial identities win, then model names, followed by deterministic
    order. Existing port/baud values are intentionally ignored in automatic
    mode. Extra detected GMC counters receive safe generic defaults so they are
    connected without requiring a configuration click.
    """
    detected = [
        port
        for port in detected_ports
        if port.exists
        and port.suitable
        and port.status == "detected"
        and port.detected_baudrate
        and port.path.startswith("/dev/")
    ]
    detected.sort(key=lambda port: (0 if port.stable_path else 1, port.path))

    configs = [deepcopy(item) for item in configured_devices if isinstance(item, dict)]
    assigned_config_to_port: dict[int, int] = {}
    used_ports: set[int] = set()

    # First preserve exact per-device identity, which is important when two
    # counters of the same model are connected.
    for config_index, device in enumerate(configs):
        expected_serial = _identity_hint(device)
        if not expected_serial:
            continue
        for port_index, port in enumerate(detected):
            if port_index in used_ports:
                continue
            if _detected_identity(port) == expected_serial:
                assigned_config_to_port[config_index] = port_index
                used_ports.add(port_index)
                break

    # Then match model families. A stable path is already preferred by sorting.
    for config_index, device in enumerate(configs):
        if config_index in assigned_config_to_port:
            continue
        for port_index, port in enumerate(detected):
            if port_index in used_ports:
                continue
            if model_matches(device.get("name"), port.detected_model or port.display_name):
                assigned_config_to_port[config_index] = port_index
                used_ports.add(port_index)
                break

    # Deterministic fallback keeps unusual but valid GMC models usable.
    remaining_configs = [index for index in range(len(configs)) if index not in assigned_config_to_port]
    remaining_ports = [index for index in range(len(detected)) if index not in used_ports]
    for config_index, port_index in zip(remaining_configs, remaining_ports, strict=False):
        assigned_config_to_port[config_index] = port_index
        used_ports.add(port_index)

    resolved: list[dict[str, Any]] = []
    used_names: set[str] = set()
    for config_index, device in enumerate(configs):
        port_index = assigned_config_to_port.get(config_index)
        if port_index is None:
            continue
        detected_port = detected[port_index]
        device["port"] = detected_port.path
        device["baudrate"] = int(detected_port.detected_baudrate or 0)
        name = str(device.get("name") or detected_port.detected_model or "GMC").strip()
        device["name"] = _unique_device_name(name, detected_port.detected_serial, used_names)
        resolved.append(device)

    # Connect additional GMC counters even when no logical slot existed yet.
    for port_index, detected_port in enumerate(detected):
        if port_index in used_ports:
            continue
        name = _unique_device_name(
            detected_port.detected_model or detected_port.display_name or "GMC",
            detected_port.detected_serial,
            used_names,
        )
        resolved.append(
            {
                "name": name,
                "port": detected_port.path,
                "baudrate": int(detected_port.detected_baudrate or 19200),
                "serial_startup_delay": None,
            }
        )

    return resolved


def discover_gmc_devices(
    discovery: SerialDiscoveryService | None = None,
    *,
    assigned_devices: Sequence[dict[str, Any]] = (),
) -> list[SerialPortInfo]:
    service = discovery or SerialDiscoveryService(probe_cache_seconds=30)
    ports = service.discover(
        device_options=[dict(item) for item in assigned_devices],
        registry_devices=[],
        refresh_probe=True,
    )
    return [
        port
        for port in ports
        if port.status == "detected" and port.exists and port.detected_baudrate
    ]


class AutomaticSerialBridge:
    """Run the bridge with automatically detected ports and baud rates.

    The wrapper rescans when a new unassigned GMC appears and restarts only the
    bridge child, not the report server or the whole add-on.
    """

    def __init__(
        self,
        configured_devices: Sequence[dict[str, Any]],
        *,
        child_command: Sequence[str] | None = None,
        discovery_factory: Callable[[], SerialDiscoveryService] | None = None,
        rescan_seconds: float = AUTO_RESCAN_SECONDS,
    ) -> None:
        self.configured_devices = [deepcopy(item) for item in configured_devices if isinstance(item, dict)]
        self.child_command = list(child_command or [sys.executable, "/usr/local/bin/gmc_bridge.py"])
        self.discovery_factory = discovery_factory or (
            lambda: SerialDiscoveryService(probe_cache_seconds=600)
        )
        self.monitor_discovery = self.discovery_factory()
        self.rescan_seconds = max(MINIMUM_SERIAL_STARTUP_STAGGER_SECONDS, float(rescan_seconds))
        self.stop_event = threading.Event()
        self.child: subprocess.Popen[bytes] | None = None

    def request_stop(self, *_args: object) -> None:
        self.stop_event.set()
        self._stop_child()

    def _stop_child(self) -> None:
        child = self.child
        if child is None or child.poll() is not None:
            return
        child.terminate()
        try:
            child.wait(timeout=10.0)
        except subprocess.TimeoutExpired:
            child.kill()
            child.wait(timeout=5.0)

    def _scan_all(self) -> list[SerialPortInfo]:
        return discover_gmc_devices(self.discovery_factory())

    def _scan_new(self, assigned_devices: Sequence[dict[str, Any]]) -> list[SerialPortInfo]:
        return discover_gmc_devices(self.monitor_discovery, assigned_devices=assigned_devices)

    @staticmethod
    def _log_resolved_devices(devices: Iterable[dict[str, Any]]) -> None:
        for device in devices:
            LOG.info(
                "Automatically assigned %s to %s at %s baud",
                device.get("name") or "GMC",
                device.get("port") or "unknown port",
                device.get("baudrate") or "unknown",
            )

    def run(self) -> int:
        signal.signal(signal.SIGTERM, self.request_stop)
        signal.signal(signal.SIGINT, self.request_stop)

        while not self.stop_event.is_set():
            detected = self._scan_all()
            resolved = resolve_automatic_devices(self.configured_devices, detected)
            if not resolved:
                LOG.warning(
                    "No compatible GMC counter detected. Retrying automatically in %.0f seconds",
                    self.rescan_seconds,
                )
                self.stop_event.wait(self.rescan_seconds)
                continue

            self._log_resolved_devices(resolved)
            child_env = os.environ.copy()
            child_env["DEVICES_JSON"] = json.dumps(resolved, separators=(",", ":"))
            child_env["PORT"] = str(resolved[0]["port"])
            child_env["BAUDRATE"] = str(resolved[0]["baudrate"])
            self.child = subprocess.Popen(self.child_command, env=child_env)
            known_targets = {
                os.path.realpath(str(device.get("port") or ""))
                for device in resolved
                if device.get("port")
            }
            all_missing_since: float | None = None
            restart_for_topology = False

            while not self.stop_event.is_set() and self.child.poll() is None:
                if self.stop_event.wait(self.rescan_seconds):
                    break
                newly_detected = self._scan_new(resolved)
                new_targets = [
                    port
                    for port in newly_detected
                    if os.path.realpath(port.path) not in known_targets
                ]
                if new_targets:
                    LOG.info(
                        "Detected %d additional GMC counter(s); refreshing automatic assignments",
                        len(new_targets),
                    )
                    restart_for_topology = True
                    break

                any_assigned_path_exists = any(
                    os.path.exists(str(device.get("port") or ""))
                    or os.path.exists(os.path.realpath(str(device.get("port") or "")))
                    for device in resolved
                )
                if any_assigned_path_exists:
                    all_missing_since = None
                elif all_missing_since is None:
                    all_missing_since = time.monotonic()
                elif time.monotonic() - all_missing_since >= ALL_DEVICES_MISSING_RESCAN_SECONDS:
                    LOG.warning("All automatically assigned GMC ports disappeared; rescanning")
                    restart_for_topology = True
                    break

            return_code = self.child.poll()
            self._stop_child()
            self.child = None
            if self.stop_event.is_set():
                return 0
            if not restart_for_topology:
                LOG.warning(
                    "GMC bridge child exited with status %s; rediscovering devices",
                    return_code,
                )
                self.stop_event.wait(2.0)

        return 0
