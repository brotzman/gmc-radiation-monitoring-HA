from __future__ import annotations

from pathlib import Path

import yaml
from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.version import APP_VERSION

ROOT = Path(__file__).resolve().parents[1]


def _page(tmp_path: Path) -> str:
    store = HistoryStore(tmp_path / "mobile-layout.sqlite3")
    app = ReportApplication(
        store=store,
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_language="de",
        ui_mode="advanced",
    )
    return app.render_index(language_override="de", mode_override="advanced").decode()


def test_8412_release_metadata_is_current() -> None:
    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    assert APP_VERSION == "9.1.2"
    assert config["version"] == "9.1.2"
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    section = changelog.split("## 8.4.12", 1)[1].split("## 8.4.11", 1)[0]
    assert "floating dashboard navigation" in section
    assert "date, week, month and date-time fields" in section


def test_mobile_navigation_remains_sticky_and_compact(tmp_path: Path) -> None:
    page = _page(tmp_path)
    assert ".dashboard-controls { position:-webkit-sticky; position:sticky;" in page
    assert "top:env(safe-area-inset-top,0px)" in page
    assert ".jump-links { flex-wrap:nowrap; overflow-x:auto; overflow-y:hidden;" in page
    assert ".dashboard-controls { position:static;" not in page


def test_temporal_inputs_are_width_constrained(tmp_path: Path) -> None:
    page = _page(tmp_path)
    assert 'input[type="date"], input[type="week"], input[type="month"], input[type="datetime-local"]' in page
    assert "min-inline-size:0; max-inline-size:100%;" in page
    assert ".form-grid > *, label { min-width:0; max-width:100%; }" in page
    assert 'input type="date" name="date"' in page
    assert 'input type="week" name="week"' in page
