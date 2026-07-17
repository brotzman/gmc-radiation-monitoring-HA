from __future__ import annotations

from dataclasses import dataclass

import pytest
from gmc_bridge.device_profiles import resolve_device_profile, split_device_version
from gmc_bridge.errors import GmcProtocolError
from gmc_bridge.serial_device import SerialGmc, ensure_same_serial


@pytest.mark.parametrize(
    ("version", "profile_id", "model", "firmware", "counter_bytes"),
    (
        ("GMC-300 Re 3.20", "gmc_300_320", "GMC-300", "Re 3.20", 2),
        ("GMC-320Re 4.52", "gmc_300_320", "GMC-320", "Re 4.52", 2),
        ("GMC-500+Re 1.14", "gmc_500", "GMC-500+", "Re 1.14", 4),
        ("GMC-600+ Re 2.01", "gmc_600", "GMC-600+", "Re 2.01", 4),
        ("GMC-RFC1201 custom", "gmc_generic", "GMC-RFC1201 custom", "unknown", 2),
    ),
)
def test_supported_family_matrix(
    version: str,
    profile_id: str,
    model: str,
    firmware: str,
    counter_bytes: int,
) -> None:
    profile = resolve_device_profile(version)
    assert profile.profile_id == profile_id
    assert split_device_version(version) == (model, firmware)

    device = SerialGmc("/dev/null", 115200, timeout=1.0, delay_ms=0)
    device.configure_for_version(version)
    assert device.cpm_bytes == counter_bytes


@pytest.mark.parametrize(
    ("payload", "size", "expected"),
    (
        (bytes.fromhex("00 2a"), 2, 42),
        (bytes.fromhex("aa 00 2a"), 2, 42),
        (bytes.fromhex("00 00 00 2a"), 4, 42),
        (bytes.fromhex("aa 00 00 00 2a"), 4, 42),
    ),
)
def test_counter_frame_matrix(payload: bytes, size: int, expected: int) -> None:
    assert SerialGmc._decode_counter_bytes(payload, size, "GETCPM") == expected


@pytest.mark.parametrize("payload", (b"\xff\xff", b"\xff\xff\xff\xff", bytes.fromhex("ff 00 00 2a")))
def test_corrupt_counter_frames_are_rejected_across_protocol_widths(payload: bytes) -> None:
    with pytest.raises(GmcProtocolError):
        SerialGmc._decode_counter_bytes(payload, len(payload), "GETCPM")


@dataclass(frozen=True)
class IdentityCase:
    expected: str
    actual: str
    accepted: bool


@pytest.mark.parametrize(
    "case",
    (
        IdentityCase("080048303838a0", "080048303838a0", True),
        IdentityCase("f488c59b0031f0", "f488c59b0031f0", True),
        IdentityCase("080048303838a0", "f488c59b0031f0", False),
    ),
)
def test_device_identity_matrix(case: IdentityCase) -> None:
    if case.accepted:
        ensure_same_serial(case.expected, case.actual)
    else:
        with pytest.raises(GmcProtocolError):
            ensure_same_serial(case.expected, case.actual)
