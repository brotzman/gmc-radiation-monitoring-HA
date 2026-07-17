from __future__ import annotations

import hashlib
import secrets
import threading
import time
from dataclasses import dataclass
from http import HTTPStatus
from urllib.parse import urlparse


@dataclass(frozen=True)
class CsrfValidationResult:
    valid: bool
    status: HTTPStatus = HTTPStatus.FORBIDDEN
    message: str = "Invalid or expired form token"


class CsrfTokenManager:
    """Issue short-lived, one-time tokens for destructive web actions.

    Tokens are held only in memory. A restart invalidates all outstanding forms,
    which is preferable to accepting a stale destructive request.
    """

    def __init__(self, *, lifetime_seconds: int = 900, maximum_tokens: int = 256) -> None:
        self.lifetime_seconds = max(60, int(lifetime_seconds))
        self.maximum_tokens = max(16, int(maximum_tokens))
        self._lock = threading.Lock()
        self._tokens: dict[str, tuple[str, float]] = {}

    @staticmethod
    def _digest(token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    def _prune_locked(self, now: float) -> None:
        expired = [digest for digest, (_action, expires) in self._tokens.items() if expires <= now]
        for digest in expired:
            self._tokens.pop(digest, None)
        if len(self._tokens) <= self.maximum_tokens:
            return
        overflow = len(self._tokens) - self.maximum_tokens
        oldest = sorted(self._tokens.items(), key=lambda item: item[1][1])[:overflow]
        for digest, _value in oldest:
            self._tokens.pop(digest, None)

    def issue(self, action: str) -> str:
        normalized_action = str(action or "").strip()
        if not normalized_action:
            raise ValueError("CSRF action must not be empty")
        token = secrets.token_urlsafe(32)
        now = time.monotonic()
        with self._lock:
            self._prune_locked(now)
            self._tokens[self._digest(token)] = (
                normalized_action,
                now + self.lifetime_seconds,
            )
        return token

    def consume(self, token: str, action: str) -> CsrfValidationResult:
        normalized_token = str(token or "").strip()
        normalized_action = str(action or "").strip()
        if not normalized_token or not normalized_action:
            return CsrfValidationResult(False)
        now = time.monotonic()
        digest = self._digest(normalized_token)
        with self._lock:
            self._prune_locked(now)
            stored = self._tokens.pop(digest, None)
        if stored is None:
            return CsrfValidationResult(False)
        expected_action, expires = stored
        if expires <= now or not secrets.compare_digest(expected_action, normalized_action):
            return CsrfValidationResult(False)
        return CsrfValidationResult(True, HTTPStatus.OK, "")


def _normalized_authority(value: str) -> str:
    authority = str(value or "").strip().lower()
    if not authority:
        return ""
    # Host headers are authorities without a scheme. Reject path/control data.
    if any(character in authority for character in ("/", "\\", "\r", "\n", "\t", " ")):
        return ""
    return authority


def request_authorities(headers: object) -> set[str]:
    """Return accepted same-origin authorities from proxy-aware request headers."""

    getter = getattr(headers, "get", None)
    if getter is None:
        return set()
    authorities: set[str] = set()
    for header_name in ("Host", "X-Forwarded-Host"):
        raw = str(getter(header_name, "") or "")
        # RFC 7239-style proxy chains are left-most original first. Accept each
        # syntactically safe authority because ingress implementations differ.
        for candidate in raw.split(","):
            normalized = _normalized_authority(candidate)
            if normalized:
                authorities.add(normalized)
    return authorities


def validate_same_origin(headers: object, *, remote_address: str = "") -> CsrfValidationResult:
    """Reject explicitly cross-site unsafe requests while remaining ingress-safe.

    A valid one-time CSRF token is still required independently. Origin/Referer
    checks add defence in depth and are deliberately proxy-aware.
    """

    getter = getattr(headers, "get", None)
    if getter is None:
        return CsrfValidationResult(False, message="Invalid request headers")

    fetch_site = str(getter("Sec-Fetch-Site", "") or "").strip().lower()
    if fetch_site in {"cross-site", "none"}:
        return CsrfValidationResult(False, message="Cross-site form submission rejected")

    authorities = request_authorities(headers)
    if not authorities:
        return CsrfValidationResult(False, message="Missing or invalid Host header")

    source = str(getter("Origin", "") or "").strip()
    if not source:
        source = str(getter("Referer", "") or "").strip()
    if not source:
        # Some direct clients and ingress/proxy combinations omit both headers.
        # The mandatory one-time token still prevents a blind cross-site POST.
        return CsrfValidationResult(True, HTTPStatus.OK, "")

    trusted_ingress = str(remote_address or "").strip() == "172.30.32.2"

    # Firefox can serialize the origin of a sandboxed Home Assistant ingress
    # iframe as the literal value ``null``. Accept only that special value from
    # the fixed Supervisor ingress proxy address. Explicit cross-site requests
    # were rejected above and the one-time action token remains mandatory.
    if trusted_ingress and source.lower() == "null":
        return CsrfValidationResult(True, HTTPStatus.OK, "")

    try:
        parsed = urlparse(source)
    except ValueError:
        return CsrfValidationResult(False, message="Invalid request origin")
    source_authority = _normalized_authority(parsed.netloc)
    if parsed.scheme not in {"http", "https"} or not source_authority:
        return CsrfValidationResult(False, message="Invalid request origin")

    if source_authority in authorities:
        return CsrfValidationResult(True, HTTPStatus.OK, "")

    # Home Assistant ingress terminates the browser-facing origin and forwards
    # the request with an internal add-on Host. A valid external HTTP(S) origin
    # may therefore differ from Host when the fixed ingress proxy forwarded it.
    if trusted_ingress:
        return CsrfValidationResult(True, HTTPStatus.OK, "")

    return CsrfValidationResult(False, message="Request origin does not match Host")
