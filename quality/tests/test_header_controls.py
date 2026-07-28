from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


class HeaderControlTests(unittest.TestCase):
    def test_language_dropdown_and_reload_button_are_rendered(self) -> None:
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
                mode_override="advanced",
                language_override="de",
                device_override="",
                accept_language="de",
            ).decode("utf-8")
        self.assertIn('id="analysis-level-select"', page)
        self.assertIn('id="language-select"', page)
        self.assertIn('name="lang"', page)
        self.assertIn('<option value="de" selected>Deutsch</option>', page)
        self.assertIn('id="header-status-badge"', page)
        self.assertIn('id="reload-dashboard"', page)
        self.assertIn('aria-label="Seite aktualisieren"', page)
        self.assertIn('class="analysis-select-control"', page)
        self.assertIn('class="analysis-select-group"', page)
        self.assertIn('class="header-status-badge', page)
        self.assertIn('class="language-select-control"', page)
        self.assertIn('class="language-select-icon"', page)
        self.assertIn('aria-label="Sprache"', page)
        self.assertNotIn('<span>Sprache</span>', page)
        self.assertNotIn('class="language-switcher"', page)

    def test_dashboard_script_wires_both_header_controls(self) -> None:
        source = (
            Path(__file__).resolve().parents[2]
            / "gmc_radiation_monitor/rootfs/usr/local/lib/gmc_bridge/static/dashboard.js"
        ).read_text(encoding="utf-8")
        self.assertIn("languageSelect?.addEventListener('change'", source)
        self.assertIn("analysisLevelSelect?.addEventListener('change'", source)
        self.assertIn("form.requestSubmit()", source)
        self.assertIn("document.getElementById('reload-dashboard')", source)
        self.assertIn("window.location.reload()", source)


if __name__ == "__main__":
    unittest.main()
