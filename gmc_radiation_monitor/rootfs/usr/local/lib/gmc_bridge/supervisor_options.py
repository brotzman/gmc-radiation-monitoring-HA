from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SUPERVISOR_OPTIONS_URL = "http://supervisor/addons/self/options"


class _Response(Protocol):
    status: int

    def __enter__(self) -> _Response: ...

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None: ...

    def read(self) -> bytes: ...


class SupervisorOptionsError(RuntimeError):
    """Raised when migrated app options cannot be persisted safely."""


def build_options_payload(options: dict[str, Any]) -> bytes:
    """Encode a complete Supervisor options payload without shell interpolation."""

    return json.dumps(
        {"options": options},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def persist_self_options(
    options: dict[str, Any],
    *,
    token: str,
    timeout: float = 10.0,
    opener: Callable[..., _Response] = urlopen,
) -> None:
    """Persist the complete current app options through the Supervisor API."""

    if not token:
        raise SupervisorOptionsError("SUPERVISOR_TOKEN is unavailable")

    request = Request(
        SUPERVISOR_OPTIONS_URL,
        data=build_options_payload(options),
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with opener(request, timeout=timeout) as response:
            status = int(getattr(response, "status", 200))
            raw_body = response.read()
    except HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise SupervisorOptionsError(
            f"Supervisor rejected migrated options with HTTP {exc.code}: {detail}"
        ) from exc
    except URLError as exc:
        raise SupervisorOptionsError(f"Supervisor API is unavailable: {exc.reason}") from exc
    except OSError as exc:
        raise SupervisorOptionsError(f"Supervisor API request failed: {exc}") from exc

    if status < 200 or status >= 300:
        raise SupervisorOptionsError(f"Supervisor returned unexpected HTTP status {status}")

    if not raw_body:
        return

    try:
        body = json.loads(raw_body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise SupervisorOptionsError("Supervisor returned an invalid JSON response") from exc

    if isinstance(body, dict) and body.get("result") == "error":
        message = body.get("message") or "Supervisor rejected migrated options"
        raise SupervisorOptionsError(str(message))
