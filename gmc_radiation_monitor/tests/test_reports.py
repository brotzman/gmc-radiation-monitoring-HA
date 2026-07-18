from __future__ import annotations

import csv
import io
import json
import sys
import tempfile
import threading
import unittest
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from pypdf import PdfReader

LIB_DIR = Path(__file__).parents[1] / "rootfs/usr/local/lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from gmc_bridge.history import HistoryStore  # noqa: E402
from gmc_bridge.report_web import ReportApplication, ReportRequestHandler  # noqa: E402
from gmc_bridge.reports import (  # noqa: E402
    build_live_analysis,
    build_report,
    build_statistics,
    csv_bytes,
    daily_summary_csv_bytes,
    data_quality_summary,
    detect_events,
    events_csv_bytes,
    expected_samples,
    heatmap_png_bytes,
    histogram_png_bytes,
    load_timezone,
    resolve_period,
)


class HistoryStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "history.sqlite3"
        self.store = HistoryStore(self.db_path, retention_days=90)
        self.store.set_metadata({"serial": "test-serial", "device_model": "GMC Test"})

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_insert_query_metadata_and_prune(self):
        self.store.set_metadata({"serial": "abc123", "device_model": "GMC Test"})
        self.store.insert_measurement(
            {"cpm": 12, "temperature_c": 26.8, "voltage_v": 4.2},
            timestamp_utc=1_700_000_000,
        )
        rows = self.store.query_range(1_699_999_999, 1_700_000_001)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].cpm, 12)
        self.assertEqual(rows[0].temperature_c, 26.8)
        self.assertEqual(self.store.get_metadata()["serial"], "abc123")
        self.assertEqual(self.store.prune(now_utc=1_800_000_000), 1)
        self.assertEqual(self.store.count(), 0)

    def test_same_timestamp_updates_instead_of_duplicating(self):
        self.store.insert_measurement({"cpm": 10}, timestamp_utc=1_700_000_000)
        self.store.insert_measurement({"cpm": 11}, timestamp_utc=1_700_000_000)
        rows = self.store.query_range(1_699_999_999, 1_700_000_001)
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].cpm, 11)

    def test_history_is_isolated_by_device_serial(self):
        timestamp = 1_700_000_000
        self.store.insert_measurement({"cpm": 10}, device_serial="serial-a", timestamp_utc=timestamp)
        self.store.insert_measurement({"cpm": 20}, device_serial="serial-b", timestamp_utc=timestamp)
        self.store.set_metadata({"serial": "serial-b"})
        rows = self.store.query_range(timestamp - 1, timestamp + 1)
        self.assertEqual([row.cpm for row in rows], [20])
        self.assertEqual(self.store.count(), 1)
        self.store.set_metadata({"serial": "serial-a"})
        rows = self.store.query_range(timestamp - 1, timestamp + 1)
        self.assertEqual([row.cpm for row in rows], [10])

    def test_operational_event_methods_are_available_and_persist_events(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            store = HistoryStore(Path(temp_dir) / "history.sqlite3")
            store.set_metadata({"serial": "TEST-SERIAL"})
            event = {
                "timestamp_utc": 1_700_000_000,
                "event_type": "rapid_rise",
                "severity": "warning",
                "cpm": 123,
                "details": {"rise_percent": 55.0},
            }
            store.insert_operational_event(event, device_serial="TEST-SERIAL")
            rows = store.recent_operational_events(device_serial="TEST-SERIAL")
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["event_type"], "rapid_rise")
            self.assertEqual(rows[0]["cpm"], 123)
            self.assertEqual(rows[0]["details"]["rise_percent"], 55.0)


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp_dir.name) / "history.sqlite3"
        self.store = HistoryStore(self.db_path, retention_days=90)
        self.store.set_metadata(
            {
                "serial": "f488c59b0031f0",
                "device_model": "GMC-320Re 4.52",
                "app_version": "2.0",
            }
        )
        self.tz = load_timezone("Europe/Berlin")
        self.period = resolve_period(
            kind="daily",
            selection="specific",
            tz=self.tz,
            date_value="2026-01-15",
            now=datetime(2026, 1, 20, 12, tzinfo=self.tz),
        )
        start = int(self.period.start_utc.timestamp())
        for offset, cpm in enumerate((10, 20, 15)):
            self.store.insert_measurement(
                {
                    "cpm": cpm,
                    "temperature_c": 26.5 + offset / 10,
                    "voltage_v": 4.2,
                    "gyro_x": 27 + offset,
                    "gyro_y": -5,
                    "gyro_z": -236,
                },
                timestamp_utc=start + offset * 60,
            )

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_daily_and_weekly_period_resolution(self):
        daily = resolve_period(
            kind="daily",
            selection="specific",
            tz=self.tz,
            date_value="2026-03-29",
            now=datetime(2026, 4, 1, tzinfo=self.tz),
        )
        self.assertEqual(expected_samples(daily, 60), 23 * 60)
        weekly = resolve_period(
            kind="weekly",
            selection="specific",
            tz=self.tz,
            week_value="2026-W03",
            now=datetime(2026, 2, 1, tzinfo=self.tz),
        )
        self.assertEqual(weekly.start_local.weekday(), 0)
        self.assertEqual((weekly.end_local.date() - weekly.start_local.date()).days, 7)

    def test_statistics_are_scientifically_reproducible(self):
        rows = self.store.query_range(
            int(self.period.start_utc.timestamp()), int(self.period.end_utc.timestamp())
        )
        stats = build_statistics(rows, expected_count=1440)
        self.assertEqual(stats["cpm_min"], 10.0)
        self.assertEqual(stats["cpm_max"], 20.0)
        self.assertEqual(stats["cpm_mean"], 15.0)
        self.assertEqual(stats["cpm_median"], 15.0)
        self.assertEqual(stats["missing_samples"], 1437)

    def test_live_analysis_calculates_rolling_scientific_metrics(self):
        start = int(self.period.start_utc.timestamp())
        # Replace the tiny fixture with a stable one-hour Poisson-like sequence.
        for offset, cpm in enumerate([10, 14, 18, 14] * 15):
            self.store.insert_measurement(
                {"cpm": cpm},
                timestamp_utc=start + 3600 + offset * 60,
            )
        analysis = build_live_analysis(self.store, scan_interval_seconds=60)
        self.assertTrue(analysis["available"])
        self.assertEqual(analysis["latest_cpm"], 14.0)
        self.assertEqual(analysis["samples_1h"], 60)
        self.assertAlmostEqual(analysis["mean_1h"], 14.0)
        self.assertIsNotNone(analysis["sd_24h"])
        self.assertIsNotNone(analysis["median_24h"])
        self.assertIsNotNone(analysis["p99_24h"])
        self.assertEqual(analysis["min_24h"], 10.0)
        self.assertEqual(analysis["max_24h"], 20.0)
        self.assertIsNotNone(analysis["z_score_24h"])
        self.assertIsNotNone(analysis["fano_factor_24h"])
        self.assertIsNotNone(analysis["poisson_sd_ratio_24h"])
        self.assertIsNotNone(analysis["background_index_percent"])

    def test_live_analysis_correlations_use_paired_samples_and_handle_constant_sensor(self):
        correlation_store = HistoryStore(Path(self.temp_dir.name) / "correlation.sqlite3", retention_days=90)
        correlation_store.set_metadata({"serial": "correlation-test"})
        start = int(self.period.start_utc.timestamp()) + 10_000
        for offset, cpm in enumerate((10, 12, 14, 16, 18)):
            correlation_store.insert_measurement(
                {
                    "cpm": cpm,
                    "temperature_c": 20.0 + cpm / 10.0,
                    "voltage_v": 4.2,
                },
                timestamp_utc=start + offset * 60,
            )
        analysis = build_live_analysis(correlation_store, scan_interval_seconds=60)
        self.assertAlmostEqual(analysis["temperature_correlation_24h"], 1.0)
        self.assertEqual(analysis["temperature_correlation_status_24h"], "ok")
        self.assertEqual(analysis["temperature_pairs_24h"], 5)
        self.assertIsNone(analysis["voltage_correlation_24h"])
        self.assertEqual(analysis["voltage_correlation_status_24h"], "no sensor variation")

    def test_ingress_page_has_ios_touch_scroll_container(self):
        app = ReportApplication(
            store=self.store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=True,
            cpm_per_usvh=154.0,
        )
        page = app.render_index().decode("utf-8")
        self.assertIn("viewport-fit=cover", page)
        self.assertIn('class="page-scroll"', page)
        self.assertIn("overflow-y: auto", page)
        self.assertIn("-webkit-overflow-scrolling: touch", page)
        self.assertIn("touch-action: pan-y", page)
        self.assertIn("overflow-x: hidden", page)
        self.assertIn("safe-area-inset-bottom", page)

    def test_analysis_page_derives_dose_rate_from_configured_factor(self):
        app = ReportApplication(
            store=self.store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=True,
            cpm_per_usvh=154.0,
        )
        page = app.render_index().decode("utf-8")
        self.assertIn("Latest dose rate", page)
        self.assertIn("0.097 µSv/h", page)
        self.assertIn("154 CPM per µSv/h", page)
        self.assertIn("not independently measured", page)

    def test_traffic_light_green_yellow_red_and_learning_states(self):
        app = ReportApplication(
            store=self.store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=True,
            cpm_per_usvh=154.0,
            traffic_light_yellow_percent=125.0,
            traffic_light_red_percent=175.0,
        )
        base = {
            "background_index_percent": 100.0,
            "samples_7d": 400,
            "coverage_1h_percent": 100.0,
        }
        self.assertIn('data-state="green"', app._render_traffic_light(base))
        self.assertIn("Within local background range", app._render_traffic_light(base))

        elevated = dict(base, background_index_percent=140.0)
        self.assertIn('data-state="yellow"', app._render_traffic_light(elevated))

        high = dict(base, background_index_percent=190.0)
        self.assertIn('data-state="red"', app._render_traffic_light(high))

        learning = dict(base, samples_7d=10)
        learning_html = app._render_traffic_light(learning)
        self.assertIn('data-state="learning"', learning_html)
        self.assertIn("Learning baseline", learning_html)
        self.assertIn("Baseline readiness", learning_html)
        self.assertIn("6 h minimum sample coverage", learning_html)

    def test_live_analysis_empty_history_is_safe(self):
        empty_store = HistoryStore(Path(self.temp_dir.name) / "empty.sqlite3", retention_days=90)
        analysis = build_live_analysis(empty_store, scan_interval_seconds=60)
        self.assertFalse(analysis["available"])
        self.assertIsNone(analysis["latest_cpm"])

    def test_csv_preserves_raw_resolution_and_missing_values(self):
        rows = self.store.query_range(
            int(self.period.start_utc.timestamp()), int(self.period.end_utc.timestamp())
        )
        payload = csv_bytes(rows, ZoneInfo("Europe/Berlin"))
        parsed = list(csv.DictReader(io.StringIO(payload.decode("utf-8"))))
        self.assertEqual(len(parsed), 3)
        self.assertEqual(parsed[0]["cpm"], "10")
        self.assertIn("+01:00", parsed[0]["timestamp_local"])
        self.assertEqual(parsed[0]["gyro_z"], "-236")

    def test_png_report_is_valid_png(self):
        filename, content_type, payload = build_report(
            self.store,
            period=self.period,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            output_format="png",
        )
        self.assertTrue(filename.endswith(".png"))
        self.assertEqual(content_type, "image/png")
        self.assertTrue(payload.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertGreater(len(payload), 10_000)

    def test_empty_period_still_generates_a_valid_png(self):
        empty_period = resolve_period(
            kind="daily",
            selection="specific",
            tz=self.tz,
            date_value="2025-01-01",
            now=datetime(2026, 1, 20, 12, tzinfo=self.tz),
        )
        _, content_type, payload = build_report(
            self.store,
            period=empty_period,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            output_format="png",
        )
        self.assertEqual(content_type, "image/png")
        self.assertTrue(payload.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_zip_bundle_contains_png_csv_and_metadata(self):
        filename, content_type, payload = build_report(
            self.store,
            period=self.period,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            output_format="zip",
        )
        self.assertTrue(filename.endswith(".zip"))
        self.assertEqual(content_type, "application/zip")
        with zipfile.ZipFile(io.BytesIO(payload)) as archive:
            names = archive.namelist()
            self.assertEqual(sum(name.endswith(".png") for name in names), 3)
            self.assertEqual(sum(name.endswith(".csv") for name in names), 5)
            self.assertTrue(any(name.endswith("annotations.csv") for name in names))
            self.assertEqual(sum(name.endswith(".pdf") for name in names), 1)
            self.assertEqual(sum(name.endswith("analysis.json") for name in names), 1)
            metadata_name = next(name for name in names if name.endswith("metadata.json"))
            metadata = json.loads(archive.read(metadata_name))
        self.assertEqual(metadata["serial"], "f488c59b0031f0")
        self.assertEqual(metadata["samples"], 3)
        self.assertEqual(metadata["timezone"], "Europe/Berlin")

    def test_data_quality_and_daily_summary_exports(self):
        rows = self.store.query_range(
            int(self.period.start_utc.timestamp()), int(self.period.end_utc.timestamp())
        )
        quality = data_quality_summary(rows, expected_count=3, scan_interval_seconds=60)
        self.assertEqual(quality["label"], "Excellent")
        self.assertEqual(quality["longest_gap_seconds"], 60)
        payload = daily_summary_csv_bytes(rows, tz=self.tz, scan_interval_seconds=60)
        text = payload.decode("utf-8")
        self.assertIn("data_quality", text)
        self.assertIn("2026-01-15", text)

    def test_event_export_detects_sustained_relative_anomaly(self):
        event_store = HistoryStore(Path(self.temp_dir.name) / "events.sqlite3", retention_days=90)
        event_store.set_metadata({"serial": "events"})
        start = int(self.period.start_utc.timestamp())
        for offset in range(20):
            event_store.insert_measurement({"cpm": 30}, timestamp_utc=start + offset * 60)
        rows = event_store.query_range(start, start + 3600)
        events = detect_events(
            rows,
            baseline_mean=10.0,
            yellow_percent=125.0,
            red_percent=175.0,
            scan_interval_seconds=60,
        )
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["severity"], "red")
        csv_payload = events_csv_bytes(events, self.tz)
        self.assertIn(b"max_background_index_percent", csv_payload)

    def test_histogram_and_heatmap_are_valid_pngs(self):
        rows = self.store.query_range(
            int(self.period.start_utc.timestamp()), int(self.period.end_utc.timestamp())
        )
        histogram = histogram_png_bytes(rows, title=self.period.label)
        heatmap = heatmap_png_bytes(rows, tz=self.tz, title=self.period.label)
        self.assertTrue(histogram.startswith(b"\x89PNG\r\n\x1a\n"))
        self.assertTrue(heatmap.startswith(b"\x89PNG\r\n\x1a\n"))

    def test_professional_pdf_has_five_pages_and_unit_correct_beta_gamma_labels(self):
        _name, _content_type, payload = build_report(
            self.store,
            period=self.period,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            output_format="pdf",
            language="de",
        )
        reader = PdfReader(io.BytesIO(payload))
        self.assertEqual(len(reader.pages), 5)
        text = "\n".join(page.extract_text() or "" for page in reader.pages)
        self.assertIn("Beta-/Gamma-Strahlungsbericht", text)
        self.assertIn("Zählrate [CPM]", text)
        self.assertIn("Lokale Zeit [Europe/Berlin]", text)
        self.assertIn("Akzeptierte Messwerte [Anzahl]", text)
        self.assertIn("Mittlere Zählrate [CPM]", text)
        self.assertIn("Statistische Analyse und Ereignisse", text)
        self.assertIn("Methodischer Hinweis", text)
        self.assertNotIn("Bq/m", text)

    def test_advanced_download_formats(self):
        for output_format, prefix in (
            ("analysis-json", b"{"),
            ("daily-summary-csv", b"date,samples"),
            ("events-csv", b"start_time_utc"),
            ("histogram-png", b"\x89PNG\r\n\x1a\n"),
            ("heatmap-png", b"\x89PNG\r\n\x1a\n"),
            ("pdf", b"%PDF"),
        ):
            _, _, payload = build_report(
                self.store,
                period=self.period,
                timezone_name="Europe/Berlin",
                scan_interval_seconds=60,
                output_format=output_format,
            )
            self.assertTrue(payload.startswith(prefix), output_format)

    def test_unknown_timezone_is_rejected(self):
        with self.assertRaises(ValueError):
            load_timezone("Mars/Olympus_Mons")


class ReportWebTests(unittest.TestCase):
    def setUp(self):
        from http.server import ThreadingHTTPServer

        self.temp_dir = tempfile.TemporaryDirectory()
        self.store = HistoryStore(Path(self.temp_dir.name) / "history.sqlite3", retention_days=90)
        self.store.set_metadata({"serial": "abc123", "device_model": "GMC Test"})
        tz = ZoneInfo("Europe/Berlin")
        period = resolve_period(
            kind="daily",
            selection="specific",
            tz=tz,
            date_value="2026-01-15",
            now=datetime(2026, 1, 20, 12, tzinfo=tz),
        )
        self.store.insert_measurement(
            {"cpm": 12, "temperature_c": 26.8, "voltage_v": 4.2},
            timestamp_utc=int(period.start_utc.timestamp()),
        )
        app = ReportApplication(
            store=self.store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
        )
        self.server = ThreadingHTTPServer(("127.0.0.1", 0), ReportRequestHandler)
        self.server.app = app
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.server.server_port}"

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        self.temp_dir.cleanup()

    def test_health_index_and_csv_download(self):
        with urllib.request.urlopen(f"{self.base_url}/health", timeout=5) as response:
            self.assertEqual(response.status, 200)
            self.assertEqual(response.read(), b"ok\n")
        with urllib.request.urlopen(f"{self.base_url}/", timeout=5) as response:
            page = response.read().decode("utf-8")
            self.assertIn("GMC Radiation Monitoring", page)
            self.assertNotIn(
                "Download scientifically labelled PNG graphs and matching raw-resolution CSV files.", page
            )
            self.assertIn("Previous day", page)
            self.assertIn("Time-series PNG", page)
            self.assertIn("Analysis", page)
            self.assertIn("24 h Fano factor", page)
            self.assertIn("24 h median", page)
            self.assertIn("24 h P99", page)
            self.assertIn("24 h minimum", page)
            self.assertIn("24 h maximum", page)
            self.assertIn("CPM–temperature correlation", page)
            self.assertIn("CPM–voltage correlation", page)
            self.assertIn("Background index", page)
            self.assertIn("Data quality", page)
            self.assertIn("Baseline deviation", page)
            self.assertIn("7 d baseline drift", page)
            self.assertIn("Temperature bins (24 h)", page)
            self.assertIn("Quick downloads", page)
            self.assertIn("Data exports", page)
            self.assertIn("Advanced visuals", page)
            self.assertIn("Custom period", page)
            self.assertIn("Overview", page)
            self.assertIn("Counting statistics", page)
            self.assertIn("Long-term context", page)
            self.assertIn("Advanced diagnostics", page)
            self.assertIn("Not available yet", page)
            self.assertIn("Analysis PDF", page)
        self.assertIn("Radiation traffic light", page)
        self.assertIn("Relative anomaly indicator only", page)
        url = (
            f"{self.base_url}/download?period=daily&selection=specific"
            "&date=2026-01-15&format=csv&device=abc123"
        )
        with urllib.request.urlopen(url, timeout=5) as response:
            payload = response.read()
            self.assertEqual(response.headers.get_content_type(), "text/csv")
            self.assertIn("attachment;", response.headers["Content-Disposition"])
            self.assertIn(b"timestamp_utc,timestamp_local,cpm", payload)

        json_url = (
            f"{self.base_url}/download?period=daily&selection=specific"
            "&date=2026-01-15&format=analysis-json&device=abc123"
        )
        with urllib.request.urlopen(json_url, timeout=10) as response:
            analysis_payload = json.loads(response.read())
            self.assertEqual(response.headers.get_content_type(), "application/json")
            self.assertIn("data_quality", analysis_payload["statistics"])

        pdf_url = (
            f"{self.base_url}/download?period=daily&selection=specific"
            "&date=2026-01-15&format=pdf&device=abc123"
        )
        with urllib.request.urlopen(pdf_url, timeout=20) as response:
            self.assertEqual(response.headers.get_content_type(), "application/pdf")
            self.assertTrue(response.read().startswith(b"%PDF"))


if __name__ == "__main__":
    unittest.main()
