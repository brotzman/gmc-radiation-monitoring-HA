from __future__ import annotations
import html
import json
import logging
import re
import sqlite3
import time
from datetime import UTC, datetime
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, quote_plus, urlparse

from .automation import automation_status
from .calibration_http import (
    calibration_history_payload,
    calibration_profiles_payload,
    persist_calibration_profile,
)
from .config_validation import validate_candidate_options
from .maintenance import diagnostics_json_bytes, full_history_zip_to_path
from .report_web_support import (
    MAX_DOWNLOAD_BYTES,
    MAX_RESTORE_BYTES,
    STREAM_CHUNK_BYTES,
    _one,
    _optional_one,
    _resolve_user_manual,
    _stream_restore_upload_to_temp,
    _temporary_path,
)
from .reports import build_report_to_path, resolve_period
from .translations import Translator, resolve_language
from .utils import slugify
from .version import REPORT_SERVER_VERSION
from .web_security import validate_same_origin
from .workflow import (
    WorkflowSettings,
    load_workflow_settings,
    local_range,
    save_workflow_settings,
)

if TYPE_CHECKING:
    from .report_web import ReportApplication

LOG = logging.getLogger("gmc_reports")

class ReportRequestHandler(BaseHTTPRequestHandler):
    server_version = REPORT_SERVER_VERSION
    protocol_version = "HTTP/1.1"

    @property
    def app(self) -> ReportApplication:
        return self.server.app  # type: ignore[attr-defined]

    def log_message(self, format_string: str, *args: Any) -> None:
        LOG.info("HTTP %s - %s", self.address_string(), format_string % args)

    def log_error(self, format_string: str, *args: Any) -> None:
        message = format_string % args
        if message.startswith("Request timed out:"):
            LOG.debug("HTTP client %s left an idle keep-alive connection", self.address_string())
            return
        LOG.warning("HTTP %s - %s", self.address_string(), message)

    def _request_translator(self, query: dict[str, list[str]] | None = None) -> Translator:
        query = query or {}
        override = _optional_one(query, "lang")
        language = resolve_language(
            self.app.ui_language,
            accept_language=self.headers.get("Accept-Language", ""),
            override=override,
        )
        return Translator(language)

    def _validate_unsafe_request(self, t: Translator) -> bool:
        result = validate_same_origin(self.headers, remote_address=self.client_address[0])
        if result.valid:
            return True
        LOG.warning("Rejected unsafe HTTP request from %s: %s", self.client_address[0], result.message)
        self._send_error(result.status, t(result.message), close_connection=True)
        return False

    def _consume_csrf_token(self, token: str, action: str, t: Translator) -> bool:
        result = self.app.csrf_tokens.consume(token, action)
        if result.valid:
            return True
        LOG.warning("Rejected invalid CSRF token for %s from %s", action, self.client_address[0])
        self._send_error(result.status, t(result.message))
        return False

    def _read_urlencoded_form(self, *, maximum_bytes: int = 64 * 1024) -> dict[str, list[str]]:
        content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
        if content_type != "application/x-www-form-urlencoded":
            raise ValueError("Expected a form-encoded request")
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0 or length > maximum_bytes:
            raise ValueError("Invalid form size")
        return parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)

    def _redirect_dashboard(self, *, anchor: str = "workflow", language: str = "") -> None:
        suffix = f"?lang={quote_plus(language)}" if language else ""
        self.send_response(HTTPStatus.SEE_OTHER)
        self.send_header("Location", f"./{suffix}#{anchor}")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _parse_local_datetime(self, value: str, *, fallback: int | None = None) -> int:
        text = str(value or "").strip()
        if not text:
            if fallback is None:
                raise ValueError("A date and time are required")
            return int(fallback)
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=self.app.timezone)
        return int(parsed.astimezone(UTC).timestamp())

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        query = parse_qs(parsed.query, keep_blank_values=False)
        t = self._request_translator(query)
        try:
            if path == "/health":
                health = self.app.api_health()
                response_status = HTTPStatus.OK if bool(health.get("healthy")) else HTTPStatus.SERVICE_UNAVAILABLE
                payload = json.dumps(health, separators=(",", ":"), sort_keys=True).encode("utf-8")
                self._send_bytes(response_status, "application/json; charset=utf-8", payload)
                return
            if path in {"/docs/user-manual.pdf", "/docs/benutzerhandbuch.pdf"}:
                requested_language = (
                    "de" if path == "/docs/benutzerhandbuch.pdf" and "lang" not in query else t.language
                )
                _manual_language, manual_filename, manual_path = _resolve_user_manual(requested_language)
                if not manual_path.is_file():
                    self._send_error(HTTPStatus.NOT_FOUND, t("User manual is not available"))
                    return
                self._send_file_inline(
                    manual_filename,
                    "application/pdf",
                    manual_path,
                    max_bytes=MAX_DOWNLOAD_BYTES,
                    t=t,
                )
                return
            if path == "/api/status":
                payload = json.dumps(self.app.status(), separators=(",", ":"), sort_keys=True).encode("utf-8")
                self._send_bytes(HTTPStatus.OK, "application/json; charset=utf-8", payload)
                return
            if path == "/api/v1/status":
                payload = self.app.status()
                payload["workflow_settings"] = load_workflow_settings(self.app.store).as_dict()
                payload["workflow_automation"] = automation_status(self.app.store)
                self._send_bytes(
                    HTTPStatus.OK,
                    "application/json; charset=utf-8",
                    json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/v1/analysis":
                payload = self.app.api_analysis(_optional_one(query, "device"))
                self._send_bytes(
                    HTTPStatus.OK,
                    "application/json; charset=utf-8",
                    json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/v1/history":
                start_text = _optional_one(query, "start_utc")
                end_text = _optional_one(query, "end_utc")
                include_raw = str(_optional_one(query, "raw") or "").lower() in {"1", "true", "yes"}
                payload = self.app.api_history(
                    device_serial=_optional_one(query, "device"),
                    start_utc=int(start_text) if start_text else None,
                    end_utc=int(end_text) if end_text else None,
                    include_raw=include_raw,
                )
                self._send_bytes(
                    HTTPStatus.OK,
                    "application/json; charset=utf-8",
                    json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/v1/events":
                serial = self.app._known_device_serial(_optional_one(query, "device"))
                start_text = _optional_one(query, "start_utc")
                end_text = _optional_one(query, "end_utc")
                start = int(start_text) if start_text else int(time.time()) - 30 * 86400
                end = int(end_text) if end_text else int(time.time()) + 1
                payload = {
                    "device_serial": serial,
                    "annotations": self.app.store.list_event_annotations(
                        start_utc=start, end_utc=end, device_serial=serial, limit=1000
                    ),
                    "operational_events": [
                        event
                        for event in self.app.store.recent_operational_events(
                            limit=1000, device_serial=serial
                        )
                        if start <= int(event.get("timestamp_utc") or 0) < end
                    ],
                }
                self._send_bytes(
                    HTTPStatus.OK,
                    "application/json; charset=utf-8",
                    json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/v1/comparison":
                first_range = second_range = None
                if all(
                    _optional_one(query, key)
                    for key in ("first_start", "first_end", "second_start", "second_end")
                ):
                    first_range = local_range(
                        _one(query, "first_start"), _one(query, "first_end"), self.app.timezone
                    )
                    second_range = local_range(
                        _one(query, "second_start"), _one(query, "second_end"), self.app.timezone
                    )
                payload = self.app.api_comparison(
                    device_serial=_optional_one(query, "device"),
                    first_range=first_range,
                    second_range=second_range,
                )
                self._send_bytes(
                    HTTPStatus.OK,
                    "application/json; charset=utf-8",
                    json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/v1/self-test":
                payload = self.app.api_self_test()
                self._send_bytes(
                    HTTPStatus.OK,
                    "application/json; charset=utf-8",
                    json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/v1/config-validation":
                payload = self.app.api_config_validation()
                self._send_bytes(
                    HTTPStatus.OK,
                    "application/json; charset=utf-8",
                    json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/v1/calibration-profiles":
                self._send_bytes(
                    HTTPStatus.OK, "application/json; charset=utf-8",
                    json.dumps(calibration_profiles_payload(self.app.store), separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/v1/calibration-history":
                payload = calibration_history_payload(
                    self.app.store, device_serial=_optional_one(query, "device")
                )
                self._send_bytes(
                    HTTPStatus.OK, "application/json; charset=utf-8",
                    json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/v1/scheduled-reports":
                payload = {"reports": self.app.list_scheduled_reports(limit=200)}
                self._send_bytes(
                    HTTPStatus.OK,
                    "application/json; charset=utf-8",
                    json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/v1/backups":
                payload: dict[str, Any] = {
                    "backups": [item.as_dict() for item in self.app.backup_manager.list()]
                }
                first_name = _optional_one(query, "first")
                second_name = _optional_one(query, "second")
                if first_name and second_name:
                    payload["comparison"] = self.app.backup_manager.compare(first_name, second_name)
                self._send_bytes(
                    HTTPStatus.OK,
                    "application/json; charset=utf-8",
                    json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8"),
                )
                return
            if path == "/api/device-cards":
                self._send_bytes(
                    HTTPStatus.OK,
                    "text/html; charset=utf-8",
                    self.app.render_devices_fragment(
                        mode_override=_optional_one(query, "mode"),
                        language_override=_optional_one(query, "lang"),
                        device_override=_optional_one(query, "device"),
                        report_device_override=_optional_one(query, "report_device"),
                        accept_language=self.headers.get("Accept-Language", ""),
                    ),
                )
                return
            if path == "/":
                action = _optional_one(query, "action")
                if action == "download":
                    self._handle_download(query)
                    return
                if action == "database-backup":
                    self._handle_maintenance_file_download(
                        "gmc_history_backup.sqlite3",
                        "application/vnd.sqlite3",
                        self.app.store.backup_to_path,
                        suffix=".sqlite3",
                        t=t,
                    )
                    return
                if action == "history-export":
                    self._handle_maintenance_file_download(
                        "gmc_history_full.zip",
                        "application/zip",
                        lambda output_path: full_history_zip_to_path(self.app.store, output_path),
                        suffix=".zip",
                        t=t,
                    )
                    return
                if action == "scheduled-report-download":
                    name = _one(query, "name")
                    report_path = self.app.resolve_scheduled_report(name)
                    content_type = (
                        "application/zip"
                        if report_path.suffix.lower() == ".zip"
                        else "application/json; charset=utf-8"
                    )
                    self._send_file_attachment(
                        name, content_type, report_path, max_bytes=MAX_DOWNLOAD_BYTES, t=t
                    )
                    return
                if action == "managed-backup-download":
                    name = _one(query, "name")
                    path_to_backup = self.app.backup_manager.resolve(name)
                    self._send_file_attachment(
                        name, "application/vnd.sqlite3", path_to_backup, max_bytes=MAX_RESTORE_BYTES, t=t
                    )
                    return
                if action == "diagnostics":
                    self._handle_maintenance_bytes_download(
                        "gmc_diagnostics.json",
                        "application/json; charset=utf-8",
                        lambda: diagnostics_json_bytes(self.app.store),
                        t=t,
                    )
                    return
                self._send_bytes(
                    HTTPStatus.OK,
                    "text/html; charset=utf-8",
                    self.app.render_index(
                        mode_override=_optional_one(query, "mode"),
                        language_override=_optional_one(query, "lang"),
                        device_override=_optional_one(query, "device"),
                        report_device_override=_optional_one(query, "report_device"),
                        compare_device_override=_optional_one(query, "compare_device"),
                        first_start_override=_optional_one(query, "first_start"),
                        first_end_override=_optional_one(query, "first_end"),
                        second_start_override=_optional_one(query, "second_start"),
                        second_end_override=_optional_one(query, "second_end"),
                        history_start_override=_optional_one(query, "history_start"),
                        history_end_override=_optional_one(query, "history_end"),
                        history_raw_override=_optional_one(query, "history_raw"),
                        data_mode_override=_optional_one(query, "data_mode"),
                        accept_language=self.headers.get("Accept-Language", ""),
                    ),
                )
                return
            if path == "/database-backup":
                self._handle_maintenance_file_download(
                    "gmc_history_backup.sqlite3",
                    "application/vnd.sqlite3",
                    self.app.store.backup_to_path,
                    suffix=".sqlite3",
                    t=t,
                )
                return
            if path == "/history-export":
                self._handle_maintenance_file_download(
                    "gmc_history_full.zip",
                    "application/zip",
                    lambda output_path: full_history_zip_to_path(self.app.store, output_path),
                    suffix=".zip",
                    t=t,
                )
                return
            if path == "/diagnostics.json":
                self._handle_maintenance_bytes_download(
                    "gmc_diagnostics.json",
                    "application/json; charset=utf-8",
                    lambda: diagnostics_json_bytes(self.app.store),
                    t=t,
                )
                return
            if path == "/download":
                self._handle_download(parse_qs(parsed.query, keep_blank_values=False))
                return
            self._send_error(HTTPStatus.NOT_FOUND, t("Not found"))
        except (ValueError, OSError) as exc:
            LOG.warning("Report request rejected: %s", exc)
            self._send_error(HTTPStatus.BAD_REQUEST, _localized_exception_message(t, exc))
        except Exception as exc:
            LOG.exception("Report request failed: %s", exc)
            self._send_error(HTTPStatus.INTERNAL_SERVER_ERROR, t("Report generation failed"))

    def _handle_workflow_action(self, action: str | None, t: Translator) -> bool:
        supported = {
            "workflow-settings",
            "annotation-add",
            "annotation-status",
            "annotation-delete",
            "managed-backup-create",
            "managed-backup-delete",
            "scheduled-report-delete",
        }
        if action not in supported:
            return False
        try:
            data = self._read_urlencoded_form()
            token = (data.get("csrf_token") or [""])[0]
            if action == "workflow-settings":
                if not self._consume_csrf_token(token, "workflow-settings", t):
                    return True

                def enabled(name: str) -> bool:
                    return str((data.get(name) or [""])[0]).strip().lower() in {"1", "true", "yes", "on"}

                settings = WorkflowSettings.from_mapping(
                    {
                        "notifications_enabled": enabled("notifications_enabled"),
                        "notify_device_offline": enabled("notify_device_offline"),
                        "notify_data_stale": enabled("notify_data_stale"),
                        "notify_confirmed_event": enabled("notify_confirmed_event"),
                        "notify_database_problem": enabled("notify_database_problem"),
                        "offline_minutes": (data.get("offline_minutes") or ["15"])[0],
                        "stale_minutes": (data.get("stale_minutes") or ["15"])[0],
                        "cooldown_minutes": (data.get("cooldown_minutes") or ["180"])[0],
                        "scheduled_reports_enabled": enabled("scheduled_reports_enabled"),
                        "daily_report": enabled("daily_report"),
                        "weekly_report": enabled("weekly_report"),
                        "monthly_summary": enabled("monthly_summary"),
                        "report_hour": (data.get("report_hour") or ["6"])[0],
                        "managed_backup_retention": (data.get("managed_backup_retention") or ["7"])[0],
                    }
                )
                save_workflow_settings(self.app.store, settings)
                self.app.backup_manager.prune(settings.managed_backup_retention)
                self._redirect_dashboard(anchor="workflow", language=t.language)
                return True
            if action == "scheduled-report-delete":
                if not self._consume_csrf_token(token, "scheduled-reports", t):
                    return True
                self.app.delete_scheduled_report((data.get("name") or [""])[0])
                self._redirect_dashboard(anchor="generated-reports", language=t.language)
                return True
            if action.startswith("annotation-"):
                if not self._consume_csrf_token(token, "event-annotations", t):
                    return True
                if action == "annotation-add":
                    start = self._parse_local_datetime((data.get("start_local") or [""])[0])
                    end = self._parse_local_datetime((data.get("end_local") or [""])[0], fallback=start)
                    self.app.store.add_event_annotation(
                        start_timestamp_utc=start,
                        end_timestamp_utc=end,
                        category=(data.get("category") or ["other"])[0],
                        status=(data.get("status") or ["note"])[0],
                        note=(data.get("note") or [""])[0],
                        device_serial=(data.get("device_serial") or [""])[0] or None,
                    )
                elif action == "annotation-status":
                    self.app.store.update_event_annotation_status(
                        int((data.get("annotation_id") or ["0"])[0]),
                        (data.get("status") or ["note"])[0],
                    )
                else:
                    self.app.store.delete_event_annotation(int((data.get("annotation_id") or ["0"])[0]))
                self._redirect_dashboard(anchor="workflow", language=t.language)
                return True
            if not self._consume_csrf_token(token, "managed-backups", t):
                return True
            if action == "managed-backup-create":
                settings = load_workflow_settings(self.app.store)
                self.app.backup_manager.create(label="manual")
                self.app.backup_manager.prune(settings.managed_backup_retention)
            else:
                self.app.backup_manager.delete((data.get("name") or [""])[0])
            self._redirect_dashboard(anchor="maintenance", language=t.language)
            return True
        except (ValueError, OSError, sqlite3.Error) as exc:
            LOG.warning("Workflow action %s rejected: %s", action, exc)
            self._send_error(HTTPStatus.BAD_REQUEST, _localized_exception_message(t, exc))
            return True

    def _handle_calibration_action(self, action: str | None, t: Translator) -> bool:
        if action != "save-calibration-profile":
            return False
        try:
            data = self._read_urlencoded_form()
            token = (data.get("calibration_csrf_token") or [""])[0]
            if not self._consume_csrf_token(token, "calibration-profiles", t):
                return True
            persist_calibration_profile(self.app.store, data, translate=t)
            self._redirect_dashboard(anchor="calibration-management", language=t.language)
        except (ValueError, OSError, sqlite3.Error) as exc:
            LOG.warning("Calibration profile action rejected: %s", exc)
            self._send_error(HTTPStatus.BAD_REQUEST, _localized_exception_message(t, exc))
        return True

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        query = parse_qs(parsed.query, keep_blank_values=False)
        t = self._request_translator(query)
        if not self._validate_unsafe_request(t):
            return
        if path == "/api/v1/config-validation":
            try:
                content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
                if content_type != "application/json":
                    raise ValueError(t("Candidate configuration must be sent as JSON"))
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > 256 * 1024:
                    raise ValueError(t("Candidate configuration is empty or too large"))
                candidate = json.loads(self.rfile.read(length).decode("utf-8"))
                problems = validate_candidate_options(candidate)
                payload = json.dumps(
                    {"valid": not problems, "problems": problems}, separators=(",", ":"), sort_keys=True
                ).encode("utf-8")
                self._send_bytes(HTTPStatus.OK, "application/json; charset=utf-8", payload)
            except (ValueError, json.JSONDecodeError) as exc:
                self._send_error(HTTPStatus.BAD_REQUEST, _localized_exception_message(t, exc))
            return
        action = _optional_one(query, "action")
        if path == "/" and self._handle_calibration_action(action, t):
            return
        if path == "/" and self._handle_workflow_action(action, t):
            return
        is_purge = path == "/purge-all-history" or (path == "/" and action == "purge-all-history")
        if is_purge:
            self._handle_purge_all_history(t)
            return
        is_restore_preview = path == "/restore-preview" or (path == "/" and action == "restore-preview")
        if is_restore_preview:
            self._handle_restore_preview(t)
            return
        if path != "/restore" and not (path == "/" and action == "restore"):
            self._send_error(HTTPStatus.NOT_FOUND, t("Not found"))
            return
        if not self.app.restore_enabled:
            self._send_error(
                HTTPStatus.FORBIDDEN,
                t(
                    "History restore is disabled. Enable “{setting}” in the app configuration and restart.",
                    setting=t("Allow restore"),
                ),
            )
            return
        backup_path: Path | None = None
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > MAX_RESTORE_BYTES:
                raise ValueError(t("Restore upload must be between 1 byte and 128 MiB"))
            content_type = self.headers.get("Content-Type", "")
            confirm, csrf_token, backup_path = _stream_restore_upload_to_temp(
                content_type,
                self.rfile,
                content_length=content_length,
            )
            if not self._consume_csrf_token(csrf_token, "restore", t):
                return
            if confirm != "RESTORE":
                raise ValueError(t("Restore confirmation text must be exactly RESTORE"))
            if not self.app.report_slot.acquire(blocking=False):
                self._send_error(HTTPStatus.TOO_MANY_REQUESTS, t("Another report or restore job is running"))
                return
            try:
                result = self.app.store.restore_backup_path(backup_path)
                self.app.analysis_cache.clear()
            finally:
                self.app.report_slot.release()
            payload = (
                f"<!doctype html><meta charset=utf-8><title>{html.escape(t('Restore complete'))}</title>"
                f"<h1>{html.escape(t('Restore complete'))}</h1>"
                f"<p>{html.escape(t('Merged {rows} measurement rows from schema {schema}.', rows=int(result['rows_merged']), schema=int(result['source_schema_version'])))}</p>"
                f'<p><a href="./?mode=advanced&amp;lang={t.language}">{html.escape(t("Return to GMC Radiation Monitoring"))}</a></p>'
            ).encode()
            self._send_bytes(HTTPStatus.OK, "text/html; charset=utf-8", payload)
        except (ValueError, OSError, sqlite3.Error) as exc:
            LOG.warning("History restore rejected: %s", exc)
            self._send_error(HTTPStatus.BAD_REQUEST, _localized_exception_message(t, exc))
        except Exception as exc:
            LOG.exception("History restore failed: %s", exc)
            self._send_error(HTTPStatus.INTERNAL_SERVER_ERROR, t("History restore failed"))
        finally:
            if backup_path is not None:
                backup_path.unlink(missing_ok=True)

    def _handle_restore_preview(self, t: Translator) -> None:
        if not self.app.restore_enabled:
            self._send_error(
                HTTPStatus.FORBIDDEN,
                t(
                    "History restore is disabled. Enable “{setting}” in the app configuration and restart.",
                    setting=t("Allow restore"),
                ),
                close_connection=True,
            )
            return
        backup_path: Path | None = None
        token_consumed = False
        try:
            content_length = int(self.headers.get("Content-Length", "0"))
            if content_length <= 0 or content_length > MAX_RESTORE_BYTES:
                raise ValueError(t("Restore upload must be between 1 byte and 128 MiB"))
            _confirm, csrf_token, backup_path = _stream_restore_upload_to_temp(
                self.headers.get("Content-Type", ""),
                self.rfile,
                content_length=content_length,
                csrf_field="preview_csrf_token",
                require_confirm=False,
            )
            if not self._consume_csrf_token(csrf_token, "restore-preview", t):
                return
            token_consumed = True
            if not self.app.report_slot.acquire(blocking=False):
                self._send_error(
                    HTTPStatus.TOO_MANY_REQUESTS,
                    t("Another report or restore job is running"),
                    close_connection=True,
                )
                return
            try:
                preview = self.app.store.inspect_backup_path(backup_path)
            finally:
                self.app.report_slot.release()
            preview["next_csrf_token"] = self.app.csrf_tokens.issue("restore-preview")
            payload = json.dumps(preview, separators=(",", ":"), sort_keys=True).encode("utf-8")
            self._send_bytes(HTTPStatus.OK, "application/json; charset=utf-8", payload)
        except (ValueError, OSError, sqlite3.Error) as exc:
            LOG.warning("History restore preview rejected: %s", exc)
            error_payload = {"error": _localized_exception_message(t, exc)}
            if token_consumed:
                error_payload["next_csrf_token"] = self.app.csrf_tokens.issue("restore-preview")
            payload = json.dumps(error_payload).encode("utf-8")
            self._send_bytes(HTTPStatus.BAD_REQUEST, "application/json; charset=utf-8", payload)
        except Exception as exc:
            LOG.exception("History restore preview failed: %s", exc)
            payload = json.dumps({"error": t("Backup preview failed")}).encode("utf-8")
            self._send_bytes(HTTPStatus.INTERNAL_SERVER_ERROR, "application/json; charset=utf-8", payload)
        finally:
            if backup_path is not None:
                backup_path.unlink(missing_ok=True)

    def _handle_purge_all_history(self, t: Translator) -> None:
        if not self.app.purge_all_history_enabled:
            self._send_error(
                HTTPStatus.FORBIDDEN,
                t("Complete history deletion is disabled in the app configuration."),
                close_connection=True,
            )
            return
        try:
            content_type = self.headers.get("Content-Type", "").split(";", 1)[0].strip().lower()
            if content_type != "application/x-www-form-urlencoded":
                raise ValueError(t("Invalid deletion confirmation"))
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 4096:
                raise ValueError(t("Invalid deletion confirmation"))
            data = parse_qs(self.rfile.read(length).decode("utf-8"), keep_blank_values=True)
            csrf_token = (data.get("csrf_token") or [""])[0]
            if not self._consume_csrf_token(csrf_token, "purge-all-history", t):
                return
            if (data.get("confirm") or [""])[0].strip() != "DELETE ALL GMC HISTORY":
                raise ValueError(t("Deletion confirmation text must be exactly DELETE ALL GMC HISTORY"))
            if not self.app.report_slot.acquire(blocking=False):
                self._send_error(
                    HTTPStatus.TOO_MANY_REQUESTS,
                    t("Another report or maintenance job is running"),
                )
                return
            try:
                serials = [str(item.get("serial") or "").strip() for item in self.app.store.list_devices()]
                globs = [f"sensor.gmc_{slugify(serial)}_*" for serial in serials if serial]
                if self.app.home_assistant_client is None:
                    raise OSError(t("Home Assistant API client is not configured"))
                recorder_result = self.app.home_assistant_client.purge_recorder_entity_globs(globs, serials)
                result = self.app.store.purge_all_history()
                self.app.analysis_cache.clear()
            finally:
                self.app.report_slot.release()
            entity_count = len(recorder_result.get("entity_ids", []))
            statistic_count = len(recorder_result.get("statistic_ids", []))
            payload = (
                f"<!doctype html><meta charset=utf-8><title>{html.escape(t('History deleted'))}</title>"
                f"<h1>{html.escape(t('All GMC history was deleted'))}</h1>"
                f"<ul>"
                f"<li>✓ {html.escape(t('Internal database cleared'))}: {int(result['measurements']):,} {html.escape(t('measurements'))}</li>"
                f"<li>✓ {html.escape(t('Raw-data archive'))}: {int(result.get('raw_measurements', 0)):,}</li>"
                f"<li>✓ {html.escape(t('Operational events cleared'))}: {int(result['events']):,}</li>"
                f"<li>✓ {html.escape(t('Ingest diagnostics cleared'))}: {int(result['diagnostics']):,}</li>"
                f"<li>✓ {html.escape(t('Home Assistant Recorder history cleared'))}: {entity_count} exact Home Assistant entities</li>"
                f"<li>✓ Home Assistant long-term statistics cleared: {statistic_count}</li>"
                f"<li>✓ {html.escape(t('SQLite database vacuum completed'))}</li>"
                f"<li>✓ {html.escape(t('Ready for new measurements'))}</li>"
                f"</ul>"
                f'<p><a href="./?mode=advanced&amp;lang={t.language}">{html.escape(t("Return to GMC Radiation Monitoring"))}</a></p>'
            ).encode()
            self._send_bytes(HTTPStatus.OK, "text/html; charset=utf-8", payload)
        except (ValueError, OSError, HTTPError, URLError) as exc:
            LOG.warning("Complete history purge rejected: %s", exc)
            self._send_error(HTTPStatus.BAD_REQUEST, _localized_exception_message(t, exc))
        except Exception as exc:
            LOG.exception("Complete history purge failed: %s", exc)
            self._send_error(HTTPStatus.INTERNAL_SERVER_ERROR, t("Complete history deletion failed"))

    def _handle_download(self, query: dict[str, list[str]]) -> None:
        t = self._request_translator(query)
        language = t.language
        period_kind = _one(query, "period")
        selection = _one(query, "selection")
        output_format = _one(query, "format")
        allowed_formats = {
            "png",
            "csv",
            "raw-archive-csv",
            "zip",
            "analysis-json",
            "daily-summary-csv",
            "events-csv",
            "histogram-png",
            "heatmap-png",
            "pdf",
        }
        if output_format not in allowed_formats:
            raise ValueError(t("Unsupported report format"))
        device_serial = _one(query, "device").strip()
        known_serials = {
            str(item.get("serial"))
            for item in self.app.store.list_devices()
            if str(item.get("serial") or "").strip()
        }
        if not device_serial or device_serial not in known_serials:
            raise ValueError(t("Unknown report device"))
        all_devices = False
        data_mode = _optional_one(query, "data_mode") or "raw"
        if data_mode not in {"raw", "corrected", "comparison"}:
            raise ValueError(t("Unsupported data mode"))
        scientific_page = str(_optional_one(query, "scientific") or "").strip().lower() in {"1", "true", "yes", "on"}
        period = resolve_period(
            kind=period_kind,
            selection=selection,
            tz=self.app.timezone,
            date_value=_optional_one(query, "date"),
            week_value=_optional_one(query, "week"),
        )
        if not self.app.report_slot.acquire(blocking=False):
            self._send_error(HTTPStatus.TOO_MANY_REQUESTS, t("Another report is already being generated"))
            return
        temp_path = _temporary_path(prefix="gmc-report-", suffix=f".{output_format}")
        try:
            try:
                report_scan_interval, report_cpm_per_usvh = self.app._device_report_settings(
                    None if all_devices else device_serial
                )
                filename, content_type, _output_path = build_report_to_path(
                    self.app.store,
                    temp_path,
                    period=period,
                    timezone_name=self.app.timezone_name,
                    scan_interval_seconds=report_scan_interval,
                    output_format=output_format,
                    cpm_per_usvh=report_cpm_per_usvh,
                    traffic_light_yellow_percent=self.app.traffic_light_yellow_percent,
                    traffic_light_red_percent=self.app.traffic_light_red_percent,
                    device_serial=device_serial,
                    all_devices=all_devices,
                    language=language,
                    data_mode=data_mode,
                    scientific_page=scientific_page,
                )
                if temp_path.stat().st_size > MAX_DOWNLOAD_BYTES:
                    raise ValueError(t("Generated report exceeds the 64 MiB safety limit"))
            finally:
                self.app.report_slot.release()
            self._send_file_attachment(
                filename,
                content_type,
                temp_path,
                max_bytes=MAX_DOWNLOAD_BYTES,
                t=t,
            )
        finally:
            temp_path.unlink(missing_ok=True)

    def _handle_maintenance_file_download(
        self,
        filename: str,
        content_type: str,
        builder: Any,
        *,
        suffix: str,
        t: Translator,
    ) -> None:
        if not self.app.report_slot.acquire(blocking=False):
            self._send_error(
                HTTPStatus.TOO_MANY_REQUESTS,
                t("Another report, maintenance export, or restore job is running"),
            )
            return
        temp_path = _temporary_path(prefix="gmc-maintenance-", suffix=suffix)
        try:
            try:
                builder(temp_path)
            finally:
                self.app.report_slot.release()
            self._send_file_attachment(
                filename,
                content_type,
                temp_path,
                max_bytes=MAX_RESTORE_BYTES,
                t=t,
            )
        finally:
            temp_path.unlink(missing_ok=True)

    def _handle_maintenance_bytes_download(
        self,
        filename: str,
        content_type: str,
        builder: Any,
        *,
        t: Translator,
    ) -> None:
        if not self.app.report_slot.acquire(blocking=False):
            self._send_error(
                HTTPStatus.TOO_MANY_REQUESTS,
                t("Another report, maintenance export, or restore job is running"),
            )
            return
        try:
            payload = builder()
        finally:
            self.app.report_slot.release()
        if len(payload) > MAX_RESTORE_BYTES:
            raise ValueError(t("Generated maintenance export exceeds the 128 MiB safety limit"))
        self._send_attachment_bytes(filename, content_type, payload)

    def _send_attachment_bytes(self, filename: str, content_type: str, payload: bytes) -> None:
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Content-Security-Policy", "default-src 'none'; sandbox")
        self.end_headers()
        for offset in range(0, len(payload), STREAM_CHUNK_BYTES):
            self.wfile.write(payload[offset : offset + STREAM_CHUNK_BYTES])

    def _send_file_inline(
        self,
        filename: str,
        content_type: str,
        path: Path,
        *,
        max_bytes: int,
        t: Translator,
    ) -> None:
        size = path.stat().st_size
        if size > max_bytes:
            limit_mib = max_bytes // (1024 * 1024)
            raise ValueError(
                t("Generated export exceeds the {limit_mib} MiB safety limit", limit_mib=limit_mib)
            )
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(size))
        self.send_header("Content-Disposition", f'inline; filename="{filename}"')
        self.send_header("Cache-Control", "public, max-age=3600")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Cross-Origin-Resource-Policy", "same-origin")
        self.end_headers()
        with path.open("rb") as handle:
            while chunk := handle.read(STREAM_CHUNK_BYTES):
                self.wfile.write(chunk)

    def _send_file_attachment(
        self,
        filename: str,
        content_type: str,
        path: Path,
        *,
        max_bytes: int,
        t: Translator,
    ) -> None:
        size = path.stat().st_size
        if size > max_bytes:
            limit_mib = max_bytes // (1024 * 1024)
            raise ValueError(
                t("Generated export exceeds the {limit_mib} MiB safety limit", limit_mib=limit_mib)
            )
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(size))
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        self.send_header("Content-Security-Policy", "default-src 'none'; sandbox")
        self.end_headers()
        with path.open("rb") as handle:
            while chunk := handle.read(STREAM_CHUNK_BYTES):
                self.wfile.write(chunk)

    def _send_bytes(
        self,
        status: HTTPStatus,
        content_type: str,
        payload: bytes,
        *,
        close_connection: bool = False,
    ) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        self.send_header("Permissions-Policy", "camera=(), microphone=(), geolocation=()")
        script_nonce_match = (
            re.search(rb'<script nonce="([A-Za-z0-9_-]+)"', payload)
            if content_type.startswith("text/html")
            else None
        )
        script_policy = (
            f"; script-src 'nonce-{script_nonce_match.group(1).decode('ascii')}'"
            if script_nonce_match
            else ""
        )
        self.send_header(
            "Content-Security-Policy",
            "default-src 'none'; style-src 'unsafe-inline'; form-action 'self'; connect-src 'self'"
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


def _localized_exception_message(t: Translator, exc: BaseException) -> str:
    """Return a localized, user-safe message while preserving full details in logs."""
    message = str(exc).strip()
    translated = t(message)
    if translated != message:
        return translated
    prefix_templates = (
        ("Unknown IANA timezone: ", "Unknown IANA timezone: {value}"),
        ("Unsupported daily selection: ", "Unsupported daily selection: {value}"),
        ("Unsupported weekly selection: ", "Unsupported weekly selection: {value}"),
        ("Unsupported report period: ", "Unsupported report period: {value}"),
        ("Unsupported report format: ", "Unsupported report format: {value}"),
    )
    for prefix, template in prefix_templates:
        if message.startswith(prefix):
            return t(template, value=message[len(prefix) :])
    if message.startswith("Exactly one ") or message.startswith("At most one "):
        return t("Invalid request parameters")
    return t("The request could not be processed. Check the selected options.")
