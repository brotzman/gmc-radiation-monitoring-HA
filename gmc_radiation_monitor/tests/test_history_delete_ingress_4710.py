from pathlib import Path

from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def _app(tmp_path: Path) -> ReportApplication:
    return ReportApplication(
        store=HistoryStore(tmp_path / "history.sqlite"),
        timezone_name="Europe/Berlin",
        scan_interval_seconds=60,
        read_gyro=False,
        cpm_per_usvh=154.0,
        purge_all_history_enabled=True,
    )


def test_purge_form_posts_to_ingress_root_query(tmp_path: Path):
    page = _app(tmp_path).render_index(language_override="de", mode_override="advanced").decode()
    assert 'action="?action=purge-all-history"' in page
    assert 'action="purge-all-history"' not in page


def test_purge_success_link_stays_on_ingress_root():
    source = Path(__file__).parents[1] / "rootfs/usr/local/lib/gmc_bridge/report_web_http.py"
    text = source.read_text()
    assert 'href="./?mode=advanced&amp;lang={t.language}"' in text
    assert 'href="../?mode=advanced&amp;lang={t.language}"' not in text
