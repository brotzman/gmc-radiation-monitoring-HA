from __future__ import annotations

import errno
import termios
from unittest import mock

import pytest
from gmc_bridge.device_profiles import split_device_version
from gmc_bridge.errors import GmcProtocolError
from gmc_bridge.serial_device import SerialGmc


def test_rejects_ffff0000_counter_pattern() -> None:
    with pytest.raises(GmcProtocolError, match="0xff prefix"):
        SerialGmc._decode_counter_bytes(bytes.fromhex("ff ff 00 00"), 4, "GETCPM")


def test_rejects_any_four_byte_counter_with_ff_msb() -> None:
    with pytest.raises(GmcProtocolError, match="0xff prefix"):
        SerialGmc._decode_counter_bytes(bytes.fromhex("ff 00 00 2a"), 4, "GETCPM")


def test_accepts_normal_four_byte_counter() -> None:
    assert SerialGmc._decode_counter_bytes(bytes.fromhex("00 00 00 2a"), 4, "GETCPM") == 42


def test_input_flush_is_best_effort_when_driver_rejects_it() -> None:
    device = SerialGmc("/dev/null", 115200, 1.0, 100)
    device.fd = 7
    with mock.patch.object(termios, "tcflush", side_effect=OSError(errno.ENOTTY, "not a tty")):
        device._discard_pending_input()


def test_re_marker_is_firmware_not_model_name() -> None:
    assert split_device_version("GMC-320Re 4.52") == ("GMC-320", "Re 4.52")
    assert split_device_version("GMC-500+Re 1.14") == ("GMC-500+", "Re 1.14")


class CounterSequenceStub(SerialGmc):
    def __init__(self, responses: list[bytes]):
        self.responses = iter(responses)
        self.cpm_bytes = 4
        self.heartbeat_active = False
        self.port = "/dev/test-gmc"
        self.recoveries = 0

    def request_until_idle(self, command: bytes, *, max_size: int = 32, idle_timeout: float = 0.05) -> bytes:
        assert command == b"<GETCPM>>"
        return next(self.responses)

    def _discard_pending_input(self) -> None:
        return None

    def _recover_protocol_stream(self) -> None:
        self.recoveries += 1


def test_high_ff_fragment_is_replaced_by_immediate_normal_verification() -> None:
    device = CounterSequenceStub(
        [
            bytes.fromhex("00 00 14 ff"),  # 5375, observed dirty-line signature
            bytes.fromhex("00 00 00 10"),  # stable normal reread
        ]
    )
    assert device.get_cpm() == 16
    assert device.recoveries == 1


def test_genuine_high_cpm_requires_two_consistent_protocol_reads() -> None:
    device = CounterSequenceStub(
        [
            (5000).to_bytes(4, "big"),
            (5050).to_bytes(4, "big"),
        ]
    )
    assert device.get_cpm() == 5050
    assert device.recoveries == 1


def test_unstable_ff_fragment_sequence_is_rejected_before_peak_gate() -> None:
    device = CounterSequenceStub(
        [
            bytes.fromhex("00 00 0f ff"),  # 4095
            bytes.fromhex("00 00 15 ff"),  # 5631
            bytes.fromhex("00 00 0d ff"),  # 3583
        ]
    )
    with pytest.raises(GmcProtocolError, match="Unstable GETCPM verification"):
        device.get_cpm()
    assert device.recoveries == 2
