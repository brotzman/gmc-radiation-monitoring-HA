from __future__ import annotations

import mmap
import os
import tempfile
from email.message import Message
from pathlib import Path
from typing import BinaryIO

from .version import APP_VERSION

MAX_DOWNLOAD_BYTES = 64 * 1024 * 1024
MAX_RESTORE_BYTES = 128 * 1024 * 1024
STREAM_CHUNK_BYTES = 1024 * 1024
MULTIPART_HEADER_LIMIT = 64 * 1024
REPORT_TARGET_COMBINED = "combined"
REPORT_TARGET_DEVICE_PREFIX = "device:"
USER_MANUAL_DIRECTORY = (
    Path(__file__).resolve().parents[2]
    / "share"
    / "gmc-bridge"
    / "docs"
)
USER_MANUAL_FILENAMES = {
    "de": f"GMC_Radiation_Monitor_Benutzerhandbuch_{APP_VERSION}.pdf",
    "en": f"GMC_Radiation_Monitor_User_Manual_{APP_VERSION}_en.pdf",
    "es": f"GMC_Radiation_Monitor_User_Manual_{APP_VERSION}_es.pdf",
    "fr": f"GMC_Radiation_Monitor_User_Manual_{APP_VERSION}_fr.pdf",
    "it": f"GMC_Radiation_Monitor_User_Manual_{APP_VERSION}_it.pdf",
    "nl": f"GMC_Radiation_Monitor_User_Manual_{APP_VERSION}_nl.pdf",
    "pl": f"GMC_Radiation_Monitor_User_Manual_{APP_VERSION}_pl.pdf",
    "hr": f"GMC_Radiation_Monitor_User_Manual_{APP_VERSION}_hr.pdf",
}
USER_MANUAL_LANGUAGE_NAMES = {
    "de": "Deutsch",
    "en": "English",
    "es": "Español",
    "fr": "Français",
    "it": "Italiano",
    "nl": "Nederlands",
    "pl": "Polski",
    "hr": "Hrvatski",
}
# Backwards-compatible German aliases used by existing integrations and tests.
USER_MANUAL_FILENAME = USER_MANUAL_FILENAMES["de"]
USER_MANUAL_PATH = USER_MANUAL_DIRECTORY / USER_MANUAL_FILENAME


def _resolve_user_manual(language: str) -> tuple[str, str, Path]:
    selected = language if language in USER_MANUAL_FILENAMES else "en"
    filename = USER_MANUAL_FILENAMES[selected]
    path = USER_MANUAL_DIRECTORY / filename
    if not path.is_file() and selected != "de":
        selected = "de"
        filename = USER_MANUAL_FILENAMES[selected]
        path = USER_MANUAL_DIRECTORY / filename
    return selected, filename, path


def _encode_report_target(device_serial: str | None = None, *, combined: bool = False) -> str:
    if combined:
        return REPORT_TARGET_COMBINED
    serial = str(device_serial or "").strip()
    if not serial:
        raise ValueError("A device serial is required for an individual report target")
    return REPORT_TARGET_DEVICE_PREFIX + serial


def _decode_report_target(value: str, known_serials: set[str]) -> tuple[bool, str | None]:
    """Return (all_devices, device_serial) for an explicit report target.

    Downloads never silently fall back to a combined report. Legacy values are
    accepted only when they identify an explicit target.
    """
    target = str(value or "").strip()
    if target in {REPORT_TARGET_COMBINED, "all"}:
        return True, None
    serial = target[len(REPORT_TARGET_DEVICE_PREFIX):] if target.startswith(REPORT_TARGET_DEVICE_PREFIX) else target
    if not serial or serial not in known_serials:
        raise ValueError("Unknown or missing report device")
    return False, serial


def _temporary_path(*, prefix: str, suffix: str) -> Path:
    fd, temp_name = tempfile.mkstemp(prefix=prefix, suffix=suffix)
    os.close(fd)
    return Path(temp_name)


def _stream_request_to_path(stream: BinaryIO, destination: Path, *, content_length: int) -> None:
    remaining = content_length
    with destination.open("wb") as output:
        while remaining:
            chunk = stream.read(min(STREAM_CHUNK_BYTES, remaining))
            if not chunk:
                raise ValueError("Restore upload ended before Content-Length bytes were received")
            output.write(chunk)
            remaining -= len(chunk)


def _multipart_ranges(content_type: str, source_path: Path) -> dict[str, tuple[int, int]]:
    message = Message()
    message["content-type"] = content_type
    if message.get_content_type() != "multipart/form-data":
        raise ValueError("Restore requires multipart/form-data")
    boundary = message.get_param("boundary")
    if not isinstance(boundary, str) or not boundary:
        raise ValueError("Multipart boundary is missing")
    try:
        delimiter = b"--" + boundary.encode("ascii", errors="strict")
    except UnicodeEncodeError as exc:
        raise ValueError("Multipart boundary must be ASCII") from exc

    fields: dict[str, tuple[int, int]] = {}
    with source_path.open("rb") as handle, mmap.mmap(handle.fileno(), 0, access=mmap.ACCESS_READ) as mapped:
        if len(mapped) < len(delimiter) or mapped[: len(delimiter)] != delimiter:
            raise ValueError("Malformed multipart upload")
        position = 0
        while True:
            if mapped[position : position + len(delimiter)] != delimiter:
                raise ValueError("Malformed multipart boundary")
            position += len(delimiter)
            if mapped[position : position + 2] == b"--":
                break
            if mapped[position : position + 2] != b"\r\n":
                raise ValueError("Malformed multipart delimiter")
            header_start = position + 2
            header_end = mapped.find(b"\r\n\r\n", header_start)
            if header_end < 0 or header_end - header_start > MULTIPART_HEADER_LIMIT:
                raise ValueError("Malformed or oversized multipart headers")
            payload_start = header_end + 4
            next_boundary = mapped.find(b"\r\n" + delimiter, payload_start)
            if next_boundary < 0:
                raise ValueError("Multipart closing boundary is missing")

            headers: dict[str, str] = {}
            header_blob = mapped[header_start:header_end].decode("utf-8", errors="replace")
            for line in header_blob.split("\r\n"):
                key, separator, value = line.partition(":")
                if separator:
                    headers[key.strip().lower()] = value.strip()
            disposition_message = Message()
            disposition_message["content-disposition"] = headers.get("content-disposition", "")
            name = disposition_message.get_param("name", header="content-disposition")
            if name:
                fields[str(name)] = (payload_start, next_boundary)
            position = next_boundary + 2
    return fields


def _copy_file_range(source_path: Path, destination_path: Path, *, start: int, end: int) -> None:
    if end <= start:
        raise ValueError("No SQLite backup file was uploaded")
    with source_path.open("rb") as source, destination_path.open("wb") as destination:
        source.seek(start)
        remaining = end - start
        while remaining:
            chunk = source.read(min(STREAM_CHUNK_BYTES, remaining))
            if not chunk:
                raise ValueError("Restore upload could not be read completely")
            destination.write(chunk)
            remaining -= len(chunk)


def _stream_restore_upload_to_temp(
    content_type: str,
    stream: BinaryIO,
    *,
    content_length: int,
    csrf_field: str = "csrf_token",
    require_confirm: bool = True,
) -> tuple[str, str, Path]:
    multipart_path = _temporary_path(prefix="gmc-restore-upload-", suffix=".multipart")
    backup_path = _temporary_path(prefix="gmc-restore-", suffix=".sqlite3")
    try:
        _stream_request_to_path(stream, multipart_path, content_length=content_length)
        fields = _multipart_ranges(content_type, multipart_path)
        confirm_range = fields.get("confirm")
        csrf_range = fields.get(csrf_field)
        backup_range = fields.get("backup")
        if require_confirm and confirm_range is None:
            raise ValueError("Restore confirmation field is missing")
        if confirm_range is not None and confirm_range[1] - confirm_range[0] > 64:
            raise ValueError("Restore confirmation field is too large")
        confirm = ""
        if confirm_range is not None:
            with multipart_path.open("rb") as handle:
                handle.seek(confirm_range[0])
                confirm = handle.read(confirm_range[1] - confirm_range[0]).decode(
                    "utf-8", errors="replace"
                ).strip()
        if csrf_range is None:
            raise ValueError("Restore form token is missing")
        if csrf_range[1] - csrf_range[0] > 256:
            raise ValueError("Restore form token is too large")
        with multipart_path.open("rb") as handle:
            handle.seek(csrf_range[0])
            csrf_token = handle.read(csrf_range[1] - csrf_range[0]).decode(
                "ascii", errors="strict"
            ).strip()
        if backup_range is None:
            raise ValueError("No SQLite backup file was uploaded")
        _copy_file_range(
            multipart_path,
            backup_path,
            start=backup_range[0],
            end=backup_range[1],
        )
        return confirm, csrf_token, backup_path
    except Exception:
        backup_path.unlink(missing_ok=True)
        raise
    finally:
        multipart_path.unlink(missing_ok=True)


def _parse_multipart_form(content_type: str, body: bytes) -> dict[str, bytes]:
    message = Message()
    message["content-type"] = content_type
    if message.get_content_type() != "multipart/form-data":
        raise ValueError("Restore requires multipart/form-data")
    boundary = message.get_param("boundary")
    if not isinstance(boundary, str) or not boundary:
        raise ValueError("Multipart boundary is missing")
    delimiter = b"--" + boundary.encode("ascii", errors="strict")
    fields: dict[str, bytes] = {}
    for raw_part in body.split(delimiter):
        part = raw_part.strip(b"\r\n")
        if not part or part == b"--":
            continue
        if part.endswith(b"--"):
            part = part[:-2].rstrip(b"\r\n")
        header_blob, separator, payload = part.partition(b"\r\n\r\n")
        if not separator:
            continue
        headers: dict[str, str] = {}
        for line in header_blob.decode("utf-8", errors="replace").split("\r\n"):
            key, sep, value = line.partition(":")
            if sep:
                headers[key.strip().lower()] = value.strip()
        disposition = headers.get("content-disposition", "")
        disposition_message = Message()
        disposition_message["content-disposition"] = disposition
        name = disposition_message.get_param("name", header="content-disposition")
        if name:
            fields[str(name)] = payload.rstrip(b"\r\n")
    return fields


def _one(query: dict[str, list[str]], key: str) -> str:
    values = query.get(key)
    if not values or len(values) != 1:
        raise ValueError(f"Exactly one {key} parameter is required")
    return values[0]


def _optional_one(query: dict[str, list[str]], key: str) -> str | None:
    values = query.get(key)
    if values is None:
        return None
    if len(values) != 1:
        raise ValueError(f"At most one {key} parameter is allowed")
    return values[0]
