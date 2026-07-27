from __future__ import annotations

from collections.abc import Mapping, Sequence
from string import Formatter

_PLACEHOLDER_EXCEPTIONS = {
    "Dose rate formula explanation",
    "Radiation traffic light hysteresis explanation",
}
_IDENTICAL_TRANSLATION_ALLOWLIST = {
    "Home Assistant API",
    "GMCMap world map",
    "Certificate SHA-256",
    "Correction active",
    "PDF",
    "CSV",
    "JSON",
    "CPM",
    "ACPM",
}


def _fields(text: str) -> set[str]:
    result: set[str] = set()
    for _literal, field, _spec, _conversion in Formatter().parse(text):
        if field:
            result.add(field.split(".", 1)[0].split("[", 1)[0])
    return result


def _looks_untranslated(key: str, value: str) -> bool:
    if key != value or key in _IDENTICAL_TRANSLATION_ALLOWLIST:
        return False
    if "{" in key or "}" in key:
        return False
    words = [
        part
        for part in key.replace("/", " ").replace("-", " ").split()
        if any(character.isalpha() for character in part)
    ]
    return len(key) >= 15 and len(words) >= 2


def validate_catalogs(
    catalogs: Mapping[str, Mapping[str, str]],
    supported_languages: Sequence[str],
) -> list[str]:
    """Return deterministic, human-readable catalogue problems."""
    problems: list[str] = []
    if "en" not in catalogs:
        return ["English reference catalogue is missing"]
    canonical = set(catalogs["en"])
    for language in supported_languages:
        catalogue = catalogs.get(language)
        if catalogue is None:
            problems.append(f"{language} catalogue is missing")
            continue
        missing = sorted(canonical - set(catalogue))
        extra = sorted(set(catalogue) - canonical)
        if missing:
            problems.append(f"{language} missing {len(missing)} keys: {missing[:5]}")
        if extra:
            problems.append(f"{language} has {len(extra)} unexpected keys: {extra[:5]}")
        for key in sorted(canonical):
            value = catalogue.get(key, "")
            if not value:
                problems.append(f"{language} has an empty translation for {key!r}")
                continue
            if key not in _PLACEHOLDER_EXCEPTIONS and _fields(key) != _fields(value):
                problems.append(
                    f"{language} placeholder mismatch for {key!r}: "
                    f"{_fields(key)} != {_fields(value)}"
                )
            if language != "en" and _looks_untranslated(key, value):
                problems.append(f"{language} appears untranslated for {key!r}")
    return problems


__all__ = ["validate_catalogs"]
