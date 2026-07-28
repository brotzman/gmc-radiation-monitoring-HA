from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


class AnalysisLevelControlTests(unittest.TestCase):
    def test_analysis_level_dropdown_is_rendered_in_header(self) -> None:
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
        self.assertIn('class="analysis-select-icon"', page)
        self.assertIn('>◉ Zusammenfassung<', page)
        self.assertIn('>▤ Analyse<', page)
        self.assertIn('>∑ Experte<', page)
        self.assertNotIn('id="analysis-level-panel"', page)


if __name__ == "__main__":
    unittest.main()
