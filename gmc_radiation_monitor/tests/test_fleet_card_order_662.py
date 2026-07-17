from __future__ import annotations

from types import SimpleNamespace

from gmc_bridge.report_web import ReportApplication


def test_fleet_stability_cards_prefer_320_then_500() -> None:
    items = [
        SimpleNamespace(label="GMC-500+ Re 2.53", serial="500"),
        SimpleNamespace(label="GMC-320 Re 4.52", serial="320"),
    ]

    ordered = sorted(items, key=ReportApplication._fleet_stability_display_key)

    assert [item.serial for item in ordered] == ["320", "500"]


def test_fleet_stability_display_order_is_independent_of_input_order() -> None:
    items = [
        SimpleNamespace(label="GMC-320 Re 4.52", serial="320"),
        SimpleNamespace(label="GMC-500+ Re 2.53", serial="500"),
    ]

    ordered = sorted(reversed(items), key=ReportApplication._fleet_stability_display_key)

    assert [item.serial for item in ordered] == ["320", "500"]
