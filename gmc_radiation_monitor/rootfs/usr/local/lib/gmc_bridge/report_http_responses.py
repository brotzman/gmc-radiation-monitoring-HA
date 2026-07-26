from __future__ import annotations

import re
from http import HTTPStatus


class HttpResponseMixin:
    """Shared secure HTTP response helpers for report handlers."""
    def _send_bytes(
        self,
        status: HTTPStatus,
        content_type: str,
        payload: bytes,
        *,
        close_connection: bool = False,
        cache_control: str = "no-store",
        content_disposition: str | None = None,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", cache_control)
        if content_disposition:
            self.send_header("Content-Disposition", content_disposition)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        script_nonce_match = (
            re.search(rb'<script nonce="([A-Za-z0-9_-]+)"', payload)
            if content_type.startswith("text/html")
            else None
        )
        script_policy = (
            f"; script-src 'self' 'nonce-{script_nonce_match.group(1).decode('ascii')}'"
            if script_nonce_match
            else ""
        )
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; style-src 'self' 'unsafe-inline'; form-action 'self'; connect-src 'self'"
            + script_policy,
        )
        if close_connection:
            self.send_header("Connection", "close")
            self.close_connection = True
        self.end_headers()
        self.wfile.write(payload)

    def _send_error(
        self,
        status: HTTPStatus,
        message: str,
        *,
        close_connection: bool | None = None,
    ) -> None:
        payload = f"{status.value}\n{message}\n".encode()
        # On an unsuccessful POST the request body may not have been consumed.
        # Closing the HTTP/1.1 connection prevents those bytes from being parsed
        # as a second request line (for example "csrf_token=..." as a method).
        should_close = self.command == "POST" if close_connection is None else close_connection
        self._send_bytes(
            status,
            "text/plain; charset=utf-8",
            payload,
            close_connection=should_close,
        )

