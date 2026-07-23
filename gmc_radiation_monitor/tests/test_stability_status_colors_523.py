from pathlib import Path


def test_stability_status_colors_are_rendered():
    root = Path("rootfs/usr/local/lib/gmc_bridge")
    source = "\n".join(
        (root / name).read_text()
        for name in ("analysis_presentation.py", "web_analysis_views.py", "web_assets.py", "static/dashboard.css")
    )
    assert 'class="stability-dot {_STATUS_COLOR[entity.status]}"' in source
    assert '"Stable": AnalysisStatus.GOOD' in source
    assert '"Slightly noticeable": AnalysisStatus.NOTICE' in source
    assert '"Unstable": AnalysisStatus.WARNING' in source
    assert '"Critical": AnalysisStatus.ERROR' in source
    assert 'AnalysisStatus.GOOD: "green"' in source
    assert 'AnalysisStatus.LEARNING: "blue"' in source
    assert ".stability-dot.green" in source
    assert ".stability-dot.blue" in source
