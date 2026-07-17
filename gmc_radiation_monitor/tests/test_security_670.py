from __future__ import annotations

import json
import logging
import random
import socket
import stat
import sys
import threading
import types
import zipfile
from pathlib import Path

import pytest
from gmc_bridge.file_security import PRIVATE_FILE_MODE
from gmc_bridge.history import HistoryStore
from gmc_bridge.home_assistant import HomeAssistantPressureClient
from gmc_bridge.maintenance import diagnostics_document
from gmc_bridge.report_web import ReportApplication, ReportRequestHandler
from gmc_bridge.reports import build_report_to_path, load_timezone, resolve_period
from gmc_bridge.revision_cache import RevisionCache
from gmc_bridge.runtime_options import OptionsError, runtime_environment
from gmc_bridge.security_logging import SecretRedactingFormatter, redact_text
from gmc_bridge.serial_device import SerialGmc
from gmc_bridge.web_security import CsrfTokenManager, validate_same_origin
from gmc_bridge.web_server import BoundedThreadingHTTPServer, _is_expected_client_disconnect


class HeaderMap(dict[str, str]):
    def get(self, key: str, default: str = "") -> str:
        return super().get(key, default)


def test_bridge_logging_setup_calls_secure_configurator(monkeypatch: pytest.MonkeyPatch) -> None:
    try:
        import paho.mqtt.client  # type: ignore[import-not-found]
    except ImportError:
        paho = types.ModuleType("paho")
        paho_mqtt = types.ModuleType("paho.mqtt")
        paho_client = types.ModuleType("paho.mqtt.client")
        paho_client.MQTT_ERR_SUCCESS = 0
        paho_mqtt.client = paho_client
        paho.mqtt = paho_mqtt
        monkeypatch.setitem(sys.modules, "paho", paho)
        monkeypatch.setitem(sys.modules, "paho.mqtt", paho_mqtt)
        monkeypatch.setitem(sys.modules, "paho.mqtt.client", paho_client)

    import gmc_bridge.service as service

    captured: dict[str, object] = {}

    def fake_configure_secure_logging(*, level: int, format_string: str) -> None:
        captured["level"] = level
        captured["format_string"] = format_string

    monkeypatch.setenv("LOG_LEVEL", "warning")
    monkeypatch.setattr(service, "configure_secure_logging", fake_configure_secure_logging)
    service.configure_logging()

    assert captured["level"] == logging.WARNING
    assert captured["format_string"] == "%(asctime)s %(levelname)s %(message)s"


def test_csrf_tokens_are_action_bound_and_one_time() -> None:
    tokens = CsrfTokenManager()
    token = tokens.issue("restore")
    assert not tokens.consume(token, "purge-all-history").valid
    assert not tokens.consume(token, "restore").valid

    second = tokens.issue("restore")
    assert tokens.consume(second, "restore").valid
    assert not tokens.consume(second, "restore").valid


def test_same_origin_validation_accepts_home_assistant_ingress_host_rewrite() -> None:
    result = validate_same_origin(
        HeaderMap(
            {
                "Host": "127.0.0.1:8099",
                "Origin": "https://homeassistant.example.test",
                "Sec-Fetch-Site": "same-origin",
            }
        ),
        remote_address="172.30.32.2",
    )
    assert result.valid


def test_same_origin_validation_does_not_require_optional_ingress_path_header() -> None:
    result = validate_same_origin(
        HeaderMap(
            {
                "Host": "addon.internal:8099",
                "Origin": "https://ha.example.test",
                "Referer": "https://ha.example.test/hassio/ingress/session/",
                "Sec-Fetch-Site": "same-origin",
            }
        ),
        remote_address="172.30.32.2",
    )
    assert result.valid


def test_same_origin_validation_accepts_firefox_null_origin_from_ingress() -> None:
    result = validate_same_origin(
        HeaderMap(
            {
                "Host": "addon.internal:8099",
                "Origin": "null",
                "Sec-Fetch-Site": "same-origin",
            }
        ),
        remote_address="172.30.32.2",
    )
    assert result.valid


def test_same_origin_validation_rejects_null_origin_outside_ingress() -> None:
    result = validate_same_origin(
        HeaderMap(
            {
                "Host": "addon.internal:8099",
                "Origin": "null",
                "Sec-Fetch-Site": "same-origin",
            }
        ),
        remote_address="192.0.2.50",
    )
    assert not result.valid
    assert result.message == "Invalid request origin"


def test_same_origin_validation_does_not_trust_spoofed_ingress_header() -> None:
    result = validate_same_origin(
        HeaderMap(
            {
                "Host": "127.0.0.1:8099",
                "Origin": "https://homeassistant.example.test",
                "Sec-Fetch-Site": "same-origin",
                "X-Ingress-Path": "/api/hassio_ingress/session-token",
            }
        ),
        remote_address="192.0.2.50",
    )
    assert not result.valid
    assert result.message == "Request origin does not match Host"


def test_same_origin_validation_keeps_strict_fallback_without_ingress_signals() -> None:
    result = validate_same_origin(
        HeaderMap(
            {
                "Host": "127.0.0.1:8099",
                "Origin": "https://homeassistant.example.test",
            }
        )
    )
    assert not result.valid
    assert result.message == "Request origin does not match Host"


def test_same_origin_validation_is_proxy_aware_and_rejects_cross_site() -> None:
    valid = validate_same_origin(
        HeaderMap(
            {
                "Host": "addon.internal:8099",
                "X-Forwarded-Host": "ha.example.test",
                "Origin": "https://ha.example.test",
                "Sec-Fetch-Site": "same-origin",
            }
        )
    )
    assert valid.valid

    rejected = validate_same_origin(
        HeaderMap(
            {
                "Host": "addon.internal:8099",
                "Origin": "https://attacker.example",
                "Sec-Fetch-Site": "cross-site",
            }
        )
    )
    assert not rejected.valid


def test_rendered_destructive_forms_contain_one_time_tokens(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
        restore_enabled=True,
        purge_all_history_enabled=True,
    )
    page = app.render_index().decode("utf-8")
    assert page.count('name="csrf_token"') == 5
    for action in (
        "purge-all-history",
        "restore",
        "workflow-settings",
        "annotation-add",
        "managed-backup-create",
    ):
        assert f'action="?action={action}"' in page
    assert 'name="confirm"' in page


def test_history_database_and_backup_are_owner_only(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    store.insert_measurement({"cpm": 12}, device_serial="device-a", timestamp_utc=1_800_000_000)
    backup = store.backup_to_path(tmp_path / "backup.sqlite3")
    assert stat.S_IMODE(store.path.stat().st_mode) == PRIVATE_FILE_MODE
    assert stat.S_IMODE(backup.stat().st_mode) == PRIVATE_FILE_MODE
    assert stat.S_IMODE(store.lock_path.stat().st_mode) == PRIVATE_FILE_MODE


def test_runtime_options_are_centralized_and_reject_invalid_sections() -> None:
    options = {
        "devices": [{"name": "GMC-320", "scan_interval": 61}],
        "history": {"retention_days": 120, "report_timezone": "Europe/Berlin"},
        "system": {"log_level": "warning"},
    }
    bridge = runtime_environment(options, "bridge")
    reports = runtime_environment(options, "reports")
    assert json.loads(bridge["DEVICES_JSON"])[0]["name"] == "GMC-320"
    assert bridge["SCAN_INTERVAL"] == "61"
    assert reports["HISTORY_RETENTION_DAYS"] == "120"
    assert reports["HTTP_MAX_WORKERS"] == "12"
    assert reports["ENABLE_PURGE_ALL_HISTORY"] == "false"
    assert "PORT" not in bridge and "BAUDRATE" not in bridge

    with pytest.raises(OptionsError):
        runtime_environment({"history": []}, "bridge")


def test_secret_redaction_covers_exact_values_and_credential_patterns() -> None:
    value = "super-secret-value"
    text = redact_text(
        f"Authorization: Bearer abc.def password={value} token=visible account_id=12345",
        sensitive_values=(value,),
    )
    assert value not in text
    assert "abc.def" not in text
    assert "token=visible" not in text
    assert "account_id=12345" not in text
    assert text.count("[REDACTED]") >= 4


def test_secret_redacting_formatter_covers_exception_text() -> None:
    formatter = SecretRedactingFormatter(
        "%(levelname)s %(message)s",
        sensitive_values=("exception-secret",),
    )
    try:
        raise RuntimeError("token=visible exception-secret")
    except RuntimeError:
        record = logging.LogRecord(
            name="security-test",
            level=logging.ERROR,
            pathname=__file__,
            lineno=1,
            msg="request failed",
            args=(),
            exc_info=__import__("sys").exc_info(),
        )
    rendered = formatter.format(record)
    assert "visible" not in rendered
    assert "exception-secret" not in rendered
    assert "[REDACTED]" in rendered


def test_diagnostics_never_export_credentials(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    store.set_metadata(
        {
            "serial": "device-a",
            "mqtt_password": "secret",
            "supervisor_token": "token",
            "gmcmap_account_id": "account",
        }
    )
    payload = json.dumps(diagnostics_document(store))
    assert "secret" not in payload
    assert '"token"' not in payload
    assert "account" not in payload


def test_home_assistant_entity_id_is_url_encoded(monkeypatch: pytest.MonkeyPatch) -> None:
    captured: dict[str, str] = {}

    class Response:
        status = 200

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def read(self) -> bytes:
            return b"{}"

    def fake_urlopen(request, timeout):
        del timeout
        captured["url"] = request.full_url
        return Response()

    monkeypatch.setattr("gmc_bridge.home_assistant.urlopen", fake_urlopen)
    client = HomeAssistantPressureClient(entity_ids=("weather.home",), token="token")
    client._request_state("weather.home/../../config")
    assert captured["url"].endswith("weather.home%2F..%2F..%2Fconfig")


def test_report_zip_is_written_directly_to_path(tmp_path: Path) -> None:
    store = HistoryStore(tmp_path / "history.sqlite3")
    store.set_metadata({"serial": "device-a", "device_model": "GMC Test"})
    store.insert_measurement({"cpm": 14}, timestamp_utc=1_800_000_000)
    tz = load_timezone("Europe/Berlin")
    period = resolve_period(
        kind="daily",
        selection="specific",
        tz=tz,
        date_value="2027-01-15",
    )
    destination = tmp_path / "report.zip"
    filename, content_type, path = build_report_to_path(
        store,
        destination,
        period=period,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        output_format="zip",
        device_serial="device-a",
    )
    assert filename.endswith(".zip")
    assert content_type == "application/zip"
    assert path == destination
    assert stat.S_IMODE(destination.stat().st_mode) == PRIVATE_FILE_MODE
    with zipfile.ZipFile(destination) as archive:
        assert any(name.endswith("analysis.json") for name in archive.namelist())
        assert any(name.endswith("analysis.pdf") for name in archive.namelist())


def test_revision_cache_builds_once_and_returns_isolated_values() -> None:
    cache = RevisionCache(max_entries=2, ttl_seconds=60)
    calls = 0

    def builder() -> dict[str, list[int]]:
        nonlocal calls
        calls += 1
        return {"values": [1]}

    first = cache.get_or_build(("key", 1), builder)
    first["values"].append(2)
    second = cache.get_or_build(("key", 1), builder)
    assert calls == 1
    assert second == {"values": [1]}


def test_expected_http_client_disconnects_are_suppressed() -> None:
    assert _is_expected_client_disconnect(ConnectionResetError(104, "reset"))
    assert _is_expected_client_disconnect(BrokenPipeError(32, "pipe"))
    assert _is_expected_client_disconnect(TimeoutError("timeout"))
    assert not _is_expected_client_disconnect(RuntimeError("unexpected"))


def test_bounded_server_does_not_print_disconnect_traceback(capsys: pytest.CaptureFixture[str]) -> None:
    from http.server import BaseHTTPRequestHandler

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *_args):
            pass

    server = BoundedThreadingHTTPServer(("127.0.0.1", 0), Handler)
    try:
        try:
            raise ConnectionResetError(104, "reset")
        except ConnectionResetError:
            server.handle_error(None, ("127.0.0.1", 12345))  # type: ignore[arg-type]
        assert capsys.readouterr().err == ""
    finally:
        server.server_close()


def test_bounded_server_has_safe_defaults() -> None:
    from http.server import BaseHTTPRequestHandler

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-Length", "0")
            self.end_headers()

        def log_message(self, *_args):
            pass

    server = BoundedThreadingHTTPServer(("127.0.0.1", 0), Handler, max_workers=3)
    try:
        assert server.max_workers == 3
        assert server.request_queue_size == 16
        assert server.socket_timeout_seconds == 30.0
    finally:
        server.server_close()


def test_serial_counter_decoder_is_total_for_random_frames() -> None:
    random_source = random.Random(670)
    for size in (2, 4):
        for _ in range(500):
            raw = random_source.randbytes(random_source.randrange(0, 10))
            try:
                value = SerialGmc._decode_counter_bytes(raw, size, "GETCPM")
            except Exception as exc:
                assert exc.__class__.__name__ in {"GmcTimeout", "GmcProtocolError"}
            else:
                assert 0 <= value < 2 ** (8 * size)


def test_rejected_post_closes_connection_before_body_can_be_reparsed(tmp_path: Path) -> None:
    app = ReportApplication(
        store=HistoryStore(tmp_path / "history.sqlite3"),
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
    )
    server = BoundedThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
    server.app = app
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    body = b"csrf_token=not-consumed&confirm=DELETE+ALL+GMC+HISTORY"
    request = (
        b"POST /?action=purge-all-history HTTP/1.1\r\n"
        b"Host: addon.internal:8099\r\n"
        b"Origin: https://ha.example.test\r\n"
        b"Sec-Fetch-Site: same-origin\r\n"
        b"Content-Type: application/x-www-form-urlencoded\r\n"
        + f"Content-Length: {len(body)}\r\n".encode("ascii")
        + b"Connection: keep-alive\r\n\r\n"
        + body
    )
    try:
        with socket.create_connection(("127.0.0.1", server.server_port), timeout=5) as connection:
            connection.sendall(request)
            chunks: list[bytes] = []
            while True:
                chunk = connection.recv(65536)
                if not chunk:
                    break
                chunks.append(chunk)
        response = b"".join(chunks)
        assert response.startswith(b"HTTP/1.1 403")
        assert b"Connection: close" in response
        assert response.count(b"HTTP/1.1") == 1
        assert b"501" not in response
        assert b"400" not in response
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
