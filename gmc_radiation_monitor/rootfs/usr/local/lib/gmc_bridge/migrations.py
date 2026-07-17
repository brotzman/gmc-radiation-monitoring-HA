from __future__ import annotations

import sqlite3
from collections.abc import Callable

SCHEMA_VERSION = 8

Migration = Callable[[sqlite3.Connection], None]


def _migration_1(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS measurements (
            device_serial TEXT NOT NULL,
            timestamp_utc INTEGER NOT NULL,
            cpm INTEGER NOT NULL CHECK(cpm >= 0),
            temperature_c REAL,
            voltage_v REAL,
            gyro_x INTEGER,
            gyro_y INTEGER,
            gyro_z INTEGER,
            cpm_quality TEXT NOT NULL CHECK(cpm_quality IN ('normal', 'confirmed_high')),
            PRIMARY KEY(device_serial, timestamp_utc)
        );
        CREATE INDEX IF NOT EXISTS idx_measurements_device_timestamp
        ON measurements(device_serial, timestamp_utc);
        CREATE TABLE IF NOT EXISTS metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        """
    )


def _migration_2(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS device_capabilities (
            device_serial TEXT NOT NULL,
            capability TEXT NOT NULL,
            supported INTEGER NOT NULL CHECK(supported IN (0, 1)),
            source TEXT NOT NULL,
            detected_at_utc INTEGER NOT NULL,
            PRIMARY KEY(device_serial, capability)
        );
        """
    )


def _migration_3(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS ingest_diagnostics (
            device_serial TEXT PRIMARY KEY,
            last_timestamp_utc INTEGER,
            duplicate_timestamp_count INTEGER NOT NULL DEFAULT 0,
            clock_regression_count INTEGER NOT NULL DEFAULT 0,
            short_interval_count INTEGER NOT NULL DEFAULT 0,
            long_interval_count INTEGER NOT NULL DEFAULT 0,
            updated_at_utc INTEGER NOT NULL DEFAULT 0
        );
        """
    )


def _migration_4(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS operational_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_serial TEXT NOT NULL,
            timestamp_utc INTEGER NOT NULL,
            event_type TEXT NOT NULL,
            severity TEXT NOT NULL,
            cpm INTEGER,
            details_json TEXT NOT NULL DEFAULT '{}'
        );
        CREATE INDEX IF NOT EXISTS idx_operational_events_device_timestamp
        ON operational_events(device_serial, timestamp_utc);
        """
    )


def _migration_5(connection: sqlite3.Connection) -> None:
    columns = {row[1] for row in connection.execute("PRAGMA table_info(measurements)")}
    if "tube_low_cpm" not in columns:
        connection.execute("ALTER TABLE measurements ADD COLUMN tube_low_cpm INTEGER CHECK(tube_low_cpm >= 0)")
    if "tube_high_cpm" not in columns:
        connection.execute("ALTER TABLE measurements ADD COLUMN tube_high_cpm INTEGER CHECK(tube_high_cpm >= 0)")


def _migration_6(connection: sqlite3.Connection) -> None:
    columns = {row[1] for row in connection.execute("PRAGMA table_info(measurements)")}
    if "pressure_hpa" not in columns:
        connection.execute(
            "ALTER TABLE measurements ADD COLUMN pressure_hpa REAL "
            "CHECK(pressure_hpa IS NULL OR (pressure_hpa >= 750.0 AND pressure_hpa <= 1150.0))"
        )


def _migration_7(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS raw_measurements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_serial TEXT NOT NULL,
            timestamp_utc INTEGER NOT NULL,
            cpm INTEGER NOT NULL CHECK(cpm >= 0),
            tube_low_cpm INTEGER,
            tube_high_cpm INTEGER,
            temperature_c REAL,
            voltage_v REAL,
            gyro_x INTEGER,
            gyro_y INTEGER,
            gyro_z INTEGER,
            gate_state TEXT NOT NULL,
            accepted INTEGER NOT NULL CHECK(accepted IN (0, 1)),
            raw_json TEXT NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_raw_measurements_device_timestamp
        ON raw_measurements(device_serial, timestamp_utc);
        """
    )


def _migration_8(connection: sqlite3.Connection) -> None:
    connection.executescript(
        """
        CREATE TABLE IF NOT EXISTS event_annotations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_serial TEXT,
            start_timestamp_utc INTEGER NOT NULL,
            end_timestamp_utc INTEGER NOT NULL,
            category TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('note', 'confirmed', 'dismissed')),
            note TEXT NOT NULL,
            created_at_utc INTEGER NOT NULL,
            updated_at_utc INTEGER NOT NULL
        );
        CREATE INDEX IF NOT EXISTS idx_event_annotations_time
        ON event_annotations(start_timestamp_utc, end_timestamp_utc);
        CREATE INDEX IF NOT EXISTS idx_event_annotations_device_time
        ON event_annotations(device_serial, start_timestamp_utc);
        """
    )


MIGRATIONS: dict[int, Migration] = {
    1: _migration_1,
    2: _migration_2,
    3: _migration_3,
    4: _migration_4,
    5: _migration_5,
    6: _migration_6,
    7: _migration_7,
    8: _migration_8,
}


def apply_migrations(connection: sqlite3.Connection) -> int:
    current = int(connection.execute("PRAGMA user_version").fetchone()[0])
    if current > SCHEMA_VERSION:
        raise RuntimeError(
            f"History database schema {current} is newer than supported {SCHEMA_VERSION}"
        )

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS schema_migrations (
            version INTEGER PRIMARY KEY,
            applied_at_utc TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
        )
        """
    )
    for version in range(current + 1, SCHEMA_VERSION + 1):
        migration = MIGRATIONS[version]
        migration(connection)
        connection.execute(
            "INSERT OR IGNORE INTO schema_migrations(version) VALUES (?)", (version,)
        )
        connection.execute(f"PRAGMA user_version={version}")
        connection.commit()
    return SCHEMA_VERSION
