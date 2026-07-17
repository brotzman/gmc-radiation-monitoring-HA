from pathlib import Path


def test_mobile_analysis_reflows_without_page_horizontal_scrolling() -> None:
    source = Path("rootfs/usr/local/lib/gmc_bridge/web_assets.py").read_text(encoding="utf-8")
    assert "overflow-x: hidden;" in source
    assert "touch-action: pan-y;" in source
    assert (
        ".assessment-grid, .assessment-grid.baseline-grid { grid-template-columns:repeat(2,minmax(0,1fr)); }"
        in source
    )
    assert ".assessment-grid, .assessment-grid.baseline-grid { grid-template-columns:1fr; }" in source
    assert ".assessment-primary { grid-column:1 / -1; }" in source
    assert ".table-wrap { overflow-x: auto;" in source
    assert ".control-options { overflow-x:auto;" not in source
