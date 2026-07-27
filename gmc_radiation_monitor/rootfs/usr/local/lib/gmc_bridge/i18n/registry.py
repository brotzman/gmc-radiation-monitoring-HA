from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping


@dataclass(frozen=True, slots=True)
class LanguageSpec:
    code: str
    native_name: str
    manual_suffix: str


LANGUAGE_SPECS: tuple[LanguageSpec, ...] = (
    LanguageSpec("en", "English", "en"),
    LanguageSpec("de", "Deutsch", "de"),
    LanguageSpec("fr", "Français", "fr"),
    LanguageSpec("es", "Español", "es"),
    LanguageSpec("it", "Italiano", "it"),
    LanguageSpec("nl", "Nederlands", "nl"),
    LanguageSpec("pl", "Polski", "pl"),
    LanguageSpec("hr", "Hrvatski", "hr"),
)
SUPPORTED_UI_LANGUAGES: tuple[str, ...] = tuple(item.code for item in LANGUAGE_SPECS)
LANGUAGE_NAMES: dict[str, str] = {item.code: item.native_name for item in LANGUAGE_SPECS}


def build_catalogs(source: Mapping[str, Mapping[str, str]]) -> dict[str, dict[str, str]]:
    """Return mutable catalogues in the canonical language order.

    Keeping language registration in one place prevents the UI, validation and
    release-override loader from silently drifting apart.
    """
    missing = [code for code in SUPPORTED_UI_LANGUAGES if code not in source]
    extra = sorted(set(source) - set(SUPPORTED_UI_LANGUAGES))
    if missing or extra:
        raise ValueError(f"Invalid language registry: missing={missing}, extra={extra}")
    return {code: dict(source[code]) for code in SUPPORTED_UI_LANGUAGES}


__all__ = [
    "LANGUAGE_NAMES",
    "LANGUAGE_SPECS",
    "SUPPORTED_UI_LANGUAGES",
    "LanguageSpec",
    "build_catalogs",
]
