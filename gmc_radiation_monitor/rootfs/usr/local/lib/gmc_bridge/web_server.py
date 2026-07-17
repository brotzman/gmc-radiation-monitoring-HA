from __future__ import annotations

import errno
import logging
import socket
import sys
import threading
from http.server import ThreadingHTTPServer
from typing import Any

LOG = logging.getLogger(__name__)
_EXPECTED_DISCONNECT_ERRNOS = {
    errno.ECONNABORTED,
    errno.ECONNRESET,
    errno.EPIPE,
    errno.ETIMEDOUT,
}


def _is_expected_client_disconnect(error: BaseException | None) -> bool:
    if isinstance(
        error,
        (BrokenPipeError, ConnectionAbortedError, ConnectionResetError, TimeoutError),
    ):
        return True
    return isinstance(error, OSError) and error.errno in _EXPECTED_DISCONNECT_ERRNOS


class BoundedThreadingHTTPServer(ThreadingHTTPServer):
    """Threading HTTP server with a hard concurrency ceiling and socket timeout."""

    daemon_threads = True
    block_on_close = True
    allow_reuse_address = True
    request_queue_size = 16

    def __init__(
        self,
        server_address: tuple[str, int],
        request_handler_class: type,
        *,
        max_workers: int = 12,
        socket_timeout_seconds: float = 30.0,
    ) -> None:
        self.max_workers = max(2, int(max_workers))
        self.socket_timeout_seconds = max(5.0, float(socket_timeout_seconds))
        self._worker_slots = threading.BoundedSemaphore(self.max_workers)
        super().__init__(server_address, request_handler_class)

    def get_request(self) -> tuple[socket.socket, Any]:
        request, client_address = super().get_request()
        request.settimeout(self.socket_timeout_seconds)
        return request, client_address

    def process_request(self, request: socket.socket, client_address: Any) -> None:
        if not self._worker_slots.acquire(blocking=False):
            try:
                request.sendall(
                    b"HTTP/1.1 503 Service Unavailable\r\n"
                    b"Connection: close\r\n"
                    b"Content-Type: text/plain; charset=utf-8\r\n"
                    b"Cache-Control: no-store\r\n"
                    b"Content-Length: 16\r\n\r\n"
                    b"Server is busy.\n"
                )
            except OSError:
                pass
            finally:
                self.shutdown_request(request)
            return
        try:
            super().process_request(request, client_address)
        except Exception:
            self._worker_slots.release()
            raise

    def process_request_thread(self, request: socket.socket, client_address: Any) -> None:
        try:
            super().process_request_thread(request, client_address)
        finally:
            self._worker_slots.release()

    def handle_error(self, request: socket.socket, client_address: Any) -> None:
        error = sys.exc_info()[1]
        if _is_expected_client_disconnect(error):
            LOG.debug("HTTP client %s disconnected before the request completed", client_address[0])
            return
        super().handle_error(request, client_address)
