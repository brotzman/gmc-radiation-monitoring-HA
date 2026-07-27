from __future__ import annotations

import sqlite3
import tempfile
import unittest
from contextlib import closing
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.migrations import SCHEMA_VERSION, apply_migrations


class HistoryMigrationTests(unittest.TestCase):
    def test_empty_database_reaches_current_schema_and_audit_tables(self) -> None:
        with closing(sqlite3.connect(":memory:")) as connection:
            self.assertEqual(apply_migrations(connection), SCHEMA_VERSION)
            self.assertEqual(connection.execute("PRAGMA user_version").fetchone()[0], SCHEMA_VERSION)
            tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertTrue({"measurements", "raw_measurements", "event_annotations", "calibration_history", "custom_calibration_profiles"}.issubset(tables))
            columns = {row[1] for row in connection.execute("PRAGMA table_info(measurements)")}
            self.assertTrue({"raw_cpm", "corrected_cpm", "measurement_quality_index", "derived_dose_usvh"}.issubset(columns))

    def test_device_capability_probe_uses_current_timestamp_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = HistoryStore(Path(directory) / "history.sqlite3", retention_days=3650)
            store.set_device_capabilities(
                "SERIAL-CAPABILITY",
                {"cpm": True, "temperature": False},
                source="runtime_probe",
            )
            self.assertEqual(
                store.get_device_capabilities("SERIAL-CAPABILITY"),
                {"cpm": True, "temperature": False},
            )

    def test_history_round_trip_and_ingest_diagnostics(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            store = HistoryStore(Path(directory) / "history.sqlite3", retention_days=3650)
            store.upsert_device_registry("SERIAL-A", {"device_model": "GMC-500+", "runtime_online": True, "scan_interval_seconds": 60})
            base = 1_700_000_000
            sample = {
                "cpm": 42,
                "temperature_c": 21.5,
                "voltage_v": 3.1,
                "raw_cpm": 42.0,
                "corrected_cpm": 42.2,
                "measurement_quality_index": 96,
                "derived_dose_usvh": 0.274,
            }
            store.insert_measurement(sample, device_serial="SERIAL-A", timestamp_utc=base, expected_interval_seconds=60)
            duplicate = store.insert_measurement(sample, device_serial="SERIAL-A", timestamp_utc=base, expected_interval_seconds=60)
            store.insert_measurement({**sample, "cpm": 44}, device_serial="SERIAL-A", timestamp_utc=base + 180, expected_interval_seconds=60)
            rows = store.query_range(base, base + 181, device_serial="SERIAL-A")
            self.assertEqual([row.cpm for row in rows], [42, 44])
            self.assertEqual(rows[0].measurement_quality_index, 96)
            self.assertEqual(duplicate["duplicate_timestamp_count"], 1)
            diagnostics = store.get_ingest_diagnostics(device_serial="SERIAL-A")
            self.assertEqual(diagnostics["long_interval_count"], 1)
            self.assertEqual(store.schema_version(), SCHEMA_VERSION)


if __name__ == "__main__":
    unittest.main()
