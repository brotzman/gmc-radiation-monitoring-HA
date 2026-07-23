from __future__ import annotations

import re
from decimal import Decimal
from typing import Any

_NUMERIC_TOKEN = re.compile(
    r"(?<![\w.])(?P<sign>[+-]?)(?P<number>(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?)(?![\w.]|\.\d)"
)


def translator_language(translator: object) -> str:
    """Return the language carried by a translator or translator wrapper."""
    current: object | None = translator
    visited: set[int] = set()
    while current is not None and id(current) not in visited:
        visited.add(id(current))
        language = getattr(current, "language", None)
        if isinstance(language, str) and language:
            return language
        current = getattr(current, "_translator", None)
    return "en"


def _swap_german_separators(text: str) -> str:
    marker = "\u0000"
    return text.replace(",", marker).replace(".", ",").replace(marker, ".")


def format_number(
    value: int | float | Decimal,
    language: str,
    *,
    decimals: int | None = None,
    grouping: bool = False,
    sign: bool = False,
    trim: bool = False,
) -> str:
    """Format one display number without relying on process-global locales."""
    if isinstance(value, bool):
        value = int(value)
    if decimals is None:
        if isinstance(value, int):
            spec = "+,d" if sign and grouping else "+d" if sign else ",d" if grouping else "d"
        else:
            spec = "+,g" if sign and grouping else "+g" if sign else ",g" if grouping else "g"
    else:
        spec = f"{'+' if sign else ''}{',' if grouping else ''}.{max(0, int(decimals))}f"
    rendered = format(value, spec)
    if trim and "." in rendered:
        rendered = rendered.rstrip("0").rstrip(".")
    return _swap_german_separators(rendered) if language == "de" else rendered


def localize_numeric_text(text: Any, language: str, *, group_plain_integers: bool = False) -> str:
    """Localize display numbers embedded in already formatted UI strings.

    Version-like tokens with multiple decimal points are deliberately left alone.
    This function is intended for visible measurement/statistics text, not HTML
    attributes, paths or machine-readable values.
    """
    rendered = str(text)
    if language != "de" or not rendered:
        return rendered

    def replace(match: re.Match[str]) -> str:
        # Revision and firmware numbers are identifiers rather than display quantities.
        if re.search(r"(?:\bRe|\bRev(?:ision)?|\bFirmware)\s*$", rendered[max(0, match.start() - 18):match.start()], re.IGNORECASE):
            return match.group(0)
        sign = match.group("sign") or ""
        number = match.group("number")
        if number.count(".") > 1:
            return match.group(0)
        if "," in number and "." in number:
            localized = _swap_german_separators(number)
        elif "," in number:
            localized = number.replace(",", ".")
        elif "." in number:
            localized = number.replace(".", ",")
        elif group_plain_integers and len(number) >= 4 and not number.startswith("0"):
            localized = f"{int(number):,}".replace(",", ".")
        else:
            localized = number
        return sign + localized

    return _NUMERIC_TOKEN.sub(replace, rendered)


class LocalizedNumber:
    """Number wrapper that honours format specs inside translated templates."""

    __slots__ = ("value", "language")

    def __init__(self, value: int | float | Decimal, language: str) -> None:
        self.value = value
        self.language = language

    def __format__(self, spec: str) -> str:
        rendered = format(self.value, spec)
        return _swap_german_separators(rendered) if self.language == "de" else rendered

    def __str__(self) -> str:
        return format_number(self.value, self.language)

    def __repr__(self) -> str:
        return repr(self.value)
