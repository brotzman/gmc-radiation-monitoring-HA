from __future__ import annotations

import errno
import fcntl
import logging
import os
import re
import select
import termios
import time
from contextlib import suppress
from dataclasses import dataclass, field
from datetime import datetime
from threading import Event
from typing import Any

from .config import SUPPORTED_BAUDRATES
from .device_profiles import DeviceCapabilities
from .errors import (
    DeviceBusy,
    DeviceIdentityChanged,
    GmcError,
    GmcProtocolError,
    GmcTimeout,
    classify_optional_issue,
)
from .utils import interruptible_sleep

LOG = logging.getLogger("gmc_bridge")

BAUD_CONSTANTS = {
    1200: termios.B1200,
    2400: termios.B2400,
    4800: termios.B4800,
    9600: termios.B9600,
    19200: termios.B19200,
    38400: termios.B38400,
    57600: termios.B57600,
    115200: termios.B115200,
}


@dataclass(frozen=True)
class OptionalReadError:
    sensor: str
    error: str
    code: str = "optional_channel_unavailable"
    affects_measurement: bool = False
    retryable: bool = True


@dataclass
class SampleResult:
    state: dict[str, Any]
    available: dict[str, bool]
    optional_errors: list[OptionalReadError] = field(default_factory=list)
    reconnect_required: bool = False


class SerialGmc:
    """Exact-length RFC1201 client with one deadline per command transaction."""

    def __init__(
        self,
        port: str,
        baudrate: int,
        timeout: float,
        delay_ms: int,
        stop_event: Event | None = None,
        debug_frames: bool = False,
        debug_max_bytes: int = 64,
    ) -> None:
        if baudrate not in SUPPORTED_BAUDRATES:
            raise ValueError(f"Unsupported baud rate: {baudrate}")
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.delay = delay_ms / 1000.0
        self.stop_event = stop_event or Event()
        self.fd: int | None = None
        self._last_command_at = 0.0
        self._kernel_exclusive = False
        self.cpm_bytes = 2
        self.rfc1801 = False
        self.heartbeat_active = False
        self.debug_frames = bool(debug_frames)
        self.debug_max_bytes = max(16, int(debug_max_bytes))


    def _log_frame(self, direction: str, data: bytes) -> None:
        if not self.debug_frames:
            return
        shown = data[: self.debug_max_bytes]
        suffix = f" …(+{len(data) - len(shown)} bytes)" if len(data) > len(shown) else ""
        ascii_preview = "".join(chr(byte) if 32 <= byte <= 126 else "." for byte in shown)
        LOG.warning(
            "[%s] SERIAL %s len=%d hex=%s ascii=%s%s",
            self.port, direction, len(data), shown.hex(" "), ascii_preview, suffix,
        )

    def recover_protocol_stream(self) -> None:
        """Public state-machine transition back to a synchronized command stream."""
        self._recover_protocol_stream()

    def open(self) -> None:
        if self.fd is not None:
            return
        try:
            fd = os.open(self.port, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
        except OSError as exc:
            raise GmcError(f"Cannot open {self.port}: {exc}") from exc

        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError as exc:
            os.close(fd)
            if exc.errno in (errno.EACCES, errno.EAGAIN):
                raise DeviceBusy(f"Serial device is already in use: {self.port}") from exc
            raise

        try:
            tioc_excl = getattr(termios, "TIOCEXCL", None)
            if tioc_excl is not None:
                try:
                    fcntl.ioctl(fd, tioc_excl)
                    self._kernel_exclusive = True
                except OSError as exc:
                    if exc.errno in (errno.EBUSY, errno.EACCES):
                        raise DeviceBusy(f"Serial device is exclusively in use: {self.port}") from exc
                    if exc.errno not in (errno.ENOTTY, errno.EINVAL, errno.ENOSYS, errno.ENOTSUP):
                        raise
                    LOG.debug("Kernel serial exclusivity is unavailable for %s: %s", self.port, exc)

            attrs = termios.tcgetattr(fd)
            attrs[0] = 0
            attrs[1] = 0
            attrs[2] = termios.CLOCAL | termios.CREAD | termios.CS8
            attrs[3] = 0
            attrs[4] = BAUD_CONSTANTS[self.baudrate]
            attrs[5] = BAUD_CONSTANTS[self.baudrate]
            attrs[6][termios.VMIN] = 0
            attrs[6][termios.VTIME] = 0
            termios.tcsetattr(fd, termios.TCSANOW, attrs)
            self.fd = fd
            termios.tcflush(fd, termios.TCIOFLUSH)
            self._quiesce_heartbeat_stream(repeats=2, fail_if_stopping=True)
            self._last_command_at = time.monotonic()
        except Exception:
            self.close()
            raise

    def close(self) -> None:
        if self.fd is None:
            return
        self.heartbeat_active = False
        fd = self.fd
        self.fd = None
        try:
            if self._kernel_exclusive:
                tioc_nxcl = getattr(termios, "TIOCNXCL", None)
                if tioc_nxcl is not None:
                    with suppress(OSError):
                        fcntl.ioctl(fd, tioc_nxcl)
        finally:
            self._kernel_exclusive = False
        with suppress(OSError):
            fcntl.flock(fd, fcntl.LOCK_UN)
        with suppress(OSError):
            os.close(fd)

    def _quiesce_heartbeat_stream(
        self,
        *,
        repeats: int = 1,
        fail_if_stopping: bool = False,
    ) -> None:
        """Stop unsolicited heartbeat bytes and clear stale input safely."""
        fd = getattr(self, "fd", None)
        if fd is None:
            self.heartbeat_active = False
            return
        for _ in range(max(1, repeats)):
            deadline = time.monotonic() + self.timeout
            self._write_all(b"<HEARTBEAT0>>", deadline)
            self._last_command_at = time.monotonic()
            if not interruptible_sleep(0.35, self.stop_event):
                if fail_if_stopping:
                    raise GmcError("Interrupted while initializing serial device")
                break
            with suppress(OSError, termios.error):
                termios.tcflush(fd, termios.TCIFLUSH)
        self.heartbeat_active = False

    def _recover_protocol_stream(self) -> None:
        """Attempt one safe serial resynchronization after malformed framing."""
        self._quiesce_heartbeat_stream(repeats=1, fail_if_stopping=True)

    @staticmethod
    def _decode_version_bytes(raw: bytes) -> str:
        candidates = [
            match.group(0).decode("ascii")
            for match in re.finditer(rb"[\x20-\x7e]{4,}", raw)
        ]
        for text in candidates:
            cleaned = text.strip("\x00 ")
            if "GMC" in cleaned.upper():
                return cleaned[cleaned.upper().find("GMC") :]
        raise GmcProtocolError(f"Invalid GETVER response bytes: {raw.hex(' ')}")

    @staticmethod
    def _decode_voltage_bytes(raw: bytes) -> float:
        """Extract an RFC1801 ASCII voltage value from a possibly dirty response.

        Some counters leave one or more heartbeat/binary bytes queued before the
        five-byte ``GETVOLT`` reply.  Decoding the complete buffer as ASCII would
        raise ``UnicodeDecodeError`` and, previously, terminate the device worker.
        Search the raw bytes for the documented numeric value followed by ``V``
        instead, while still rejecting malformed or implausible replies.
        """
        matches = list(re.finditer(rb"(?<![0-9.])([0-9](?:\.[0-9]{1,3})?)[vV]", raw))
        if not matches:
            raise GmcProtocolError(f"Invalid GETVOLT response bytes: {raw.hex(' ')}")
        try:
            value = float(matches[-1].group(1).decode("ascii"))
        except (UnicodeDecodeError, ValueError) as exc:
            raise GmcProtocolError(
                f"Invalid GETVOLT response bytes: {raw.hex(' ')}"
            ) from exc
        if not 0.0 <= value <= 9.0:
            raise GmcProtocolError(f"Implausible GETVOLT response: {value}")
        return round(value, 2)

    @staticmethod
    def _extract_terminated_frame(
        raw: bytes,
        size: int,
        command_name: str,
    ) -> bytes:
        """Extract the final complete ``... 0xaa`` frame from a dirty response.

        Some CH340-backed GMC counters occasionally prepend one or more stale
        bytes to an otherwise valid optional-channel response.  An exact-length
        read then consumes the stale prefix plus the payload and leaves the real
        ``0xaa`` terminator queued for the next command.  The observed GETGYRO
        sequence ``ff 00 70 01 10 c1 40 aa`` is one example: the valid seven-byte
        frame starts at byte one and decodes to ``(112, 272, -16064)``.

        Read the complete burst and select the last full frame ending in the
        documented terminator.  Choosing the last frame also tolerates stale
        prefix bytes and an older terminated frame that was already queued.
        """
        if size < 2:
            raise ValueError("Terminated frame size must be at least two bytes")
        if len(raw) < size:
            raise GmcTimeout(
                f"Short {command_name} response: expected at least {size} bytes, "
                f"received {len(raw)} ({raw.hex(' ')})"
            )

        candidates = [
            raw[start : start + size]
            for start in range(0, len(raw) - size + 1)
            if raw[start + size - 1] == 0xAA
        ]
        if candidates:
            return candidates[-1]

        raise GmcProtocolError(
            f"Invalid {command_name} response {raw.hex(' ')}; "
            "no complete frame ending in terminator 0xaa"
        )

    def _request_with_terminator(
        self,
        command: bytes,
        size: int,
        command_name: str,
        *,
        attempts: int = 3,
    ) -> bytes:
        """Read a terminator-framed command without truncating a dirty prefix."""
        errors: list[str] = []
        for attempt in range(max(1, attempts)):
            # Clear bytes that were already queued before the command and then
            # read through the idle gap.  Unlike request_exact(), this includes
            # the real terminator even when a stale prefix arrives first.
            self._discard_pending_input()
            raw = self.request_until_idle(
                command,
                max_size=max(24, size * 4),
                idle_timeout=0.08,
            )
            try:
                frame = self._extract_terminated_frame(raw, size, command_name)
            except (GmcProtocolError, GmcTimeout) as exc:
                errors.append(str(exc))
                if attempt + 1 < attempts:
                    self._recover_protocol_stream()
                continue
            if len(raw) != size:
                LOG.warning(
                    "[%s] Recovered %s frame from contaminated serial response: %s",
                    getattr(self, "port", "serial"), command_name, raw.hex(" "),
                )
            return frame
        raise GmcProtocolError("; ".join(errors))

    def _wait_command_gap(self) -> None:
        remaining = self.delay - (time.monotonic() - self._last_command_at)
        if remaining > 0 and not interruptible_sleep(remaining, self.stop_event):
            raise GmcError("Interrupted while waiting between serial commands")

    def _poll_ready(self, mask: int, deadline: float) -> None:
        if self.fd is None:
            raise GmcError("Serial port is not open")
        poller = select.poll()
        poller.register(self.fd, mask | select.POLLERR | select.POLLHUP | select.POLLNVAL)
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise GmcTimeout("Serial command deadline exceeded")
            timeout_ms = max(1, int(remaining * 1000))
            try:
                events = poller.poll(timeout_ms)
            except InterruptedError:
                continue
            if not events:
                continue
            for _, event_mask in events:
                if event_mask & select.POLLNVAL:
                    raise GmcError("Serial descriptor became invalid")
                if event_mask & select.POLLHUP:
                    raise GmcError("Serial device disconnected (HUP)")
                if event_mask & select.POLLERR:
                    raise GmcError("Serial device reported an I/O error")
                if event_mask & mask:
                    return

    def _write_all(self, data: bytes, deadline: float) -> None:
        if self.fd is None:
            raise GmcError("Serial port is not open")
        view = memoryview(data)
        while view:
            self._poll_ready(select.POLLOUT, deadline)
            try:
                written = os.write(self.fd, view)
            except (InterruptedError, BlockingIOError):
                continue
            if written <= 0:
                raise GmcError("Serial write returned zero bytes")
            view = view[written:]

    def _read_exact(self, size: int, deadline: float | None = None) -> bytes:
        if self.fd is None:
            raise GmcError("Serial port is not open")
        if deadline is None:
            deadline = time.monotonic() + self.timeout
        result = bytearray()
        while len(result) < size:
            try:
                self._poll_ready(select.POLLIN, deadline)
            except GmcTimeout as exc:
                raise GmcTimeout(f"Received {len(result)} of {size} bytes") from exc
            try:
                chunk = os.read(self.fd, size - len(result))
            except (InterruptedError, BlockingIOError):
                continue
            if not chunk:
                raise GmcError("Serial device returned EOF")
            result.extend(chunk)
        return bytes(result)

    def request_exact(self, command: bytes, size: int) -> bytes:
        self._wait_command_gap()
        deadline = time.monotonic() + self.timeout
        self._log_frame("TX", command)
        self._write_all(command, deadline)
        self._last_command_at = time.monotonic()
        response = self._read_exact(size, deadline)
        self._log_frame("RX", response)
        return response

    def request_until_idle(
        self, command: bytes, *, max_size: int = 32, idle_timeout: float = 0.05
    ) -> bytes:
        """Read a variable-length response until the serial stream becomes idle."""
        if self.fd is None:
            raise GmcError("Serial port is not open")
        self._wait_command_gap()
        deadline = time.monotonic() + self.timeout
        self._log_frame("TX", command)
        self._write_all(command, deadline)
        self._last_command_at = time.monotonic()
        result = bytearray()
        poller = select.poll()
        poller.register(self.fd, select.POLLIN | select.POLLERR | select.POLLHUP | select.POLLNVAL)
        while len(result) < max_size:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                if result:
                    break
                raise GmcTimeout("Serial command deadline exceeded")
            wait_seconds = min(remaining, idle_timeout) if result else remaining
            try:
                events = poller.poll(max(1, int(wait_seconds * 1000)))
            except InterruptedError:
                continue
            if not events:
                if result:
                    break
                continue
            for _, event_mask in events:
                if event_mask & select.POLLNVAL:
                    raise GmcError("Serial descriptor became invalid")
                if event_mask & select.POLLHUP:
                    raise GmcError("Serial device disconnected (HUP)")
                if event_mask & select.POLLERR:
                    raise GmcError("Serial device reported an I/O error")
                if event_mask & select.POLLIN:
                    try:
                        chunk = os.read(self.fd, max_size - len(result))
                    except (InterruptedError, BlockingIOError):
                        continue
                    if not chunk:
                        raise GmcError("Serial device returned EOF")
                    result.extend(chunk)
        if not result:
            raise GmcTimeout("Received no response bytes")
        response = bytes(result)
        self._log_frame("RX", response)
        return response

    def get_version(self) -> str:
        errors: list[str] = []
        for attempt in range(3):
            raw = self.request_until_idle(b"<GETVER>>", max_size=32)
            try:
                return self._decode_version_bytes(raw)
            except GmcProtocolError as exc:
                errors.append(str(exc))
                if attempt < 2:
                    self._recover_protocol_stream()
        raise GmcProtocolError("; ".join(errors))

    def get_serial(self, expected_serial: str | None = None) -> str:
        """Read and validate the seven-byte device serial.

        Dirty CH340 streams can add idle-high ``0xff`` bytes before *or after*
        the real seven-byte reply.  Reading the final seven bytes alone therefore
        fails for a response such as ``08 00 48 30 38 38 a0 ff``.  Strip only
        surplus edge sentinels, prefer an exact previously known serial when one
        is available, and retry after a full stream recovery.
        """
        expected = (expected_serial or "").strip().lower()
        errors: list[str] = []
        for attempt in range(3):
            raw = self.request_until_idle(b"<GETSERIAL>>", max_size=32)
            candidates: list[bytes] = []
            if len(raw) >= 7:
                # If reconnecting, the known serial is the strongest framing
                # signal and safely distinguishes it from shifted seven-byte
                # windows containing stale edge bytes.
                if expected:
                    try:
                        expected_bytes = bytes.fromhex(expected)
                    except ValueError:
                        expected_bytes = b""
                    if len(expected_bytes) == 7 and expected_bytes in raw:
                        return expected

                trimmed = raw
                while len(trimmed) > 7 and trimmed[:1] == b"\xff":
                    trimmed = trimmed[1:]
                while len(trimmed) > 7 and trimmed[-1:] == b"\xff":
                    trimmed = trimmed[:-1]
                if len(trimmed) == 7:
                    candidates.append(trimmed)

                for offset in range(len(raw) - 6):
                    candidate = raw[offset : offset + 7]
                    if candidate not in candidates:
                        candidates.append(candidate)

                valid = [
                    value for value in candidates
                    if value not in (b"\x00" * 7, b"\xff" * 7)
                    and value[:1] != b"\xff"
                    and value[-1:] != b"\xff"
                ]
                if len(valid) == 1:
                    return valid[0].hex()
                if valid:
                    # Prefer the window with the fewest sentinel-looking bytes.
                    valid.sort(key=lambda value: (value.count(0xff), value.count(0x00)))
                    best = valid[0]
                    if len(valid) == 1 or (best.count(0xff), best.count(0x00)) < (valid[1].count(0xff), valid[1].count(0x00)):
                        return best.hex()
                errors.append(f"Ambiguous GETSERIAL response: {raw.hex(' ')}")
            else:
                errors.append(
                    f"Short GETSERIAL response: expected 7 bytes, received "
                    f"{len(raw)} ({raw.hex(' ')})"
                )
            if attempt < 2:
                self._recover_protocol_stream()
        raise GmcProtocolError("; ".join(errors))

    def configure_for_version(self, version: str) -> None:
        """Select model-family response formats after GETVER detection."""
        normalized = version.upper().replace(" ", "")
        self.rfc1801 = any(model in normalized for model in ("GMC-500", "GMC500", "GMC-600", "GMC600"))
        self.cpm_bytes = 4 if self.rfc1801 else 2

    @staticmethod
    def _decode_counter_bytes(raw: bytes, size: int, command_name: str) -> int:
        """Decode a binary counter response while rejecting dirty-line sentinels.

        RFC1801 counters return four unsigned big-endian bytes. A dirty CH340
        stream may prepend idle-high bytes (``0xff``), while a disconnected or
        unsynchronised device may return an all-ones frame. Use the final complete
        response width so ordinary stale prefixes are consumed, but reject frames
        whose RFC1801 most-significant byte is ``0xff``. Such a frame represents
        at least 4,278,190,080 CPM and is a serial corruption signature on these
        counters, not a value that should ever reach the high-CPM confirmation
        gate. This also covers observed partial sentinels such as ``ff ff 00 00``.
        """
        if len(raw) < size:
            # Preserve the public behaviour of the former exact-length reader:
            # an incomplete mandatory counter reply is a transport timeout, not
            # a syntactically complete protocol response.
            raise GmcTimeout(
                f"Short {command_name} response: expected {size} bytes, received "
                f"{len(raw)} ({raw.hex(' ')})"
            )
        payload = raw[-size:]
        if payload == b"\xff" * size:
            raise GmcProtocolError(
                f"Invalid {command_name} response: all 0xff bytes ({raw.hex(' ')})"
            )
        if size == 4 and payload[0] == 0xFF:
            raise GmcProtocolError(
                f"Invalid {command_name} response: reserved 0xff prefix "
                f"({raw.hex(' ')})"
            )
        return int.from_bytes(payload, "big", signed=False)

    def _discard_pending_input(self) -> None:
        """Best-effort removal of bytes queued before a request is transmitted."""
        fd = getattr(self, "fd", None)
        if fd is None or getattr(self, "heartbeat_active", False):
            return
        try:
            termios.tcflush(fd, termios.TCIFLUSH)
        except (OSError, termios.error) as exc:
            # Some pseudo terminals and unusual USB drivers reject TCIFLUSH.
            # The response parser still provides the protocol-level safeguard.
            LOG.debug("Could not flush pending serial input on %s: %s", self.port, exc)

    def _read_counter_transaction(
        self, command: bytes, size: int, command_name: str
    ) -> int:
        """Read one counter transaction, retrying malformed protocol frames once."""
        errors: list[str] = []
        for attempt in range(2):
            # Remove bytes that were already queued before this transaction. This
            # is safe while heartbeat is disabled and prevents old binary frames
            # from being mistaken for the next RFC1801 counter response.
            self._discard_pending_input()
            # Read through the idle gap so any additional stale prefix bytes are
            # consumed rather than left queued to corrupt the next command.
            raw = self.request_until_idle(
                command, max_size=max(24, size * 4), idle_timeout=0.08
            )
            try:
                return self._decode_counter_bytes(raw, size, command_name)
            except GmcProtocolError as exc:
                errors.append(str(exc))
                if attempt == 0:
                    self._recover_protocol_stream()
        raise GmcProtocolError("; ".join(errors))

    @staticmethod
    def _counter_values_consistent(first: int, second: int) -> bool:
        """Return whether two immediate high-counter reads plausibly agree.

        A genuine high count should remain close across two back-to-back GETCPM
        requests. CH340 stream corruption observed in the field instead produced
        unrelated values such as 5375, 4095, 5631 and 1048575, commonly from
        partial ``0xff`` sentinel bytes. A small absolute tolerance covers normal
        counting jitter at the verification boundary; otherwise require the two
        values to agree within ten percent.
        """
        low = min(int(first), int(second))
        high = max(int(first), int(second))
        if low < 0:
            return False
        if high - low <= 64:
            return True
        if low == 0:
            return high == 0
        return high / low <= 1.10

    def _read_counter(self, command: bytes, size: int, command_name: str) -> int:
        value = self._read_counter_transaction(command, size, command_name)

        # The live plausibility gate starts at 1000 CPM. Verify a value at or
        # above that boundary immediately at the protocol layer before it is
        # allowed to count as one of the three high-CPM confirmations. This
        # prevents repeated fragments ending in 0xff from forming a false
        # confirmation sequence several minutes apart.
        if command_name != "GETCPM" or value < 1000:
            return value

        self._recover_protocol_stream()
        verification = self._read_counter_transaction(command, size, command_name)
        if verification < 1000:
            LOG.warning(
                "[%s] Rejected unstable GETCPM candidate %d; immediate verification returned %d",
                getattr(self, "port", "serial"), value, verification,
            )
            return verification
        if self._counter_values_consistent(value, verification):
            return verification

        # One final fresh read distinguishes a genuinely elevated and stable
        # counter from two unrelated dirty-line values. Only two mutually
        # consistent high reads are passed to the higher-level three-cycle gate.
        self._recover_protocol_stream()
        final_value = self._read_counter_transaction(command, size, command_name)
        if final_value < 1000:
            LOG.warning(
                "[%s] Rejected unstable GETCPM candidates %d/%d; final verification returned %d",
                getattr(self, "port", "serial"), value, verification, final_value,
            )
            return final_value
        if self._counter_values_consistent(verification, final_value):
            return final_value
        raise GmcProtocolError(
            "Unstable GETCPM verification: "
            f"first={value}, second={verification}, third={final_value}"
        )

    def get_cpm(self) -> int:
        return self._read_counter(b"<GETCPM>>", self.cpm_bytes, "GETCPM")

    def get_high_dose_tube_cpm(self) -> int:
        return self._read_counter(b"<GETCPMH>>", 4, "GETCPMH")

    def get_low_dose_tube_cpm(self) -> int:
        return self._read_counter(b"<GETCPML>>", 4, "GETCPML")

    def get_temperature_c(self) -> float:
        raw = self._request_with_terminator(b"<GETTEMP>>", 4, "GETTEMP")
        magnitude = float(raw[0]) + float(raw[1]) / 10.0
        return -magnitude if raw[2] else magnitude

    def get_voltage_v(self) -> float:
        if self.rfc1801:
            errors: list[str] = []
            for attempt in range(2):
                # Read until idle rather than exactly five bytes. If a stale byte
                # precedes the reply, an exact read truncates the trailing ``V``
                # and leaves it queued to corrupt the next command.
                raw = self.request_until_idle(
                    b"<GETVOLT>>", max_size=24, idle_timeout=0.08
                )
                try:
                    return self._decode_voltage_bytes(raw)
                except GmcProtocolError as exc:
                    errors.append(str(exc))
                    if attempt == 0:
                        self._recover_protocol_stream()
            raise GmcProtocolError("; ".join(errors))
        return round(self.request_exact(b"<GETVOLT>>", 1)[0] / 10.0, 1)

    def get_datetime(self) -> datetime:
        raw = self._request_with_terminator(b"<GETDATETIME>>", 7, "GETDATETIME")
        try:
            return datetime(2000 + raw[0], raw[1], raw[2], raw[3], raw[4], raw[5])
        except ValueError as exc:
            raise GmcProtocolError(f"Invalid GETDATETIME response: {raw.hex()}") from exc

    def get_cps(self) -> int:
        return int.from_bytes(self.request_exact(b"<GETCPS>>", 4), "big", signed=False)

    def start_heartbeat(self) -> None:
        self._wait_command_gap()
        deadline = time.monotonic() + self.timeout
        self._write_all(b"<HEARTBEAT1>>", deadline)
        self._last_command_at = time.monotonic()
        self.heartbeat_active = True

    def read_heartbeat_cps(self) -> int:
        if not self.heartbeat_active:
            raise GmcProtocolError("Heartbeat is not active")
        return int.from_bytes(self._read_exact(4), "big", signed=False)

    def stop_heartbeat(self) -> None:
        self._quiesce_heartbeat_stream(repeats=1, fail_if_stopping=False)

    def get_gyro(self) -> tuple[int, int, int]:
        raw = self._request_with_terminator(b"<GETGYRO>>", 7, "GETGYRO")
        return (
            int.from_bytes(raw[0:2], "big", signed=True),
            int.from_bytes(raw[2:4], "big", signed=True),
            int.from_bytes(raw[4:6], "big", signed=True),
        )


def read_identity(device: SerialGmc, *, expected_serial: str | None = None) -> tuple[str, str]:
    version = device.get_version()
    if hasattr(device, "configure_for_version"):
        device.configure_for_version(version)
    try:
        serial = device.get_serial(expected_serial=expected_serial)
    except TypeError as exc:
        # Compatibility with simple protocol stubs and third-party wrappers that
        # implement the pre-5.1 get_serial() signature.
        if "expected_serial" not in str(exc):
            raise
        serial = device.get_serial()
    if serial == "00000000000000":
        raise GmcProtocolError("Device returned an all-zero serial number")
    return version, serial


def ensure_same_serial(expected: str, actual: str) -> None:
    if actual != expected:
        raise DeviceIdentityChanged(
            f"Serial device changed from {expected} to {actual}; refusing to mix devices"
        )


def probe_capabilities(
    device: SerialGmc,
    *,
    expected_serial: str,
    probe_gyro: bool,
    probe_dual_tube: bool = False,
    probe_device_time: bool = False,
    probe_heartbeat: bool = False,
) -> DeviceCapabilities:
    """Probe optional commands defensively.

    Each failed optional command is followed by a close/open cycle and identity check so a
    partial or unsupported response cannot desynchronize later probes. The result, not the
    model profile hint, is the runtime source of truth.
    """

    supported = {
        "temperature": False, "voltage": False, "gyro": False, "dual_tube": False,
        "device_time": False, "heartbeat": False,
    }
    probes: list[tuple[str, Any]] = [
        ("temperature", device.get_temperature_c),
        ("voltage", device.get_voltage_v),
    ]
    if probe_gyro:
        probes.append(("gyro", device.get_gyro))
    if probe_dual_tube:
        probes.append(("dual_tube", lambda: (device.get_low_dose_tube_cpm(), device.get_high_dose_tube_cpm())))
    if probe_device_time:
        probes.append(("device_time", device.get_datetime))
    if probe_heartbeat:
        def heartbeat_probe() -> int:
            device.start_heartbeat()
            try:
                return device.read_heartbeat_cps()
            finally:
                with suppress(GmcError, OSError):
                    device.stop_heartbeat()
        probes.append(("heartbeat", heartbeat_probe))

    for name, reader in probes:
        try:
            reader()
        except (GmcError, OSError) as exc:
            LOG.info("Capability probe %s: unsupported or unavailable (%s)", name, exc)
            device.close()
            device.open()
            _, actual_serial = read_identity(device, expected_serial=expected_serial)
            ensure_same_serial(expected_serial, actual_serial)
        else:
            supported[name] = True
            LOG.info("Capability probe %s: supported", name)

    return DeviceCapabilities(
        cpm=True,
        temperature=supported["temperature"],
        voltage=supported["voltage"],
        gyro=supported["gyro"],
        gyro_probe_requested=probe_gyro,
        dual_tube=supported["dual_tube"],
        device_time=supported["device_time"],
        heartbeat=supported["heartbeat"],
    )


def read_sample(
    device: SerialGmc,
    read_gyro: bool,
    capabilities: DeviceCapabilities | None = None,
    *,
    read_device_time: bool = False,
    read_optional_channels: bool = True,
) -> SampleResult:
    """Read CPM first, then supported optional channels without discarding a valid CPM.

    After the first optional-channel failure no further commands are sent on the possibly
    desynchronized stream. The caller can publish verified data and reconnect afterwards.
    """
    state: dict[str, Any] = {"cpm": device.get_cpm()}
    available = {
        "cpm": True, "temperature": False, "voltage": False, "gyro": False,
        "dual_tube": False, "device_time": False,
    }
    errors: list[OptionalReadError] = []
    reconnect_required = False

    caps = capabilities or DeviceCapabilities(
        cpm=True, temperature=True, voltage=True, gyro=read_gyro, gyro_probe_requested=read_gyro
    )
    optional_steps: list[tuple[str, Any]] = []
    if not read_optional_channels:
        return SampleResult(
            state=state, available=available, optional_errors=errors, reconnect_required=False
        )
    if caps.dual_tube:
        optional_steps.append(("dual_tube", lambda: (device.get_low_dose_tube_cpm(), device.get_high_dose_tube_cpm())))
    if caps.temperature:
        optional_steps.append(("temperature", device.get_temperature_c))
    if caps.voltage:
        optional_steps.append(("voltage", device.get_voltage_v))
    if read_device_time and caps.device_time:
        optional_steps.append(("device_time", device.get_datetime))
    if read_gyro and caps.gyro:
        optional_steps.append(("gyro", device.get_gyro))

    for sensor, reader in optional_steps:
        try:
            value = reader()
        except (GmcError, OSError) as first_exc:
            if sensor == "gyro" and isinstance(first_exc, GmcProtocolError):
                # A malformed GETGYRO frame is optional-channel corruption, not
                # proof that the complete device connection is lost. Flush and
                # retry once, then let the service temporarily pause gyro only.
                try:
                    recover = getattr(device, "recover_protocol_stream", None)
                    if callable(recover):
                        recover()
                    value = reader()
                except (GmcError, OSError) as retry_exc:
                    issue = classify_optional_issue(sensor, retry_exc)
                    errors.append(OptionalReadError(
                        sensor=sensor,
                        error=f"{retry_exc} (retry after resynchronization; first error: {first_exc})",
                        code=issue.code,
                        affects_measurement=issue.affects_measurement,
                        retryable=issue.retryable,
                    ))
                    reconnect_required = not isinstance(retry_exc, GmcProtocolError)
                    break
            else:
                issue = classify_optional_issue(sensor, first_exc)
                errors.append(OptionalReadError(
                    sensor=sensor,
                    error=str(first_exc),
                    code=issue.code,
                    affects_measurement=issue.affects_measurement,
                    retryable=issue.retryable,
                ))
                reconnect_required = True
                break
        if sensor == "dual_tube":
            low, high = value
            state.update({"tube_low_cpm": low, "tube_high_cpm": high})
            available["dual_tube"] = True
        elif sensor == "temperature":
            state["temperature_c"] = value
            available["temperature"] = True
        elif sensor == "voltage":
            state["voltage_v"] = value
            available["voltage"] = True
        elif sensor == "device_time":
            state["device_time_local"] = value.isoformat(timespec="seconds")
            available["device_time"] = True
        else:
            x, y, z = value
            state.update({"gyro_x": x, "gyro_y": y, "gyro_z": z})
            available["gyro"] = True

    return SampleResult(
        state=state,
        available=available,
        optional_errors=errors,
        reconnect_required=reconnect_required,
    )

