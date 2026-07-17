from __future__ import annotations

from gmc_bridge.filtering import HighCpmGate


def _stable_gate() -> HighCpmGate:
    gate = HighCpmGate(10000, 3)
    gate.seed([14, 15, 16, 15, 17, 14, 16, 15])
    return gate


def test_isolated_5887_cpm_spike_is_held_back() -> None:
    gate = _stable_gate()
    assessment = gate.assess(5887)
    assert assessment.suspicious is True
    assert assessment.trigger == "adaptive_threshold"
    assert assessment.baseline_median == 15.0
    assert assessment.adaptive_threshold == 1000
    assert gate.accept(5887, assessment=assessment) is False
    assert gate.pending == 1


def test_ordinary_warning_and_danger_values_are_not_delayed() -> None:
    gate = _stable_gate()
    for cpm in (51, 100, 500, 1000):
        assessment = gate.assess(cpm)
        assert assessment.suspicious is False
        assert gate.accept(cpm, assessment=assessment) is True


def test_exactly_three_similarly_sized_spikes_are_required() -> None:
    gate = _stable_gate()
    assert gate.accept(5800) is False
    assert gate.accept(6100) is False
    assert gate.pending == 2
    assert gate.accept(5900) is True
    assert gate.just_confirmed is True
    assert gate.last_accept_reason == "consecutive_confirmed"


def test_unrelated_spike_magnitudes_restart_confirmation_count() -> None:
    gate = _stable_gate()
    assert gate.accept(1200) is False
    assert gate.pending == 1
    assert gate.accept(9000) is False
    assert gate.pending == 1


def test_normal_value_resets_pending_and_updates_baseline() -> None:
    gate = _stable_gate()
    assert gate.accept(5887) is False
    assert gate.accept(18) is True
    assert gate.state == gate.NORMAL
    assert gate.pending == 0


def test_seed_rejects_legacy_one_off_spike() -> None:
    gate = HighCpmGate(10000, 3)
    gate.seed([14, 15, 16, 5887, 15, 17])
    assert gate.baseline_median == 15.0
    assert gate.adaptive_threshold == 1000


def test_ff_fragment_like_spikes_do_not_form_one_confirmation_sequence() -> None:
    gate = _stable_gate()
    assert gate.accept(4095) is False
    assert gate.pending == 1
    assert gate.accept(5631) is False
    assert gate.pending == 1
    assert gate.accept(3583) is False
    assert gate.pending == 1
