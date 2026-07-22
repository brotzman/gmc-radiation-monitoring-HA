from __future__ import annotations

from pathlib import Path

import yaml
from gmc_bridge.reports import (
    _PAGE1_ASSESSMENT_RECT,
    _PAGE1_CHART_RECT,
    _PAGE1_METROLOGY_Y,
)
from gmc_bridge.version import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]


def test_8411_release_metadata_and_notes_are_current() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "8.4.11"
    assert config["version"] == "8.4.11"
    notes = (ROOT / "RELEASE_NOTES_8.4.11.md").read_text(encoding="utf-8")
    assert "report-layout maintenance release" in notes
    assert "released in version 8.4.10" in notes
    assert "bridge-heartbeat behavior" in notes


def test_8410_and_8411_documentation_scopes_are_separate() -> None:
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    release_8411 = changelog.split("## 8.4.11", 1)[1].split("\n## ", 1)[0]
    release_8410 = changelog.split("## 8.4.10", 1)[1].split("\n## ", 1)[0]
    assert "report-layout" in release_8411
    assert "Added an independent atomic bridge heartbeat" not in release_8411
    assert "independent atomic bridge heartbeat" in release_8410
    assert "report-layout" not in release_8410


def test_8411_page_one_regions_keep_minimum_spacing() -> None:
    _chart_x, chart_bottom, _chart_width, _chart_height = _PAGE1_CHART_RECT
    _panel_x, panel_bottom, _panel_width, panel_height = _PAGE1_ASSESSMENT_RECT
    panel_top = panel_bottom + panel_height
    assert chart_bottom - _PAGE1_METROLOGY_Y >= 0.055
    assert _PAGE1_METROLOGY_Y - panel_top >= 0.02
    assert chart_bottom - panel_top >= 0.08
