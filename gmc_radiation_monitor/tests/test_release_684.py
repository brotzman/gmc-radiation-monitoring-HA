from __future__ import annotations

from pathlib import Path

import yaml
from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication
from gmc_bridge.translations import Translator
from gmc_bridge.version import APP_VERSION


def _configuration_restore_labels() -> dict[str, str]:
    labels: dict[str, str] = {}
    for path in sorted(Path("translations").glob("*.yaml")):
        payload = yaml.safe_load(path.read_text())
        labels[path.stem] = payload["configuration"]["history"]["fields"]["enable_restore"]["name"]
    return labels


def _app(tmp_path: Path) -> ReportApplication:
    return ReportApplication(
        store=HistoryStore(tmp_path / "history.sqlite3"),
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        ui_mode="advanced",
        restore_enabled=False,
        purge_all_history_enabled=False,
    )


def test_runtime_restore_label_matches_addon_configuration_translations() -> None:
    labels = _configuration_restore_labels()
    assert labels
    for language, expected in labels.items():
        assert Translator(language)("Allow restore") == expected


def test_disabled_restore_notice_uses_localized_configuration_label(tmp_path: Path) -> None:
    app = _app(tmp_path)
    labels = _configuration_restore_labels()
    for language, expected in labels.items():
        page = app.render_index(language_override=language, mode_override="advanced").decode()
        assert expected in page
        restore_section = page.split("<h2>", 1)[-1] if expected not in page else page
        assert "enable_restore" not in restore_section


def test_release_version_is_690() -> None:
    assert APP_VERSION == "8.1.0"
