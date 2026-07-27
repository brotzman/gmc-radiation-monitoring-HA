from __future__ import annotations

import unittest

from gmc_bridge.filtering import HighCpmGate


class HighCpmGateTests(unittest.TestCase):
    def test_adaptive_spike_requires_three_consistent_confirmations(self) -> None:
        gate = HighCpmGate(adaptive_multiplier=4, adaptive_minimum_cpm=100, adaptive_minimum_delta=50)
        gate.seed([20, 21, 19, 20, 22, 20])
        self.assertFalse(gate.accept(200))
        self.assertFalse(gate.accept(205))
        self.assertTrue(gate.accept(198))
        self.assertTrue(gate.just_confirmed)
        self.assertEqual(gate.state, gate.CONFIRMED)

    def test_inconsistent_spike_restarts_confirmation_sequence(self) -> None:
        gate = HighCpmGate(confirmations=3, pending_consistency_ratio=1.2)
        self.assertFalse(gate.accept(1500))
        self.assertFalse(gate.accept(4000))
        self.assertEqual(gate.pending, 1)
        self.assertFalse(gate.accept(4100))
        self.assertTrue(gate.accept(4050))

    def test_normal_value_resets_pending_state_and_updates_baseline(self) -> None:
        gate = HighCpmGate(adaptive_minimum_cpm=100)
        self.assertFalse(gate.accept(500))
        self.assertTrue(gate.accept(25))
        self.assertEqual(gate.state, gate.NORMAL)
        self.assertEqual(gate.pending, 0)
        self.assertEqual(gate.last_accept_reason, "normal")

    def test_seed_rejects_legacy_one_off_contamination(self) -> None:
        gate = HighCpmGate(adaptive_multiplier=5, adaptive_minimum_cpm=100, adaptive_minimum_delta=50)
        gate.seed([20, 21, 19, 20, 22, 9999])
        self.assertLess(gate.baseline_median or 0, 30)


if __name__ == "__main__":
    unittest.main()
