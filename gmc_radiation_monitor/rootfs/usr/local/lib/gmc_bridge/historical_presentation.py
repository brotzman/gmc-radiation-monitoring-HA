from __future__ import annotations

from typing import Any, Protocol

from .analysis_presentation import build_historical_section
from .web_analysis_views import render_historical_section


class TranslatorLike(Protocol):
    def __call__(self, text: str, **values: object) -> str: ...


def trend_symbol(value: float | None) -> str:
    if value is None:
        return "—"
    if value > 1.0:
        return "↗"
    if value < -1.0:
        return "↘"
    return "→"


def render_historical_development(
    *, profile: dict[str, Any], translator: TranslatorLike
) -> str:
    """Compatibility facade over the shared historical analysis model."""
    return render_historical_section(build_historical_section(profile), translator)
