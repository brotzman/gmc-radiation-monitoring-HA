from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

from .i18n import CATALOGS, SUPPORTED_UI_LANGUAGES, validate_catalogs
from .number_format import LocalizedNumber

# Backwards-compatible alias used by existing tests and integrations.
_TRANSLATIONS = CATALOGS


@dataclass(frozen=True, slots=True)
class Translator:
    language: str

    def __call__(self, text: str, **values: object) -> str:
        translated = _TRANSLATIONS.get(self.language, {}).get(text, text)
        if not values:
            return translated
        localized_values = {
            key: LocalizedNumber(value, self.language) if isinstance(value, (int, float, Decimal)) and not isinstance(value, bool) else value
            for key, value in values.items()
        }
        return translated.format(**localized_values)


def resolve_language(
    configured: str,
    *,
    accept_language: str = "",
    override: str | None = None,
) -> str:
    if override and override in SUPPORTED_UI_LANGUAGES:
        return override
    if override == "auto":
        configured = "auto"
    if configured in SUPPORTED_UI_LANGUAGES:
        return configured
    if configured != "auto":
        return "en"
    for item in accept_language.split(","):
        code = item.split(";", 1)[0].strip().lower().split("-", 1)[0]
        if code in SUPPORTED_UI_LANGUAGES:
            return code
    return "en"


__all__ = [
    "SUPPORTED_UI_LANGUAGES",
    "Translator",
    "resolve_language",
    "validate_catalogs",
]
