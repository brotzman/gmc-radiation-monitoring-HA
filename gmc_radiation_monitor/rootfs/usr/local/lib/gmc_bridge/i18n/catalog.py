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


# Version 8.3.4 detector-calibration and dual-tube presentation.
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

# Version 8.4.0: detector presets, single/dual distinction and reduced duplication.
_calibration_profile_835_overrides = {
    "en": {
        "Predefined profile": "Predefined profile",
        "Customized profile": "Customized profile",
        "Detector preset": "Detector preset",
        "Physical detector layout": "Physical detector layout",
        "Single physical tube": "Single physical tube",
        "Two physical tubes": "Two physical tubes",
        "Custom single-tube profile": "Custom single-tube profile",
        "Custom dual-tube profile": "Custom dual-tube profile",
        "Tube profile": "Tube profile",
        "Primary tube": "Primary tube",
        "Second tube": "Second tube",
        "Primary tube profile": "Primary tube profile",
        "Second tube profile": "Second tube profile",
    },
    "de": {
        "Predefined profile": "Vordefiniertes Profil",
        "Customized profile": "Angepasstes Profil",
        "Detector preset": "Detektor-Voreinstellung",
        "Physical detector layout": "Physischer Detektoraufbau",
        "Single physical tube": "Ein physisches Zählrohr",
        "Two physical tubes": "Zwei physische Zählrohre",
        "Custom single-tube profile": "Benutzerdefiniertes Ein-Zählrohr-Profil",
        "Custom dual-tube profile": "Benutzerdefiniertes Zwei-Zählrohr-Profil",
        "Tube profile": "Zählrohrprofil",
        "Primary tube": "Primäres Zählrohr",
        "Second tube": "Zweites Zählrohr",
        "Primary tube profile": "Profil des primären Zählrohrs",
        "Second tube profile": "Profil des zweiten Zählrohrs",
        "Single-tube profile": "Ein-Zählrohr-Profil",
        "Separate tube profiles": "Getrennte Zählrohrprofile",
        "Dual-tube calibration curve": "Kalibrierkennlinie für zwei Zählrohre",
        "Low-dose tube profile": "Profil des primären Zählrohrs",
        "High-dose tube profile": "Profil des zweiten Zählrohrs",
        "Active tube profile": "Aktives Zählrohrprofil",
        "Dual-tube switch": "Umschaltung des zweiten Zählrohrs",
        "Tube model": "Zählrohrmodell",
    },
    "fr": {
        "Predefined profile": "Profil prédéfini",
        "Customized profile": "Profil personnalisé",
        "Detector preset": "Préréglage du détecteur",
        "Physical detector layout": "Architecture physique du détecteur",
        "Single physical tube": "Un tube physique",
        "Two physical tubes": "Deux tubes physiques",
        "Custom single-tube profile": "Profil personnalisé à un tube",
        "Custom dual-tube profile": "Profil personnalisé à deux tubes",
        "Tube profile": "Profil du tube",
        "Primary tube": "Tube principal",
        "Second tube": "Second tube",
        "Primary tube profile": "Profil du tube principal",
        "Second tube profile": "Profil du second tube",
    },
    "es": {
        "Predefined profile": "Perfil predefinido",
        "Customized profile": "Perfil personalizado",
        "Detector preset": "Preajuste del detector",
        "Physical detector layout": "Disposición física del detector",
        "Single physical tube": "Un tubo físico",
        "Two physical tubes": "Dos tubos físicos",
        "Custom single-tube profile": "Perfil personalizado de un tubo",
        "Custom dual-tube profile": "Perfil personalizado de dos tubos",
        "Tube profile": "Perfil del tubo",
        "Primary tube": "Tubo principal",
        "Second tube": "Segundo tubo",
        "Primary tube profile": "Perfil del tubo principal",
        "Second tube profile": "Perfil del segundo tubo",
    },
    "it": {
        "Predefined profile": "Profilo predefinito",
        "Customized profile": "Profilo personalizzato",
        "Detector preset": "Preimpostazione del rivelatore",
        "Physical detector layout": "Struttura fisica del rivelatore",
        "Single physical tube": "Un tubo fisico",
        "Two physical tubes": "Due tubi fisici",
        "Custom single-tube profile": "Profilo personalizzato a tubo singolo",
        "Custom dual-tube profile": "Profilo personalizzato a doppio tubo",
        "Tube profile": "Profilo del tubo",
        "Primary tube": "Tubo principale",
        "Second tube": "Secondo tubo",
        "Primary tube profile": "Profilo del tubo principale",
        "Second tube profile": "Profilo del secondo tubo",
    },
    "nl": {
        "Predefined profile": "Vooraf ingesteld profiel",
        "Customized profile": "Aangepast profiel",
        "Detector preset": "Detectorvoorinstelling",
        "Physical detector layout": "Fysieke detectoropbouw",
        "Single physical tube": "Eén fysieke buis",
        "Two physical tubes": "Twee fysieke buizen",
        "Custom single-tube profile": "Aangepast profiel met één buis",
        "Custom dual-tube profile": "Aangepast profiel met twee buizen",
        "Tube profile": "Buisprofiel",
        "Primary tube": "Primaire buis",
        "Second tube": "Tweede buis",
        "Primary tube profile": "Profiel van primaire buis",
        "Second tube profile": "Profiel van tweede buis",
    },
    "pl": {
        "Predefined profile": "Profil wstępnie zdefiniowany",
        "Customized profile": "Profil dostosowany",
        "Detector preset": "Ustawienie wstępne detektora",
        "Physical detector layout": "Fizyczny układ detektora",
        "Single physical tube": "Jedna fizyczna tuba",
        "Two physical tubes": "Dwie fizyczne tuby",
        "Custom single-tube profile": "Własny profil jednotubowy",
        "Custom dual-tube profile": "Własny profil dwutubowy",
        "Tube profile": "Profil tuby",
        "Primary tube": "Tuba główna",
        "Second tube": "Druga tuba",
        "Primary tube profile": "Profil tuby głównej",
        "Second tube profile": "Profil drugiej tuby",
    },
    "hr": {
        "Predefined profile": "Unaprijed definirani profil",
        "Customized profile": "Prilagođeni profil",
        "Detector preset": "Zadana postavka detektora",
        "Physical detector layout": "Fizički raspored detektora",
        "Single physical tube": "Jedna fizička cijev",
        "Two physical tubes": "Dvije fizičke cijevi",
        "Custom single-tube profile": "Prilagođeni profil jedne cijevi",
        "Custom dual-tube profile": "Prilagođeni profil dviju cijevi",
        "Tube profile": "Profil cijevi",
        "Primary tube": "Primarna cijev",
        "Second tube": "Druga cijev",
        "Primary tube profile": "Profil primarne cijevi",
        "Second tube profile": "Profil druge cijevi",
    },
}
for _language, _catalogue in _calibration_profile_835_overrides.items():
    CATALOGS[_language].update(_catalogue)

# Version 8.4.0 scientific detector, calibration and raw/corrected workflow.
# Version 8.4.2 reuses these keys with corrected layout and configuration grouping.
_release_840_overrides = {
    "en": {
        "Detector and calibration": "Detector and calibration",
        "Factory calibrated": "Factory calibrated",
        "User profile": "User profile",
        "Not calibrated": "Not calibrated",
        "Unknown": "Unknown",
        "Calibrated": "Calibrated",
        "Not configured": "Not configured",
        "Active": "Active",
        "Current CPM": "Current CPM",
        "Calibration": "Calibration",
        "Dead time": "Dead time",
        "Measurement quality": "Measurement quality",
        "Detector load": "Detector load",
        "Active detector": "Active detector",
        "Model": "Model",
        "Occupancy": "Occupancy",
        "Estimated losses": "Estimated losses",
        "Correction": "Correction",
        "Inactive": "Inactive",
        "No losses": "No losses",
        "Live dose quality": "Live dose quality",
        "High": "High",
        "Medium": "Medium",
        "Low": "Low",
        "Raw CPM": "Raw CPM",
        "Corrected CPM": "Corrected CPM",
        "Dead-time losses": "Dead-time losses",
        "Correction factor": "Correction factor",
        "Detector": "Detector",
        "Conversion factor is implausible": "Conversion factor is implausible",
        "Dead time is missing": "Dead time is missing",
        "Tube model is unknown": "Tube model is unknown",
        "Calibration is incomplete": "Calibration is incomplete",
        "Dead time is implausible": "Dead time is implausible",
        "Non-Paralyzable": "Non-Paralyzable",
        "Device comparison": "Device comparison",
        "Compare the latest accepted count rate of all connected GMC devices.": "Compare the latest accepted count rate of all connected GMC devices.",
        "Maximum deviation": "Maximum deviation",
        "Check difference": "Check difference",
        "Calibration profiles": "Calibration profiles",
        "Review predefined detector profiles, create device-specific profiles and audit every change.": "Review predefined detector profiles, create device-specific profiles and audit every change.",
        "Predefined profiles": "Predefined profiles",
        "Custom profiles": "Custom profiles",
        "No custom calibration profiles yet.": "No custom calibration profiles yet.",
        "Calibration assistant": "Calibration assistant",
        "Create a transparent custom calibration profile in four steps.": "Create a transparent custom calibration profile in four steps.",
        "Select device": "Select device",
        "Confirm tube": "Confirm tube",
        "Apply calibration": "Apply calibration",
        "Done": "Done",
        "Profile ID": "Profile ID",
        "Profile name": "Profile name",
        "CPM per µSv/h": "CPM per µSv/h",
        "Maximum reliable CPM": "Maximum reliable CPM",
        "Dead-time model": "Dead-time model",
        "Source": "Source",
        "User": "User",
        "Manufacturer": "Manufacturer",
        "Import": "Import",
        "Comment": "Comment",
        "New calibration": "New calibration",
        "Calibration history": "Calibration history",
        "Date, changed values, source and comment": "Date, changed values, source and comment",
        "Profile saved": "Profile saved",
        "No calibration changes have been recorded yet.": "No calibration changes have been recorded yet.",
        "Open calibration history JSON": "Open calibration history JSON",
        "Open calibration profiles JSON": "Open calibration profiles JSON",
        "Data mode": "Data mode",
        "Raw data": "Raw data",
        "Dead-time corrected": "Dead-time corrected",
        "Raw and corrected comparison": "Raw and corrected comparison",
        "Comparison view": "Comparison view",
        "Report data mode": "Report data mode",
        "Choose whether charts and statistics use raw or dead-time-corrected values.": "Choose whether charts and statistics use raw or dead-time-corrected values.",
        "Scientific PDF": "Scientific PDF",
        "Scientific ZIP bundle": "Scientific ZIP bundle",
        "Profile ID, profile name, tube model and conversion factor are required": "Profile ID, profile name, tube model and conversion factor are required",
        "Unsupported dead-time model": "Unsupported dead-time model",
        "Unsupported data mode": "Unsupported data mode",
    },
    "de": {
        "Detector and calibration": "Detektor & Kalibrierung",
        "Factory calibrated": "Werkskalibriert",
        "User profile": "Benutzerprofil",
        "Not calibrated": "Nicht kalibriert",
        "Unknown": "Unbekannt",
        "Calibrated": "Kalibriert",
        "Not configured": "Nicht konfiguriert",
        "Active": "Aktiv",
        "Current CPM": "Aktuelle CPM",
        "Calibration": "Kalibrierung",
        "Dead time": "Totzeit",
        "Measurement quality": "Messqualität",
        "Detector load": "Detektorauslastung",
        "Active detector": "Aktiver Detektor",
        "Model": "Modell",
        "Occupancy": "Auslastung",
        "Estimated losses": "Geschätzte Verluste",
        "Correction": "Korrektur",
        "Inactive": "Inaktiv",
        "No losses": "Keine Verluste",
        "Live dose quality": "Live-Dosisqualität",
        "High": "Hoch",
        "Medium": "Mittel",
        "Low": "Niedrig",
        "Raw CPM": "Roh-CPM",
        "Corrected CPM": "Korrigierte CPM",
        "Dead-time losses": "Totzeitverluste",
        "Correction factor": "Korrekturfaktor",
        "Detector": "Detektor",
        "Conversion factor is implausible": "Umrechnungsfaktor unplausibel",
        "Dead time is missing": "Totzeit fehlt",
        "Tube model is unknown": "Zählrohrmodell unbekannt",
        "Calibration is incomplete": "Kalibrierung unvollständig",
        "Dead time is implausible": "Totzeit unplausibel",
        "Non-Paralyzable": "Nicht lähmend",
        "Device comparison": "Gerätevergleich",
        "Compare the latest accepted count rate of all connected GMC devices.": "Vergleicht die neuesten akzeptierten Zählraten aller verbundenen GMC-Geräte.",
        "Maximum deviation": "Maximale Abweichung",
        "Check difference": "Abweichung prüfen",
        "Calibration profiles": "Kalibrierungsprofile",
        "Review predefined detector profiles, create device-specific profiles and audit every change.": "Vordefinierte Detektorprofile prüfen, gerätespezifische Profile erstellen und jede Änderung nachvollziehen.",
        "Predefined profiles": "Vordefinierte Profile",
        "Custom profiles": "Eigene Profile",
        "No custom calibration profiles yet.": "Noch keine eigenen Kalibrierungsprofile vorhanden.",
        "Calibration assistant": "Kalibrierungsassistent",
        "Create a transparent custom calibration profile in four steps.": "Erstellt in vier Schritten ein nachvollziehbares eigenes Kalibrierungsprofil.",
        "Select device": "Gerät auswählen",
        "Confirm tube": "Zählrohr bestätigen",
        "Apply calibration": "Kalibrierung übernehmen",
        "Done": "Fertig",
        "Profile ID": "Profil-ID",
        "Profile name": "Profilname",
        "CPM per µSv/h": "CPM je µSv/h",
        "Maximum reliable CPM": "Maximal zuverlässige CPM",
        "Dead-time model": "Totzeitmodell",
        "Source": "Quelle",
        "User": "Benutzer",
        "Manufacturer": "Hersteller",
        "Import": "Import",
        "Comment": "Kommentar",
        "New calibration": "Neue Kalibrierung",
        "Calibration history": "Kalibrierhistorie",
        "Date, changed values, source and comment": "Datum, geänderte Werte, Quelle und Kommentar",
        "Profile saved": "Profil gespeichert",
        "No calibration changes have been recorded yet.": "Noch keine Kalibrieränderungen aufgezeichnet.",
        "Open calibration history JSON": "Kalibrierhistorie als JSON öffnen",
        "Open calibration profiles JSON": "Kalibrierungsprofile als JSON öffnen",
        "Data mode": "Datenmodus",
        "Raw data": "Rohdaten",
        "Dead-time corrected": "Totzeitkorrigiert",
        "Raw and corrected comparison": "Roh- und Korrekturvergleich",
        "Comparison view": "Vergleichsansicht",
        "Report data mode": "Datenmodus des Berichts",
        "Choose whether charts and statistics use raw or dead-time-corrected values.": "Legt fest, ob Diagramme und Statistiken Rohwerte oder totzeitkorrigierte Werte verwenden.",
        "Scientific PDF": "Wissenschaftliches PDF",
        "Scientific ZIP bundle": "Wissenschaftliches ZIP-Paket",
        "Profile ID, profile name, tube model and conversion factor are required": "Profil-ID, Profilname, Zählrohrmodell und Umrechnungsfaktor sind erforderlich",
        "Unsupported dead-time model": "Nicht unterstütztes Totzeitmodell",
        "Unsupported data mode": "Nicht unterstützter Datenmodus",
    },
    "fr": {
        "Detector and calibration": "Détecteur et étalonnage", "Factory calibrated": "Étalonné en usine", "User profile": "Profil utilisateur", "Not calibrated": "Non étalonné", "Unknown": "Inconnu", "Calibrated": "Étalonné", "Not configured": "Non configuré", "Active": "Actif", "Current CPM": "CPM actuels", "Calibration": "Étalonnage", "Dead time": "Temps mort", "Measurement quality": "Qualité de mesure", "Detector load": "Charge du détecteur", "Active detector": "Détecteur actif", "Model": "Modèle", "Occupancy": "Occupation", "Estimated losses": "Pertes estimées", "Correction": "Correction", "Inactive": "Inactive", "No losses": "Aucune perte", "Live dose quality": "Qualité de dose en direct", "High": "Élevée", "Medium": "Moyenne", "Low": "Faible", "Raw CPM": "CPM bruts", "Corrected CPM": "CPM corrigés", "Dead-time losses": "Pertes de temps mort", "Correction factor": "Facteur de correction", "Detector": "Détecteur", "Conversion factor is implausible": "Facteur de conversion invraisemblable", "Dead time is missing": "Temps mort manquant", "Tube model is unknown": "Modèle de tube inconnu", "Calibration is incomplete": "Étalonnage incomplet", "Dead time is implausible": "Temps mort invraisemblable", "Non-Paralyzable": "Non paralysable", "Device comparison": "Comparaison des appareils", "Compare the latest accepted count rate of all connected GMC devices.": "Compare les derniers taux de comptage acceptés de tous les appareils GMC connectés.", "Maximum deviation": "Écart maximal", "Check difference": "Vérifier l’écart", "Calibration profiles": "Profils d’étalonnage", "Predefined profiles": "Profils prédéfinis", "Custom profiles": "Profils personnalisés", "No custom calibration profiles yet.": "Aucun profil personnalisé.", "Calibration assistant": "Assistant d’étalonnage", "Select device": "Sélectionner l’appareil", "Confirm tube": "Confirmer le tube", "Apply calibration": "Appliquer l’étalonnage", "Done": "Terminé", "Profile ID": "ID du profil", "Profile name": "Nom du profil", "CPM per µSv/h": "CPM par µSv/h", "Maximum reliable CPM": "CPM fiables maximaux", "Dead-time model": "Modèle de temps mort", "Source": "Source", "User": "Utilisateur", "Manufacturer": "Fabricant", "Import": "Importation", "Comment": "Commentaire", "New calibration": "Nouvel étalonnage", "Calibration history": "Historique d’étalonnage", "Data mode": "Mode de données", "Raw data": "Données brutes", "Dead-time corrected": "Corrigé du temps mort", "Raw and corrected comparison": "Comparaison brut/corrigé", "Comparison view": "Vue comparative", "Report data mode": "Mode de données du rapport", "Scientific PDF": "PDF scientifique", "Scientific ZIP bundle": "Archive ZIP scientifique"
    },
    "es": {
        "Detector and calibration": "Detector y calibración", "Factory calibrated": "Calibrado de fábrica", "User profile": "Perfil de usuario", "Not calibrated": "Sin calibrar", "Unknown": "Desconocido", "Calibrated": "Calibrado", "Not configured": "No configurado", "Active": "Activo", "Current CPM": "CPM actuales", "Calibration": "Calibración", "Dead time": "Tiempo muerto", "Measurement quality": "Calidad de medición", "Detector load": "Carga del detector", "Active detector": "Detector activo", "Model": "Modelo", "Occupancy": "Ocupación", "Estimated losses": "Pérdidas estimadas", "Correction": "Corrección", "Inactive": "Inactiva", "No losses": "Sin pérdidas", "Live dose quality": "Calidad de dosis en directo", "High": "Alta", "Medium": "Media", "Low": "Baja", "Raw CPM": "CPM brutos", "Corrected CPM": "CPM corregidos", "Dead-time losses": "Pérdidas por tiempo muerto", "Correction factor": "Factor de corrección", "Detector": "Detector", "Conversion factor is implausible": "Factor de conversión inverosímil", "Dead time is missing": "Falta el tiempo muerto", "Tube model is unknown": "Modelo de tubo desconocido", "Calibration is incomplete": "Calibración incompleta", "Dead time is implausible": "Tiempo muerto inverosímil", "Non-Paralyzable": "No paralizable", "Device comparison": "Comparación de dispositivos", "Maximum deviation": "Desviación máxima", "Check difference": "Revisar diferencia", "Calibration profiles": "Perfiles de calibración", "Predefined profiles": "Perfiles predefinidos", "Custom profiles": "Perfiles propios", "No custom calibration profiles yet.": "Aún no hay perfiles propios.", "Calibration assistant": "Asistente de calibración", "Select device": "Seleccionar dispositivo", "Confirm tube": "Confirmar tubo", "Apply calibration": "Aplicar calibración", "Done": "Listo", "Profile ID": "ID del perfil", "Profile name": "Nombre del perfil", "CPM per µSv/h": "CPM por µSv/h", "Maximum reliable CPM": "CPM máximos fiables", "Dead-time model": "Modelo de tiempo muerto", "Source": "Fuente", "User": "Usuario", "Manufacturer": "Fabricante", "Import": "Importar", "Comment": "Comentario", "New calibration": "Nueva calibración", "Calibration history": "Historial de calibración", "Data mode": "Modo de datos", "Raw data": "Datos brutos", "Dead-time corrected": "Corregido por tiempo muerto", "Raw and corrected comparison": "Comparación bruto/corregido", "Comparison view": "Vista comparativa", "Report data mode": "Modo de datos del informe", "Scientific PDF": "PDF científico", "Scientific ZIP bundle": "Paquete ZIP científico"
    },
    "it": {
        "Detector and calibration": "Rivelatore e calibrazione", "Factory calibrated": "Calibrato in fabbrica", "User profile": "Profilo utente", "Not calibrated": "Non calibrato", "Unknown": "Sconosciuto", "Calibrated": "Calibrato", "Not configured": "Non configurato", "Active": "Attivo", "Current CPM": "CPM attuali", "Calibration": "Calibrazione", "Dead time": "Tempo morto", "Measurement quality": "Qualità della misura", "Detector load": "Carico del rivelatore", "Active detector": "Rivelatore attivo", "Model": "Modello", "Occupancy": "Occupazione", "Estimated losses": "Perdite stimate", "Correction": "Correzione", "Inactive": "Inattiva", "No losses": "Nessuna perdita", "Live dose quality": "Qualità dose in tempo reale", "High": "Alta", "Medium": "Media", "Low": "Bassa", "Raw CPM": "CPM grezzi", "Corrected CPM": "CPM corretti", "Dead-time losses": "Perdite per tempo morto", "Correction factor": "Fattore di correzione", "Detector": "Rivelatore", "Conversion factor is implausible": "Fattore di conversione non plausibile", "Dead time is missing": "Tempo morto mancante", "Tube model is unknown": "Modello del tubo sconosciuto", "Calibration is incomplete": "Calibrazione incompleta", "Dead time is implausible": "Tempo morto non plausibile", "Non-Paralyzable": "Non paralizzabile", "Device comparison": "Confronto dispositivi", "Maximum deviation": "Deviazione massima", "Check difference": "Controllare la differenza", "Calibration profiles": "Profili di calibrazione", "Predefined profiles": "Profili predefiniti", "Custom profiles": "Profili personalizzati", "Calibration assistant": "Assistente di calibrazione", "Select device": "Seleziona dispositivo", "Confirm tube": "Conferma tubo", "Apply calibration": "Applica calibrazione", "Done": "Fatto", "Profile ID": "ID profilo", "Profile name": "Nome profilo", "CPM per µSv/h": "CPM per µSv/h", "Maximum reliable CPM": "CPM massimi affidabili", "Dead-time model": "Modello del tempo morto", "Source": "Fonte", "User": "Utente", "Manufacturer": "Produttore", "Import": "Importazione", "Comment": "Commento", "New calibration": "Nuova calibrazione", "Calibration history": "Cronologia calibrazione", "Data mode": "Modalità dati", "Raw data": "Dati grezzi", "Dead-time corrected": "Corretto per tempo morto", "Raw and corrected comparison": "Confronto grezzo/corretto", "Comparison view": "Vista confronto", "Report data mode": "Modalità dati rapporto", "Scientific PDF": "PDF scientifico", "Scientific ZIP bundle": "Pacchetto ZIP scientifico"
    },
    "nl": {
        "Detector and calibration": "Detector en kalibratie", "Factory calibrated": "Fabrieksgekalibreerd", "User profile": "Gebruikersprofiel", "Not calibrated": "Niet gekalibreerd", "Unknown": "Onbekend", "Calibrated": "Gekalibreerd", "Not configured": "Niet geconfigureerd", "Active": "Actief", "Current CPM": "Huidige CPM", "Calibration": "Kalibratie", "Dead time": "Dode tijd", "Measurement quality": "Meetkwaliteit", "Detector load": "Detectorbelasting", "Active detector": "Actieve detector", "Model": "Model", "Occupancy": "Bezetting", "Estimated losses": "Geschatte verliezen", "Correction": "Correctie", "Inactive": "Inactief", "No losses": "Geen verliezen", "Live dose quality": "Live dosiskwaliteit", "High": "Hoog", "Medium": "Gemiddeld", "Low": "Laag", "Raw CPM": "Ruwe CPM", "Corrected CPM": "Gecorrigeerde CPM", "Dead-time losses": "Dode-tijdverliezen", "Correction factor": "Correctiefactor", "Detector": "Detector", "Conversion factor is implausible": "Omrekenfactor is onwaarschijnlijk", "Dead time is missing": "Dode tijd ontbreekt", "Tube model is unknown": "Buismodel onbekend", "Calibration is incomplete": "Kalibratie onvolledig", "Dead time is implausible": "Dode tijd is onwaarschijnlijk", "Non-Paralyzable": "Niet-verlammend", "Device comparison": "Apparaatvergelijking", "Maximum deviation": "Maximale afwijking", "Check difference": "Verschil controleren", "Calibration profiles": "Kalibratieprofielen", "Predefined profiles": "Vooraf ingestelde profielen", "Custom profiles": "Eigen profielen", "Calibration assistant": "Kalibratie-assistent", "Select device": "Apparaat selecteren", "Confirm tube": "Buis bevestigen", "Apply calibration": "Kalibratie toepassen", "Done": "Gereed", "Profile ID": "Profiel-ID", "Profile name": "Profielnaam", "CPM per µSv/h": "CPM per µSv/h", "Maximum reliable CPM": "Maximaal betrouwbare CPM", "Dead-time model": "Dode-tijdmodel", "Source": "Bron", "User": "Gebruiker", "Manufacturer": "Fabrikant", "Import": "Import", "Comment": "Opmerking", "New calibration": "Nieuwe kalibratie", "Calibration history": "Kalibratiegeschiedenis", "Data mode": "Gegevensmodus", "Raw data": "Ruwe gegevens", "Dead-time corrected": "Dode-tijdgecorrigeerd", "Raw and corrected comparison": "Vergelijking ruw/gecorrigeerd", "Comparison view": "Vergelijkingsweergave", "Report data mode": "Gegevensmodus rapport", "Scientific PDF": "Wetenschappelijke PDF", "Scientific ZIP bundle": "Wetenschappelijk ZIP-pakket"
    },
    "pl": {
        "Detector and calibration": "Detektor i kalibracja", "Factory calibrated": "Kalibracja fabryczna", "User profile": "Profil użytkownika", "Not calibrated": "Nieskalibrowany", "Unknown": "Nieznany", "Calibrated": "Skalibrowany", "Not configured": "Nieskonfigurowany", "Active": "Aktywny", "Current CPM": "Bieżące CPM", "Calibration": "Kalibracja", "Dead time": "Czas martwy", "Measurement quality": "Jakość pomiaru", "Detector load": "Obciążenie detektora", "Active detector": "Aktywny detektor", "Model": "Model", "Occupancy": "Wykorzystanie", "Estimated losses": "Szacowane straty", "Correction": "Korekcja", "Inactive": "Nieaktywna", "No losses": "Brak strat", "Live dose quality": "Jakość dawki na żywo", "High": "Wysoka", "Medium": "Średnia", "Low": "Niska", "Raw CPM": "Surowe CPM", "Corrected CPM": "Skorygowane CPM", "Dead-time losses": "Straty czasu martwego", "Correction factor": "Współczynnik korekcji", "Detector": "Detektor", "Conversion factor is implausible": "Współczynnik przeliczeniowy jest niewiarygodny", "Dead time is missing": "Brak czasu martwego", "Tube model is unknown": "Nieznany model tuby", "Calibration is incomplete": "Kalibracja niepełna", "Dead time is implausible": "Czas martwy jest niewiarygodny", "Non-Paralyzable": "Nieparaliżujący", "Device comparison": "Porównanie urządzeń", "Maximum deviation": "Maksymalne odchylenie", "Check difference": "Sprawdź różnicę", "Calibration profiles": "Profile kalibracji", "Predefined profiles": "Profile wstępnie zdefiniowane", "Custom profiles": "Profile własne", "Calibration assistant": "Asystent kalibracji", "Select device": "Wybierz urządzenie", "Confirm tube": "Potwierdź tubę", "Apply calibration": "Zastosuj kalibrację", "Done": "Gotowe", "Profile ID": "ID profilu", "Profile name": "Nazwa profilu", "CPM per µSv/h": "CPM na µSv/h", "Maximum reliable CPM": "Maksymalne wiarygodne CPM", "Dead-time model": "Model czasu martwego", "Source": "Źródło", "User": "Użytkownik", "Manufacturer": "Producent", "Import": "Import", "Comment": "Komentarz", "New calibration": "Nowa kalibracja", "Calibration history": "Historia kalibracji", "Data mode": "Tryb danych", "Raw data": "Dane surowe", "Dead-time corrected": "Skorygowane o czas martwy", "Raw and corrected comparison": "Porównanie surowe/skorygowane", "Comparison view": "Widok porównania", "Report data mode": "Tryb danych raportu", "Scientific PDF": "Naukowy PDF", "Scientific ZIP bundle": "Naukowy pakiet ZIP"
    },
    "hr": {
        "Detector and calibration": "Detektor i kalibracija", "Factory calibrated": "Tvornički kalibrirano", "User profile": "Korisnički profil", "Not calibrated": "Nije kalibrirano", "Unknown": "Nepoznato", "Calibrated": "Kalibrirano", "Not configured": "Nije konfigurirano", "Active": "Aktivno", "Current CPM": "Trenutačni CPM", "Calibration": "Kalibracija", "Dead time": "Mrtvo vrijeme", "Measurement quality": "Kvaliteta mjerenja", "Detector load": "Opterećenje detektora", "Active detector": "Aktivni detektor", "Model": "Model", "Occupancy": "Zauzeće", "Estimated losses": "Procijenjeni gubici", "Correction": "Korekcija", "Inactive": "Neaktivna", "No losses": "Bez gubitaka", "Live dose quality": "Kvaliteta doze uživo", "High": "Visoka", "Medium": "Srednja", "Low": "Niska", "Raw CPM": "Sirovi CPM", "Corrected CPM": "Ispravljeni CPM", "Dead-time losses": "Gubici mrtvog vremena", "Correction factor": "Faktor korekcije", "Detector": "Detektor", "Conversion factor is implausible": "Faktor pretvorbe nije vjerodostojan", "Dead time is missing": "Nedostaje mrtvo vrijeme", "Tube model is unknown": "Model cijevi nije poznat", "Calibration is incomplete": "Kalibracija je nepotpuna", "Dead time is implausible": "Mrtvo vrijeme nije vjerodostojno", "Non-Paralyzable": "Neparalizirajući", "Device comparison": "Usporedba uređaja", "Maximum deviation": "Najveće odstupanje", "Check difference": "Provjeri razliku", "Calibration profiles": "Profili kalibracije", "Predefined profiles": "Unaprijed definirani profili", "Custom profiles": "Vlastiti profili", "Calibration assistant": "Pomoćnik za kalibraciju", "Select device": "Odaberi uređaj", "Confirm tube": "Potvrdi cijev", "Apply calibration": "Primijeni kalibraciju", "Done": "Gotovo", "Profile ID": "ID profila", "Profile name": "Naziv profila", "CPM per µSv/h": "CPM po µSv/h", "Maximum reliable CPM": "Najveći pouzdani CPM", "Dead-time model": "Model mrtvog vremena", "Source": "Izvor", "User": "Korisnik", "Manufacturer": "Proizvođač", "Import": "Uvoz", "Comment": "Komentar", "New calibration": "Nova kalibracija", "Calibration history": "Povijest kalibracije", "Data mode": "Način podataka", "Raw data": "Sirovi podaci", "Dead-time corrected": "Ispravljeno za mrtvo vrijeme", "Raw and corrected comparison": "Usporedba sirovo/ispravljeno", "Comparison view": "Usporedni prikaz", "Report data mode": "Način podataka izvješća", "Scientific PDF": "Znanstveni PDF", "Scientific ZIP bundle": "Znanstveni ZIP paket"
    },
}
for _language, _catalogue in _release_840_overrides.items():
    CATALOGS[_language].update(_catalogue)

# Ensure every 8.4.0 key is available in every supported language. Where a
# dedicated translation is not yet present, the English technical term is
# retained rather than exposing an empty label.
for _language in SUPPORTED_UI_LANGUAGES:
    for _key, _english_value in _release_840_overrides["en"].items():
        CATALOGS[_language].setdefault(_key, _english_value)
_none_labels = {"en": "None", "de": "Keine", "fr": "Aucun", "es": "Ninguno", "it": "Nessuno", "nl": "Geen", "pl": "Brak", "hr": "Nema"}
for _language, _value in _none_labels.items():
    CATALOGS[_language]["None"] = _value

# Complete release 8.4 runtime wording in every bundled language.  These
# overrides deliberately avoid long English fallbacks in localized dashboards.
_release_840_complete_translations = {
    "en": {
        "Tube": "Tube",
        "Dead-time occupancy": "Dead-time occupancy",
        "Correction active": "Correction active",
    },
    "de": {
        "Tube": "Zählrohr",
        "Dead-time occupancy": "Totzeitauslastung",
        "Correction active": "Korrektur aktiv",
    },
    "fr": {
        "Tube": "Tube",
        "Dead-time occupancy": "Occupation du temps mort",
        "Correction active": "Correction active",
        "Review predefined detector profiles, create device-specific profiles and audit every change.": "Vérifiez les profils de détecteur prédéfinis, créez des profils propres à chaque appareil et retracez chaque modification.",
        "Create a transparent custom calibration profile in four steps.": "Créez un profil d’étalonnage personnalisé et traçable en quatre étapes.",
        "Date, changed values, source and comment": "Date, valeurs modifiées, source et commentaire",
        "No calibration changes have been recorded yet.": "Aucune modification d’étalonnage n’a encore été enregistrée.",
        "Open calibration history JSON": "Ouvrir l’historique d’étalonnage JSON",
        "Open calibration profiles JSON": "Ouvrir les profils d’étalonnage JSON",
        "Choose whether charts and statistics use raw or dead-time-corrected values.": "Choisissez si les graphiques et les statistiques utilisent les valeurs brutes ou corrigées du temps mort.",
        "Profile ID, profile name, tube model and conversion factor are required": "L’identifiant, le nom du profil, le modèle de tube et le facteur de conversion sont requis",
        "Unsupported dead-time model": "Modèle de temps mort non pris en charge",
    },
    "es": {
        "Tube": "Tubo",
        "Dead-time occupancy": "Ocupación por tiempo muerto",
        "Correction active": "Corrección activa",
        "Review predefined detector profiles, create device-specific profiles and audit every change.": "Revise los perfiles de detector predefinidos, cree perfiles específicos para cada dispositivo y audite cada cambio.",
        "Create a transparent custom calibration profile in four steps.": "Cree un perfil de calibración propio y trazable en cuatro pasos.",
        "Date, changed values, source and comment": "Fecha, valores modificados, fuente y comentario",
        "No calibration changes have been recorded yet.": "Todavía no se han registrado cambios de calibración.",
        "Open calibration history JSON": "Abrir historial de calibración JSON",
        "Open calibration profiles JSON": "Abrir perfiles de calibración JSON",
        "Choose whether charts and statistics use raw or dead-time-corrected values.": "Elija si los gráficos y las estadísticas usan valores brutos o corregidos por tiempo muerto.",
        "Profile ID, profile name, tube model and conversion factor are required": "Se requieren el ID, el nombre del perfil, el modelo de tubo y el factor de conversión",
        "Unsupported dead-time model": "Modelo de tiempo muerto no compatible",
    },
    "it": {
        "Tube": "Tubo",
        "Dead-time occupancy": "Occupazione del tempo morto",
        "Correction active": "Correzione attiva",
        "Review predefined detector profiles, create device-specific profiles and audit every change.": "Verifica i profili del rivelatore predefiniti, crea profili specifici per dispositivo e controlla ogni modifica.",
        "Create a transparent custom calibration profile in four steps.": "Crea un profilo di calibrazione personalizzato e tracciabile in quattro passaggi.",
        "Date, changed values, source and comment": "Data, valori modificati, fonte e commento",
        "No calibration changes have been recorded yet.": "Non sono ancora state registrate modifiche alla calibrazione.",
        "Open calibration history JSON": "Apri cronologia calibrazione JSON",
        "Open calibration profiles JSON": "Apri profili di calibrazione JSON",
        "Choose whether charts and statistics use raw or dead-time-corrected values.": "Scegli se grafici e statistiche usano valori grezzi o corretti per il tempo morto.",
        "Profile ID, profile name, tube model and conversion factor are required": "Sono richiesti ID, nome del profilo, modello del tubo e fattore di conversione",
        "Unsupported dead-time model": "Modello del tempo morto non supportato",
    },
    "nl": {
        "Tube": "Buis",
        "Dead-time occupancy": "Dode-tijdbezetting",
        "Correction active": "Correctie actief",
        "Review predefined detector profiles, create device-specific profiles and audit every change.": "Controleer vooraf ingestelde detectorprofielen, maak apparaatspecifieke profielen en volg elke wijziging.",
        "Create a transparent custom calibration profile in four steps.": "Maak in vier stappen een transparant eigen kalibratieprofiel.",
        "Date, changed values, source and comment": "Datum, gewijzigde waarden, bron en opmerking",
        "No calibration changes have been recorded yet.": "Er zijn nog geen kalibratiewijzigingen vastgelegd.",
        "Open calibration history JSON": "Kalibratiegeschiedenis als JSON openen",
        "Open calibration profiles JSON": "Kalibratieprofielen als JSON openen",
        "Choose whether charts and statistics use raw or dead-time-corrected values.": "Kies of grafieken en statistieken ruwe of voor dode tijd gecorrigeerde waarden gebruiken.",
        "Profile ID, profile name, tube model and conversion factor are required": "Profiel-ID, profielnaam, buismodel en omrekenfactor zijn verplicht",
        "Unsupported dead-time model": "Niet-ondersteund dode-tijdmodel",
    },
    "pl": {
        "Tube": "Tuba",
        "Dead-time occupancy": "Wykorzystanie czasu martwego",
        "Correction active": "Korekcja aktywna",
        "Review predefined detector profiles, create device-specific profiles and audit every change.": "Sprawdź wstępnie zdefiniowane profile detektorów, twórz profile dla konkretnych urządzeń i rejestruj każdą zmianę.",
        "Create a transparent custom calibration profile in four steps.": "Utwórz przejrzysty własny profil kalibracji w czterech krokach.",
        "Date, changed values, source and comment": "Data, zmienione wartości, źródło i komentarz",
        "No calibration changes have been recorded yet.": "Nie zarejestrowano jeszcze żadnych zmian kalibracji.",
        "Open calibration history JSON": "Otwórz historię kalibracji JSON",
        "Open calibration profiles JSON": "Otwórz profile kalibracji JSON",
        "Choose whether charts and statistics use raw or dead-time-corrected values.": "Wybierz, czy wykresy i statystyki mają używać wartości surowych czy skorygowanych o czas martwy.",
        "Profile ID, profile name, tube model and conversion factor are required": "Wymagane są identyfikator, nazwa profilu, model tuby i współczynnik przeliczeniowy",
        "Unsupported dead-time model": "Nieobsługiwany model czasu martwego",
    },
    "hr": {
        "Tube": "Cijev",
        "Dead-time occupancy": "Zauzeće mrtvog vremena",
        "Correction active": "Korekcija aktivna",
        "Review predefined detector profiles, create device-specific profiles and audit every change.": "Pregledajte unaprijed definirane profile detektora, izradite profile za pojedine uređaje i pratite svaku promjenu.",
        "Create a transparent custom calibration profile in four steps.": "Izradite transparentan prilagođeni profil kalibracije u četiri koraka.",
        "Date, changed values, source and comment": "Datum, promijenjene vrijednosti, izvor i komentar",
        "No calibration changes have been recorded yet.": "Još nisu zabilježene promjene kalibracije.",
        "Open calibration history JSON": "Otvori povijest kalibracije JSON",
        "Open calibration profiles JSON": "Otvori profile kalibracije JSON",
        "Choose whether charts and statistics use raw or dead-time-corrected values.": "Odaberite koriste li grafikoni i statistike sirove vrijednosti ili vrijednosti ispravljene za mrtvo vrijeme.",
        "Profile ID, profile name, tube model and conversion factor are required": "Obavezni su ID profila, naziv profila, model cijevi i faktor pretvorbe",
        "Unsupported dead-time model": "Nepodržan model mrtvog vremena",
    },
}
for _language, _catalogue in _release_840_complete_translations.items():
    CATALOGS[_language].update(_catalogue)

_release_840_comparison_sentence = {
    "es": "Compara las últimas tasas de conteo aceptadas de todos los dispositivos GMC conectados.",
    "it": "Confronta le ultime frequenze di conteggio accettate di tutti i dispositivi GMC collegati.",
    "nl": "Vergelijkt de nieuwste geaccepteerde telsnelheid van alle verbonden GMC-apparaten.",
    "pl": "Porównuje najnowsze zaakceptowane szybkości zliczania wszystkich podłączonych urządzeń GMC.",
    "hr": "Uspoređuje najnovije prihvaćene brzine brojanja svih povezanih GMC uređaja.",
}
for _language, _value in _release_840_comparison_sentence.items():
    CATALOGS[_language]["Compare the latest accepted count rate of all connected GMC devices."] = _value

_release_840_no_custom_profiles = {
    "it": "Non sono ancora presenti profili di calibrazione personalizzati.",
    "nl": "Er zijn nog geen eigen kalibratieprofielen.",
    "pl": "Nie ma jeszcze własnych profili kalibracji.",
    "hr": "Još nema vlastitih profila kalibracije.",
}
for _language, _value in _release_840_no_custom_profiles.items():
    CATALOGS[_language]["No custom calibration profiles yet."] = _value

_release_840_final_translations = {
    "de": {"Profile saved": "Profil gespeichert", "Unsupported data mode": "Nicht unterstützter Datenmodus"},
    "fr": {"Profile saved": "Profil enregistré", "Unsupported data mode": "Mode de données non pris en charge"},
    "es": {"Profile saved": "Perfil guardado", "Unsupported data mode": "Modo de datos no compatible"},
    "it": {"Profile saved": "Profilo salvato", "Unsupported data mode": "Modalità dati non supportata"},
    "nl": {"Profile saved": "Profiel opgeslagen", "Unsupported data mode": "Niet-ondersteunde gegevensmodus"},
    "pl": {"Profile saved": "Profil zapisany", "Unsupported data mode": "Nieobsługiwany tryb danych"},
    "hr": {"Profile saved": "Profil spremljen", "Unsupported data mode": "Nepodržani način podataka"},
}
for _language, _catalogue in _release_840_final_translations.items():
    CATALOGS[_language].update(_catalogue)


# Version 8.4.2: precise profile/calibration terminology and measurement-quality explanation.
_release_842_overrides = {
    "en": {
        "Detector profile": "Detector profile",
        "Automatically recognized device profile": "Automatically recognized device profile",
        "Application profile working values": "Application profile working values",
        "Application working values": "Application working values",
        "Documented calibration": "Documented calibration",
        "Measurement quality explanation": "The quality score evaluates data completeness, counting statistics, dead-time load and calibration status. It is not a certified accuracy statement.",
    },
    "de": {
        "Detector profile": "Detektorprofil",
        "Automatically recognized device profile": "Automatisch erkanntes Geräteprofil",
        "Application profile working values": "Arbeitswerte des Anwendungsprofils",
        "Application working values": "Anwendungs-Arbeitswerte",
        "Documented calibration": "Dokumentierte Kalibrierung",
        "Measurement quality explanation": "Die Messqualität bewertet Datenvollständigkeit, Zählstatistik, Totzeitauslastung und Kalibrierstatus. Sie ist keine zertifizierte Genauigkeitsangabe.",
    },
    "fr": {
        "Detector profile": "Profil du détecteur",
        "Automatically recognized device profile": "Profil d’appareil reconnu automatiquement",
        "Application profile working values": "Valeurs de travail du profil d’application",
        "Application working values": "Valeurs de travail de l’application",
        "Documented calibration": "Étalonnage documenté",
        "Measurement quality explanation": "L’indice de qualité évalue l’intégrité des données, la statistique de comptage, la charge de temps mort et l’état d’étalonnage. Il ne constitue pas une précision certifiée.",
    },
    "es": {
        "Detector profile": "Perfil del detector",
        "Automatically recognized device profile": "Perfil de dispositivo reconocido automáticamente",
        "Application profile working values": "Valores de trabajo del perfil de aplicación",
        "Application working values": "Valores de trabajo de la aplicación",
        "Documented calibration": "Calibración documentada",
        "Measurement quality explanation": "El índice de calidad evalúa la integridad de los datos, la estadística de conteo, la carga por tiempo muerto y el estado de calibración. No es una declaración de exactitud certificada.",
    },
    "it": {
        "Detector profile": "Profilo del rivelatore",
        "Automatically recognized device profile": "Profilo dispositivo riconosciuto automaticamente",
        "Application profile working values": "Valori operativi del profilo applicativo",
        "Application working values": "Valori operativi dell’applicazione",
        "Documented calibration": "Calibrazione documentata",
        "Measurement quality explanation": "L’indice di qualità valuta completezza dei dati, statistica di conteggio, carico del tempo morto e stato della calibrazione. Non è una dichiarazione di accuratezza certificata.",
    },
    "nl": {
        "Detector profile": "Detectorprofiel",
        "Automatically recognized device profile": "Automatisch herkend apparaatprofiel",
        "Application profile working values": "Werkwaarden van het toepassingsprofiel",
        "Application working values": "Werkwaarden van de toepassing",
        "Documented calibration": "Gedocumenteerde kalibratie",
        "Measurement quality explanation": "De kwaliteitsscore beoordeelt gegevensvolledigheid, telstatistiek, dode-tijdbelasting en kalibratiestatus. Het is geen gecertificeerde nauwkeurigheidsverklaring.",
    },
    "pl": {
        "Detector profile": "Profil detektora",
        "Automatically recognized device profile": "Automatycznie rozpoznany profil urządzenia",
        "Application profile working values": "Wartości robocze profilu aplikacji",
        "Application working values": "Wartości robocze aplikacji",
        "Documented calibration": "Udokumentowana kalibracja",
        "Measurement quality explanation": "Wskaźnik jakości ocenia kompletność danych, statystykę zliczeń, obciążenie czasem martwym i stan kalibracji. Nie jest certyfikowaną deklaracją dokładności.",
    },
    "hr": {
        "Detector profile": "Profil detektora",
        "Automatically recognized device profile": "Automatski prepoznat profil uređaja",
        "Application profile working values": "Radne vrijednosti profila aplikacije",
        "Application working values": "Radne vrijednosti aplikacije",
        "Documented calibration": "Dokumentirana kalibracija",
        "Measurement quality explanation": "Indeks kvalitete procjenjuje potpunost podataka, statistiku brojanja, opterećenje mrtvim vremenom i status kalibracije. Nije certificirana izjava o točnosti.",
    },
}
for _language, _catalogue in _release_842_overrides.items():
    CATALOGS[_language].update(_catalogue)
