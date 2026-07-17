from __future__ import annotations

import html
import re
import threading
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import UTC, datetime
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen

from .version import USER_AGENT

DEFAULT_GMCMAP_ENDPOINT = "https://www.gmcmap.com/log2.asp"
DEFAULT_STARTUP_DELAY_SECONDS = 30.0
GMCMAP_SERVER_DEADLINE_SECONDS = 300.0
GMCMAP_DEADLINE_SAFETY_SECONDS = 20.0
DEFAULT_MINIMUM_UPLOAD_GAP_SECONDS = 10.0
_ID_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")


def validate_identifier(name: str, value: str) -> None:
    if not _ID_RE.fullmatch(value):
        raise ValueError(f"{name} contains unsupported characters")


@dataclass(frozen=True)
class GmcMapReading:
    cpm: int
    average_cpm: float
    dose_rate_usvh: float
    captured_at_utc: int
    average_sample_count: int = 0


@dataclass
class AcpmAccumulator:
    """Cumulative mean of accepted CPM readings for the current app session.

    GMCMap calls this value ACPM (Average Counts Per Minute). GQ counters derive
    it from total counts divided by elapsed minutes. The bridge receives periodic
    CPM rates rather than the counter's internal total-count accumulator, so the
    equivalent robust estimate is the cumulative mean of every accepted CPM
    reading since this device worker started.
    """

    sample_count: int = 0
    average_cpm: float = 0.0

    def add(self, cpm: int | float) -> float:
        value = max(0.0, float(cpm))
        self.sample_count += 1
        self.average_cpm += (value - self.average_cpm) / self.sample_count
        return self.average_cpm


@dataclass(frozen=True)
class GmcMapConfig:
    account_id: str
    counter_id: str
    upload_interval_seconds: int = 300
    timeout_seconds: float = 10.0
    endpoint: str = DEFAULT_GMCMAP_ENDPOINT
    startup_delay_seconds: float = DEFAULT_STARTUP_DELAY_SECONDS

    def validate(self) -> None:
        validate_identifier("GMCMap account ID", self.account_id)
        validate_identifier("GMCMap counter ID", self.counter_id)
        if not 60 <= self.upload_interval_seconds <= 86400:
            raise ValueError("GMCMap upload interval must be between 60 and 86400 seconds")
        if not 1.0 <= self.timeout_seconds <= 30.0:
            raise ValueError("GMCMap timeout must be between 1 and 30 seconds")
        if not 0.0 <= self.startup_delay_seconds <= 300.0:
            raise ValueError("GMCMap startup delay must be between 0 and 300 seconds")
        parsed = urlsplit(self.endpoint)
        if parsed.scheme not in {"https", "http"}:
            raise ValueError("GMCMap endpoint must use HTTP or HTTPS")
        if (parsed.hostname or "").lower() not in {"gmcmap.com", "www.gmcmap.com"}:
            raise ValueError("GMCMap endpoint must use gmcmap.com")
        if parsed.path.rstrip("/").lower() != "/log2.asp":
            raise ValueError("GMCMap endpoint path must be /log2.asp")


def parse_device_id_mappings(value: str) -> tuple[tuple[str, str], ...]:
    """Parse SERIAL=COUNTER_ID pairs; a lone ID becomes a single-device wildcard."""
    normalized = value.replace("\n", ",").replace(";", ",")
    mappings: list[tuple[str, str]] = []
    seen: set[str] = set()
    for raw in normalized.split(","):
        item = raw.strip()
        if not item:
            continue
        if "=" in item:
            serial, counter_id = (part.strip() for part in item.split("=", 1))
        else:
            serial, counter_id = "*", item
        if not serial or not counter_id:
            raise ValueError("GMCMap mappings must use SERIAL=COUNTER_ID")
        if serial != "*" and not _ID_RE.fullmatch(serial):
            raise ValueError("GMCMap device serial contains unsupported characters")
        if not _ID_RE.fullmatch(counter_id):
            raise ValueError("GMCMap counter ID contains unsupported characters")
        if serial in seen:
            raise ValueError(f"Duplicate GMCMap mapping for {serial}")
        seen.add(serial)
        mappings.append((serial, counter_id))
    return tuple(mappings)


def resolve_counter_id(
    serial: str,
    mappings: tuple[tuple[str, str], ...],
    *,
    configured_device_count: int,
) -> str | None:
    table = dict(mappings)
    if serial in table:
        return table[serial]
    wildcard = table.get("*")
    if wildcard and configured_device_count == 1:
        return wildcard
    return None


def mask_identifier(value: str) -> str:
    if len(value) <= 4:
        return "*" * len(value)
    return f"{'*' * (len(value) - 4)}{value[-4:]}"


def effective_upload_interval(upload_interval_seconds: int) -> float:
    """Return a cadence that stays safely below GMCMap's 300-second deadline."""
    requested = float(upload_interval_seconds)
    safe_deadline = GMCMAP_SERVER_DEADLINE_SECONDS - GMCMAP_DEADLINE_SAFETY_SECONDS
    return min(requested, safe_deadline)


def staggered_startup_delay(
    device_index: int,
    device_count: int,
    upload_interval_seconds: int,
) -> float:
    """Assign deterministic upload phases across independently running devices.

    With two devices and the normal 300-second setting, the first upload is at +30 s
    and the second at +170 s. Both then use a 280-second effective cadence.
    """
    count = max(1, int(device_count))
    index = max(0, min(int(device_index), count - 1))
    cadence = effective_upload_interval(upload_interval_seconds)
    if count == 1:
        return min(DEFAULT_STARTUP_DELAY_SECONDS, max(0.0, cadence - 5.0))
    slot = cadence / count
    return min(
        DEFAULT_STARTUP_DELAY_SECONDS + index * slot,
        max(0.0, cadence - 5.0),
    )


class GmcMapUploadCoordinator:
    """Serialize all GMCMap requests and keep a quiet gap between connections."""

    def __init__(
        self,
        minimum_gap_seconds: float = DEFAULT_MINIMUM_UPLOAD_GAP_SECONDS,
        *,
        monotonic: Callable[[], float] = time.monotonic,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        if minimum_gap_seconds < 0.0:
            raise ValueError("GMCMap minimum upload gap cannot be negative")
        self.minimum_gap_seconds = float(minimum_gap_seconds)
        self._monotonic = monotonic
        self._sleep = sleep
        self._lock = threading.Lock()
        self._last_finished_monotonic: float | None = None

    def execute(self, action: Callable[[], tuple[int, str]]) -> tuple[int, str]:
        with self._lock:
            if self._last_finished_monotonic is not None:
                remaining = (
                    self._last_finished_monotonic
                    + self.minimum_gap_seconds
                    - self._monotonic()
                )
                if remaining > 0.0:
                    self._sleep(remaining)
            try:
                return action()
            finally:
                self._last_finished_monotonic = self._monotonic()


def build_upload_url(config: GmcMapConfig, reading: GmcMapReading) -> str:
    config.validate()
    query = urlencode(
        {
            "AID": config.account_id,
            "GID": config.counter_id,
            "CPM": str(max(0, int(reading.cpm))),
            "ACPM": f"{max(0.0, float(reading.average_cpm)):.1f}",
            "uSV": f"{max(0.0, float(reading.dose_rate_usvh)):.3f}",
        }
    )
    separator = "&" if "?" in config.endpoint else "?"
    return f"{config.endpoint}{separator}{query}"




_TAG_RE = re.compile(r"<[^>]+>")
_EXPLICIT_REJECTION_PATTERNS = (
    re.compile(r"^\s*(?:error|failed|invalid)(?:\s*[:=-].*)?\s*$", re.IGNORECASE),
    re.compile(r"\blink\s+server\s+failed\b", re.IGNORECASE),
    re.compile(
        r"\b(?:invalid|unknown|missing)\s+(?:aid|gid|account(?:\s+id)?|counter(?:\s+id)?)\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:aid|gid|account(?:\s+id)?|counter(?:\s+id)?)\s+(?:is\s+)?(?:invalid|unknown|missing)\b",
        re.IGNORECASE,
    ),
)


def response_diagnostic(body: str, *, limit: int = 240) -> str:
    """Return a compact, tag-free response summary suitable for diagnostics."""
    text = html.unescape(_TAG_RE.sub(" ", body or ""))
    text = " ".join(text.split())
    if not text:
        return "Empty response body"
    return text[:limit]


def response_rejected(body: str) -> bool:
    """Detect only explicit GMCMap rejection messages, not incidental HTML words."""
    diagnostic = response_diagnostic(body)
    return any(pattern.search(diagnostic) for pattern in _EXPLICIT_REJECTION_PATTERNS)


def redact_identifiers(value: str | None, config: GmcMapConfig) -> str | None:
    if value is None:
        return None
    return value.replace(config.account_id, "***").replace(config.counter_id, "***")


Transport = Callable[[str, float], tuple[int, str]]
StatusCallback = Callable[[dict[str, object]], None]


def _default_transport(url: str, timeout: float) -> tuple[int, str]:
    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/plain,text/html;q=0.9,*/*;q=0.1",
            "Cache-Control": "no-cache",
        },
        method="GET",
    )
    with urlopen(request, timeout=timeout) as response:
        status = int(getattr(response, "status", response.getcode()))
        body = response.read(4096).decode("utf-8", errors="replace")
    return status, body


class GmcMapUploader:
    """Non-blocking, per-device GMCMap uploader with retry and latest-value coalescing."""

    def __init__(
        self,
        config: GmcMapConfig,
        *,
        status_callback: StatusCallback | None = None,
        transport: Transport | None = None,
        monotonic: Callable[[], float] = time.monotonic,
        wall_time: Callable[[], float] = time.time,
        coordinator: GmcMapUploadCoordinator | None = None,
    ) -> None:
        config.validate()
        self.config = config
        self._status_callback = status_callback
        self._transport = transport or _default_transport
        self._monotonic = monotonic
        self._wall_time = wall_time
        self._coordinator = coordinator
        self._effective_interval_seconds = effective_upload_interval(
            config.upload_interval_seconds
        )
        self._condition = threading.Condition()
        self._stopping = False
        self._paused = False
        self._latest: GmcMapReading | None = None
        self._next_due_monotonic = 0.0
        self._retry_delay_seconds = 60.0
        self._thread: threading.Thread | None = None
        self._status: dict[str, object] = {
            "gmcmap_enabled": True,
            "gmcmap_configured": True,
            "gmcmap_counter_id_masked": mask_identifier(config.counter_id),
            "gmcmap_upload_status": "waiting",
            "gmcmap_last_upload_utc": None,
            "gmcmap_last_attempt_utc": None,
            "gmcmap_last_cpm": None,
            "gmcmap_last_average_cpm": None,
            "gmcmap_acpm_sample_count": 0,
            "gmcmap_last_dose_rate_usvh": None,
            "gmcmap_upload_success_count": 0,
            "gmcmap_upload_error_count": 0,
            "gmcmap_consecutive_error_count": 0,
            "gmcmap_last_error": None,
            "gmcmap_last_error_utc": None,
            "gmcmap_last_http_status": None,
            "gmcmap_last_response": None,
            "gmcmap_next_upload_utc": None,
            "gmcmap_startup_delay_seconds": round(config.startup_delay_seconds, 1),
            "gmcmap_upload_interval_seconds": config.upload_interval_seconds,
            "gmcmap_effective_upload_interval_seconds": round(
                self._effective_interval_seconds, 1
            ),
            "gmcmap_minimum_connection_gap_seconds": (
                coordinator.minimum_gap_seconds if coordinator is not None else 0.0
            ),
        }

    def start(self) -> None:
        with self._condition:
            if self._thread is not None:
                return
            if self._status["gmcmap_next_upload_utc"] is None:
                self._set_next_due(float(self.config.startup_delay_seconds))
            self._thread = threading.Thread(
                target=self._run,
                name=f"gmcmap-{mask_identifier(self.config.counter_id)}",
                daemon=True,
            )
            self._thread.start()
        self._emit_status()

    def stop(self, timeout: float = 5.0) -> None:
        with self._condition:
            self._stopping = True
            self._condition.notify_all()
            thread = self._thread
        if thread is not None:
            thread.join(timeout=timeout)

    def set_paused(self, paused: bool) -> None:
        with self._condition:
            self._paused = bool(paused)
            if self._paused:
                self._status["gmcmap_upload_status"] = "paused"
            elif self._latest is not None:
                self._set_next_due(float(self.config.startup_delay_seconds))
                self._status["gmcmap_upload_status"] = "waiting"
            self._condition.notify_all()
        self._emit_status()

    def offer(self, reading: GmcMapReading) -> None:
        with self._condition:
            self._latest = reading
            self._condition.notify_all()

    def snapshot(self) -> dict[str, object]:
        with self._condition:
            return dict(self._status)

    def _iso_utc(self, epoch: float) -> str:
        return datetime.fromtimestamp(epoch, UTC).isoformat(timespec="seconds").replace("+00:00", "Z")

    def _set_next_due(self, delay_seconds: float) -> None:
        self._next_due_monotonic = self._monotonic() + delay_seconds
        self._status["gmcmap_next_upload_utc"] = self._iso_utc(self._wall_time() + delay_seconds)

    def _emit_status(self) -> None:
        callback = self._status_callback
        if callback is not None:
            callback(self.snapshot())

    def _run(self) -> None:
        while True:
            with self._condition:
                while not self._stopping:
                    if self._paused:
                        self._condition.wait(timeout=1.0)
                        continue
                    if self._latest is None:
                        self._condition.wait(timeout=1.0)
                        continue
                    delay = self._next_due_monotonic - self._monotonic()
                    if delay > 0:
                        self._condition.wait(timeout=min(delay, 1.0))
                        continue
                    reading = self._latest
                    break
                else:
                    return
            self._attempt_upload(reading)

    def _attempt_upload(self, reading: GmcMapReading) -> None:
        attempt_epoch = self._wall_time()
        with self._condition:
            self._status.update(
                {
                    "gmcmap_upload_status": "uploading",
                    "gmcmap_last_attempt_utc": self._iso_utc(attempt_epoch),
                    "gmcmap_last_cpm": reading.cpm,
                    "gmcmap_last_average_cpm": round(reading.average_cpm, 1),
                    "gmcmap_acpm_sample_count": max(0, int(reading.average_sample_count)),
                    "gmcmap_last_dose_rate_usvh": round(reading.dose_rate_usvh, 3),
                }
            )
        self._emit_status()

        http_status: int | None = None
        response_summary: str | None = None
        try:
            url = build_upload_url(self.config, reading)
            transport_started_monotonic: list[float] = []

            def perform_transport() -> tuple[int, str]:
                transport_started_monotonic.append(self._monotonic())
                return self._transport(url, self.config.timeout_seconds)

            if self._coordinator is None:
                http_status, body = perform_transport()
            else:
                http_status, body = self._coordinator.execute(perform_transport)
            response_summary = redact_identifiers(response_diagnostic(body), self.config)
            if not 200 <= http_status < 300:
                raise RuntimeError(f"HTTP {http_status}")
            if response_rejected(body):
                raise RuntimeError(f"GMCMap rejected the upload: {response_summary}")
        except (HTTPError, URLError, OSError, RuntimeError, ValueError) as exc:
            if isinstance(exc, HTTPError):
                http_status = int(exc.code)
                try:
                    response_summary = redact_identifiers(
                        response_diagnostic(exc.read(4096).decode("utf-8", errors="replace")),
                        self.config,
                    )
                except (OSError, AttributeError, ValueError):
                    response_summary = None
                error_message = f"HTTP {exc.code}"
            elif isinstance(exc, URLError):
                error_message = f"Network error: {exc.reason}"
            else:
                error_message = str(exc)
            error_message = redact_identifiers(error_message, self.config) or "Unknown GMCMap error"
            error_epoch = self._wall_time()
            with self._condition:
                self._status["gmcmap_upload_status"] = "error"
                self._status["gmcmap_upload_error_count"] = int(
                    self._status["gmcmap_upload_error_count"]
                ) + 1
                self._status["gmcmap_consecutive_error_count"] = int(
                    self._status["gmcmap_consecutive_error_count"]
                ) + 1
                self._status["gmcmap_last_error"] = error_message[:240]
                self._status["gmcmap_last_error_utc"] = self._iso_utc(error_epoch)
                self._status["gmcmap_last_http_status"] = http_status
                self._status["gmcmap_last_response"] = response_summary
                delay = min(self._retry_delay_seconds, self._effective_interval_seconds)
                self._retry_delay_seconds = min(
                    self._retry_delay_seconds * 2.0,
                    self._effective_interval_seconds,
                )
                self._set_next_due(delay)
            self._emit_status()
            return

        success_epoch = self._wall_time()
        with self._condition:
            if self._latest is reading:
                self._latest = None
            self._status["gmcmap_upload_status"] = "success"
            self._status["gmcmap_last_upload_utc"] = self._iso_utc(success_epoch)
            self._status["gmcmap_upload_success_count"] = int(
                self._status["gmcmap_upload_success_count"]
            ) + 1
            self._status["gmcmap_consecutive_error_count"] = 0
            self._status["gmcmap_last_http_status"] = http_status
            self._status["gmcmap_last_response"] = response_summary
            self._retry_delay_seconds = 60.0
            transport_started = (
                transport_started_monotonic[0]
                if transport_started_monotonic
                else self._monotonic()
            )
            elapsed_since_transport_start = max(0.0, self._monotonic() - transport_started)
            self._set_next_due(
                max(0.0, self._effective_interval_seconds - elapsed_since_transport_start)
            )
        self._emit_status()
