from __future__ import annotations

from gmc_bridge.history import HistoryRow
from gmc_bridge.intelligence import build_radiation_intelligence
from gmc_bridge.scientific_analysis import recent_change_significance


def row(timestamp: int, cpm: int) -> HistoryRow:
    return HistoryRow(device_serial="test", timestamp_utc=timestamp, cpm=cpm, temperature_c=None, voltage_v=None, gyro_x=None, gyro_y=None, gyro_z=None, cpm_quality="accepted")


def test_significance_detects_clear_increase() -> None:
    baseline = [row(index * 60, 20) for index in range(24 * 60)]
    recent = [row(24 * 3600 + index * 60, 35) for index in range(60)]
    result = recent_change_significance(recent, baseline)
    assert result["available"] is True
    assert result["state"] == "Statistically significant increase"
    assert result["significance_sigma"] > 5
    assert result["probability_not_counting_noise_percent"] > 99.9
    assert result["confidence"] == "Very high"


def test_significance_keeps_normal_variation_low_confidence() -> None:
    baseline = [row(index * 60, 20 + (index % 3) - 1) for index in range(24 * 60)]
    recent = [row(24 * 3600 + index * 60, 20 + (index % 3) - 1) for index in range(60)]
    result = recent_change_significance(recent, baseline)
    assert result["available"] is True
    assert result["state"] == "Consistent with normal counting variation"
    assert abs(result["significance_sigma"]) < 2
    assert result["confidence"] == "Low"


def test_significance_requires_enough_history() -> None:
    result = recent_change_significance([row(0, 20)], [row(60, 20)])
    assert result["available"] is False


def test_intelligence_exposes_significance_and_rarity() -> None:
    analysis = {
        "available": True,
        "baseline_ready": True,
        "data_quality_score_24h": 95,
        "excluded_samples_24h": 0,
        "z_score_24h": 4.0,
        "baseline_deviation_percent": 40.0,
        "trend_30m_cpm": 4.0,
        "change_significance": {
            "available": True,
            "significance_sigma": 4.2,
            "probability_not_counting_noise_percent": 99.997,
            "confidence": "High",
            "historical_rarity_one_in": 18.0,
        },
    }
    result = build_radiation_intelligence(analysis)
    assert result["confidence"] == "High"
    assert result["significance"]["available"] is True
    assert any("counting noise" in reason["key"] for reason in result["reasons"])
    assert any("historical hours" in reason["key"] for reason in result["reasons"])
