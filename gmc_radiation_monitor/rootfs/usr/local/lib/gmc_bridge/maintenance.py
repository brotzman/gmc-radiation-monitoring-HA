from __future__ import annotations

import csv
import io
import json
import os
import sqlite3
import tempfile
import zipfile
from collections.abc import Iterable
from contextlib import closing, suppress
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .file_security import secure_file
from .history import HistoryRow, HistoryStore, metadata_json_bytes

CSV_HEADER = [
    "device_serial",
    "timestamp_utc",
    "cpm",
    "temperature_c",
    "voltage_v",
    "gyro_x",
    "gyro_y",
    "gyro_z",
    "cpm_quality",
]

RAW_CSV_HEADER = [
    "raw_id", "device_serial", "timestamp_utc", "cpm", "tube_low_cpm",
    "tube_high_cpm", "temperature_c", "voltage_v", "gyro_x", "gyro_y",
    "gyro_z", "gate_state", "accepted", "raw_json",
]


def _row_value(row: HistoryRow | sqlite3.Row, name: str) -> Any:
    if isinstance(row, sqlite3.Row):
        return row[name]
    return getattr(row, name)


def _csv_values(row: HistoryRow | sqlite3.Row) -> list[Any]:
    timestamp_utc = int(_row_value(row, "timestamp_utc"))
    temperature_c = _row_value(row, "temperature_c")
    voltage_v = _row_value(row, "voltage_v")
    gyro_x = _row_value(row, "gyro_x")
    gyro_y = _row_value(row, "gyro_y")
    gyro_z = _row_value(row, "gyro_z")
    return [
        _row_value(row, "device_serial"),
        datetime.fromtimestamp(timestamp_utc, UTC)
        .isoformat(timespec="seconds")
        .replace("+00:00", "Z"),
        _row_value(row, "cpm"),
        "" if temperature_c is None else temperature_c,
        "" if voltage_v is None else voltage_v,
        "" if gyro_x is None else gyro_x,
        "" if gyro_y is None else gyro_y,
        "" if gyro_z is None else gyro_z,
        _row_value(row, "cpm_quality"),
    ]


def _write_csv_rows(text_stream: Any, rows: Iterable[HistoryRow | sqlite3.Row]) -> None:
    writer = csv.writer(text_stream, lineterminator="\n")
    writer.writerow(CSV_HEADER)
    for row in rows:
        writer.writerow(_csv_values(row))


def full_history_csv_bytes(rows: list[HistoryRow]) -> bytes:
    output = io.StringIO(newline="")
    _write_csv_rows(output, rows)
    return output.getvalue().encode("utf-8")


def _iter_backup_rows(backup_path: Path, *, batch_size: int = 2000) -> Iterable[sqlite3.Row]:
    with closing(sqlite3.connect(f"file:{backup_path}?mode=ro", uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        cursor = connection.execute(
            """
            SELECT device_serial, timestamp_utc, cpm, temperature_c, voltage_v,
                   gyro_x, gyro_y, gyro_z, cpm_quality
            FROM measurements ORDER BY device_serial, timestamp_utc ASC
            """
        )
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield from batch


def _iter_backup_raw_rows(backup_path: Path, *, batch_size: int = 2000) -> Iterable[sqlite3.Row]:
    with closing(sqlite3.connect(f"file:{backup_path}?mode=ro", uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        tables = {str(row[0]) for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        ).fetchall()}
        if "raw_measurements" not in tables:
            return
        cursor = connection.execute(
            """
            SELECT id, device_serial, timestamp_utc, cpm, tube_low_cpm, tube_high_cpm,
                   temperature_c, voltage_v, gyro_x, gyro_y, gyro_z, gate_state, accepted, raw_json
            FROM raw_measurements ORDER BY device_serial, timestamp_utc, id
            """
        )
        while True:
            batch = cursor.fetchmany(batch_size)
            if not batch:
                break
            yield from batch


def _write_raw_csv_rows(text_stream: Any, rows: Iterable[sqlite3.Row]) -> None:
    writer = csv.writer(text_stream, lineterminator="\n")
    writer.writerow(RAW_CSV_HEADER)
    for row in rows:
        writer.writerow([
            row["id"],
            row["device_serial"],
            datetime.fromtimestamp(int(row["timestamp_utc"]), UTC).isoformat(timespec="seconds").replace("+00:00", "Z"),
            row["cpm"],
            "" if row["tube_low_cpm"] is None else row["tube_low_cpm"],
            "" if row["tube_high_cpm"] is None else row["tube_high_cpm"],
            "" if row["temperature_c"] is None else row["temperature_c"],
            "" if row["voltage_v"] is None else row["voltage_v"],
            "" if row["gyro_x"] is None else row["gyro_x"],
            "" if row["gyro_y"] is None else row["gyro_y"],
            "" if row["gyro_z"] is None else row["gyro_z"],
            row["gate_state"],
            row["accepted"],
            row["raw_json"],
        ])


def full_history_zip_to_path(store: HistoryStore, destination_path: str | Path) -> Path:
    """Build the full-history archive on disk and stream CSV rows into the ZIP."""
    destination_path = Path(destination_path)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(prefix="gmc-history-export-", suffix=".sqlite3")
    os.close(fd)
    backup_path = Path(temp_name)
    try:
        store.backup_to_path(backup_path)
        with zipfile.ZipFile(
            destination_path,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            allowZip64=True,
        ) as archive:
            archive.write(backup_path, arcname="gmc_history.sqlite3")
            raw_csv = archive.open("gmc_history.csv", mode="w", force_zip64=True)
            text_csv = io.TextIOWrapper(raw_csv, encoding="utf-8", newline="")
            try:
                _write_csv_rows(text_csv, _iter_backup_rows(backup_path))
                text_csv.flush()
            finally:
                with suppress(Exception):
                    text_csv.detach()
                raw_csv.close()
            raw_archive = archive.open("gmc_raw_history.csv", mode="w", force_zip64=True)
            raw_text = io.TextIOWrapper(raw_archive, encoding="utf-8", newline="")
            try:
                _write_raw_csv_rows(raw_text, _iter_backup_raw_rows(backup_path))
                raw_text.flush()
            finally:
                with suppress(Exception):
                    raw_text.detach()
                raw_archive.close()
            archive.writestr("gmc_history.metadata.json", metadata_json_bytes(store))
        secure_file(destination_path)
        return destination_path
    finally:
        with suppress(OSError):
            backup_path.unlink()


def full_history_zip_bytes(store: HistoryStore) -> bytes:
    fd, temp_name = tempfile.mkstemp(prefix="gmc-history-export-", suffix=".zip")
    os.close(fd)
    temp_path = Path(temp_name)
    try:
        full_history_zip_to_path(store, temp_path)
        return temp_path.read_bytes()
    finally:
        with suppress(OSError):
            temp_path.unlink()


def diagnostics_document(store: HistoryStore) -> dict[str, Any]:
    metadata = store.get_metadata()
    return {
        "app_version": metadata.get("app_version", "unknown"),
        "device": {
            "model": metadata.get("device_model", "unknown"),
            "serial": metadata.get("serial", "unknown"),
            "profile": metadata.get("device_profile", "unknown"),
            "capabilities": store.get_device_capabilities(),
        },
        "database": store.database_stats(),
        "ingest_diagnostics": store.get_ingest_diagnostics(),
        "runtime": {
            key: value
            for key, value in metadata.items()
            if key.endswith("_count") or key in {"app_started_at", "last_successful_measurement"}
        },
        "privacy_note": "No MQTT password or broker credentials are included.",
    }


def diagnostics_json_bytes(store: HistoryStore) -> bytes:
    return json.dumps(diagnostics_document(store), indent=2, sort_keys=True).encode("utf-8") + b"\n"
