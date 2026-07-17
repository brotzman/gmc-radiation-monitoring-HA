from __future__ import annotations

import glob
import os
import re
import threading
import time
from collections.abc import Callable, Iterable
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any

from .device_profiles import normalize_device_version_display, split_device_version
from .serial_device import SerialGmc

KNOWN_NON_GMC_TERMS = (
    "zigbee",
    "sonoff",
    "itead",
    "conbee",
    "skyconnect",
    "z-wave",
    "zwave",
    "thread",
    "multipan",
    "ember",
)


@dataclass(frozen=True)
class SerialPortInfo:
    path: str
    resolved_path: str
    display_name: str
    detail: str
    category: str
    suitable: bool
    exists: bool
    stable_path: bool
    assigned_index: int | None = None
    assigned_name: str = ""
    detected_model: str = ""
    firmware_version: str = ""
    detected_serial: str = ""
    detected_baudrate: int | None = None
    runtime_online: bool = False
    status: str = "available"
    reason: str = ""

    def as_dict(self) -> dict[str, Any]:
        return asdict(self)


class SerialDiscoveryService:
    """Discover serial ports and cautiously identify unassigned GMC counters."""

    def __init__(
        self,
        *,
        path_provider: Callable[[], Iterable[str]] | None = None,
        realpath: Callable[[str], str] = os.path.realpath,
        exists: Callable[[str], bool] = os.path.exists,
        probe_cache_seconds: int = 600,
    ) -> None:
        self.path_provider = path_provider or self._default_paths
        self.realpath = realpath
        self.exists = exists
        self.probe_cache_seconds = max(30, int(probe_cache_seconds))
        self._probe_cache: dict[str, tuple[float, SerialPortInfo]] = {}
        self._lock = threading.Lock()

    @staticmethod
    def _default_paths() -> list[str]:
        patterns = (
            "/dev/serial/by-id/*",
            "/dev/serial/by-path/*",
            "/dev/ttyUSB*",
            "/dev/ttyACM*",
            "/dev/ttyAMA*",
            "/dev/ttyS*",
        )
        paths: list[str] = []
        for pattern in patterns:
            paths.extend(glob.glob(pattern))
        return paths

    @staticmethod
    def _path_priority(path: str) -> tuple[int, str]:
        if "/serial/by-id/" in path:
            return (0, path)
        if "/serial/by-path/" in path:
            return (1, path)
        if re.search(r"/tty(?:USB|ACM)\d+$", path):
            return (2, path)
        if re.search(r"/ttyAMA\d+$", path):
            return (3, path)
        return (4, path)

    @staticmethod
    def _clean_usb_name(path: str) -> str:
        basename = Path(path).name
        text = basename
        if text.startswith("usb-"):
            text = text[4:]
        text = re.sub(r"-if\d+(?:-port\d+)?$", "", text, flags=re.IGNORECASE)
        text = text.replace("_", " ").replace("-", " ")
        return " ".join(text.split())

    @classmethod
    def _describe_path(cls, path: str, registry: dict[str, Any] | None) -> tuple[str, str, str, bool, str]:
        registry = registry or {}
        model = normalize_device_version_display(str(registry.get("device_model") or "").strip())
        hardware_model = str(registry.get("hardware_model") or "").strip()
        firmware = str(registry.get("firmware_version") or "").strip()
        if hardware_model:
            display = hardware_model
        elif model and model != "GMC":
            display, parsed_firmware = split_device_version(model)
            firmware = firmware or parsed_firmware
        else:
            display = ""
        if display:
            detail = f"Detected GMC device{f' · Firmware {firmware}' if firmware and firmware != 'unknown' else ''}"
            return display, detail, "gmc", True, ""

        lowered = cls._clean_usb_name(path).casefold()
        if any(term in lowered for term in KNOWN_NON_GMC_TERMS):
            product = cls._clean_usb_name(path)
            display = product or "Serieller Funkadapter"
            return display, "Not suitable as a GMC device", "other", False, "Known radio or Zigbee adapter"
        if re.search(r"/ttyAMA\d+$", path):
            return "Internal serial port", "Home Assistant host UART", "advanced", True, ""
        if "1a86" in lowered or "ch340" in lowered or "ch341" in lowered:
            return "USB-Seriellgerät (CH340/CH341)", "Possible GMC connection cable", "usb", True, ""
        cleaned = cls._clean_usb_name(path)
        if cleaned and not path.startswith("/dev/tty"):
            return cleaned, "Serial USB device", "usb", True, ""
        return "Unknown serial device", "Not yet checked as a GMC device", "advanced", True, ""

    def discover(
        self,
        *,
        device_options: list[dict[str, Any]],
        registry_devices: list[dict[str, Any]],
        refresh_probe: bool = False,
    ) -> list[SerialPortInfo]:
        configured_paths = [str(item.get("port") or "").strip() for item in device_options]
        raw_paths = list(self.path_provider()) + [path for path in configured_paths if path]
        preferred_by_target: dict[str, str] = {}
        for path in sorted(set(raw_paths), key=self._path_priority):
            target = self.realpath(path) if path else path
            preferred_by_target.setdefault(target, path)

        registry_by_path: dict[str, dict[str, Any]] = {}
        for item in registry_devices:
            for key in ("port", "serial_port", "serial_resolved_target"):
                value = str(item.get(key) or "").strip()
                if value:
                    registry_by_path[value] = item
                    registry_by_path[self.realpath(value)] = item

        assigned_by_target: dict[str, tuple[int, str]] = {}
        for index, item in enumerate(device_options):
            path = str(item.get("port") or "").strip()
            if not path:
                continue
            assigned_by_target[self.realpath(path)] = (index, str(item.get("name") or f"GMC {index + 1}"))

        results: list[SerialPortInfo] = []
        for target, path in preferred_by_target.items():
            registry = registry_by_path.get(path) or registry_by_path.get(target)
            display, detail, category, suitable, reason = self._describe_path(path, registry)
            assigned = assigned_by_target.get(target)
            exists = self.exists(path) or self.exists(target)
            runtime_online = bool((registry or {}).get("runtime_online"))
            firmware = str((registry or {}).get("firmware_version") or "").strip()
            model = str((registry or {}).get("hardware_model") or "").strip()
            if not model and registry:
                model, parsed_firmware = split_device_version(
                    normalize_device_version_display(str(registry.get("device_model") or ""))
                )
                firmware = firmware or parsed_firmware
            status = "missing" if not exists else "available"
            if not suitable:
                status = "not_gmc"
            if assigned:
                status = "online" if runtime_online else "assigned"
            info = SerialPortInfo(
                path=path,
                resolved_path=target,
                display_name=display,
                detail=detail,
                category=category,
                suitable=suitable,
                exists=exists,
                stable_path="/serial/by-id/" in path or "/serial/by-path/" in path,
                assigned_index=assigned[0] if assigned else None,
                assigned_name=assigned[1] if assigned else "",
                detected_model=model if model and model != "GMC" else "",
                firmware_version=firmware if firmware != "unknown" else "",
                detected_serial=str((registry or {}).get("serial") or ""),
                detected_baudrate=int((registry or {}).get("configured_baudrate") or 0) or None,
                runtime_online=runtime_online,
                status=status,
                reason=reason,
            )
            if refresh_probe and info.suitable and info.exists and info.assigned_index is None and info.category == "usb":
                info = self._probe_with_cache(info)
            results.append(info)
        return sorted(
            results,
            key=lambda item: (
                0 if item.runtime_online else 1,
                0 if item.detected_model else 1,
                0 if item.suitable else 2,
                self._path_priority(item.path),
            ),
        )

    def _probe_with_cache(self, info: SerialPortInfo) -> SerialPortInfo:
        now = time.monotonic()
        with self._lock:
            cached = self._probe_cache.get(info.resolved_path)
            if cached and now - cached[0] < self.probe_cache_seconds:
                return replace(cached[1], path=info.path, resolved_path=info.resolved_path)
        result = self._probe(info)
        with self._lock:
            self._probe_cache[info.resolved_path] = (now, result)
        return result

    @staticmethod
    def _probe(info: SerialPortInfo) -> SerialPortInfo:
        errors: list[str] = []
        for baudrate in (115200, 19200, 9600, 57600, 38400, 4800, 2400, 1200):
            device = SerialGmc(info.path, baudrate, timeout=0.9, delay_ms=80)
            try:
                device.open()
                version = normalize_device_version_display(device.get_version())
                serial = device.get_serial()
                model, firmware = split_device_version(version)
                return replace(
                    info,
                    display_name=model,
                    detail=f"GMC detected · Firmware {firmware}" if firmware != "unknown" else "GMC detected",
                    category="gmc",
                    detected_model=model,
                    firmware_version="" if firmware == "unknown" else firmware,
                    detected_serial=serial,
                    detected_baudrate=baudrate,
                    status="detected",
                    reason="",
                )
            except Exception as exc:  # The probe must never interrupt the configuration page.
                errors.append(str(exc))
            finally:
                device.close()
        return replace(
            info,
            status="unverified",
            detail="No GMC device detected",
            reason="; ".join(errors[-2:]),
        )
