from __future__ import annotations

from pathlib import Path

import yaml

from gmc_bridge.runtime_options import runtime_environment


def test_history_configuration_exposes_exactly_one_protected_management_switch() -> None:
    config = yaml.safe_load(Path("config.yaml").read_text())
    options = config["options"]["history"]
    schema = config["schema"]["history"]
    assert options["history_management_enabled"] is False
    assert schema["history_management_enabled"] == "bool"
    assert "enable_restore" not in options
    assert "enable_purge_all_history" not in options
    assert "enable_restore" not in schema
    assert "enable_purge_all_history" not in schema


def test_legacy_history_switches_migrate_to_single_runtime_gate() -> None:
    legacy = runtime_environment(
        {"devices": [{}], "history": {"enable_restore": True}},
        "reports",
    )
    current = runtime_environment(
        {"devices": [{}], "history": {"history_management_enabled": True}},
        "reports",
    )
    assert legacy["HISTORY_MANAGEMENT_ENABLED"] == "true"
    assert current["HISTORY_MANAGEMENT_ENABLED"] == "true"
    assert current["ENABLE_RESTORE"] == "true"
    assert current["ENABLE_PURGE_ALL_HISTORY"] == "true"


def test_history_explorer_contains_explicit_axes_quick_ranges_and_responsive_chart() -> None:
    workflow = Path("rootfs/usr/local/lib/gmc_bridge/workflow_web.py").read_text()
    css = Path("rootfs/usr/local/lib/gmc_bridge/web_assets.py").read_text()
    assert 't("Local date and time")' in workflow
    assert 't("Count rate [CPM]")' in workflow
    assert "24 h" in workflow
    assert "7 days" in workflow
    assert "30 days" in workflow
    assert "90 days" in workflow
    assert "history-trend-line" in workflow
    assert ".workflow-history-chart" in css
    assert "overflow-x:auto" in css.replace(" ", "")


def test_release_notes_describe_combined_beta_gamma_scope_and_report_structure() -> None:
    notes = Path("RELEASE_NOTES_8.3.1.md").read_text()
    assert "five-page" in notes
    assert "Count rate [CPM]" in notes
    assert "combined beta/gamma response" in notes
    assert "history_management_enabled" in notes
