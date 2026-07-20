from __future__ import annotations

import re
from pathlib import Path

import yaml

from gmc_bridge.history import HistoryStore
from gmc_bridge.i18n import CATALOGS, SUPPORTED_UI_LANGUAGES
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import resolve_language, validate_catalogs


ROOT = Path(__file__).parents[1]


def _app(tmp_path: Path, *, language: str = "auto") -> ReportApplication:
    return ReportApplication(
        store=HistoryStore(tmp_path / "localization.sqlite3"),
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language=language,
        ui_mode="advanced",
    )


def _flatten(value: object, prefix: str = "") -> dict[str, str]:
    flattened: dict[str, str] = {}
    if isinstance(value, dict):
        for key, item in value.items():
            path = f"{prefix}.{key}" if prefix else str(key)
            flattened.update(_flatten(item, path))
    elif isinstance(value, str):
        flattened[prefix] = value
    return flattened


def test_auto_override_uses_browser_language_even_with_fixed_configuration() -> None:
    assert resolve_language("de", accept_language="fr-FR,fr;q=0.9", override="auto") == "fr"
    assert resolve_language("de", accept_language="hr-HR,hr;q=0.9", override="auto") == "hr"
    assert resolve_language("de", accept_language="xx-XX", override="auto") == "en"


def test_dashboard_header_exposes_all_languages_and_localized_world_map(tmp_path: Path) -> None:
    page = _app(tmp_path, language="auto").render_index(
        language_override="de",
        mode_override="advanced",
    ).decode()

    assert '<nav class="language-switcher" aria-label="Sprache">' in page
    assert page.count('class="language-switcher"') == 1
    for code, native_name in (
        ("auto", "Auto"),
        ("de", "Deutsch"),
        ("en", "English"),
        ("es", "Español"),
        ("fr", "Français"),
        ("hr", "Hrvatski"),
        ("it", "Italiano"),
        ("nl", "Nederlands"),
        ("pl", "Polski"),
    ):
        assert f'?lang={code}&amp;mode=advanced' in page
        assert f">{native_name}</a>" in page
    assert '?lang=de&amp;mode=advanced" lang="de" aria-current="page"' in page
    assert "GMCMap-Weltkarte" in page
    assert 'aria-label="GMCMap-Weltkarte öffnen"' in page
    assert "Geiger Counter World Map" not in page
    assert "Lokale Überwachung für GQ-GMC-Geigerzähler" in page


def test_dashboard_auto_link_is_active_while_resolved_page_uses_browser_language(
    tmp_path: Path,
) -> None:
    page = _app(tmp_path, language="de").render_index(
        language_override="auto",
        accept_language="fr-FR,fr;q=0.9",
    ).decode()
    assert '<html lang="fr">' in page
    assert '?lang=auto&amp;mode=advanced" title="Utiliser la langue du navigateur ou du système" aria-current="page">Auto</a>' in page
    assert "Carte mondiale GMCMap" in page


def test_runtime_catalogues_have_no_long_english_fallback_sentences() -> None:
    assert validate_catalogs() == []
    for language in SUPPORTED_UI_LANGUAGES:
        if language == "en":
            continue
        fallback_sentences = []
        for source, translated in CATALOGS[language].items():
            plain_source = re.sub(r"\{[^{}]+\}", "", source)
            if translated == CATALOGS["en"][source] and len(re.findall(r"[A-Za-z]{3,}", plain_source)) >= 4:
                fallback_sentences.append(source)
        assert fallback_sentences == [], f"{language} English fallbacks: {fallback_sentences[:10]}"


def test_configuration_translations_are_complete_without_english_fallbacks() -> None:
    documents = {
        path.stem: _flatten(yaml.safe_load(path.read_text(encoding="utf-8")))
        for path in (ROOT / "translations").glob("*.yaml")
    }
    english = documents["en"]
    for language in SUPPORTED_UI_LANGUAGES:
        if language == "en":
            continue
        assert set(documents[language]) == set(english)
        fallback_sentences = [
            key
            for key, value in documents[language].items()
            if value == english[key]
            and value not in {"CPM per µSv/h"}
            and len(re.findall(r"[A-Za-z]{3,}", value)) >= 2
        ]
        assert fallback_sentences == [], f"{language} configuration fallbacks: {fallback_sentences}"

