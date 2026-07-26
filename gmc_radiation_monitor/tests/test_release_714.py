from __future__ import annotations

import ast
from pathlib import Path

from gmc_bridge.analysis_presentation import (
    build_historical_section,
    build_radiation_intelligence_result,
)
from gmc_bridge.translations import _TRANSLATIONS, SUPPORTED_UI_LANGUAGES, Translator
from gmc_bridge.version import APP_VERSION
from gmc_bridge.web_analysis_views import (
    render_historical_section,
    render_radiation_intelligence,
)

ROOT = Path(__file__).resolve().parents[1]
LIB = ROOT / "rootfs/usr/local/lib/gmc_bridge"


def _runtime_translation_keys() -> set[str]:
    """Collect static strings that can reach the dashboard translation layer."""
    keys: set[str] = set()
    for path in LIB.rglob("*.py"):
        if "i18n" in path.parts or path.name == "translations.py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                function = ""
                if isinstance(node.func, ast.Name):
                    function = node.func.id
                elif isinstance(node.func, ast.Attribute):
                    function = node.func.attr

                if (
                    function in {"t", "translator"}
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                ):
                    keys.add(node.args[0].value)

                if (
                    function == "_metric"
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                ):
                    keys.add(node.args[0].value)

                if (
                    function == "_message"
                    and len(node.args) > 1
                    and isinstance(node.args[1], ast.Constant)
                    and isinstance(node.args[1].value, str)
                ):
                    keys.add(node.args[1].value)

                for keyword in node.keywords:
                    if not keyword.arg or not (keyword.arg.endswith("_key") or keyword.arg == "title"):
                        continue
                    if (
                        isinstance(keyword.value, ast.Constant)
                        and isinstance(keyword.value.value, str)
                        and keyword.value.value
                    ):
                        keys.add(keyword.value.value)

            if isinstance(node, ast.Dict):
                for key_node, value_node in zip(node.keys, node.values, strict=False):
                    if not (
                        isinstance(key_node, ast.Constant)
                        and isinstance(key_node.value, str)
                        and isinstance(value_node, ast.Constant)
                        and isinstance(value_node.value, str)
                        and value_node.value
                    ):
                        continue
                    field_name = key_node.value
                    value = value_node.value
                    if field_name.endswith("_key"):
                        keys.add(value)
                    elif field_name == "key" and (
                        value[:1].isupper() or any(character.isspace() for character in value) or "{" in value
                    ):
                        # Runtime analysis models use {"key": <translation key>}
                        # for explanatory messages. Short lowercase values such as
                        # "device" are internal identifiers, not display strings.
                        keys.add(value)
    return keys


def test_release_version_and_notes() -> None:
    assert APP_VERSION == "9.1.2"
    assert "version: 9.1.2" in (ROOT / "config.yaml").read_text(encoding="utf-8")
    assert (ROOT / "RELEASE_NOTES_9.1.2.md").is_file()


def test_every_runtime_translation_key_exists_in_every_catalogue() -> None:
    runtime_keys = _runtime_translation_keys()
    assert runtime_keys
    for language in SUPPORTED_UI_LANGUAGES:
        missing = sorted(runtime_keys - set(_TRANSLATIONS[language]))
        assert missing == [], f"missing {language} runtime translations: {missing}"


def test_signal_probability_card_is_fully_localized_in_every_language() -> None:
    result = build_radiation_intelligence_result(
        {
            "available": True,
            "probability_percent": 2.0,
            "confidence": "Low",
            "state": "Normal",
            "reasons": [],
            "disclaimer": "Heuristic statistical assessment; not a radiation-protection classification.",
        }
    )
    raw_template = "{probability:.0f}% estimated signal probability"
    for language in SUPPORTED_UI_LANGUAGES:
        translator = Translator(language)
        rendered = render_radiation_intelligence(result, translator)
        expected = translator(raw_template, probability=2.0)
        assert expected in rendered
        if language != "en":
            assert "estimated signal probability" not in rendered

    german = render_radiation_intelligence(result, Translator("de"))
    assert "Unauffällig" in german
    assert "2 % geschätzte Signalwahrscheinlichkeit" in german
    assert "Vertrauen: Niedrig" in german


def test_nested_historical_template_values_are_localized() -> None:
    section = build_historical_section(
        {
            "historical_development": {
                "temperature_trend": {"change": None, "samples": 3},
                "pressure_trend": {"change": None, "samples": 4},
                "jump_count": 0,
                "span_days": 12,
                "daily_points": 7,
                "points": [],
            },
            "drift": {},
        }
    )
    for language in SUPPORTED_UI_LANGUAGES:
        rendered = render_historical_section(section, Translator(language))
        if language != "en":
            assert "Insufficient paired daily values" not in rendered
            assert ">days<" not in rendered
            assert "daily values" not in rendered

    german = render_historical_section(section, Translator("de"))
    assert "Nicht genügend vergleichbare Tageswerte" in german
    assert "12 Tage · 7 Tageswerte" in german


def test_statistical_significance_reasons_are_fully_localized() -> None:
    result = build_radiation_intelligence_result(
        {
            "available": True,
            "probability_percent": 18.0,
            "confidence": "Low",
            "state": "Likely device-specific deviation",
            "reasons": [
                {
                    "key": "The recent level differs from counting noise with {probability:.2f}% statistical confidence",
                    "params": {"probability": 17.79},
                },
                {
                    "key": "A comparable or more extreme hourly level occurred about once in {rarity:.1f} historical hours",
                    "params": {"rarity": 2.6},
                },
            ],
            "disclaimer": "Heuristic statistical assessment; not a radiation-protection classification.",
        }
    )
    english_fragments = (
        "The recent level differs from counting noise",
        "A comparable or more extreme hourly level occurred",
    )
    for language in SUPPORTED_UI_LANGUAGES:
        rendered = render_radiation_intelligence(result, Translator(language))
        if language != "en":
            for fragment in english_fragments:
                assert fragment not in rendered, f"{language} still exposes {fragment!r}"

    german = render_radiation_intelligence(result, Translator("de"))
    assert "statistischen Sicherheit von 17,79 %" in german
    assert "historisch etwa einmal in 2,6 Stunden" in german
