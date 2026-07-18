from __future__ import annotations

import json
import sqlite3
import sys
import tempfile
import types
import unittest
import urllib.error
import urllib.request
import zipfile
from contextlib import closing
from datetime import datetime
from http.server import ThreadingHTTPServer
from io import BytesIO
from pathlib import Path
from threading import Thread
from unittest.mock import patch

# Keep the optimization tests independent from the local availability of paho-mqtt.
try:
    import paho.mqtt.client  # type: ignore[import-not-found]
except ImportError:
    paho = types.ModuleType("paho")
    paho_mqtt = types.ModuleType("paho.mqtt")
    paho_client = types.ModuleType("paho.mqtt.client")
    paho_client.MQTT_ERR_SUCCESS = 0
    paho_mqtt.client = paho_client
    paho.mqtt = paho_mqtt
    sys.modules.setdefault("paho", paho)
    sys.modules.setdefault("paho.mqtt", paho_mqtt)
    sys.modules.setdefault("paho.mqtt.client", paho_client)

LIB_DIR = Path(__file__).parents[1] / "rootfs/usr/local/lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from gmc_bridge.analysis import data_quality_summary  # noqa: E402
from gmc_bridge.config import Settings  # noqa: E402
from gmc_bridge.device_profiles import DeviceCapabilities, resolve_device_profile  # noqa: E402
from gmc_bridge.errors import GmcTimeout  # noqa: E402
from gmc_bridge.events import (  # noqa: E402
    AnomalyThresholds,
    EventStateMachine,
    current_hysteretic_state,
)
from gmc_bridge.history import HistoryRow, HistoryStore  # noqa: E402
from gmc_bridge.maintenance import (  # noqa: E402
    diagnostics_json_bytes,
    full_history_zip_bytes,
    full_history_zip_to_path,
)
from gmc_bridge.migrations import SCHEMA_VERSION  # noqa: E402
from gmc_bridge.mqtt_pub import MqttPublisher  # noqa: E402
from gmc_bridge.report_web import (  # noqa: E402
    ReportApplication,
    ReportRequestHandler,
    _parse_multipart_form,
    _stream_restore_upload_to_temp,
)
from gmc_bridge.reports import expected_samples, load_timezone, resolve_period  # noqa: E402
from gmc_bridge.serial_device import probe_capabilities  # noqa: E402
from gmc_bridge.translations import (  # noqa: E402
    _TRANSLATIONS,
    SUPPORTED_UI_LANGUAGES,
    Translator,
    resolve_language,
)


class DeviceCompatibilityTests(unittest.TestCase):
    def test_model_profiles_recognize_major_gmc_families(self):
        cases = {
            "GMC-320Re 4.52": "gmc_300_320",
            "GMC-300E Plus": "gmc_300_320",
            "GMC-500+ 2.20": "gmc_500",
            "GMC-600 Plus": "gmc_600",
            "GMC-999 experimental": "gmc_generic",
            "RFC1201 laboratory bridge": "generic_rfc1201",
        }
        for version, expected in cases.items():
            with self.subTest(version=version):
                self.assertEqual(resolve_device_profile(version).profile_id, expected)
        self.assertTrue(resolve_device_profile("GMC-320Re 4.52").tested_with_project)
        self.assertFalse(resolve_device_profile("GMC-500+ 2.20").tested_with_project)

    def test_dual_tube_probe_hint_is_only_enabled_for_gmc_500_family(self):
        self.assertEqual(resolve_device_profile("GMC-500+ 2.20").dual_tube_hint, "yes")
        self.assertNotEqual(resolve_device_profile("GMC-320Re 4.52").dual_tube_hint, "yes")
        self.assertNotEqual(resolve_device_profile("GMC-600 Plus").dual_tube_hint, "yes")

    def test_capability_probe_recovers_after_unsupported_command_and_checks_identity(self):
        class FakeDevice:
            def __init__(self):
                self.close_calls = 0
                self.open_calls = 0
                self.version_calls = 0
                self.serial_calls = 0

            def get_temperature_c(self):
                raise GmcTimeout("temperature unsupported")

            def get_voltage_v(self):
                return 4.2

            def get_gyro(self):
                return (1, -2, -3)

            def close(self):
                self.close_calls += 1

            def open(self):
                self.open_calls += 1

            def get_version(self):
                self.version_calls += 1
                return "GMC-500+ 2.20"

            def get_serial(self):
                self.serial_calls += 1
                return "abcdef12345678"

        device = FakeDevice()
        capabilities = probe_capabilities(
            device,
            expected_serial="abcdef12345678",
            probe_gyro=True,
        )
        self.assertEqual(
            capabilities,
            DeviceCapabilities(
                cpm=True,
                temperature=False,
                voltage=True,
                gyro=True,
                gyro_probe_requested=True,
            ),
        )
        self.assertEqual(device.close_calls, 1)
        self.assertEqual(device.open_calls, 1)
        self.assertEqual(device.version_calls, 1)
        self.assertEqual(device.serial_calls, 1)

    def test_unsupported_channels_are_removed_from_mqtt_discovery(self):
        publisher = MqttPublisher.__new__(MqttPublisher)
        publisher.settings = Settings(
            port="/dev/null",
            baudrate=19200,
            scan_interval=60,
            command_timeout=2.0,
            inter_command_delay_ms=150,
            high_cpm_threshold=10000,
            high_cpm_confirmations=3,
            read_gyro=True,
            mqtt_host="localhost",
            mqtt_port=1883,
            mqtt_username="",
            mqtt_password="",
        )
        publisher.capabilities = DeviceCapabilities(
            cpm=True,
            temperature=False,
            voltage=True,
            gyro=False,
            gyro_probe_requested=True,
        )
        publisher.serial = "abcdef12345678"
        publisher.version = "GMC-500+ 2.20"
        publisher.node_id = "gmc_abcdef12345678"
        base = "gmc/abcdef12345678"
        publisher.state_topic = f"{base}/state"
        publisher.diagnostics_topic = f"{base}/diagnostics"
        publisher.device_availability_topic = f"{base}/device_availability"
        publisher.availability_topics = {
            "cpm": f"{base}/availability",
            "temperature": f"{base}/temperature_availability",
            "voltage": f"{base}/voltage_availability",
            "gyro": f"{base}/gyro_availability",
        }

        messages = dict(publisher._discovery_messages())
        self.assertEqual(messages[publisher._discovery_topic("temperature")], "")
        self.assertEqual(messages[publisher._discovery_topic("gyro_x")], "")
        self.assertNotEqual(messages[publisher._discovery_topic("voltage")], "")
        self.assertNotEqual(messages[publisher._discovery_topic("cpm")], "")


class MigrationAndHistoryMaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_existing_schema_v1_is_migrated_to_current_without_losing_measurements(self):
        path = self.base / "legacy.sqlite3"
        connection = sqlite3.connect(path)
        connection.executescript(
            """
            CREATE TABLE measurements (
                device_serial TEXT NOT NULL,
                timestamp_utc INTEGER NOT NULL,
                cpm INTEGER NOT NULL,
                temperature_c REAL,
                voltage_v REAL,
                gyro_x INTEGER,
                gyro_y INTEGER,
                gyro_z INTEGER,
                cpm_quality TEXT NOT NULL,
                PRIMARY KEY(device_serial, timestamp_utc)
            );
            CREATE TABLE metadata (key TEXT PRIMARY KEY, value TEXT NOT NULL);
            INSERT INTO metadata(key, value) VALUES ('serial', 'legacy-device');
            INSERT INTO measurements VALUES ('legacy-device', 1700000000, 17, 26.8, 4.2, NULL, NULL, NULL, 'normal');
            PRAGMA user_version=1;
            """
        )
        connection.commit()
        connection.close()

        store = HistoryStore(path)
        self.assertEqual(store.schema_version(), SCHEMA_VERSION)
        self.assertEqual(store.count(), 1)
        self.assertEqual(store.query_all()[0].cpm, 17)
        with closing(sqlite3.connect(path)) as migrated:
            tables = {row[0] for row in migrated.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        self.assertIn("device_capabilities", tables)
        self.assertIn("ingest_diagnostics", tables)
        self.assertIn("schema_migrations", tables)

    def test_backup_restore_is_an_integrity_checked_merge(self):
        source = HistoryStore(self.base / "source.sqlite3")
        source.set_metadata({"serial": "device-a", "device_model": "GMC Test"})
        source.set_device_capabilities("device-a", {"cpm": True, "temperature": True})
        source.insert_measurement(
            {"cpm": 11, "temperature_c": 24.0},
            timestamp_utc=1_700_000_000,
        )
        backup = source.backup_bytes()

        target = HistoryStore(self.base / "target.sqlite3")
        target.set_metadata({"serial": "device-a"})
        target.insert_measurement({"cpm": 22}, timestamp_utc=1_700_000_060)
        result = target.restore_backup_bytes(backup)

        self.assertEqual(result["source_schema_version"], SCHEMA_VERSION)
        self.assertEqual(target.integrity_check(), "ok")
        self.assertEqual([row.cpm for row in target.query_all()], [11, 22])
        self.assertTrue(target.get_device_capabilities("device-a")["temperature"])

        with self.assertRaises(ValueError):
            target.restore_backup_bytes(b"not a sqlite database")

    def test_full_history_archive_contains_sqlite_csv_and_metadata(self):
        store = HistoryStore(self.base / "history.sqlite3")
        store.set_metadata({"serial": "device-a", "app_version": "2.0"})
        store.insert_measurement({"cpm": 12}, timestamp_utc=1_700_000_000)
        payload = full_history_zip_bytes(store)
        with zipfile.ZipFile(BytesIO(payload)) as archive:
            self.assertEqual(
                set(archive.namelist()),
                {
                    "gmc_history.sqlite3",
                    "gmc_history.csv",
                    "gmc_raw_history.csv",
                    "gmc_history.metadata.json",
                },
            )
            self.assertIn(b"device_serial,timestamp_utc,cpm", archive.read("gmc_history.csv"))
            self.assertIn(b"raw_id,device_serial,timestamp_utc,cpm", archive.read("gmc_raw_history.csv"))
            metadata = json.loads(archive.read("gmc_history.metadata.json"))
            self.assertEqual(metadata["database"]["integrity"], "ok")

    def test_full_history_archive_can_be_built_directly_to_disk(self):
        store = HistoryStore(self.base / "history-streamed.sqlite3")
        store.set_metadata({"serial": "device-a"})
        for index in range(2500):
            store.insert_measurement({"cpm": 10 + index % 5}, timestamp_utc=1_700_000_000 + index)
        output_path = self.base / "history-streamed.zip"
        self.assertEqual(full_history_zip_to_path(store, output_path), output_path)
        with zipfile.ZipFile(output_path) as archive:
            self.assertIn("gmc_history.sqlite3", archive.namelist())
            self.assertGreater(len(archive.read("gmc_history.csv")), 100_000)

    def test_database_stats_cache_quick_check_and_skip_integrity_check(self):
        store = HistoryStore(self.base / "quick-check.sqlite3")
        with (
            patch.object(store, "quick_check", wraps=store.quick_check) as quick_check,
            patch.object(store, "integrity_check", side_effect=AssertionError("must not run")),
        ):
            first = store.database_stats()
            second = store.database_stats()
        self.assertEqual(first["integrity"], "ok")
        self.assertEqual(first["check_type"], "quick_check")
        self.assertEqual(second["integrity"], "ok")
        self.assertEqual(quick_check.call_count, 1)

    def test_ingest_diagnostics_detect_duplicate_clock_regression_and_interval_anomalies(self):
        store = HistoryStore(self.base / "diagnostics.sqlite3")
        store.set_metadata({"serial": "device-a"})
        store.insert_measurement({"cpm": 10}, timestamp_utc=1000, expected_interval_seconds=60)
        store.insert_measurement({"cpm": 11}, timestamp_utc=1000, expected_interval_seconds=60)
        store.insert_measurement({"cpm": 12}, timestamp_utc=900, expected_interval_seconds=60)
        store.insert_measurement({"cpm": 13}, timestamp_utc=1020, expected_interval_seconds=60)
        store.insert_measurement({"cpm": 14}, timestamp_utc=1200, expected_interval_seconds=60)
        diagnostics = store.get_ingest_diagnostics()
        self.assertEqual(diagnostics["duplicate_timestamp_count"], 1)
        self.assertEqual(diagnostics["clock_regression_count"], 1)
        self.assertEqual(diagnostics["short_interval_count"], 1)
        self.assertEqual(diagnostics["long_interval_count"], 1)

    def test_diagnostics_export_excludes_credentials(self):
        store = HistoryStore(self.base / "privacy.sqlite3")
        store.set_metadata(
            {
                "serial": "device-a",
                "app_version": "2.0",
                "mqtt_password": "super-secret",
                "mqtt_username": "private-user",
                "serial_error_count": "2",
            }
        )
        payload = diagnostics_json_bytes(store)
        self.assertNotIn(b"super-secret", payload)
        self.assertNotIn(b"private-user", payload)
        document = json.loads(payload)
        self.assertEqual(document["runtime"]["serial_error_count"], "2")
        self.assertIn("No MQTT password", document["privacy_note"])


class DataQualityAndTimeTests(unittest.TestCase):
    @staticmethod
    def _row(timestamp: int, cpm: int = 14) -> HistoryRow:
        return HistoryRow(
            device_serial="device-a",
            timestamp_utc=timestamp,
            cpm=cpm,
            temperature_c=None,
            voltage_v=None,
            gyro_x=None,
            gyro_y=None,
            gyro_z=None,
            cpm_quality="normal",
        )

    def test_data_quality_explains_timestamp_and_gap_problems(self):
        rows = [self._row(1000), self._row(1060), self._row(1240)]
        quality = data_quality_summary(
            rows,
            expected_count=4,
            scan_interval_seconds=60,
            ingest_diagnostics={
                "duplicate_timestamp_count": 1,
                "clock_regression_count": 1,
                "short_interval_count": 0,
                "long_interval_count": 1,
            },
            capabilities={"temperature": False, "voltage": False},
        )
        self.assertLess(quality["score"], 75.0)
        self.assertIn(quality["label"], {"Limited", "Poor"})
        reason_text = " | ".join(quality["reasons"])
        self.assertIn("coverage", reason_text)
        self.assertIn("longest gap", reason_text)
        self.assertIn("duplicate timestamps", reason_text)
        self.assertIn("clock regressions", reason_text)
        # Unsupported optional sensors must not reduce the quality score.
        self.assertNotIn("temperature coverage", reason_text)
        self.assertNotIn("voltage coverage", reason_text)

    def test_dst_days_have_23_and_25_hours_without_local_time_ambiguity(self):
        tz = load_timezone("Europe/Berlin")
        spring = resolve_period(
            kind="daily",
            selection="specific",
            tz=tz,
            date_value="2025-03-30",
            now=datetime(2025, 4, 1, tzinfo=tz),
        )
        autumn = resolve_period(
            kind="daily",
            selection="specific",
            tz=tz,
            date_value="2025-10-26",
            now=datetime(2025, 11, 1, tzinfo=tz),
        )
        self.assertEqual(expected_samples(spring, 60), 23 * 60)
        self.assertEqual(expected_samples(autumn, 60), 25 * 60)
        self.assertLess(spring.start_utc, spring.end_utc)
        self.assertLess(autumn.start_utc, autumn.end_utc)


class HysteresisTests(unittest.TestCase):
    def test_state_machine_prevents_threshold_flapping(self):
        thresholds = AnomalyThresholds.from_enter_thresholds(125.0, 175.0)
        machine = EventStateMachine(thresholds)
        self.assertEqual(machine.update(126.0), "yellow")
        self.assertEqual(machine.update(120.0), "yellow")
        self.assertEqual(machine.update(115.0), "yellow")
        self.assertEqual(machine.update(114.9), "normal")
        self.assertEqual(machine.update(180.0), "red")
        self.assertEqual(machine.update(165.0), "red")
        self.assertEqual(machine.update(159.9), "yellow")
        self.assertEqual(machine.update(114.9), "normal")

    def test_current_state_uses_complete_recent_sequence(self):
        self.assertEqual(
            current_hysteretic_state([100.0, 130.0, 120.0], yellow=125.0, red=175.0),
            "yellow",
        )
        self.assertEqual(
            current_hysteretic_state([], yellow=125.0, red=175.0),
            "learning",
        )


class UiAndTranslationTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store = HistoryStore(Path(self.temp_dir.name) / "ui.sqlite3")
        self.store.set_metadata(
            {
                "serial": "device-a",
                "device_model": "GMC-320Re 4.52",
                "device_profile_name": "GMC-300/320 family",
            }
        )
        self.store.set_device_capabilities(
            "device-a", {"cpm": True, "temperature": True, "voltage": True, "gyro": False}
        )
        for index in range(12):
            self.store.insert_measurement(
                {"cpm": 14, "temperature_c": 26.0, "voltage_v": 4.2},
                timestamp_utc=1_800_000_000 + index * 60,
                expected_interval_seconds=60,
            )

    def tearDown(self):
        self.temp_dir.cleanup()

    def _app(self, **kwargs):
        return ReportApplication(
            store=self.store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
            **kwargs,
        )

    def test_simple_and_advanced_modes_have_distinct_analysis_depth(self):
        app = self._app(ui_mode="simple")
        simple = app.render_index().decode("utf-8")
        advanced = app.render_index(mode_override="advanced").decode("utf-8")
        self.assertIn('body class="mode-simple"', simple)
        self.assertIn('body class="mode-advanced"', advanced)
        self.assertIn('data-analysis-level="summary"', simple)
        self.assertIn('data-analysis-level="analysis"', advanced)
        self.assertIn("Counting statistics", simple)
        self.assertIn("Counting statistics", advanced)
        self.assertIn('data-analysis-level="expert"', simple)
        self.assertIn('class="advanced-only history-management-section" id="maintenance"', simple)
        self.assertIn(
            'body[data-analysis-level="summary"] .advanced-only { display:none !important; }', simple
        )
        self.assertIn("History management", advanced)

    def test_language_auto_detection_and_override(self):
        app = self._app(ui_language="auto")
        german = app.render_index(accept_language="de-DE,de;q=0.9,en;q=0.8").decode("utf-8")
        french = app.render_index(language_override="fr").decode("utf-8")
        self.assertIn("GMC-Strahlungsüberwachung", german)
        self.assertIn("Datenqualität", german)
        self.assertIn("Surveillance du rayonnement GMC", french)
        self.assertEqual(resolve_language("auto", accept_language="pl-PL"), "pl")
        self.assertEqual(resolve_language("invalid", accept_language="de"), "en")
        self.assertEqual(set(SUPPORTED_UI_LANGUAGES), {"en", "de", "fr", "es", "it", "nl", "pl", "hr"})
        self.assertEqual(Translator("de")("Restore history"), "Historie wiederherstellen")

    def test_mobile_dashboard_reflows_analysis_without_page_horizontal_scrolling(self):
        rendered = self._app().render_index(mode_override="advanced").decode("utf-8")
        self.assertIn("overflow-x: hidden;", rendered)
        self.assertIn("touch-action: pan-y;", rendered)
        self.assertIn(
            ".assessment-grid, .assessment-grid.baseline-grid { grid-template-columns:1fr; }", rendered
        )
        self.assertIn(".table-wrap { overflow-x: auto;", rendered)
        self.assertNotIn(".control-options { overflow-x:auto;", rendered)

    def test_german_analysis_details_are_fully_localized(self):
        rendered = (
            self._app(ui_language="de")
            .render_index(language_override="de", mode_override="advanced")
            .decode("utf-8")
        )
        for translated in (
            "Abdeckung",
            "gegenüber lokaler Baseline",
            "Anhaltende gelbe/rote relative Anomalieereignisse",
            "Keine anhaltenden relativen Anomalieereignisse erkannt",
            "Aus dem letzten CPM-Wert abgeleitet",
        ):
            self.assertIn(translated, rendered)
        for untranslated in (
            "% coverage",
            "vs local baseline",
            "Sustained yellow/red relative anomaly events",
            "No sustained relative anomaly events detected",
            "Derived from latest CPM",
            ">Poor<",
        ):
            self.assertNotIn(untranslated, rendered)

    def test_primary_ui_translation_catalogue_is_complete(self):
        import ast

        report_web = Path(__file__).parents[1] / "rootfs/usr/local/lib/gmc_bridge/report_web.py"
        tree = ast.parse(report_web.read_text(encoding="utf-8"))
        ui_keys = {
            node.args[0].value
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "t"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        }
        for language in SUPPORTED_UI_LANGUAGES:
            if language == "en":
                continue
            missing = sorted(ui_keys - set(_TRANSLATIONS[language]))
            self.assertEqual(missing, [], f"missing {language} translations: {missing}")

    def test_multipart_restore_parser_preserves_binary_sqlite_payload(self):
        boundary = "----gmc-test-boundary"
        binary = b"SQLite format 3\x00\r\n\xff\x00payload"
        body = (
            (
                f"--{boundary}\r\n"
                'Content-Disposition: form-data; name="confirm"\r\n\r\n'
                "RESTORE\r\n"
                f"--{boundary}\r\n"
                'Content-Disposition: form-data; name="backup"; filename="history.sqlite3"\r\n'
                "Content-Type: application/vnd.sqlite3\r\n\r\n"
            ).encode("ascii")
            + binary
            + f"\r\n--{boundary}--\r\n".encode("ascii")
        )
        fields = _parse_multipart_form(
            f"multipart/form-data; boundary={boundary}",
            body,
        )
        self.assertEqual(fields["confirm"], b"RESTORE")
        self.assertEqual(fields["backup"], binary)

    def test_streaming_restore_parser_writes_backup_to_temp_file(self):
        boundary = "----gmc-streaming-boundary"
        binary = b"SQLite format 3\x00" + (b"payload\r\n" * 200_000)
        body = (
            (
                f"--{boundary}\r\n"
                'Content-Disposition: form-data; name="confirm"\r\n\r\n'
                "RESTORE\r\n"
                f"--{boundary}\r\n"
                'Content-Disposition: form-data; name="csrf_token"\r\n\r\n'
                "test-csrf-token\r\n"
                f"--{boundary}\r\n"
                'Content-Disposition: form-data; name="backup"; filename="history.sqlite3"\r\n'
                "Content-Type: application/vnd.sqlite3\r\n\r\n"
            ).encode("ascii")
            + binary
            + f"\r\n--{boundary}--\r\n".encode("ascii")
        )
        confirm, csrf_token, backup_path = _stream_restore_upload_to_temp(
            f"multipart/form-data; boundary={boundary}",
            BytesIO(body),
            content_length=len(body),
        )
        try:
            self.assertEqual(confirm, "RESTORE")
            self.assertEqual(csrf_token, "test-csrf-token")
            self.assertEqual(backup_path.read_bytes(), binary)
        finally:
            backup_path.unlink(missing_ok=True)


class MaintenanceRouteTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.store = HistoryStore(Path(self.temp_dir.name) / "web.sqlite3")
        self.store.set_metadata({"serial": "device-a", "device_model": "GMC Test", "app_version": "2.0"})
        self.store.insert_measurement({"cpm": 14}, timestamp_utc=1_800_000_000)
        app = ReportApplication(
            store=self.store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
            ui_mode="advanced",
            restore_enabled=True,
        )
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
        self.server.app = app
        self.thread = Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp_dir.cleanup()

    def test_restore_route_is_forbidden_when_disabled(self):
        self.server.app.restore_enabled = False
        request = urllib.request.Request(
            f"{self.base_url}/restore",
            data=b"not parsed while disabled",
            method="POST",
            headers={"Content-Type": "application/octet-stream"},
        )
        with self.assertRaises(urllib.error.HTTPError) as context:
            urllib.request.urlopen(request, timeout=5)
        self.assertEqual(context.exception.code, 403)
        self.server.app.restore_enabled = True

    def test_restore_route_merges_valid_backup(self):
        source = HistoryStore(Path(self.temp_dir.name) / "source-restore.sqlite3")
        source.set_metadata({"serial": "device-a"})
        source.insert_measurement({"cpm": 19}, timestamp_utc=1_800_000_060)
        backup = source.backup_bytes()
        boundary = "----gmc-http-restore"
        csrf_token = self.server.app.csrf_tokens.issue("restore")
        body = (
            (
                f"--{boundary}\r\n"
                'Content-Disposition: form-data; name="confirm"\r\n\r\n'
                "RESTORE\r\n"
                f"--{boundary}\r\n"
                'Content-Disposition: form-data; name="csrf_token"\r\n\r\n'
                f"{csrf_token}\r\n"
                f"--{boundary}\r\n"
                'Content-Disposition: form-data; name="backup"; filename="history.sqlite3"\r\n'
                "Content-Type: application/vnd.sqlite3\r\n\r\n"
            ).encode("ascii")
            + backup
            + f"\r\n--{boundary}--\r\n".encode("ascii")
        )
        request = urllib.request.Request(
            f"{self.base_url}/restore",
            data=body,
            method="POST",
            headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            page = response.read().decode("utf-8")
            self.assertEqual(response.status, 200)
            self.assertIn("Restore complete", page)
        self.assertEqual([row.cpm for row in self.store.query_all()], [14, 19])

    def test_maintenance_exports_share_the_report_semaphore(self):
        self.assertTrue(self.server.app.report_slot.acquire(blocking=False))
        try:
            with self.assertRaises(urllib.error.HTTPError) as context:
                urllib.request.urlopen(f"{self.base_url}/history-export", timeout=5)
            self.assertEqual(context.exception.code, 429)
        finally:
            self.server.app.report_slot.release()

    def test_ingress_safe_action_routes(self):
        with urllib.request.urlopen(f"{self.base_url}/?action=database-backup", timeout=5) as response:
            backup = response.read()
            self.assertEqual(response.headers.get_content_type(), "application/vnd.sqlite3")
            self.assertTrue(backup.startswith(b"SQLite format 3\x00"))

        with urllib.request.urlopen(f"{self.base_url}/?action=history-export", timeout=5) as response:
            archive_payload = response.read()
            self.assertEqual(response.headers.get_content_type(), "application/zip")
            with zipfile.ZipFile(BytesIO(archive_payload)) as archive:
                self.assertIn("gmc_history.sqlite3", archive.namelist())

        with urllib.request.urlopen(f"{self.base_url}/?action=diagnostics", timeout=5) as response:
            diagnostics = json.loads(response.read())
            self.assertEqual(response.headers.get_content_type(), "application/json")
            self.assertEqual(diagnostics["database"]["integrity"], "ok")

    def test_ingress_safe_restore_action_is_forbidden_when_disabled(self):
        self.server.app.restore_enabled = False
        request = urllib.request.Request(
            f"{self.base_url}/?action=restore",
            data=b"not parsed while disabled",
            method="POST",
            headers={"Content-Type": "application/octet-stream"},
        )
        with self.assertRaises(urllib.error.HTTPError) as context:
            urllib.request.urlopen(request, timeout=5)
        self.assertEqual(context.exception.code, 403)
        self.server.app.restore_enabled = True

    def test_backup_history_and_diagnostics_routes(self):
        with urllib.request.urlopen(f"{self.base_url}/database-backup", timeout=5) as response:
            backup = response.read()
            self.assertEqual(response.headers.get_content_type(), "application/vnd.sqlite3")
            self.assertTrue(backup.startswith(b"SQLite format 3\x00"))

        with urllib.request.urlopen(f"{self.base_url}/history-export", timeout=5) as response:
            archive_payload = response.read()
            self.assertEqual(response.headers.get_content_type(), "application/zip")
            with zipfile.ZipFile(BytesIO(archive_payload)) as archive:
                self.assertIn("gmc_history.sqlite3", archive.namelist())

        with urllib.request.urlopen(f"{self.base_url}/diagnostics.json", timeout=5) as response:
            diagnostics = json.loads(response.read())
            self.assertEqual(response.headers.get_content_type(), "application/json")
            self.assertEqual(diagnostics["database"]["integrity"], "ok")


if __name__ == "__main__":
    unittest.main()
