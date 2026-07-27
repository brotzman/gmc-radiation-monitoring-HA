from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .registry import SUPPORTED_UI_LANGUAGES, build_catalogs
from .validation import validate_catalogs as _validate_catalogs

CATALOG_SOURCE_PATH = Path(__file__).with_name("catalogs.json")


def load_catalogs(path: str | Path = CATALOG_SOURCE_PATH) -> dict[str, dict[str, str]]:
    """Load the single canonical runtime translation source.

    The JSON file contains the fully assembled catalogue for every supported
    language.  Runtime code no longer depends on generated language modules or
    a chain of release-specific override blocks.
    """
    source_path = Path(path)
    try:
        payload: Any = json.loads(source_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Cannot load translation catalogue: {source_path}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("Translation catalogue root must be an object")
    normalized: dict[str, dict[str, str]] = {}
    for language, catalogue in payload.items():
        if not isinstance(language, str) or not isinstance(catalogue, dict):
            raise RuntimeError("Translation catalogues must map language codes to objects")
        normalized[language] = {
            str(key): str(value)
            for key, value in catalogue.items()
            if isinstance(key, str) and isinstance(value, str)
        }
        if len(normalized[language]) != len(catalogue):
            raise RuntimeError(f"Translation catalogue {language!r} contains non-string entries")
    return build_catalogs(normalized)


CATALOGS: dict[str, dict[str, str]] = load_catalogs()


def validate_catalogs() -> list[str]:
    """Validate the canonical runtime catalogues."""
    return _validate_catalogs(CATALOGS, SUPPORTED_UI_LANGUAGES)


__all__ = ["CATALOGS", "CATALOG_SOURCE_PATH", "SUPPORTED_UI_LANGUAGES", "load_catalogs", "validate_catalogs"]
