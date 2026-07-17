from __future__ import annotations

from gmc_bridge.errors import GmcProtocolError
from gmc_bridge.serial_device import SerialGmc


class GyroSequenceStub(SerialGmc):
    def __init__(self, responses: list[bytes]):
        self.responses = iter(responses)
        self.heartbeat_active = False
        self.port = "/dev/test-gmc-500plus"
        self.recoveries = 0
        self.flushes = 0

    def request_until_idle(self, command: bytes, *, max_size: int = 32, idle_timeout: float = 0.05) -> bytes:
        assert command == b"<GETGYRO>>"
        assert max_size >= 24
        return next(self.responses)

    def _discard_pending_input(self) -> None:
        self.flushes += 1

    def _recover_protocol_stream(self) -> None:
        self.recoveries += 1


def test_getgyro_recovers_observed_leading_ff_without_losing_terminator() -> None:
    # Field log showed the exact-length prefix ff 00 70 01 10 c1 40.  The old
    # reader stopped after seven bytes and left the actual aa terminator queued.
    # Reading through idle obtains the full contaminated burst below.
    device = GyroSequenceStub([bytes.fromhex("ff 00 70 01 10 c1 40 aa")])

    assert device.get_gyro() == (112, 272, -16064)
    assert device.flushes == 1
    assert device.recoveries == 0


def test_getgyro_uses_final_complete_frame_with_stale_edges() -> None:
    device = GyroSequenceStub([bytes.fromhex("ff ff 00 01 00 02 00 03 aa ff")])

    assert device.get_gyro() == (1, 2, 3)


def test_getgyro_retries_a_burst_without_terminator_after_resync() -> None:
    device = GyroSequenceStub(
        [
            bytes.fromhex("ff 00 70 01 10 c1 40"),
            bytes.fromhex("00 70 01 10 c1 40 aa"),
        ]
    )

    assert device.get_gyro() == (112, 272, -16064)
    assert device.recoveries == 1
    assert device.flushes == 2


def test_getgyro_still_rejects_repeated_unterminated_frames() -> None:
    device = GyroSequenceStub(
        [
            bytes.fromhex("ff 00 70 01 10 c1 40"),
            bytes.fromhex("ff 00 70 01 10 c1 40"),
            bytes.fromhex("ff 00 70 01 10 c1 40"),
        ]
    )

    try:
        device.get_gyro()
    except GmcProtocolError as exc:
        assert "no complete frame ending in terminator 0xaa" in str(exc)
    else:
        raise AssertionError("unterminated GETGYRO frames must be rejected")
    assert device.recoveries == 2
