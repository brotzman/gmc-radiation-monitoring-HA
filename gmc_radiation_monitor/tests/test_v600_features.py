import sys
from pathlib import Path

LIB = Path(__file__).resolve().parents[1] / "rootfs/usr/local/lib"
sys.path.insert(0, str(LIB))

from gmc_bridge.intelligence import build_radiation_intelligence


def test_intelligence_rises_for_shared_signal():
    analysis = {
        "available": True,
        "baseline_ready": True,
        "data_quality_score_24h": 95,
        "z_score_24h": 3.0,
        "baseline_deviation_percent": 40,
        "trend_30m_cpm": 3,
    }
    result = build_radiation_intelligence(
        analysis, comparison={"agreement_percent": 92}, shared_event={"active": True}
    )
    assert result["probability_percent"] >= 70
    assert result["confidence"] == "High"


def test_config_version_and_fields():
    text = (Path(__file__).resolve().parents[1] / "config.yaml").read_text()
    assert "version: 8.4.5" in text
    assert "firmware_reference_version" not in text
    assert "firmware_information_url" not in text


def test_v601_intelligence_texts_are_localized():
    from gmc_bridge.translations import SUPPORTED_UI_LANGUAGES, Translator

    keys = (
        "GMC Radiation Monitoring",
        "Local background is still being learned",
        "Local background model is available",
        "Data quality is too low for a reliable assessment",
        "Both connected counters show a simultaneous rise",
    )
    for language in SUPPORTED_UI_LANGUAGES:
        translator = Translator(language)
        for key in keys:
            translated = translator(key)
            assert translated
            if language != "en":
                assert translated != key, f"{language} still falls back to English for {key!r}"
    assert Translator("de")("GMC Radiation Monitoring") == "GMC-Strahlungsüberwachung"


def test_firmware_monitoring_is_removed_from_current_app():
    from gmc_bridge import report_web

    config_text = (Path(__file__).resolve().parents[1] / "config.yaml").read_text()
    source = Path(report_web.__file__).read_text()
    assert "firmware_reference_version" not in config_text
    assert "firmware_information_url" not in config_text
    assert "Firmware monitoring" not in source
    assert "firmware_status" not in source
