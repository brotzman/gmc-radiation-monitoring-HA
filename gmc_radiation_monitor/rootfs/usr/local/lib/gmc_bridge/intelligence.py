from __future__ import annotations

from typing import Any


def _clamp(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def build_radiation_intelligence(
    analysis: dict[str, Any],
    *,
    comparison: dict[str, Any] | None = None,
    shared_event: dict[str, Any] | None = None,
    recent_orientation_change: bool = False,
    device_profile: dict[str, Any] | None = None,
    site_profile: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build an explainable heuristic assessment, never a safety classification."""
    if not analysis.get("available"):
        return {
            "available": False,
            "state": "No data",
            "probability_percent": 0.0,
            "confidence": "Low",
            "reasons": [{"key": "No measurement yet"}],
        }

    reasons: list[dict[str, Any]] = []
    probability = 3.0
    confidence = "Medium"
    baseline_ready = bool(analysis.get("baseline_ready"))
    quality = float(analysis.get("data_quality_score_24h") or 0.0)
    z = analysis.get("z_score_24h")
    deviation = analysis.get("baseline_deviation_percent")
    trend = analysis.get("trend_30m_cpm")
    excluded = int(analysis.get("excluded_samples_24h") or 0)

    if not baseline_ready:
        confidence = "Low"
        reasons.append({"key": "Local background is still being learned"})
    else:
        reasons.append({"key": "Local background model is available"})
        if z is not None:
            az = abs(float(z))
            probability += _clamp((az - 1.0) * 18.0, 0.0, 48.0)
            reasons.append({
                "key": "Current value is {z:+.2f} robust standard deviations from the 24 h median",
                "params": {"z": float(z)},
            })
        if deviation is not None:
            positive = max(0.0, float(deviation))
            probability += _clamp(positive * 0.45, 0.0, 28.0)
            reasons.append({
                "key": "One-hour robust level is {deviation:+.1f}% relative to the device baseline",
                "params": {"deviation": float(deviation)},
            })
        if trend is not None and float(trend) > 0:
            probability += _clamp(float(trend) * 1.2, 0.0, 12.0)
            reasons.append({"key": "The recent 30-minute robust trend is rising"})

    device_deviation = None if not device_profile else device_profile.get("deviation_percent")
    site_deviation = None if not site_profile else site_profile.get("deviation_percent")
    site_confidence = None if not site_profile else site_profile.get("confidence")
    classification = "normal"

    if shared_event and shared_event.get("active") and (site_deviation is None or float(site_deviation) >= 15):
        probability += 26.0
        confidence = "High" if quality >= 75 and site_confidence in {None, "High", "Medium"} else "Medium"
        classification = "shared_site_change"
        reasons.append({"key": "Both connected counters show a quality-filtered simultaneous rise"})
        if site_deviation is not None:
            reasons.append({
                "key": "The measurement-site baseline is {deviation:+.1f}% above its typical value",
                "params": {"deviation": float(site_deviation)},
            })
    elif device_deviation is not None and abs(float(device_deviation)) >= 15:
        if site_deviation is None or abs(float(site_deviation)) < 10:
            probability *= 0.62
            confidence = "Low"
            classification = "device_specific"
            reasons.append({"key": "The deviation is device-specific; the measurement-site profile remains normal"})

    if comparison:
        comparison_confidence = str(comparison.get("confidence") or "Insufficient")
        agreement = float(comparison.get("agreement_percent") or 0.0)
        if comparison_confidence == "Insufficient":
            reasons.append({"key": "Too few valid paired measurements for a reliable device comparison"})
        elif agreement >= 85:
            reasons.append({"key": "The quality-filtered counter comparison currently agrees well"})
        elif agreement < 60:
            probability *= 0.72
            confidence = "Low"
            if classification == "normal":
                classification = "device_specific"
            reasons.append({"key": "The filtered counters disagree, so a device-specific effect is more likely"})

    if site_profile:
        if site_confidence == "Reduced":
            confidence = "Low"
            reasons.append({"key": "The measurement-site profile currently relies on one device"})
        elif site_confidence in {"High", "Medium"}:
            reasons.append({"key": "The measurement-site profile combines both devices with quality weighting"})

    if recent_orientation_change:
        probability *= 0.72
        reasons.append({"key": "A recent position change can affect comparability"})
    if excluded:
        reasons.append({"key": "{count} implausible measurements were excluded from the assessment", "params": {"count": excluded}})
    if quality < 50:
        probability *= 0.55
        confidence = "Low"
        reasons.append({"key": "Data quality is too low for a reliable assessment"})
    elif quality >= 90:
        reasons.append({"key": "Recent quality-filtered data quality is high"})

    probability = _clamp(probability)
    if classification == "device_specific":
        state = "Likely device-specific deviation"
    elif classification == "shared_site_change" and probability >= 50:
        state = "Probable shared measurement-site change" if probability < 75 else "Strong common signal"
    else:
        state = "Normal" if probability < 20 else "Statistically noticeable" if probability < 50 else "Probable real change" if probability < 75 else "Strong common signal"
    return {
        "available": True,
        "state": state,
        "classification": classification,
        "probability_percent": probability,
        "confidence": confidence,
        "reasons": reasons[:8],
        "disclaimer": "Heuristic statistical assessment; not a radiation-protection classification.",
    }
