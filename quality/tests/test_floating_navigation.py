from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


class FloatingNavigationTests(unittest.TestCase):
    def test_compact_desktop_and_mobile_navigation_are_rendered(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            app = ReportApplication(
                store=HistoryStore(Path(directory) / "history.sqlite3", retention_days=30),
                timezone_name="Europe/Berlin", scan_interval_seconds=60, read_gyro=False,
                cpm_per_usvh=154.0, ui_mode="advanced", ui_language="auto",
                options_path=Path(directory) / "options.json",
            )
            page = app.render_index(mode_override="advanced", language_override="de", device_override="", accept_language="de").decode("utf-8")
        self.assertIn('class="desktop-dashboard-navigation"', page)
        self.assertIn('class="mobile-dashboard-navigation"', page)
        self.assertIn('more-navigation-menu', page)
        self.assertIn('id="mobile-sections-menu"', page)
        self.assertIn('id="current-section-label"', page)
        self.assertIn('id="back-to-top"', page)
        self.assertIn('href="#long-term-analysis"', page)
        self.assertIn('href="#calibration-management"', page)

    def test_navigation_script_tracks_all_sections(self) -> None:
        source = (Path(__file__).resolve().parents[2] / "gmc_radiation_monitor/rootfs/usr/local/lib/gmc_bridge/static/dashboard.js").read_text(encoding="utf-8")
        self.assertIn("'long-term-analysis'", source)
        self.assertIn("'calibration-management'", source)
        self.assertIn("aria-current", source)
        self.assertIn("navigation-condensed", source)


if __name__ == "__main__":
    unittest.main()
