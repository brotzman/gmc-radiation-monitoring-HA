from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


class SectionNavigationTests(unittest.TestCase):
    def test_section_dropdown_is_rendered_below_connection_status(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            app = ReportApplication(
                store=HistoryStore(Path(directory) / "history.sqlite3", retention_days=30),
                timezone_name="Europe/Berlin", scan_interval_seconds=60, read_gyro=False,
                cpm_per_usvh=154.0, ui_mode="advanced", ui_language="auto",
                options_path=Path(directory) / "options.json",
            )
            page = app.render_index(mode_override="advanced", language_override="de", device_override="", accept_language="de").decode("utf-8")
        status_position = page.index('id="header-status-badge"')
        section_position = page.index('id="section-select"')
        status_column_start = page.rfind('class="header-status-column"', 0, status_position)
        slot_position = page.index('id="section-navigation-slot"')
        floating_position = page.index('id="section-floating-navigation"')
        status_column_end = page.index("</div>\n</div>\n</div>", section_position)
        self.assertGreaterEqual(status_column_start, 0)
        self.assertLess(status_position, slot_position)
        self.assertLess(slot_position, floating_position)
        self.assertLess(floating_position, section_position)
        self.assertLess(section_position, status_column_end)
        self.assertIn('<optgroup label="Übersicht">', page)
        self.assertIn('value="devices">▣ Geräte</option>', page)
        self.assertIn('value="radiation-intelligence">✦ Intelligente Auswertung</option>', page)
        self.assertIn('value="analysis">▤ Analyse</option>', page)
        self.assertIn('value="long-term-analysis">↗ Langzeit</option>', page)
        self.assertIn('value="history">⌁ Verlauf</option>', page)
        self.assertIn('value="workflow">⚙ Arbeitsabläufe</option>', page)
        self.assertIn('value="calibration-management">◎ Kalibrierung</option>', page)
        self.assertIn('value="reports">⇩ Berichte</option>', page)
        self.assertNotIn('id="dashboard-controls"', page)
        self.assertNotIn('mobile-dashboard-navigation', page)
        self.assertIn('id="toggle-all-cards"', page)

    def test_navigation_script_tracks_all_sections_with_select(self) -> None:
        source = (Path(__file__).resolve().parents[2] / "gmc_radiation_monitor/rootfs/usr/local/lib/gmc_bridge/static/dashboard.js").read_text(encoding="utf-8")
        self.assertIn("document.getElementById('section-select')", source)
        self.assertIn("sectionSelect?.addEventListener('change'", source)
        self.assertIn("sectionFloatingNavigation.classList.add('is-floating')", source)
        self.assertIn("navigationScrollContainer?.addEventListener('scroll'", source)
        self.assertIn("'long-term-analysis'", source)
        self.assertIn("'calibration-management'", source)
        self.assertNotIn("navigation-condensed", source)
        self.assertNotIn("back-to-top", source)


if __name__ == "__main__":
    unittest.main()
