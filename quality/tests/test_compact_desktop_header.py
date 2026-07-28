from __future__ import annotations

import re
import unittest
from pathlib import Path


class CompactDesktopHeaderTests(unittest.TestCase):
    def test_desktop_header_controls_are_compact_and_subtitle_stays_on_one_line(self) -> None:
        css = (
            Path(__file__).resolve().parents[2]
            / "gmc_radiation_monitor/rootfs/usr/local/lib/gmc_bridge/static/dashboard.css"
        ).read_text(encoding="utf-8")
        self.assertIn("grid-template-columns:minmax(9rem,10.25rem) minmax(8.25rem,9rem) minmax(9rem,9.75rem) 2.25rem", css)
        self.assertIn(".header-status-badge { display:inline-flex", css)
        self.assertIn("min-height:2.25rem", css)
        self.assertRegex(css, re.compile(r"@media \(min-width:801px\).*?\.header-intro p \{ white-space:nowrap; \}", re.S))


if __name__ == "__main__":
    unittest.main()
