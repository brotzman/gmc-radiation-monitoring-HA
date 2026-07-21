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


# Version 8.3.2 usability wording for the visible report-format guide.
_report_format_guide_overrides = {
    "en": {
        "Best for reading, printing and sharing": "Best for reading, printing and sharing",
        "Includes raw data, checksums and reproducibility metadata": "Includes raw data, checksums and reproducibility metadata",
        "For spreadsheets and further analysis": "For spreadsheets and further analysis",
    },
    "de": {
        "Best for reading, printing and sharing": "Am besten zum Lesen, Drucken und Weitergeben",
        "Includes raw data, checksums and reproducibility metadata": "Enthält Rohdaten, Prüfsummen und Angaben zur Reproduzierbarkeit",
        "For spreadsheets and further analysis": "Für Tabellenprogramme und weiterführende Auswertungen",
    },
    "fr": {
        "Best for reading, printing and sharing": "Idéal pour la lecture, l’impression et le partage",
        "Includes raw data, checksums and reproducibility metadata": "Inclut les données brutes, les sommes de contrôle et les métadonnées de reproductibilité",
        "For spreadsheets and further analysis": "Pour les tableurs et les analyses complémentaires",
    },
    "es": {
        "Best for reading, printing and sharing": "Ideal para leer, imprimir y compartir",
        "Includes raw data, checksums and reproducibility metadata": "Incluye datos sin procesar, sumas de comprobación y metadatos de reproducibilidad",
        "For spreadsheets and further analysis": "Para hojas de cálculo y análisis posteriores",
    },
    "it": {
        "Best for reading, printing and sharing": "Ideale per lettura, stampa e condivisione",
        "Includes raw data, checksums and reproducibility metadata": "Include dati grezzi, checksum e metadati di riproducibilità",
        "For spreadsheets and further analysis": "Per fogli di calcolo e ulteriori analisi",
    },
    "nl": {
        "Best for reading, printing and sharing": "Geschikt voor lezen, afdrukken en delen",
        "Includes raw data, checksums and reproducibility metadata": "Bevat ruwe gegevens, controlesommen en reproduceerbaarheidsmetadata",
        "For spreadsheets and further analysis": "Voor spreadsheets en verdere analyse",
    },
    "pl": {
        "Best for reading, printing and sharing": "Najlepszy do czytania, drukowania i udostępniania",
        "Includes raw data, checksums and reproducibility metadata": "Zawiera dane surowe, sumy kontrolne i metadane odtwarzalności",
        "For spreadsheets and further analysis": "Do arkuszy kalkulacyjnych i dalszej analizy",
    },
    "hr": {
        "Best for reading, printing and sharing": "Najbolje za čitanje, ispis i dijeljenje",
        "Includes raw data, checksums and reproducibility metadata": "Uključuje sirove podatke, kontrolne zbrojeve i metapodatke ponovljivosti",
        "For spreadsheets and further analysis": "Za proračunske tablice i daljnju analizu",
    },
}
for _language, _catalogue in _report_format_guide_overrides.items():
    CATALOGS[_language].update(_catalogue)


# Version 8.3.3 detector-calibration and dual-tube presentation.
_calibration_panel_overrides = {
    "en": {
        "Documented calibration": "Documented calibration",
        "Working values": "Working values",
        "Incomplete calibration": "Incomplete calibration",
        "Single-tube profile": "Single-tube profile",
        "Separate tube profiles": "Separate tube profiles",
        "Dual-tube calibration curve": "Dual-tube calibration curve",
        "Detector dead time": "Detector dead time",
        "Maximum reliable CPM": "Maximum reliable CPM",
        "Dead-time correction": "Dead-time correction",
        "Conversion-factor uncertainty": "Conversion-factor uncertainty",
        "Calibration uncertainty": "Calibration uncertainty",
        "No calibration reference stored": "No calibration reference stored",
        "Calibration reference": "Calibration reference",
        "Unknown tube": "Unknown tube",
        "Active tube profile": "Active tube profile",
        "Not available: selected tube is not calibrated": "Not available: selected tube is not calibrated",
        "Detector profile": "Detector profile",
        "Low-dose tube profile": "Low-dose tube profile",
        "High-dose tube profile": "High-dose tube profile",
        "Detector and calibration": "Detector and calibration",
        "Calibration mode": "Calibration mode",
        "Tube model": "Tube model",
        "Dual-tube switch": "Dual-tube switch",
        "Active": "Active",
        "Inactive": "Inactive",
        "Conversion factor": "Conversion factor",
    },
    "de": {
        "Documented calibration": "Dokumentierte Kalibrierung",
        "Working values": "Arbeitswerte",
        "Incomplete calibration": "Unvollständige Kalibrierung",
        "Single-tube profile": "Einzelröhrenprofil",
        "Separate tube profiles": "Getrennte Röhrenprofile",
        "Dual-tube calibration curve": "Dual-Tube-Kalibrierkennlinie",
        "Detector dead time": "Detektor-Totzeit",
        "Maximum reliable CPM": "Maximal zuverlässige CPM",
        "Dead-time correction": "Totzeitkorrektur",
        "Conversion-factor uncertainty": "Unsicherheit des Umrechnungsfaktors",
        "Calibration uncertainty": "Kalibrierungsunsicherheit",
        "No calibration reference stored": "Keine Kalibrierungsreferenz gespeichert",
        "Calibration reference": "Kalibrierungsreferenz",
        "Unknown tube": "Unbekanntes Zählrohr",
        "Active tube profile": "Aktives Röhrenprofil",
        "Not available: selected tube is not calibrated": "Nicht verfügbar: Das ausgewählte Zählrohr ist nicht kalibriert",
        "Detector profile": "Detektorprofil",
        "Low-dose tube profile": "Niedrigdosis-Röhrenprofil",
        "High-dose tube profile": "Hochdosis-Röhrenprofil",
        "Detector and calibration": "Detektor und Kalibrierung",
        "Calibration mode": "Kalibrierungsmodus",
        "Tube model": "Röhrenmodell",
        "Dual-tube switch": "Dual-Tube-Umschaltung",
        "Active": "Aktiv",
        "Inactive": "Inaktiv",
        "Conversion factor": "Umrechnungsfaktor",
    },
    "fr": {
        "Documented calibration": "Étalonnage documenté",
        "Working values": "Valeurs de travail",
        "Incomplete calibration": "Étalonnage incomplet",
        "Single-tube profile": "Profil à tube unique",
        "Separate tube profiles": "Profils de tubes séparés",
        "Dual-tube calibration curve": "Courbe d’étalonnage à deux tubes",
        "Detector dead time": "Temps mort du détecteur",
        "Maximum reliable CPM": "CPM fiable maximal",
        "Dead-time correction": "Correction du temps mort",
        "Conversion-factor uncertainty": "Incertitude du facteur de conversion",
        "Calibration uncertainty": "Incertitude d’étalonnage",
        "No calibration reference stored": "Aucune référence d’étalonnage enregistrée",
        "Calibration reference": "Référence d’étalonnage",
        "Unknown tube": "Tube inconnu",
        "Active tube profile": "Profil de tube actif",
        "Not available: selected tube is not calibrated": "Indisponible : le tube sélectionné n’est pas étalonné",
        "Detector profile": "Profil du détecteur",
        "Low-dose tube profile": "Profil du tube faible dose",
        "High-dose tube profile": "Profil du tube haute dose",
        "Detector and calibration": "Détecteur et étalonnage",
        "Calibration mode": "Mode d’étalonnage",
        "Tube model": "Modèle de tube",
        "Dual-tube switch": "Commutation à deux tubes",
        "Active": "Actif",
        "Inactive": "Inactif",
        "Conversion factor": "Facteur de conversion",
    },
    "es": {
        "Documented calibration": "Calibración documentada",
        "Working values": "Valores de trabajo",
        "Incomplete calibration": "Calibración incompleta",
        "Single-tube profile": "Perfil de un tubo",
        "Separate tube profiles": "Perfiles de tubos separados",
        "Dual-tube calibration curve": "Curva de calibración de dos tubos",
        "Detector dead time": "Tiempo muerto del detector",
        "Maximum reliable CPM": "CPM fiable máximo",
        "Dead-time correction": "Corrección de tiempo muerto",
        "Conversion-factor uncertainty": "Incertidumbre del factor de conversión",
        "Calibration uncertainty": "Incertidumbre de calibración",
        "No calibration reference stored": "No hay referencia de calibración guardada",
        "Calibration reference": "Referencia de calibración",
        "Unknown tube": "Tubo desconocido",
        "Active tube profile": "Perfil de tubo activo",
        "Not available: selected tube is not calibrated": "No disponible: el tubo seleccionado no está calibrado",
        "Detector profile": "Perfil del detector",
        "Low-dose tube profile": "Perfil del tubo de dosis baja",
        "High-dose tube profile": "Perfil del tubo de dosis alta",
        "Detector and calibration": "Detector y calibración",
        "Calibration mode": "Modo de calibración",
        "Tube model": "Modelo de tubo",
        "Dual-tube switch": "Conmutación de dos tubos",
        "Active": "Activo",
        "Inactive": "Inactivo",
        "Conversion factor": "Factor de conversión",
    },
    "it": {
        "Documented calibration": "Calibrazione documentata",
        "Working values": "Valori operativi",
        "Incomplete calibration": "Calibrazione incompleta",
        "Single-tube profile": "Profilo a tubo singolo",
        "Separate tube profiles": "Profili dei tubi separati",
        "Dual-tube calibration curve": "Curva di calibrazione a doppio tubo",
        "Detector dead time": "Tempo morto del rivelatore",
        "Maximum reliable CPM": "CPM affidabile massimo",
        "Dead-time correction": "Correzione del tempo morto",
        "Conversion-factor uncertainty": "Incertezza del fattore di conversione",
        "Calibration uncertainty": "Incertezza di calibrazione",
        "No calibration reference stored": "Nessun riferimento di calibrazione memorizzato",
        "Calibration reference": "Riferimento di calibrazione",
        "Unknown tube": "Tubo sconosciuto",
        "Active tube profile": "Profilo del tubo attivo",
        "Not available: selected tube is not calibrated": "Non disponibile: il tubo selezionato non è calibrato",
        "Detector profile": "Profilo del rivelatore",
        "Low-dose tube profile": "Profilo del tubo a bassa dose",
        "High-dose tube profile": "Profilo del tubo ad alta dose",
        "Detector and calibration": "Rivelatore e calibrazione",
        "Calibration mode": "Modalità di calibrazione",
        "Tube model": "Modello del tubo",
        "Dual-tube switch": "Commutazione a doppio tubo",
        "Active": "Attiva",
        "Inactive": "Inattiva",
        "Conversion factor": "Fattore di conversione",
    },
    "nl": {
        "Documented calibration": "Gedocumenteerde kalibratie",
        "Working values": "Werkwaarden",
        "Incomplete calibration": "Onvolledige kalibratie",
        "Single-tube profile": "Profiel met één buis",
        "Separate tube profiles": "Afzonderlijke buisprofielen",
        "Dual-tube calibration curve": "Kalibratiecurve met twee buizen",
        "Detector dead time": "Dode tijd van detector",
        "Maximum reliable CPM": "Maximaal betrouwbare CPM",
        "Dead-time correction": "Dode-tijdcorrectie",
        "Conversion-factor uncertainty": "Onzekerheid van conversiefactor",
        "Calibration uncertainty": "Kalibratieonzekerheid",
        "No calibration reference stored": "Geen kalibratiereferentie opgeslagen",
        "Calibration reference": "Kalibratiereferentie",
        "Unknown tube": "Onbekende buis",
        "Active tube profile": "Actief buisprofiel",
        "Not available: selected tube is not calibrated": "Niet beschikbaar: de gekozen buis is niet gekalibreerd",
        "Detector profile": "Detectorprofiel",
        "Low-dose tube profile": "Lagedosisbuisprofiel",
        "High-dose tube profile": "Hogedosisbuisprofiel",
        "Detector and calibration": "Detector en kalibratie",
        "Calibration mode": "Kalibratiemodus",
        "Tube model": "Buismodel",
        "Dual-tube switch": "Omschakeling met twee buizen",
        "Active": "Actief",
        "Inactive": "Inactief",
        "Conversion factor": "Conversiefactor",
    },
    "pl": {
        "Documented calibration": "Udokumentowana kalibracja",
        "Working values": "Wartości robocze",
        "Incomplete calibration": "Niepełna kalibracja",
        "Single-tube profile": "Profil pojedynczej tuby",
        "Separate tube profiles": "Oddzielne profile tub",
        "Dual-tube calibration curve": "Dwutubowa krzywa kalibracji",
        "Detector dead time": "Czas martwy detektora",
        "Maximum reliable CPM": "Maksymalne wiarygodne CPM",
        "Dead-time correction": "Korekcja czasu martwego",
        "Conversion-factor uncertainty": "Niepewność współczynnika przeliczeniowego",
        "Calibration uncertainty": "Niepewność kalibracji",
        "No calibration reference stored": "Nie zapisano odniesienia kalibracji",
        "Calibration reference": "Odniesienie kalibracji",
        "Unknown tube": "Nieznana tuba",
        "Active tube profile": "Aktywny profil tuby",
        "Not available: selected tube is not calibrated": "Niedostępne: wybrana tuba nie jest skalibrowana",
        "Detector profile": "Profil detektora",
        "Low-dose tube profile": "Profil tuby niskodawkowej",
        "High-dose tube profile": "Profil tuby wysokodawkowej",
        "Detector and calibration": "Detektor i kalibracja",
        "Calibration mode": "Tryb kalibracji",
        "Tube model": "Model tuby",
        "Dual-tube switch": "Przełączanie dwóch tub",
        "Active": "Aktywna",
        "Inactive": "Nieaktywna",
        "Conversion factor": "Współczynnik przeliczeniowy",
    },
    "hr": {
        "Documented calibration": "Dokumentirana kalibracija",
        "Working values": "Radne vrijednosti",
        "Incomplete calibration": "Nepotpuna kalibracija",
        "Single-tube profile": "Profil jedne cijevi",
        "Separate tube profiles": "Odvojeni profili cijevi",
        "Dual-tube calibration curve": "Kalibracijska krivulja s dvije cijevi",
        "Detector dead time": "Mrtvo vrijeme detektora",
        "Maximum reliable CPM": "Najveći pouzdani CPM",
        "Dead-time correction": "Korekcija mrtvog vremena",
        "Conversion-factor uncertainty": "Nesigurnost faktora pretvorbe",
        "Calibration uncertainty": "Nesigurnost kalibracije",
        "No calibration reference stored": "Nije spremljena referenca kalibracije",
        "Calibration reference": "Referenca kalibracije",
        "Unknown tube": "Nepoznata cijev",
        "Active tube profile": "Aktivni profil cijevi",
        "Not available: selected tube is not calibrated": "Nije dostupno: odabrana cijev nije kalibrirana",
        "Detector profile": "Profil detektora",
        "Low-dose tube profile": "Profil niskodozne cijevi",
        "High-dose tube profile": "Profil visokodozne cijevi",
        "Detector and calibration": "Detektor i kalibracija",
        "Calibration mode": "Način kalibracije",
        "Tube model": "Model cijevi",
        "Dual-tube switch": "Prebacivanje dviju cijevi",
        "Active": "Aktivno",
        "Inactive": "Neaktivno",
        "Conversion factor": "Faktor pretvorbe",
    },
}
for _language, _catalogue in _calibration_panel_overrides.items():
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
