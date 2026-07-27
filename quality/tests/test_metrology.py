from __future__ import annotations

import math
import unittest

from gmc_bridge.metrology import (
    DualTubeMetrologyConfig,
    MetrologyConfig,
    TubeMetrologyProfile,
    assess_count_rate,
    derived_dual_tube_dose_estimate,
    integrated_dose_estimate,
)


class MetrologyTests(unittest.TestCase):
    def test_nonparalyzable_dead_time_correction(self) -> None:
        result = assess_count_rate(
            6000,
            MetrologyConfig(dead_time_us=100, dead_time_model="nonparalyzable", reliable_max_cpm=20000),
        )
        self.assertTrue(result["correction_applied"])
        self.assertAlmostEqual(result["detector_load_percent"], 1.0, places=6)
        self.assertAlmostEqual(result["corrected_cpm"], 6000 / 0.99, places=6)
        self.assertTrue(result["dose_rate_display_allowed"])

    def test_saturation_blocks_dose_display(self) -> None:
        result = assess_count_rate(
            25000,
            MetrologyConfig(dead_time_us=100, dead_time_model="nonparalyzable", reliable_max_cpm=20000),
        )
        self.assertTrue(result["possible_saturation_or_count_loss"])
        self.assertFalse(result["dose_rate_display_allowed"])
        self.assertIsNone(result["corrected_cpm"])

    def test_dual_tube_selects_high_range_after_low_range_limit(self) -> None:
        config = DualTubeMetrologyConfig(
            mode="separate",
            low_dose=TubeMetrologyProfile(cpm_per_usvh=100, reliable_max_cpm=1000, tube_model="low"),
            high_dose=TubeMetrologyProfile(cpm_per_usvh=1000, reliable_max_cpm=50000, tube_model="high"),
        )
        result = derived_dual_tube_dose_estimate(
            primary_cpm=1500,
            low_cpm=1500,
            high_cpm=4000,
            counting_relative_percent=2.0,
            config=config,
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["selected_tube"], "high")
        self.assertAlmostEqual(result["value_usvh"], 4.0)

    def test_integrated_dose_preserves_gaps(self) -> None:
        result = integrated_dose_estimate(
            samples=[(0, 100), (60, 100), (600, 100), (660, 100)],
            cpm_per_usvh=100,
            config=MetrologyConfig(),
            expected_interval_seconds=60,
        )
        self.assertTrue(result["available"])
        self.assertEqual(result["gap_count"], 1)
        self.assertEqual(result["covered_seconds"], 120)
        self.assertTrue(math.isclose(result["value_usv"], 2 / 60, rel_tol=1e-9))


if __name__ == "__main__":
    unittest.main()
