from __future__ import annotations

from gmc_bridge.metrology import (
    MetrologyConfig,
    assess_count_rate,
    derived_dose_estimate,
    integrated_dose_estimate,
    uncertainty_budget,
)


def test_saturation_suppresses_derived_dose() -> None:
    config = MetrologyConfig(reliable_max_cpm=1000)
    result = derived_dose_estimate(
        cpm=1200,
        cpm_per_usvh=154.0,
        counting_relative_percent=3.0,
        config=config,
    )
    assert result["available"] is False
    assert result["value_usvh"] is None
    assert result["metrology"]["possible_saturation_or_count_loss"] is True


def test_dead_time_correction_requires_device_data() -> None:
    plain = assess_count_rate(6000, MetrologyConfig())
    corrected = assess_count_rate(
        6000,
        MetrologyConfig(dead_time_us=190.0, reliable_max_cpm=20000, dead_time_model="nonparalyzable"),
    )
    assert plain["correction_applied"] is False
    assert corrected["correction_applied"] is True
    assert corrected["corrected_cpm"] > 6000


def test_incomplete_uncertainty_budget_has_no_total() -> None:
    budget = uncertainty_budget(
        counting_relative_percent=12.0,
        config=MetrologyConfig(conversion_factor_uncertainty_percent=5.0),
    )
    assert budget["complete"] is False
    assert budget["combined_standard_uncertainty_percent"] is None
    assert "cannot be determined" in budget["statement"]


def test_complete_uncertainty_budget_combines_quadratically() -> None:
    budget = uncertainty_budget(
        counting_relative_percent=3.0,
        config=MetrologyConfig(
            conversion_factor_uncertainty_percent=4.0,
            calibration_uncertainty_percent=12.0,
        ),
    )
    assert budget["complete"] is True
    assert round(budget["combined_standard_uncertainty_percent"], 6) == 13.0


def test_integrated_dose_does_not_bridge_gaps_or_saturation() -> None:
    result = integrated_dose_estimate(
        samples=[(0, 154.0), (60, 154.0), (120, 2000.0), (600, 154.0)],
        cpm_per_usvh=154.0,
        config=MetrologyConfig(reliable_max_cpm=1000),
        expected_interval_seconds=60,
    )
    assert result["value_usv"] == 1.0 / 60.0
    assert result["excluded_saturated_intervals"] == 1
    assert result["gap_count"] == 1


def test_dead_time_corrected_cpm_is_used_for_dose_conversion() -> None:
    result = derived_dose_estimate(
        cpm=6000,
        cpm_per_usvh=154.0,
        counting_relative_percent=1.0,
        config=MetrologyConfig(dead_time_us=190.0, reliable_max_cpm=20000, dead_time_model="nonparalyzable"),
    )
    assert result["effective_cpm_for_conversion"] > 6000
    assert result["value_usvh"] > 6000 / 154.0
