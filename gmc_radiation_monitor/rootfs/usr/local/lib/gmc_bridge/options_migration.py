from __future__ import annotations

from copy import deepcopy
from typing import Any


def _name(item: dict[str, Any]) -> str:
    return str(item.get("name") or "").strip().casefold()


def merge_single_and_dual_device_options(options: dict[str, Any]) -> tuple[dict[str, Any], bool]:
    """Normalize legacy 8.4.1 split overrides into one entry per physical device.

    Version 8.4.1 stored common GMC-500+ settings under ``devices`` and only
    second-tube overrides under ``dual_tube_devices``. Version 8.4.2 renders a
    complete GMC-500+ entry in the dual-tube list. This migration is deliberately
    lossless and idempotent so it can be used both at startup and by tests/imports.
    """

    normalized = deepcopy(options)
    single_value = normalized.get("devices", [])
    dual_value = normalized.get("dual_tube_devices", [])
    if not isinstance(single_value, list) or not isinstance(dual_value, list):
        return normalized, False

    singles = [deepcopy(item) for item in single_value if isinstance(item, dict)]
    duals = [deepcopy(item) for item in dual_value if isinstance(item, dict)]
    changed = False
    consumed: set[int] = set()
    merged_duals: list[dict[str, Any]] = []

    for dual in duals:
        key = _name(dual)
        matches = [
            (index, item)
            for index, item in enumerate(singles)
            if index not in consumed and key and _name(item) == key
        ]
        if len(matches) == 1:
            index, common = matches[0]
            merged = deepcopy(common)
            merged.update(dual)
            merged_duals.append(merged)
            consumed.add(index)
            changed = True
        else:
            merged_duals.append(dual)

    remaining_singles = [item for index, item in enumerate(singles) if index not in consumed]
    if remaining_singles != single_value or merged_duals != dual_value:
        changed = True
    normalized["devices"] = remaining_singles
    normalized["dual_tube_devices"] = merged_duals
    return normalized, changed
