from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Literal

CapabilityHint = Literal["yes", "no", "unknown"]


@dataclass(frozen=True)
class DeviceProfile:
    """Conservative model-family description.

    Profiles are compatibility hints only. Runtime capability probing remains the source of
    truth because firmware revisions within a model family can expose different commands.
    """

    profile_id: str
    display_name: str
    patterns: tuple[str, ...]
    temperature_hint: CapabilityHint = "unknown"
    voltage_hint: CapabilityHint = "unknown"
    gyro_hint: CapabilityHint = "unknown"
    dual_tube_hint: CapabilityHint = "unknown"
    device_time_hint: CapabilityHint = "unknown"
    heartbeat_hint: CapabilityHint = "unknown"
    tested_with_project: bool = False

    def matches(self, version: str) -> bool:
        return any(re.search(pattern, version, flags=re.IGNORECASE) for pattern in self.patterns)


PROFILES: tuple[DeviceProfile, ...] = (
    DeviceProfile(
        profile_id="gmc_300_320",
        display_name="GMC-300/320 family",
        patterns=(r"GMC[- ]?3(?:00|20)", r"GMC3(?:00|20)"),
        temperature_hint="yes",
        voltage_hint="yes",
        gyro_hint="unknown",
        tested_with_project=True,
    ),
    DeviceProfile(
        profile_id="gmc_500",
        display_name="GMC-500 family",
        patterns=(r"GMC[- ]?5\d\d", r"GMC5\d\d"),
        temperature_hint="unknown",
        voltage_hint="unknown",
        gyro_hint="unknown",
        dual_tube_hint="yes",
        device_time_hint="yes",
        heartbeat_hint="yes",
    ),
    DeviceProfile(
        profile_id="gmc_600",
        display_name="GMC-600 family",
        patterns=(r"GMC[- ]?6\d\d", r"GMC6\d\d"),
        temperature_hint="unknown",
        voltage_hint="unknown",
        gyro_hint="unknown",
        device_time_hint="yes",
        heartbeat_hint="yes",
    ),
    DeviceProfile(
        profile_id="gmc_generic",
        display_name="Generic GQ GMC / RFC1201-compatible device",
        patterns=(r"GMC",),
    ),
)

GENERIC_PROFILE = DeviceProfile(
    profile_id="generic_rfc1201",
    display_name="Generic RFC1201-compatible device",
    patterns=(),
)


@dataclass(frozen=True)
class DeviceCapabilities:
    cpm: bool = True
    temperature: bool = False
    voltage: bool = False
    gyro: bool = False
    gyro_probe_requested: bool = False
    dual_tube: bool = False
    device_time: bool = False
    heartbeat: bool = False

    def as_dict(self) -> dict[str, bool]:
        return {
            "cpm": self.cpm,
            "temperature": self.temperature,
            "voltage": self.voltage,
            "gyro": self.gyro,
            "dual_tube": self.dual_tube,
            "device_time": self.device_time,
            "heartbeat": self.heartbeat,
        }

    def enabled_channels(self) -> tuple[str, ...]:
        return tuple(name for name, supported in self.as_dict().items() if supported)


def split_device_version(version: str) -> tuple[str, str]:
    """Split GETVER text into hardware model and firmware revision."""
    normalized = version.strip()
    # Firmware strings occur both as ``GMC-500+ Re 1.14`` and without a
    # separator as ``GMC-500+Re 1.14``. Keep ``Re`` with the firmware rather
    # than accidentally treating it as part of the hardware model.
    match = re.match(
        r"^(.*?)(?:\s*)?(Re\s*)?(\d+(?:\.\d+)+)$",
        normalized,
        flags=re.IGNORECASE,
    )
    if not match:
        return normalized or "GMC", "unknown"
    model = match.group(1).strip()
    firmware = ((match.group(2) or "") + match.group(3)).strip()
    return model or normalized, firmware


def normalize_device_version_display(version: str) -> str:
    """Return a human-readable device/firmware label without changing protocol data."""
    normalized = " ".join(str(version or "").split())
    if not normalized:
        return "GMC"
    # GQ GETVER responses may omit the separator before the firmware marker,
    # for example ``GMC-320Re 4.52``. Normalize only the presentation form.
    normalized = re.sub(
        r"(?<=[A-Za-z0-9+])(?=Re\s*\d)",
        " ",
        normalized,
        flags=re.IGNORECASE,
    )
    normalized = re.sub(r"\bRe\s*(?=\d)", "Re ", normalized, flags=re.IGNORECASE)
    return normalized


def resolve_device_profile(version: str) -> DeviceProfile:
    for profile in PROFILES:
        if profile.matches(version):
            return profile
    return GENERIC_PROFILE
