from __future__ import annotations

import unittest
from pathlib import Path


class ArchiveCleanupTests(unittest.TestCase):
    def test_removed_dashboard_components_leave_no_runtime_assets(self) -> None:
        project = Path(__file__).resolve().parents[2]
        css = (project / "gmc_radiation_monitor/rootfs/usr/local/lib/gmc_bridge/static/dashboard.css").read_text(encoding="utf-8")
        js = (project / "gmc_radiation_monitor/rootfs/usr/local/lib/gmc_bridge/static/dashboard.js").read_text(encoding="utf-8")
        report = (project / "gmc_radiation_monitor/rootfs/usr/local/lib/gmc_bridge/report_web.py").read_text(encoding="utf-8")
        components = (project / "gmc_radiation_monitor/rootfs/usr/local/lib/gmc_bridge/web_components.py").read_text(encoding="utf-8")
        for obsolete in (
            ".analysis-level-panel",
            ".analysis-level-button",
            ".system-status-panel",
            ".status-details-grid",
            ".status-strip-item",
            ".dashboard-controls",
            ".mobile-dashboard-navigation",
            ".navigation-menu-popover",
            ".mobile-navigation-sheet",
            ".back-to-top-button",
        ):
            self.assertNotIn(obsolete, css)
        self.assertNotIn("analysis-level-button", js)
        self.assertNotIn("status-strip", js)
        self.assertNotIn("navigation-condensed", js)
        self.assertNotIn("back-to-top", js)
        self.assertNotIn("data-jump-link", js)
        self.assertNotIn("analysis_level_controls_html", report)
        self.assertNotIn("status_strip_html", report)
        self.assertNotIn("dashboard_controls_html", report)
        self.assertNotIn('id="dashboard-controls"', report)
        self.assertNotIn("def render_analysis_level_controls", components)


if __name__ == "__main__":
    unittest.main()
