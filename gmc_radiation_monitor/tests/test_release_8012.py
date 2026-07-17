from __future__ import annotations

from pathlib import Path

import yaml
from gmc_bridge.version import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]


def test_release_8012_sidebar_icon_and_version() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "8.0.14"
    assert config["version"] == "8.0.14"
    assert config["panel_icon"] == "mdi:radioactive"
    assert (ROOT / "RELEASE_NOTES_8.0.14.md").is_file()
