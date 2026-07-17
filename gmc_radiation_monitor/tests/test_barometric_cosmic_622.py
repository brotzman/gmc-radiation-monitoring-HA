from __future__ import annotations

from gmc_bridge.translations import Translator


def test_barometric_explanation_is_translated_in_every_supported_language() -> None:
    key = "Falling air pressure is often associated with a slightly higher intensity of cosmically generated secondary radiation at ground level, while rising air pressure is associated with a slightly lower intensity. The strength of this relationship depends on detector, location and atmosphere; the cause cannot be determined unambiguously from total counts."
    for language in ("en", "de", "fr", "es", "it", "nl", "pl", "hr"):
        rendered = Translator(language)(key)
        assert rendered
        if language != "en":
            assert rendered != key
