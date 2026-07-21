from __future__ import annotations

import json
from pathlib import Path
from string import Formatter

from .de import CATALOG as DE_CATALOG
from .en import CATALOG as EN_CATALOG
from .es import CATALOG as ES_CATALOG
from .fr import CATALOG as FR_CATALOG
from .hr import CATALOG as HR_CATALOG
from .it import CATALOG as IT_CATALOG
from .nl import CATALOG as NL_CATALOG
from .pl import CATALOG as PL_CATALOG
from .workflow import WORKFLOW_CATALOGS

SUPPORTED_UI_LANGUAGES = ('en', 'de', 'fr', 'es', 'it', 'nl', 'pl', 'hr')
CATALOGS: dict[str, dict[str, str]] = {
    "en": EN_CATALOG,
    "de": DE_CATALOG,
    "fr": FR_CATALOG,
    "es": ES_CATALOG,
    "it": IT_CATALOG,
    "nl": NL_CATALOG,
    "pl": PL_CATALOG,
    "hr": HR_CATALOG
}
for _language, _workflow_catalog in WORKFLOW_CATALOGS.items():
    CATALOGS[_language].update(_workflow_catalog)

# Version 8.2.2 completes the audit of newer workflow, diagnostics and
# maintenance strings that previously used their English key as a fallback.
_release_overrides = json.loads(
    Path(__file__).with_name("release_822.json").read_text(encoding="utf-8")
)
for _language, _catalogue in _release_overrides.items():
    CATALOGS[_language].update(_catalogue)

# Version 8.3 stability-card clarification.  These labels are shared by the
# common fleet component, so every connected device uses the same wording and
# its own configured interval and history count.
_stability_card_overrides = {
    "en": {
        "Valid measurements ({hours:g} h)": "Valid measurements ({hours:g} h)",
        "Total stored measurements": "Total stored measurements",
        "Largest measurement interval": "Largest measurement interval",
        "Expected measurement interval": "Expected measurement interval",
        "Maximum interval deviation": "Maximum interval deviation",
    },
    "de": {
        "Valid measurements ({hours:g} h)": "Gültige Messwerte ({hours:g} h)",
        "Total stored measurements": "Gesamt gespeicherte Messwerte",
        "Largest measurement interval": "Größter Messabstand",
        "Expected measurement interval": "Erwartetes Messintervall",
        "Maximum interval deviation": "Maximale Intervallabweichung",
    },
    "fr": {
        "Valid measurements ({hours:g} h)": "Mesures valides ({hours:g} h)",
        "Total stored measurements": "Total des mesures enregistrées",
        "Largest measurement interval": "Plus grand intervalle de mesure",
        "Expected measurement interval": "Intervalle de mesure attendu",
        "Maximum interval deviation": "Écart maximal de l’intervalle",
    },
    "es": {
        "Valid measurements ({hours:g} h)": "Mediciones válidas ({hours:g} h)",
        "Total stored measurements": "Total de mediciones almacenadas",
        "Largest measurement interval": "Mayor intervalo de medición",
        "Expected measurement interval": "Intervalo de medición esperado",
        "Maximum interval deviation": "Desviación máxima del intervalo",
    },
    "it": {
        "Valid measurements ({hours:g} h)": "Misure valide ({hours:g} h)",
        "Total stored measurements": "Totale misure memorizzate",
        "Largest measurement interval": "Intervallo di misura massimo",
        "Expected measurement interval": "Intervallo di misura previsto",
        "Maximum interval deviation": "Deviazione massima dell’intervallo",
    },
    "nl": {
        "Valid measurements ({hours:g} h)": "Geldige metingen ({hours:g} u)",
        "Total stored measurements": "Totaal opgeslagen metingen",
        "Largest measurement interval": "Grootste meetinterval",
        "Expected measurement interval": "Verwacht meetinterval",
        "Maximum interval deviation": "Maximale intervalafwijking",
    },
    "pl": {
        "Valid measurements ({hours:g} h)": "Prawidłowe pomiary ({hours:g} godz.)",
        "Total stored measurements": "Łączna liczba zapisanych pomiarów",
        "Largest measurement interval": "Największy odstęp pomiarowy",
        "Expected measurement interval": "Oczekiwany odstęp pomiarowy",
        "Maximum interval deviation": "Maksymalne odchylenie odstępu",
    },
    "hr": {
        "Valid measurements ({hours:g} h)": "Valjana mjerenja ({hours:g} h)",
        "Total stored measurements": "Ukupno pohranjenih mjerenja",
        "Largest measurement interval": "Najveći razmak mjerenja",
        "Expected measurement interval": "Očekivani razmak mjerenja",
        "Maximum interval deviation": "Najveće odstupanje razmaka",
    },
}
for _language, _catalogue in _stability_card_overrides.items():
    CATALOGS[_language].update(_catalogue)


# Two legacy indirection labels intentionally carry format fields only in their
# translated template. Callers resolve them to the real source sentence before
# formatting.
_PLACEHOLDER_EXCEPTIONS = {
    "Dose rate formula explanation",
    "Radiation traffic light hysteresis explanation",
}


def _fields(text: str) -> set[str]:
    result: set[str] = set()
    for _literal, field, _spec, _conversion in Formatter().parse(text):
        if field:
            result.add(field.split(".", 1)[0].split("[", 1)[0])
    return result


def validate_catalogs() -> list[str]:
    """Return human-readable catalogue problems; an empty list means valid."""
    problems: list[str] = []
    canonical = set(CATALOGS["en"])
    for language in SUPPORTED_UI_LANGUAGES:
        catalogue = CATALOGS[language]
        missing = sorted(canonical - set(catalogue))
        extra = sorted(set(catalogue) - canonical)
        if missing:
            problems.append(f"{language} missing {len(missing)} keys: {missing[:5]}")
        if extra:
            problems.append(f"{language} has {len(extra)} unexpected keys: {extra[:5]}")
        for key in canonical:
            value = catalogue.get(key, "")
            if not value:
                problems.append(f"{language} has an empty translation for {key!r}")
            if key not in _PLACEHOLDER_EXCEPTIONS and _fields(key) != _fields(value):
                problems.append(
                    f"{language} placeholder mismatch for {key!r}: {_fields(key)} != {_fields(value)}"
                )
    return problems
