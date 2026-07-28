from __future__ import annotations

import unittest

from gmc_bridge.translations import Translator
from gmc_bridge.web_components import render_analysis_level_controls


class AnalysisLevelControlTests(unittest.TestCase):
    def test_segmented_control_markup_and_compact_expert_label(self) -> None:
        html = render_analysis_level_controls(default_level="expert", translator=Translator("de"))
        self.assertIn('class="analysis-level-control-group"', html)
        self.assertIn('class="analysis-level-buttons"', html)
        self.assertIn('class="analysis-level-description"', html)
        self.assertIn('>Experte<', html)
        self.assertNotIn('>Expertenansicht<', html)


if __name__ == "__main__":
    unittest.main()
