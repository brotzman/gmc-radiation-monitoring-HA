from __future__ import annotations

import fcntl
import json
import logging
import os
import sqlite3
import statistics
import tempfile
import threading
import time
from collections import deque
from collections.abc import Iterable, Iterator
from contextlib import closing, contextmanager, suppress
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from .file_security import secure_file, secure_sqlite_family
from .migrations import SCHEMA_VERSION, apply_migrations

LOG = logging.getLogger("gmc_bridge")
DEFAULT_DB_PATH = Path("/data/gmc_history.sqlite3")


def _coerce_epoch_timestamp(value: Any | None = None) -> int:
    """Return UTC epoch seconds for numeric or ISO-8601 timestamp values."""
    if value is None:
        return int(time.time())
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return int(value)
    text = str(value).strip()
    try:
        return int(text)
    except ValueError:
        try:
            parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError(f"Unsupported UTC timestamp: {value!r}") from exc
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return int(parsed.timestamp())


@dataclass(frozen=True)
class HistoryRow:
    device_serial: str
    timestamp_utc: int
    cpm: int
    temperature_c: float | None
    voltage_v: float | None
    gyro_x: int | None
    gyro_y: int | None
    gyro_z: int | None
    cpm_quality: str
    tube_low_cpm: int | None = None
    tube_high_cpm: int | None = None
    pressure_hpa: float | None = None
    raw_cpm: float | None = None
    corrected_cpm: float | None = None
    detector_type: str | None = None
    dual_tube_mode: str | None = None
    active_tube: str | None = None
    dead_time_model: str | None = None
    dead_time_us: float | None = None
    dead_time_loss_percent: float | None = None
    detector_load_percent: float | None = None
    correction_factor: float | None = None
    calibration_status: str | None = None
    calibration_source: str | None = None
    measurement_quality_index: int | None = None
    dose_quality: str | None = None
    derived_dose_usvh: float | None = None


class HistoryStore:
    """WAL-mode SQLite history store with migrations and safe backup/merge restore."""

    def __init__(
        self,
        path: str | Path = DEFAULT_DB_PATH,
        *,
        retention_days: int = 730,
        busy_timeout_ms: int = 5000,
    ) -> None:
        self.path = Path(path)
        self.retention_days = retention_days
        self.busy_timeout_ms = busy_timeout_ms
        self._lock = threading.RLock()
        self._last_prune_monotonic = 0.0
        self._quick_check_cache_lock = threading.Lock()
        self._quick_check_cache_value: str | None = None
        self._quick_check_cache_monotonic = 0.0
        self.path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        self._initialize()
        secure_sqlite_family(self.path)

    @property
    def lock_path(self) -> Path:
        return self.path.with_suffix(self.path.suffix + ".lock")

    @contextmanager
    def _database_lock(self, *, exclusive: bool) -> Iterator[None]:
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        with self._lock, self.lock_path.open("a+b") as handle:
            secure_file(self.lock_path)
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX if exclusive else fcntl.LOCK_SH)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def _connect(self, *, read_only: bool = False) -> sqlite3.Connection:
        if read_only:
            uri = f"file:{self.path}?mode=ro"
            connection = sqlite3.connect(uri, uri=True, timeout=self.busy_timeout_ms / 1000.0)
        else:
            connection = sqlite3.connect(self.path, timeout=self.busy_timeout_ms / 1000.0)
        connection.row_factory = sqlite3.Row
        connection.execute(f"PRAGMA busy_timeout={self.busy_timeout_ms}")
        if not read_only:
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute("PRAGMA synchronous=NORMAL")
            connection.execute("PRAGMA foreign_keys=ON")
        return connection

    def _initialize(self) -> None:
        with self._database_lock(exclusive=True):
            if self.path.exists() and self.path.stat().st_size > 0:
                with closing(self._connect(read_only=True)) as probe:
                    current = int(probe.execute("PRAGMA user_version").fetchone()[0])
                if current < SCHEMA_VERSION:
                    backup = self.path.with_name(f"{self.path.name}.pre-migration-v{current}.bak")
                    if not backup.exists():
                        with (
                            closing(sqlite3.connect(self.path)) as source,
                            closing(sqlite3.connect(backup)) as target,
                        ):
                            source.backup(target)
                        secure_file(backup)
            with closing(self._connect()) as connection:
                apply_migrations(connection)
                connection.commit()

    def schema_version(self) -> int:
        with closing(self._connect(read_only=True)) as connection:
            return int(connection.execute("PRAGMA user_version").fetchone()[0])

    def set_metadata(self, values: dict[str, Any]) -> None:
        normalized = [(str(key), str(value)) for key, value in values.items()]
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            connection.executemany(
                "INSERT INTO metadata(key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                normalized,
            )
            connection.commit()

    def get_metadata(self) -> dict[str, str]:
        if not self.path.exists():
            return {}
        with closing(self._connect(read_only=True)) as connection:
            rows = connection.execute("SELECT key, value FROM metadata ORDER BY key").fetchall()
        return {str(row[0]): str(row[1]) for row in rows}

    def upsert_device_registry(self, device_serial: str, values: dict[str, Any]) -> None:
        """Persist per-device identity without overwriting the legacy primary metadata."""
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            row = connection.execute("SELECT value FROM metadata WHERE key = 'device_registry'").fetchone()
            try:
                registry = json.loads(str(row[0])) if row else {}
            except (TypeError, ValueError, json.JSONDecodeError):
                registry = {}
            current = dict(registry.get(device_serial, {}))
            current.update({str(key): value for key, value in values.items()})
            current["serial"] = device_serial
            registry[device_serial] = current
            connection.execute(
                "INSERT INTO metadata(key, value) VALUES ('device_registry', ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (json.dumps(registry, sort_keys=True, separators=(",", ":")),),
            )
            primary = connection.execute("SELECT value FROM metadata WHERE key='serial'").fetchone()
            if primary is None:
                pairs = {
                    "serial": device_serial,
                    "device_model": current.get("device_model", "unknown"),
                    "device_profile": current.get("device_profile", "unknown"),
                    "device_profile_name": current.get(
                        "device_profile_name", current.get("device_profile", "unknown")
                    ),
                    "capabilities": current.get("capabilities", "cpm"),
                }
                connection.executemany(
                    "INSERT INTO metadata(key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                    [(key, str(value)) for key, value in pairs.items()],
                )
            connection.commit()

    def reset_device_runtime_states(self, *, reason: str = "service_starting") -> None:
        """Mark all known devices offline before a new bridge process initializes them."""
        timestamp = datetime.now(UTC).isoformat(timespec="seconds").replace("+00:00", "Z")
        for item in self.list_devices():
            serial = str(item.get("serial") or "").strip()
            if not serial:
                continue
            self.upsert_device_registry(
                serial,
                {
                    "runtime_online": False,
                    "runtime_status": "offline",
                    "runtime_status_reason": reason,
                    "runtime_status_updated_utc": timestamp,
                },
            )

    def list_devices(self) -> list[dict[str, Any]]:
        """Return all known devices with identity, capabilities and history statistics."""
        if not self.path.exists():
            return []
        metadata = self.get_metadata()
        try:
            registry = json.loads(metadata.get("device_registry", "{}"))
        except (TypeError, ValueError, json.JSONDecodeError):
            registry = {}
        with closing(self._connect(read_only=True)) as connection:
            latest_rows = connection.execute(
                """
                SELECT m.*
                FROM measurements m
                JOIN (
                    SELECT device_serial, MAX(timestamp_utc) AS timestamp_utc
                    FROM measurements GROUP BY device_serial
                ) latest ON latest.device_serial=m.device_serial AND latest.timestamp_utc=m.timestamp_utc
                ORDER BY m.device_serial
                """
            ).fetchall()
            history_rows = connection.execute(
                """
                SELECT device_serial, COUNT(*) AS stored_samples,
                       MIN(timestamp_utc) AS first_timestamp_utc,
                       MAX(timestamp_utc) AS last_timestamp_utc
                FROM measurements
                GROUP BY device_serial
                """
            ).fetchall()
            capability_rows = connection.execute(
                """
                SELECT device_serial, capability, supported
                FROM device_capabilities
                ORDER BY device_serial, capability
                """
            ).fetchall()
        latest = {str(row["device_serial"]): dict(row) for row in latest_rows}
        history = {str(row["device_serial"]): dict(row) for row in history_rows}
        capabilities: dict[str, dict[str, bool]] = {}
        for row in capability_rows:
            serial = str(row["device_serial"])
            capabilities.setdefault(serial, {})[str(row["capability"])] = bool(row["supported"])
        serials = sorted(set(registry) | set(latest) | set(history) | set(capabilities))
        devices: list[dict[str, Any]] = []
        for serial in serials:
            item = dict(registry.get(serial, {}))
            item.update(history.get(serial, {}))
            # A newly added measurement column can be NULL for legacy rows.  Do not
            # let those NULL values erase the detector metadata already stored in
            # the registry (especially dual-tube mode and calibration profiles).
            item.update(
                {key: value for key, value in latest.get(serial, {}).items() if value is not None}
            )
            item["serial"] = serial
            item["capabilities_map"] = capabilities.get(serial, {})
            devices.append(item)
        return devices

    def set_device_capabilities(
        self,
        device_serial: str,
        capabilities: dict[str, bool],
        *,
        source: str = "runtime_probe",
        detected_at_utc: int | None = None,
    ) -> None:
        timestamp = _coerce_epoch_timestamp(detected_at_utc)
        rows = [
            (device_serial, name, 1 if supported else 0, source, timestamp)
            for name, supported in sorted(capabilities.items())
        ]
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            connection.executemany(
                """
                INSERT INTO device_capabilities(
                    device_serial, capability, supported, source, detected_at_utc
                ) VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(device_serial, capability) DO UPDATE SET
                    supported=excluded.supported,
                    source=excluded.source,
                    detected_at_utc=excluded.detected_at_utc
                """,
                rows,
            )
            connection.commit()

    def get_device_capabilities(self, device_serial: str | None = None) -> dict[str, bool]:
        if not self.path.exists():
            return {}
        serial = device_serial or self.get_metadata().get("serial")
        if not serial:
            return {}
        with closing(self._connect(read_only=True)) as connection:
            rows = connection.execute(
                "SELECT capability, supported FROM device_capabilities WHERE device_serial = ?",
                (serial,),
            ).fetchall()
        return {str(row[0]): bool(row[1]) for row in rows}

    def get_ingest_diagnostics(self, device_serial: str | None = None) -> dict[str, int]:
        serial = device_serial or self.get_metadata().get("serial")
        defaults = {
            "last_timestamp_utc": 0,
            "duplicate_timestamp_count": 0,
            "clock_regression_count": 0,
            "short_interval_count": 0,
            "long_interval_count": 0,
            "updated_at_utc": 0,
        }
        if not serial or not self.path.exists():
            return defaults
        with closing(self._connect(read_only=True)) as connection:
            row = connection.execute(
                "SELECT * FROM ingest_diagnostics WHERE device_serial = ?", (serial,)
            ).fetchone()
        if row is None:
            return defaults
        return {key: int(row[key] or 0) for key in defaults}

    def insert_measurement(
        self,
        sample: dict[str, Any],
        *,
        device_serial: str | None = None,
        timestamp_utc: int | None = None,
        cpm_quality: str = "normal",
        expected_interval_seconds: int | None = None,
    ) -> dict[str, int]:
        if cpm_quality not in {"normal", "confirmed_high"}:
            raise ValueError(f"Unsupported CPM quality: {cpm_quality}")
        if "cpm" not in sample:
            raise ValueError("History samples require CPM")
        serial = device_serial or self.get_metadata().get("serial")
        if not serial:
            raise ValueError("History samples require a device serial")
        timestamp = _coerce_epoch_timestamp(timestamp_utc)
        values = (
            serial,
            timestamp,
            int(sample["cpm"]),
            _optional_int(sample.get("tube_low_cpm")),
            _optional_int(sample.get("tube_high_cpm")),
            _optional_float(sample.get("temperature_c")),
            _optional_float(sample.get("voltage_v")),
            _optional_int(sample.get("gyro_x")),
            _optional_int(sample.get("gyro_y")),
            _optional_int(sample.get("gyro_z")),
            cpm_quality,
            _optional_float(sample.get("pressure_hpa")),
            _optional_float(sample.get("raw_cpm", sample.get("cpm"))),
            _optional_float(sample.get("corrected_cpm")),
            _optional_text(sample.get("detector_type")),
            _optional_text(sample.get("dual_tube_mode")),
            _optional_text(sample.get("active_tube")),
            _optional_text(sample.get("dead_time_model")),
            _optional_float(sample.get("dead_time_us")),
            _optional_float(sample.get("dead_time_loss_percent")),
            _optional_float(sample.get("detector_load_percent")),
            _optional_float(sample.get("correction_factor")),
            _optional_text(sample.get("calibration_status")),
            _optional_text(sample.get("calibration_source")),
            _optional_int(sample.get("measurement_quality_index")),
            _optional_text(sample.get("dose_quality")),
            _optional_float(sample.get("derived_dose_usvh")),
        )
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            existing = connection.execute(
                "SELECT 1 FROM measurements WHERE device_serial = ? AND timestamp_utc = ?",
                (serial, timestamp),
            ).fetchone()
            diag = connection.execute(
                "SELECT * FROM ingest_diagnostics WHERE device_serial = ?", (serial,)
            ).fetchone()
            last_timestamp = int(diag["last_timestamp_utc"] or 0) if diag else 0
            duplicate_count = int(diag["duplicate_timestamp_count"] or 0) if diag else 0
            clock_regressions = int(diag["clock_regression_count"] or 0) if diag else 0
            short_intervals = int(diag["short_interval_count"] or 0) if diag else 0
            long_intervals = int(diag["long_interval_count"] or 0) if diag else 0

            if existing is not None:
                duplicate_count += 1
            if last_timestamp and timestamp < last_timestamp:
                clock_regressions += 1
            elif last_timestamp and timestamp > last_timestamp and expected_interval_seconds:
                delta = timestamp - last_timestamp
                if delta < expected_interval_seconds * 0.5:
                    short_intervals += 1
                elif delta > expected_interval_seconds * 1.5:
                    long_intervals += 1

            connection.execute(
                """
                INSERT INTO measurements (
                    device_serial, timestamp_utc, cpm, tube_low_cpm, tube_high_cpm, temperature_c, voltage_v,
                    gyro_x, gyro_y, gyro_z, cpm_quality, pressure_hpa,
                    raw_cpm, corrected_cpm, detector_type, dual_tube_mode, active_tube,
                    dead_time_model, dead_time_us, dead_time_loss_percent, detector_load_percent,
                    correction_factor, calibration_status, calibration_source,
                    measurement_quality_index, dose_quality, derived_dose_usvh
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(device_serial, timestamp_utc) DO UPDATE SET
                    cpm=excluded.cpm,
                    tube_low_cpm=excluded.tube_low_cpm,
                    tube_high_cpm=excluded.tube_high_cpm,
                    temperature_c=excluded.temperature_c,
                    voltage_v=excluded.voltage_v,
                    gyro_x=excluded.gyro_x,
                    gyro_y=excluded.gyro_y,
                    gyro_z=excluded.gyro_z,
                    cpm_quality=excluded.cpm_quality,
                    pressure_hpa=excluded.pressure_hpa,
                    raw_cpm=excluded.raw_cpm,
                    corrected_cpm=excluded.corrected_cpm,
                    detector_type=excluded.detector_type,
                    dual_tube_mode=excluded.dual_tube_mode,
                    active_tube=excluded.active_tube,
                    dead_time_model=excluded.dead_time_model,
                    dead_time_us=excluded.dead_time_us,
                    dead_time_loss_percent=excluded.dead_time_loss_percent,
                    detector_load_percent=excluded.detector_load_percent,
                    correction_factor=excluded.correction_factor,
                    calibration_status=excluded.calibration_status,
                    calibration_source=excluded.calibration_source,
                    measurement_quality_index=excluded.measurement_quality_index,
                    dose_quality=excluded.dose_quality,
                    derived_dose_usvh=excluded.derived_dose_usvh
                """,
                values,
            )
            connection.execute(
                """
                INSERT INTO ingest_diagnostics(
                    device_serial, last_timestamp_utc, duplicate_timestamp_count,
                    clock_regression_count, short_interval_count, long_interval_count,
                    updated_at_utc
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(device_serial) DO UPDATE SET
                    last_timestamp_utc=excluded.last_timestamp_utc,
                    duplicate_timestamp_count=excluded.duplicate_timestamp_count,
                    clock_regression_count=excluded.clock_regression_count,
                    short_interval_count=excluded.short_interval_count,
                    long_interval_count=excluded.long_interval_count,
                    updated_at_utc=excluded.updated_at_utc
                """,
                (
                    serial,
                    max(last_timestamp, timestamp),
                    duplicate_count,
                    clock_regressions,
                    short_intervals,
                    long_intervals,
                    int(time.time()),
                ),
            )
            connection.commit()
        self.prune_if_due()
        return {
            "duplicate_timestamp_count": duplicate_count,
            "clock_regression_count": clock_regressions,
            "short_interval_count": short_intervals,
            "long_interval_count": long_intervals,
        }

    def insert_raw_measurement(
        self,
        sample: dict[str, Any],
        *,
        device_serial: str,
        timestamp_utc: int | None = None,
        gate_state: str,
        accepted: bool,
    ) -> int:
        """Persist the unchanged device sample separately from analysis history."""
        if "cpm" not in sample:
            raise ValueError("Raw history samples require CPM")
        timestamp = _coerce_epoch_timestamp(timestamp_utc)
        raw_json = json.dumps(sample, sort_keys=True, separators=(",", ":"), default=str)
        values = (
            str(device_serial),
            timestamp,
            int(sample["cpm"]),
            _optional_int(sample.get("tube_low_cpm")),
            _optional_int(sample.get("tube_high_cpm")),
            _optional_float(sample.get("temperature_c")),
            _optional_float(sample.get("voltage_v")),
            _optional_int(sample.get("gyro_x")),
            _optional_int(sample.get("gyro_y")),
            _optional_int(sample.get("gyro_z")),
            str(gate_state),
            1 if accepted else 0,
            raw_json,
        )
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            cursor = connection.execute(
                """
                INSERT INTO raw_measurements(
                    device_serial, timestamp_utc, cpm, tube_low_cpm, tube_high_cpm,
                    temperature_c, voltage_v, gyro_x, gyro_y, gyro_z, gate_state, accepted, raw_json
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                values,
            )
            connection.commit()
            return int(cursor.lastrowid)

    def raw_measurement_summary(
        self,
        *,
        start_timestamp_utc: int | None = None,
        end_timestamp_utc: int | None = None,
        device_serial: str | None = None,
    ) -> dict[str, int | bool]:
        if not self.path.exists():
            return {"available": False, "total": 0, "accepted": 0, "pending": 0}
        clauses: list[str] = []
        params: list[Any] = []
        if start_timestamp_utc is not None:
            clauses.append("timestamp_utc >= ?")
            params.append(int(start_timestamp_utc))
        if end_timestamp_utc is not None:
            clauses.append("timestamp_utc < ?")
            params.append(int(end_timestamp_utc))
        if device_serial:
            clauses.append("device_serial = ?")
            params.append(str(device_serial))
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        with self._database_lock(exclusive=False), closing(self._connect(read_only=True)) as connection:
            tables = {
                str(row[0])
                for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            }
            if "raw_measurements" not in tables:
                return {"available": False, "total": 0, "accepted": 0, "pending": 0}
            row = connection.execute(
                f"SELECT COUNT(*), SUM(accepted), SUM(CASE WHEN accepted=0 THEN 1 ELSE 0 END) FROM raw_measurements{where}",
                params,
            ).fetchone()
        return {
            "available": True,
            "total": int(row[0] or 0),
            "accepted": int(row[1] or 0),
            "pending": int(row[2] or 0),
        }

    def query_raw_measurements(
        self,
        start_utc: int,
        end_utc: int,
        *,
        device_serial: str | None = None,
    ) -> list[dict[str, Any]]:
        if end_utc <= start_utc or not self.path.exists():
            return []
        clauses = ["timestamp_utc >= ?", "timestamp_utc < ?"]
        params: list[Any] = [int(start_utc), int(end_utc)]
        if device_serial:
            clauses.append("device_serial = ?")
            params.append(str(device_serial))
        with self._database_lock(exclusive=False), closing(self._connect(read_only=True)) as connection:
            tables = {
                str(row[0])
                for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            }
            if "raw_measurements" not in tables:
                return []
            rows = connection.execute(
                "SELECT id,device_serial,timestamp_utc,cpm,tube_low_cpm,tube_high_cpm,"
                "temperature_c,voltage_v,gyro_x,gyro_y,gyro_z,gate_state,accepted,raw_json "
                "FROM raw_measurements WHERE " + " AND ".join(clauses) + " ORDER BY timestamp_utc,id",
                params,
            ).fetchall()
        return [dict(row) for row in rows]

    def purge_unconfirmed_adaptive_spikes(
        self,
        *,
        cleanup_marker: str = "adaptive_cpm_cleanup_last_run_6_8_2",
        fixed_threshold: int = 10000,
        confirmations: int = 3,
        adaptive_window: int = 12,
        adaptive_min_samples: int = 5,
        adaptive_multiplier: float = 20.0,
        adaptive_minimum_cpm: int = 1000,
        adaptive_minimum_delta: int = 500,
        consistency_ratio: float = 4.0,
    ) -> dict[str, int | bool]:
        """Remove legacy one-off CPM spikes that never met confirmation rules.

        Replay each device's raw CPM stream with the same conservative rule as
        the live gate. The check intentionally runs on every app start so a
        single corrupt value recorded after an earlier migration is not left in
        either raw or accepted history. Runs shorter than three similar
        suspicious values are removed; confirmed runs and ordinary values are
        preserved.
        """
        if not self.path.exists():
            return {
                "already_done": False,
                "previously_run": False,
                "raw_deleted": 0,
                "measurements_deleted": 0,
                "events_deleted": 0,
            }

        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            existing_marker = connection.execute(
                "SELECT value FROM metadata WHERE key = ?", (cleanup_marker,)
            ).fetchone()
            previously_run = existing_marker is not None

            tables = {
                str(row[0])
                for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            }
            if "raw_measurements" not in tables:
                connection.execute(
                    "INSERT INTO metadata(key, value) VALUES (?, 'complete') ",
                    (cleanup_marker,),
                )
                connection.commit()
                return {
                    "already_done": False,
                    "previously_run": previously_run,
                    "raw_deleted": 0,
                    "measurements_deleted": 0,
                    "events_deleted": 0,
                }

            rows = connection.execute(
                "SELECT id, device_serial, timestamp_utc, cpm, accepted "
                "FROM raw_measurements ORDER BY device_serial, timestamp_utc, id"
            ).fetchall()

            delete_targets: list[tuple[int, str, int]] = []
            current_serial = ""
            recent_normal: deque[int] = deque(maxlen=max(adaptive_min_samples, adaptive_window))
            pending: list[sqlite3.Row] = []
            pending_reference: float | None = None

            def adaptive_trigger() -> int:
                if len(recent_normal) < adaptive_min_samples:
                    return min(int(fixed_threshold), int(adaptive_minimum_cpm))
                baseline = float(statistics.median(recent_normal))
                return min(
                    int(fixed_threshold),
                    max(
                        int(adaptive_minimum_cpm),
                        round(baseline * adaptive_multiplier),
                        round(baseline + adaptive_minimum_delta),
                    ),
                )

            def flush_pending() -> None:
                nonlocal pending, pending_reference
                if pending and len(pending) < int(confirmations):
                    delete_targets.extend(
                        (int(row["id"]), str(row["device_serial"]), int(row["timestamp_utc"]))
                        for row in pending
                    )
                pending = []
                pending_reference = None

            for row in rows:
                serial = str(row["device_serial"])
                if serial != current_serial:
                    flush_pending()
                    current_serial = serial
                    recent_normal.clear()

                if not bool(row["accepted"]):
                    flush_pending()
                    delete_targets.append((int(row["id"]), serial, int(row["timestamp_utc"])))
                    continue

                cpm = int(row["cpm"])
                trigger = adaptive_trigger()
                suspicious = cpm > int(fixed_threshold) or cpm > trigger
                if suspicious:
                    if pending_reference is not None:
                        low = min(float(cpm), pending_reference)
                        high = max(float(cpm), pending_reference)
                        consistent = high <= 0 if low <= 0 else high / low <= float(consistency_ratio)
                        if not consistent:
                            flush_pending()
                    pending.append(row)
                    pending_reference = (
                        float(cpm)
                        if pending_reference is None
                        else float(statistics.median((pending_reference, float(cpm))))
                    )
                    continue

                flush_pending()
                recent_normal.append(cpm)

            flush_pending()

            # De-duplicate targets because accepted=0 rows and sequence flushing can
            # meet at the same boundary in imported databases.
            unique_targets = list(
                {row_id: (row_id, serial, timestamp) for row_id, serial, timestamp in delete_targets}.values()
            )
            raw_deleted = measurements_deleted = events_deleted = 0
            if unique_targets:
                connection.execute(
                    "CREATE TEMP TABLE cpm_cleanup_targets("
                    "raw_id INTEGER PRIMARY KEY, device_serial TEXT NOT NULL, timestamp_utc INTEGER NOT NULL)"
                )
                connection.executemany(
                    "INSERT INTO cpm_cleanup_targets(raw_id, device_serial, timestamp_utc) VALUES (?, ?, ?)",
                    unique_targets,
                )
                raw_deleted = int(
                    connection.execute(
                        "SELECT COUNT(*) FROM raw_measurements "
                        "WHERE id IN (SELECT raw_id FROM cpm_cleanup_targets)"
                    ).fetchone()[0]
                )
                measurements_deleted = int(
                    connection.execute(
                        "SELECT COUNT(*) FROM measurements m WHERE EXISTS ("
                        "SELECT 1 FROM cpm_cleanup_targets t "
                        "WHERE t.device_serial=m.device_serial AND t.timestamp_utc=m.timestamp_utc)"
                    ).fetchone()[0]
                )
                if "operational_events" in tables:
                    events_deleted = int(
                        connection.execute(
                            "SELECT COUNT(*) FROM operational_events e WHERE EXISTS ("
                            "SELECT 1 FROM cpm_cleanup_targets t "
                            "WHERE t.device_serial=e.device_serial AND t.timestamp_utc=e.timestamp_utc)"
                        ).fetchone()[0]
                    )
                    connection.execute(
                        "DELETE FROM operational_events WHERE EXISTS ("
                        "SELECT 1 FROM cpm_cleanup_targets t "
                        "WHERE t.device_serial=operational_events.device_serial "
                        "AND t.timestamp_utc=operational_events.timestamp_utc)"
                    )
                connection.execute(
                    "DELETE FROM measurements WHERE EXISTS ("
                    "SELECT 1 FROM cpm_cleanup_targets t "
                    "WHERE t.device_serial=measurements.device_serial "
                    "AND t.timestamp_utc=measurements.timestamp_utc)"
                )
                connection.execute(
                    "DELETE FROM raw_measurements WHERE id IN (SELECT raw_id FROM cpm_cleanup_targets)"
                )
                connection.execute("DROP TABLE cpm_cleanup_targets")
                if "ingest_diagnostics" in tables:
                    connection.execute(
                        "UPDATE ingest_diagnostics SET last_timestamp_utc=("
                        "SELECT MAX(m.timestamp_utc) FROM measurements m "
                        "WHERE m.device_serial=ingest_diagnostics.device_serial)"
                    )

            connection.execute(
                "INSERT INTO metadata(key, value) VALUES (?, ?) "
                "ON CONFLICT(key) DO UPDATE SET value=excluded.value",
                (
                    cleanup_marker,
                    json.dumps(
                        {
                            "raw_deleted": raw_deleted,
                            "measurements_deleted": measurements_deleted,
                            "events_deleted": events_deleted,
                            "completed_at_utc": int(time.time()),
                        },
                        sort_keys=True,
                        separators=(",", ":"),
                    ),
                ),
            )
            connection.commit()

        if raw_deleted or measurements_deleted or events_deleted:
            LOG.warning(
                "Removed unconfirmed adaptive CPM spikes from history: "
                "%d raw, %d accepted measurements, %d events",
                raw_deleted,
                measurements_deleted,
                events_deleted,
            )
        return {
            "already_done": False,
            "previously_run": previously_run,
            "raw_deleted": raw_deleted,
            "measurements_deleted": measurements_deleted,
            "events_deleted": events_deleted,
        }

    def prune_if_due(self, *, interval_seconds: float = 21600.0) -> int:
        now = time.monotonic()
        if now - self._last_prune_monotonic < interval_seconds:
            return 0
        self._last_prune_monotonic = now
        # Incremental inserts can be historical backfills or restored datasets.
        # Prune them relative to the newest stored sample, not the wall clock.
        # The service still performs an explicit wall-clock prune at startup.
        _first, latest = self.bounds()
        return self.prune(now_utc=latest) if latest is not None else 0

    def prune(self, *, now_utc: int | None = None) -> int:
        cutoff = (int(time.time()) if now_utc is None else int(now_utc)) - self.retention_days * 86400
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            cursor = connection.execute("DELETE FROM measurements WHERE timestamp_utc < ?", (cutoff,))
            raw_cursor = connection.execute("DELETE FROM raw_measurements WHERE timestamp_utc < ?", (cutoff,))
            connection.commit()
            deleted = int(cursor.rowcount if cursor.rowcount is not None else 0)
            deleted += int(raw_cursor.rowcount if raw_cursor.rowcount is not None else 0)
        if deleted:
            LOG.info(
                "Pruned %d historical measurements older than %d days",
                deleted,
                self.retention_days,
            )
        return deleted

    def complete_history_summary(self) -> dict[str, object]:
        """Return a deletion preview for every historical GMC record."""
        if not self.path.exists():
            return {
                "measurements": 0,
                "raw_measurements": 0,
                "events": 0,
                "diagnostics": 0,
                "annotations": 0,
                "first_timestamp_utc": None,
                "last_timestamp_utc": None,
                "device_serials": [],
            }
        with self._database_lock(exclusive=False), closing(self._connect(read_only=True)) as connection:
            row = connection.execute(
                "SELECT COUNT(*), MIN(timestamp_utc), MAX(timestamp_utc) FROM measurements"
            ).fetchone()
            raw_measurements = int(connection.execute("SELECT COUNT(*) FROM raw_measurements").fetchone()[0])
            events = int(connection.execute("SELECT COUNT(*) FROM operational_events").fetchone()[0])
            diagnostics = int(connection.execute("SELECT COUNT(*) FROM ingest_diagnostics").fetchone()[0])
            annotations = int(connection.execute("SELECT COUNT(*) FROM event_annotations").fetchone()[0])
            serials = [
                str(item[0])
                for item in connection.execute(
                    "SELECT DISTINCT device_serial FROM measurements "
                    "WHERE device_serial IS NOT NULL AND device_serial <> '' ORDER BY device_serial"
                ).fetchall()
            ]
        return {
            "measurements": int(row[0]),
            "raw_measurements": raw_measurements,
            "events": events,
            "diagnostics": diagnostics,
            "annotations": annotations,
            "first_timestamp_utc": int(row[1]) if row[1] is not None else None,
            "last_timestamp_utc": int(row[2]) if row[2] is not None else None,
            "device_serials": serials,
        }

    def purge_all_history(self) -> dict[str, int]:
        """Irreversibly remove every stored measurement and operational event."""
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            measurements = int(connection.execute("SELECT COUNT(*) FROM measurements").fetchone()[0])
            raw_measurements = int(connection.execute("SELECT COUNT(*) FROM raw_measurements").fetchone()[0])
            events = int(connection.execute("SELECT COUNT(*) FROM operational_events").fetchone()[0])
            diagnostics = int(connection.execute("SELECT COUNT(*) FROM ingest_diagnostics").fetchone()[0])
            annotations = int(connection.execute("SELECT COUNT(*) FROM event_annotations").fetchone()[0])
            connection.execute("DELETE FROM measurements")
            connection.execute("DELETE FROM raw_measurements")
            connection.execute("DELETE FROM operational_events")
            connection.execute("DELETE FROM ingest_diagnostics")
            connection.execute("DELETE FROM event_annotations")
            connection.execute(
                "DELETE FROM sqlite_sequence WHERE name IN ('operational_events','raw_measurements','event_annotations')"
            )
            connection.commit()
            connection.execute("PRAGMA wal_checkpoint(TRUNCATE)")
            connection.execute("VACUUM")
            connection.commit()
        self._quick_check_cache_value = None
        self._last_prune_monotonic = 0.0
        LOG.warning(
            "Purged all GMC history: %d measurements, %d raw measurements, %d events",
            measurements,
            raw_measurements,
            events,
        )
        return {
            "measurements": measurements,
            "raw_measurements": raw_measurements,
            "events": events,
            "diagnostics": diagnostics,
            "annotations": annotations,
        }

    def assign_custom_calibration_profile(
        self, *, device_serial: str, profile_id: str, values: dict[str, Any]
    ) -> None:
        """Persist an app-local device calibration assignment used at runtime."""
        metadata = self.get_metadata()
        try:
            assignments = json.loads(metadata.get("calibration_assignments", "{}"))
        except (TypeError, ValueError, json.JSONDecodeError):
            assignments = {}
        assignments[str(device_serial)] = {
            "profile_id": str(profile_id),
            "values": dict(values),
            "updated_at_utc": int(time.time()),
        }
        self.set_metadata(
            {"calibration_assignments": json.dumps(assignments, sort_keys=True, separators=(",", ":"))}
        )

    def get_custom_calibration_assignment(self, device_serial: str) -> dict[str, Any] | None:
        metadata = self.get_metadata()
        try:
            assignments = json.loads(metadata.get("calibration_assignments", "{}"))
        except (TypeError, ValueError, json.JSONDecodeError):
            return None
        item = assignments.get(str(device_serial))
        return dict(item) if isinstance(item, dict) else None

    def record_calibration_change(
        self,
        *,
        device_serial: str | None,
        profile_id: str,
        detector_type: str,
        values: dict[str, Any],
        changed_fields: list[str] | None = None,
        source: str = "user",
        comment: str = "",
        timestamp_utc: int | None = None,
    ) -> int:
        timestamp = _coerce_epoch_timestamp(timestamp_utc)
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            cursor = connection.execute(
                """
                INSERT INTO calibration_history(
                    device_serial,timestamp_utc,profile_id,detector_type,values_json,
                    changed_fields_json,source,comment
                ) VALUES (?,?,?,?,?,?,?,?)
                """,
                (
                    device_serial, timestamp, profile_id, detector_type,
                    json.dumps(values, sort_keys=True, separators=(",", ":"), default=str),
                    json.dumps(changed_fields or [], sort_keys=True, separators=(",", ":")),
                    source, comment,
                ),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def list_calibration_history(
        self, *, device_serial: str | None = None, limit: int = 100
    ) -> list[dict[str, Any]]:
        query = "SELECT * FROM calibration_history"
        params: list[Any] = []
        if device_serial:
            query += " WHERE device_serial = ?"
            params.append(device_serial)
        query += " ORDER BY timestamp_utc DESC, id DESC LIMIT ?"
        params.append(max(1, min(int(limit), 1000)))
        with closing(self._connect(read_only=True)) as connection:
            rows = connection.execute(query, params).fetchall()
        result: list[dict[str, Any]] = []
        for row in rows:
            item = dict(row)
            item["values"] = json.loads(item.pop("values_json"))
            item["changed_fields"] = json.loads(item.pop("changed_fields_json"))
            result.append(item)
        return result

    def save_custom_calibration_profile(
        self,
        *,
        profile_id: str,
        display_name: str,
        detector_type: str,
        values: dict[str, Any],
        source: str = "user",
        comment: str = "",
    ) -> None:
        now = int(time.time())
        normalized = str(profile_id).strip()
        if not normalized or not all(ch.isalnum() or ch in "_-" for ch in normalized):
            raise ValueError("Custom calibration profile ID is invalid")
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            connection.execute(
                """
                INSERT INTO custom_calibration_profiles(
                    profile_id,display_name,detector_type,values_json,created_at_utc,updated_at_utc,source,comment
                ) VALUES (?,?,?,?,?,?,?,?)
                ON CONFLICT(profile_id) DO UPDATE SET
                    display_name=excluded.display_name, detector_type=excluded.detector_type,
                    values_json=excluded.values_json, updated_at_utc=excluded.updated_at_utc,
                    source=excluded.source, comment=excluded.comment
                """,
                (normalized, display_name, detector_type,
                 json.dumps(values, sort_keys=True, separators=(",", ":"), default=str),
                 now, now, source, comment),
            )
            connection.commit()

    def list_custom_calibration_profiles(self) -> list[dict[str, Any]]:
        with closing(self._connect(read_only=True)) as connection:
            rows = connection.execute(
                "SELECT * FROM custom_calibration_profiles ORDER BY display_name, profile_id"
            ).fetchall()
        result = []
        for row in rows:
            item = dict(row)
            item["values"] = json.loads(item.pop("values_json"))
            result.append(item)
        return result

    def query_range(
        self,
        start_utc: int,
        end_utc: int,
        *,
        device_serial: str | None = None,
        all_devices: bool = False,
    ) -> list[HistoryRow]:
        if end_utc <= start_utc:
            raise ValueError("end_utc must be greater than start_utc")
        if not self.path.exists():
            return []
        serial = None if all_devices else (device_serial or self.get_metadata().get("serial"))
        with closing(self._connect(read_only=True)) as connection:
            if serial:
                rows = connection.execute(
                    """
                    SELECT device_serial, timestamp_utc, cpm, temperature_c, voltage_v,
                           gyro_x, gyro_y, gyro_z, cpm_quality, tube_low_cpm, tube_high_cpm, pressure_hpa,
                           raw_cpm, corrected_cpm, detector_type, dual_tube_mode, active_tube,
                           dead_time_model, dead_time_us, dead_time_loss_percent, detector_load_percent,
                           correction_factor, calibration_status, calibration_source,
                           measurement_quality_index, dose_quality, derived_dose_usvh
                    FROM measurements
                    WHERE device_serial = ? AND timestamp_utc >= ? AND timestamp_utc < ?
                    ORDER BY timestamp_utc ASC
                    """,
                    (serial, int(start_utc), int(end_utc)),
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT device_serial, timestamp_utc, cpm, temperature_c, voltage_v,
                           gyro_x, gyro_y, gyro_z, cpm_quality, tube_low_cpm, tube_high_cpm, pressure_hpa,
                           raw_cpm, corrected_cpm, detector_type, dual_tube_mode, active_tube,
                           dead_time_model, dead_time_us, dead_time_loss_percent, detector_load_percent,
                           correction_factor, calibration_status, calibration_source,
                           measurement_quality_index, dose_quality, derived_dose_usvh
                    FROM measurements
                    WHERE timestamp_utc >= ? AND timestamp_utc < ?
                    ORDER BY timestamp_utc ASC
                    """,
                    (int(start_utc), int(end_utc)),
                ).fetchall()
        return [HistoryRow(**dict(row)) for row in rows]

    def aggregate_range(
        self,
        start_utc: int,
        end_utc: int,
        *,
        bucket_seconds: int,
        expected_interval_seconds: int,
        device_serial: str | None = None,
    ) -> list[dict[str, Any]]:
        """Return compact time-bucket aggregates for long-running analyses.

        The query deliberately aggregates in SQLite so multi-year dashboards do
        not load millions of raw polling rows into memory. Only accepted quality
        states are included. ``occupied_slots`` counts distinct expected cadence
        slots and is used by the long-term analysis to estimate data coverage
        without letting dense polling bursts conceal gaps.
        """
        if end_utc <= start_utc:
            raise ValueError("end_utc must be greater than start_utc")
        bucket = max(60, int(bucket_seconds))
        cadence = max(1, int(expected_interval_seconds))
        if not self.path.exists():
            return []
        serial = device_serial or self.get_metadata().get("serial")
        if not serial:
            return []
        with closing(self._connect(read_only=True)) as connection:
            rows = connection.execute(
                """
                SELECT
                    (timestamp_utc / ?) * ? AS timestamp_utc,
                    COUNT(*) AS samples,
                    COUNT(DISTINCT (timestamp_utc / ?)) AS occupied_slots,
                    AVG(cpm) AS mean_cpm,
                    MIN(cpm) AS minimum_cpm,
                    MAX(cpm) AS maximum_cpm,
                    AVG(temperature_c) AS temperature_c,
                    AVG(pressure_hpa) AS pressure_hpa,
                    AVG(voltage_v) AS voltage_v,
                    AVG(derived_dose_usvh) AS mean_derived_dose_usvh,
                    SUM(CASE WHEN derived_dose_usvh IS NOT NULL THEN 1 ELSE 0 END) AS dose_samples,
                    MIN(timestamp_utc) AS first_sample_utc,
                    MAX(timestamp_utc) AS last_sample_utc
                FROM measurements
                WHERE device_serial = ?
                  AND timestamp_utc >= ?
                  AND timestamp_utc < ?
                  AND cpm >= 0
                  AND cpm <= 100000000
                  AND LOWER(COALESCE(cpm_quality, 'normal')) IN ('normal', 'confirmed_high')
                GROUP BY (timestamp_utc / ?)
                ORDER BY timestamp_utc ASC
                """,
                (
                    bucket,
                    bucket,
                    cadence,
                    serial,
                    int(start_utc),
                    int(end_utc),
                    bucket,
                ),
            ).fetchall()
        return [dict(row) for row in rows]

    def query_all(self, *, device_serial: str | None = None) -> list[HistoryRow]:
        if not self.path.exists():
            return []
        serial = device_serial
        with closing(self._connect(read_only=True)) as connection:
            if serial:
                rows = connection.execute(
                    """
                    SELECT device_serial, timestamp_utc, cpm, temperature_c, voltage_v,
                           gyro_x, gyro_y, gyro_z, cpm_quality, tube_low_cpm, tube_high_cpm, pressure_hpa,
                           raw_cpm, corrected_cpm, detector_type, dual_tube_mode, active_tube,
                           dead_time_model, dead_time_us, dead_time_loss_percent, detector_load_percent,
                           correction_factor, calibration_status, calibration_source,
                           measurement_quality_index, dose_quality, derived_dose_usvh
                    FROM measurements WHERE device_serial = ? ORDER BY timestamp_utc ASC
                    """,
                    (serial,),
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT device_serial, timestamp_utc, cpm, temperature_c, voltage_v,
                           gyro_x, gyro_y, gyro_z, cpm_quality, tube_low_cpm, tube_high_cpm, pressure_hpa,
                           raw_cpm, corrected_cpm, detector_type, dual_tube_mode, active_tube,
                           dead_time_model, dead_time_us, dead_time_loss_percent, detector_load_percent,
                           correction_factor, calibration_status, calibration_source,
                           measurement_quality_index, dose_quality, derived_dose_usvh
                    FROM measurements ORDER BY device_serial, timestamp_utc ASC
                    """
                ).fetchall()
        return [HistoryRow(**dict(row)) for row in rows]

    def count(self, *, device_serial: str | None = None, all_devices: bool = False) -> int:
        if not self.path.exists():
            return 0
        serial = None if all_devices else (device_serial or self.get_metadata().get("serial"))
        with closing(self._connect(read_only=True)) as connection:
            if serial:
                return int(
                    connection.execute(
                        "SELECT COUNT(*) FROM measurements WHERE device_serial = ?", (serial,)
                    ).fetchone()[0]
                )
            return int(connection.execute("SELECT COUNT(*) FROM measurements").fetchone()[0])

    def bounds(
        self, *, device_serial: str | None = None, all_devices: bool = False
    ) -> tuple[int | None, int | None]:
        if not self.path.exists():
            return None, None
        serial = None if all_devices else (device_serial or self.get_metadata().get("serial"))
        with closing(self._connect(read_only=True)) as connection:
            if serial:
                row = connection.execute(
                    "SELECT MIN(timestamp_utc), MAX(timestamp_utc) FROM measurements WHERE device_serial = ?",
                    (serial,),
                ).fetchone()
            else:
                row = connection.execute(
                    "SELECT MIN(timestamp_utc), MAX(timestamp_utc) FROM measurements"
                ).fetchone()
        return (
            int(row[0]) if row[0] is not None else None,
            int(row[1]) if row[1] is not None else None,
        )

    def integrity_check(self) -> str:
        """Run SQLite's exhaustive integrity check. Reserved for explicit restore validation."""
        if not self.path.exists():
            return "missing"
        with self._database_lock(exclusive=False), closing(self._connect(read_only=True)) as connection:
            rows = connection.execute("PRAGMA integrity_check").fetchall()
        values = [str(row[0]) for row in rows]
        return "ok" if values == ["ok"] else "; ".join(values[:10])

    def quick_check(self) -> str:
        """Run SQLite's lower-cost quick check for routine status display."""
        if not self.path.exists():
            return "missing"
        with self._database_lock(exclusive=False), closing(self._connect(read_only=True)) as connection:
            rows = connection.execute("PRAGMA quick_check").fetchall()
        values = [str(row[0]) for row in rows]
        return "ok" if values == ["ok"] else "; ".join(values[:10])

    def _invalidate_quick_check_cache(self) -> None:
        with self._quick_check_cache_lock:
            self._quick_check_cache_value = None
            self._quick_check_cache_monotonic = 0.0

    def cached_quick_check(self, *, max_age_seconds: float = 300.0) -> str:
        """Return a cached quick_check result so page loads never scan the DB repeatedly."""
        now = time.monotonic()
        if (
            self._quick_check_cache_value is not None
            and now - self._quick_check_cache_monotonic < max_age_seconds
        ):
            return self._quick_check_cache_value
        with self._quick_check_cache_lock:
            now = time.monotonic()
            if (
                self._quick_check_cache_value is not None
                and now - self._quick_check_cache_monotonic < max_age_seconds
            ):
                return self._quick_check_cache_value
            value = self.quick_check()
            self._quick_check_cache_value = value
            self._quick_check_cache_monotonic = now
            return value

    def database_stats(self) -> dict[str, Any]:
        first, last = self.bounds()
        return {
            "schema_version": self.schema_version(),
            "size_bytes": self.path.stat().st_size if self.path.exists() else 0,
            "integrity": self.cached_quick_check(),
            "check_type": "quick_check",
            "check_cache_seconds": 300,
            "measurements": self.count(),
            "raw_measurements": int(self.raw_measurement_summary().get("total", 0)),
            "first_timestamp_utc": first,
            "last_timestamp_utc": last,
        }

    def backup_to_path(self, destination_path: str | Path) -> Path:
        """Write a consistent SQLite backup directly to disk without buffering it in RAM."""
        destination_path = Path(destination_path)
        destination_path.parent.mkdir(parents=True, exist_ok=True)
        with (
            self._database_lock(exclusive=False),
            closing(self._connect(read_only=True)) as source,
            closing(sqlite3.connect(destination_path)) as destination,
        ):
            source.backup(destination)
            destination.commit()
        secure_file(destination_path)
        return destination_path

    def backup_bytes(self) -> bytes:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(prefix="gmc-history-", suffix=".sqlite3")
        os.close(fd)
        temp_path = Path(temp_name)
        try:
            self.backup_to_path(temp_path)
            return temp_path.read_bytes()
        finally:
            with suppress(OSError):
                temp_path.unlink()

    def inspect_backup_path(self, source_path: str | Path) -> dict[str, Any]:
        """Validate a SQLite backup and return a read-only restore preview."""
        source_path = Path(source_path)
        if not source_path.exists() or source_path.stat().st_size <= 0:
            raise ValueError("Backup file is empty")
        try:
            with closing(sqlite3.connect(f"file:{source_path}?mode=ro", uri=True)) as source:
                source.row_factory = sqlite3.Row
                integrity = [str(row[0]) for row in source.execute("PRAGMA integrity_check").fetchall()]
                if integrity != ["ok"]:
                    raise ValueError("Backup SQLite integrity check failed")
                version = int(source.execute("PRAGMA user_version").fetchone()[0])
                if version > SCHEMA_VERSION:
                    raise ValueError(f"Backup schema {version} is newer than supported {SCHEMA_VERSION}")
                tables = {
                    str(row[0])
                    for row in source.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
                }
                if not {"measurements", "metadata"}.issubset(tables):
                    raise ValueError("Backup does not contain the required GMC history tables")
                measurement_row = source.execute(
                    "SELECT COUNT(*), MIN(timestamp_utc), MAX(timestamp_utc) FROM measurements"
                ).fetchone()
                raw_count = (
                    int(source.execute("SELECT COUNT(*) FROM raw_measurements").fetchone()[0])
                    if "raw_measurements" in tables
                    else 0
                )
                event_count = (
                    int(source.execute("SELECT COUNT(*) FROM operational_events").fetchone()[0])
                    if "operational_events" in tables
                    else 0
                )
                annotation_count = (
                    int(source.execute("SELECT COUNT(*) FROM event_annotations").fetchone()[0])
                    if "event_annotations" in tables
                    else 0
                )
                serials = [
                    str(row[0])
                    for row in source.execute(
                        "SELECT DISTINCT device_serial FROM measurements "
                        "WHERE device_serial IS NOT NULL AND device_serial <> '' "
                        "ORDER BY device_serial"
                    ).fetchall()
                ]
                return {
                    "integrity": "ok",
                    "schema_version": version,
                    "supported_schema_version": SCHEMA_VERSION,
                    "size_bytes": int(source_path.stat().st_size),
                    "measurements": int(measurement_row[0] or 0),
                    "raw_measurements": raw_count,
                    "events": event_count,
                    "annotations": annotation_count,
                    "first_timestamp_utc": (
                        int(measurement_row[1]) if measurement_row[1] is not None else None
                    ),
                    "last_timestamp_utc": (
                        int(measurement_row[2]) if measurement_row[2] is not None else None
                    ),
                    "device_serials": serials,
                }
        except sqlite3.Error as exc:
            raise ValueError("Backup is not a readable SQLite database") from exc

    def restore_backup_path(self, source_path: str | Path) -> dict[str, int]:
        """Validate and merge a SQLite backup already stored on disk."""
        source_path = Path(source_path)
        if not source_path.exists() or source_path.stat().st_size <= 0:
            raise ValueError("Backup file is empty")
        source_connection: sqlite3.Connection | None = None
        try:
            source_connection = sqlite3.connect(f"file:{source_path}?mode=ro", uri=True)
            source_connection.row_factory = sqlite3.Row
            integrity = [
                str(row[0]) for row in source_connection.execute("PRAGMA integrity_check").fetchall()
            ]
        except sqlite3.Error as exc:
            if source_connection is not None:
                with suppress(Exception):
                    source_connection.close()
            raise ValueError("Backup is not a readable SQLite database") from exc
        with closing(source_connection) as source:
            if integrity != ["ok"]:
                raise ValueError("Backup SQLite integrity check failed")
            version = int(source.execute("PRAGMA user_version").fetchone()[0])
            if version > SCHEMA_VERSION:
                raise ValueError(f"Backup schema {version} is newer than supported {SCHEMA_VERSION}")
            tables = {
                str(row[0])
                for row in source.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
            }
            if not {"measurements", "metadata"}.issubset(tables):
                raise ValueError("Backup does not contain the required GMC history tables")

            rows_merged = 0
            raw_rows_merged = 0
            annotation_rows_merged = 0
            metadata_merged = 0
            with self._database_lock(exclusive=True), closing(self._connect()) as destination:
                source_columns = {row[1] for row in source.execute("PRAGMA table_info(measurements)")}
                tube_low_expr = "tube_low_cpm" if "tube_low_cpm" in source_columns else "NULL AS tube_low_cpm"
                tube_high_expr = (
                    "tube_high_cpm" if "tube_high_cpm" in source_columns else "NULL AS tube_high_cpm"
                )
                pressure_expr = "pressure_hpa" if "pressure_hpa" in source_columns else "NULL AS pressure_hpa"
                cursor = source.execute(
                    f"""
                    SELECT device_serial, timestamp_utc, cpm, {tube_low_expr}, {tube_high_expr},
                           temperature_c, voltage_v, gyro_x, gyro_y, gyro_z, cpm_quality, {pressure_expr}
                    FROM measurements ORDER BY device_serial, timestamp_utc
                    """
                )
                while True:
                    batch = cursor.fetchmany(1000)
                    if not batch:
                        break
                    destination.executemany(
                        """
                        INSERT INTO measurements(
                            device_serial, timestamp_utc, cpm, tube_low_cpm, tube_high_cpm,
                            temperature_c, voltage_v, gyro_x, gyro_y, gyro_z, cpm_quality, pressure_hpa
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT(device_serial, timestamp_utc) DO UPDATE SET
                            cpm=excluded.cpm,
                            tube_low_cpm=excluded.tube_low_cpm,
                            tube_high_cpm=excluded.tube_high_cpm,
                            temperature_c=excluded.temperature_c,
                            voltage_v=excluded.voltage_v,
                            gyro_x=excluded.gyro_x,
                            gyro_y=excluded.gyro_y,
                            gyro_z=excluded.gyro_z,
                            cpm_quality=excluded.cpm_quality,
                            pressure_hpa=excluded.pressure_hpa
                        """,
                        [tuple(row) for row in batch],
                    )
                    rows_merged += len(batch)

                for row in source.execute("SELECT key, value FROM metadata"):
                    destination.execute(
                        "INSERT OR IGNORE INTO metadata(key, value) VALUES (?, ?)", tuple(row)
                    )
                    metadata_merged += 1

                if "raw_measurements" in tables:
                    raw_cursor = source.execute(
                        "SELECT device_serial,timestamp_utc,cpm,tube_low_cpm,tube_high_cpm,"
                        "temperature_c,voltage_v,gyro_x,gyro_y,gyro_z,gate_state,accepted,raw_json "
                        "FROM raw_measurements ORDER BY id"
                    )
                    while True:
                        batch = raw_cursor.fetchmany(1000)
                        if not batch:
                            break
                        destination.executemany(
                            """
                            INSERT INTO raw_measurements(
                                device_serial,timestamp_utc,cpm,tube_low_cpm,tube_high_cpm,
                                temperature_c,voltage_v,gyro_x,gyro_y,gyro_z,gate_state,accepted,raw_json
                            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
                            """,
                            [tuple(row) for row in batch],
                        )
                        raw_rows_merged += len(batch)

                if "event_annotations" in tables:
                    annotation_cursor = source.execute(
                        "SELECT device_serial,start_timestamp_utc,end_timestamp_utc,category,status,note,created_at_utc,updated_at_utc "
                        "FROM event_annotations ORDER BY id"
                    )
                    while True:
                        batch = annotation_cursor.fetchmany(500)
                        if not batch:
                            break
                        for row in batch:
                            values = tuple(row)
                            cursor = destination.execute(
                                """
                                INSERT INTO event_annotations(
                                    device_serial,start_timestamp_utc,end_timestamp_utc,category,status,note,created_at_utc,updated_at_utc
                                )
                                SELECT ?,?,?,?,?,?,?,?
                                WHERE NOT EXISTS (
                                    SELECT 1 FROM event_annotations
                                    WHERE device_serial IS ?
                                      AND start_timestamp_utc=?
                                      AND end_timestamp_utc=?
                                      AND category=?
                                      AND status=?
                                      AND note=?
                                )
                                """,
                                values + values[:6],
                            )
                            annotation_rows_merged += max(0, int(cursor.rowcount or 0))

                if "device_capabilities" in tables:
                    destination.executemany(
                        """
                        INSERT INTO device_capabilities(
                            device_serial, capability, supported, source, detected_at_utc
                        ) VALUES (?, ?, ?, ?, ?)
                        ON CONFLICT(device_serial, capability) DO NOTHING
                        """,
                        [
                            tuple(row)
                            for row in source.execute(
                                "SELECT device_serial, capability, supported, source, detected_at_utc FROM device_capabilities"
                            )
                        ],
                    )
                destination.commit()
            self._invalidate_quick_check_cache()
            return {
                "rows_merged": rows_merged,
                "raw_rows_merged": raw_rows_merged,
                "annotation_rows_merged": annotation_rows_merged,
                "annotations_merged": annotation_rows_merged,
                "metadata_entries_seen": metadata_merged,
                "source_schema_version": version,
            }

    def restore_backup_bytes(self, payload: bytes) -> dict[str, int]:
        if not payload:
            raise ValueError("Backup file is empty")
        fd, temp_name = tempfile.mkstemp(prefix="gmc-restore-", suffix=".sqlite3")
        os.close(fd)
        temp_path = Path(temp_name)
        temp_path.write_bytes(payload)
        try:
            return self.restore_backup_path(temp_path)
        finally:
            with suppress(OSError):
                temp_path.unlink()

    def add_event_annotation(
        self,
        *,
        start_timestamp_utc: int,
        end_timestamp_utc: int,
        category: str,
        status: str,
        note: str,
        device_serial: str | None = None,
    ) -> int:
        start = int(start_timestamp_utc)
        end = int(end_timestamp_utc)
        if end < start:
            raise ValueError("Annotation end must not be before its start")
        category_value = str(category or "other").strip().lower()[:40] or "other"
        status_value = str(status or "note").strip().lower()
        if status_value not in {"note", "confirmed", "dismissed"}:
            raise ValueError("Unsupported annotation status")
        note_value = str(note or "").strip()
        if not note_value:
            raise ValueError("Annotation note is required")
        if len(note_value) > 2000:
            raise ValueError("Annotation note is too long")
        now = int(time.time())
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            cursor = connection.execute(
                "INSERT INTO event_annotations(device_serial,start_timestamp_utc,end_timestamp_utc,category,status,note,created_at_utc,updated_at_utc) "
                "VALUES (?,?,?,?,?,?,?,?)",
                (device_serial or None, start, end, category_value, status_value, note_value, now, now),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def update_event_annotation_status(self, annotation_id: int, status: str) -> None:
        status_value = str(status or "").strip().lower()
        if status_value not in {"note", "confirmed", "dismissed"}:
            raise ValueError("Unsupported annotation status")
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            cursor = connection.execute(
                "UPDATE event_annotations SET status=?, updated_at_utc=? WHERE id=?",
                (status_value, int(time.time()), int(annotation_id)),
            )
            if cursor.rowcount != 1:
                raise ValueError("Unknown event annotation")
            connection.commit()

    def delete_event_annotation(self, annotation_id: int) -> None:
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            cursor = connection.execute("DELETE FROM event_annotations WHERE id=?", (int(annotation_id),))
            if cursor.rowcount != 1:
                raise ValueError("Unknown event annotation")
            connection.commit()

    def list_event_annotations(
        self,
        *,
        start_utc: int | None = None,
        end_utc: int | None = None,
        device_serial: str | None = None,
        limit: int = 200,
    ) -> list[dict[str, Any]]:
        clauses: list[str] = []
        values: list[Any] = []
        if start_utc is not None:
            clauses.append("end_timestamp_utc >= ?")
            values.append(int(start_utc))
        if end_utc is not None:
            clauses.append("start_timestamp_utc < ?")
            values.append(int(end_utc))
        if device_serial:
            clauses.append("(device_serial IS NULL OR device_serial = ?)")
            values.append(str(device_serial))
        where = " WHERE " + " AND ".join(clauses) if clauses else ""
        values.append(max(1, min(1000, int(limit))))
        with closing(self._connect(read_only=True)) as connection:
            rows = connection.execute(
                "SELECT id,device_serial,start_timestamp_utc,end_timestamp_utc,category,status,note,created_at_utc,updated_at_utc "
                f"FROM event_annotations{where} ORDER BY start_timestamp_utc DESC,id DESC LIMIT ?",
                values,
            ).fetchall()
        return [dict(row) for row in rows]

    def insert_operational_event(self, event: dict[str, Any], *, device_serial: str | None = None) -> None:
        serial = device_serial or self.get_metadata().get("serial")
        if not serial:
            raise ValueError("Operational events require a device serial")
        with self._database_lock(exclusive=True), closing(self._connect()) as connection:
            connection.execute(
                "INSERT INTO operational_events(device_serial,timestamp_utc,event_type,severity,cpm,details_json) VALUES (?,?,?,?,?,?)",
                (
                    serial,
                    _coerce_epoch_timestamp(event["timestamp_utc"]),
                    str(event["event_type"]),
                    str(event.get("severity", "info")),
                    event.get("cpm"),
                    json.dumps(event.get("details", {}), separators=(",", ":")),
                ),
            )
            connection.commit()

    def recent_operational_events(
        self, *, limit: int = 100, device_serial: str | None = None
    ) -> list[dict[str, Any]]:
        serial = device_serial or self.get_metadata().get("serial")
        if not serial or not self.path.exists():
            return []
        with closing(self._connect(read_only=True)) as connection:
            rows = connection.execute(
                "SELECT timestamp_utc,event_type,severity,cpm,details_json FROM operational_events WHERE device_serial=? ORDER BY timestamp_utc DESC LIMIT ?",
                (serial, int(limit)),
            ).fetchall()
        return [
            {
                "timestamp_utc": int(r[0]),
                "event_type": str(r[1]),
                "severity": str(r[2]),
                "cpm": r[3],
                "details": json.loads(r[4] or "{}"),
            }
            for r in rows
        ]


def _optional_float(value: Any) -> float | None:
    return None if value is None else float(value)


def _optional_text(value: Any) -> str | None:
    if value in (None, ""):
        return None
    return str(value)


def _optional_int(value: Any) -> int | None:
    return None if value is None else int(value)


def rows_to_dicts(rows: Iterable[HistoryRow]) -> list[dict[str, Any]]:
    return [row.__dict__.copy() for row in rows]


def metadata_json_bytes(store: HistoryStore) -> bytes:
    payload = {
        "metadata": store.get_metadata(),
        "database": store.database_stats(),
        "capabilities": store.get_device_capabilities(),
        "ingest_diagnostics": store.get_ingest_diagnostics(),
    }
    return json.dumps(payload, indent=2, sort_keys=True).encode("utf-8") + b"\n"
