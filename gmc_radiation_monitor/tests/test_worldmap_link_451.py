from __future__ import annotations

import tempfile
from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def test_global_worldmap_link_is_rendered():
    with tempfile.TemporaryDirectory() as temp_dir:
        store = HistoryStore(Path(temp_dir) / "history.sqlite3")
        app = ReportApplication(
            store=store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
            ui_language="de",
        )
        rendered = app.render_index(language_override="de").decode("utf-8")

    assert 'class="location-details external-map-link"' in rendered
    assert 'href="https://www.gmcmap.com/index.php"' in rendered
    assert 'target="_blank"' in rendered
    assert 'rel="noopener noreferrer external"' in rendered
    assert "Geiger Counter World Map" in rendered
    assert "<small>gmcmap.com</small>" in rendered
    assert '<details class="location-details">' in rendered
