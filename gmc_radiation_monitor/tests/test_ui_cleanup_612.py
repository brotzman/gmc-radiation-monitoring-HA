from pathlib import Path

from gmc_bridge.device_profiles import normalize_device_version_display


def _web_source() -> str:
    modules = (
        "report_web.py",
        "web_assets.py",
        "web_analysis_views.py",
        "web_components.py",
    )
    root = Path("rootfs/usr/local/lib/gmc_bridge")
    return "\n".join((root / module).read_text() for module in modules)


def test_compact_device_firmware_labels_gain_a_separator():
    assert normalize_device_version_display("GMC-320Re 4.52") == "GMC-320 Re 4.52"
    assert normalize_device_version_display("GMC-500+Re1.14") == "GMC-500+ Re 1.14"
    assert normalize_device_version_display("GMC-500+ Re 1.14") == "GMC-500+ Re 1.14"


def test_adaptive_profile_has_roomier_layout_without_explanatory_notes():
    source = _web_source()
    assert "#adaptive-background .collapsible-card-body > .assessment-grid" in source
    assert "grid-template-columns:repeat(2,minmax(0,1fr)); gap:1rem" in source
    assert (
        't("All baselines and comparisons use the same robust quality-filtered measurements.")' not in source
    )
    assert 't("The comparison uses only quality-filtered, one-to-one paired measurements.")' not in source


def test_stability_metadata_has_one_unbulleted_nonwrapping_line_per_metric():
    source = _web_source()
    assert 'class="stability-meta-line bullet"' not in source
    assert ".stability-meta-line.bullet::before" not in source
    assert ".stability-meta-line { display:block; white-space:nowrap; }" in source
    assert source.count('class="stability-meta-line">') >= 1
    assert "for metric in entity.metrics" in source


def test_stability_cards_use_two_equal_width_columns():
    source = _web_source()
    assert ".stability-grid { grid-template-columns:repeat(2,minmax(0,1fr));" in source
    assert 'class="assessment-grid stability-grid"' in source


def test_assessment_explanation_has_space_before_following_status_cards():
    source = _web_source()
    assert "details.assessment-legend { margin-bottom: 1rem; }" in source
    assert 'class="analysis-group assessment-legend"' in source
