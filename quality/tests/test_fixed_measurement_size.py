from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


class FixedMeasurementSizeTests(unittest.TestCase):
    def test_dashboard_has_fixed_medium_measurement_size_without_controls(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            app = ReportApplication(
                store=HistoryStore(Path(directory) / "history.sqlite3", retention_days=30),
                timezone_name="Europe/Berlin",
                scan_interval_seconds=60,
                read_gyro=False,
                cpm_per_usvh=154.0,
                ui_mode="advanced",
                ui_language="auto",
                options_path=Path(directory) / "options.json",
            )
            page = app.render_index(
                mode_override="advanced", language_override="de", device_override="", accept_language="de"
            ).decode("utf-8")
        self.assertNotIn("Messwertdarstellung", page)
        self.assertNotIn("Hauptmesswert Schriftgröße", page)
        self.assertNotIn('name="main-value-size"', page)
        self.assertNotIn('id="custom-value-font-size"', page)
        self.assertNotIn('data-main-value-size=', page)

    def test_css_defines_only_fixed_medium_main_value_size(self) -> None:
        css = (Path(__file__).resolve().parents[2] / "gmc_radiation_monitor/rootfs/usr/local/lib/gmc_bridge/static/dashboard.css").read_text(encoding="utf-8")
        self.assertIn("--main-value-font-size:clamp(1.8rem,4vw,2.45rem)", css)
        self.assertNotIn("data-main-value-size", css)
        self.assertNotIn("measurement-display-settings", css)


if __name__ == "__main__":
    unittest.main()
