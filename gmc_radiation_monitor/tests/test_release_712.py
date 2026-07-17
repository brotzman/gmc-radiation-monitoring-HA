from __future__ import annotations

from gmc_bridge.analysis_presentation import build_cosmic_influence_result
from gmc_bridge.translations import Translator
from gmc_bridge.web_analysis_views import render_cosmic_influence


def _learning_model() -> dict[str, object]:
    return {
        "enabled": True,
        "state": "Pressure model is still being formed",
        "confidence": "Insufficient",
        "pressure_snapshot": {"available": False},
        "reasons": [],
    }


def test_cosmic_confidence_is_fully_localized_in_german() -> None:
    html = render_cosmic_influence(build_cosmic_influence_result(_learning_model()), Translator("de"))
    assert "Vertrauen: Unzureichend" in html
    assert "Confidence" not in html
    assert "Insufficient" not in html


def test_cosmic_confidence_value_uses_each_language_catalog() -> None:
    expected = {
        "en": "Confidence: Insufficient",
        "de": "Vertrauen: Unzureichend",
        "fr": "Niveau de confiance: Insuffisant",
        "es": "Confianza: Insuficiente",
        "it": "Affidabilità: Insufficiente",
        "nl": "Betrouwbaarheid: Onvoldoende",
        "pl": "Poziom ufności: Niewystarczająca",
        "hr": "Pouzdanost: Nedovoljna",
    }
    result = build_cosmic_influence_result(_learning_model())
    for language, phrase in expected.items():
        assert phrase in render_cosmic_influence(result, Translator(language))
