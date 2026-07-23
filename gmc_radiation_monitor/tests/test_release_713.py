from __future__ import annotations

from pathlib import Path

from gmc_bridge.analysis_presentation import build_cosmic_influence_result
from gmc_bridge.translations import Translator
from gmc_bridge.web_analysis_views import render_cosmic_influence

ROOT = Path(__file__).resolve().parents[1]


def _learning_model() -> dict[str, object]:
    return {
        "enabled": True,
        "state": "Pressure model is still being formed",
        "confidence": "Insufficient",
        "pressure_snapshot": {"available": False},
        "reasons": [
            {"key": "At least {days} days of learning data are required", "params": {"days": 30}},
            {"key": "At least {count} valid hourly values are required", "params": {"count": 500}},
            {"key": "At least {span:g} hPa pressure variation is required", "params": {"span": 10}},
            {"key": "Too few pressure/CPM pairs", "params": {}},
        ],
    }


def test_cosmic_learning_reasons_are_grouped_into_one_card() -> None:
    rendered = render_cosmic_influence(build_cosmic_influence_result(_learning_model()), Translator("de"))
    assert rendered.count('class="note cosmic-reasons"') == 1
    grouped = rendered.split('class="note cosmic-reasons"', 1)[1].split("</div>", 1)[0]
    assert grouped.count("<li ") == 4
    assert "Mindestens 30 Tage Lerndaten sind erforderlich" in grouped
    assert "Mindestens 500 gültige Stundenwerte sind erforderlich" in grouped
    assert "Mindestens 10 hPa beobachtete Druckspanne sind erforderlich" in grouped
    assert "Zu wenige Luftdruck-/CPM-Paare" in grouped


def test_redundant_statistical_indication_message_is_not_rendered() -> None:
    result = build_cosmic_influence_result(_learning_model())
    assert all(message.key != "pressure-statistical-label" for message in result.messages)
    rendered = render_cosmic_influence(result, Translator("de"))
    assert "Nur statistischer Hinweis" not in rendered


def test_recommendation_block_has_clear_spacing_after_metrics() -> None:
    source = (ROOT / "rootfs/usr/local/lib/gmc_bridge/static/dashboard.css").read_text(encoding="utf-8")
    assert ".recommendation-card { display:grid;" in source
    assert "margin:1.05rem 0 1rem;" in source
