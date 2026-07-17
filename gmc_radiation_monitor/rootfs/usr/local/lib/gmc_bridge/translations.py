from __future__ import annotations

from dataclasses import dataclass

from .i18n import CATALOGS, SUPPORTED_UI_LANGUAGES, validate_catalogs

# Backwards-compatible alias used by existing tests and integrations.
_TRANSLATIONS = CATALOGS


@dataclass(frozen=True, slots=True)
class Translator:
    language: str

    def __call__(self, text: str, **values: object) -> str:
        translated = _TRANSLATIONS.get(self.language, {}).get(text, text)
        return translated.format(**values) if values else translated


def resolve_language(
    configured: str,
    *,
    accept_language: str = "",
    override: str | None = None,
) -> str:
    if override and override in SUPPORTED_UI_LANGUAGES:
        return override
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
