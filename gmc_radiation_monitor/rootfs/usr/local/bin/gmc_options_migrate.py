#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

LIB_DIR = Path(__file__).resolve().parents[1] / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from gmc_bridge.options_migration import merge_single_and_dual_device_options  # noqa: E402
from gmc_bridge.supervisor_options import (  # noqa: E402
    SupervisorOptionsError,
    persist_self_options,
)


def main() -> int:
    if len(sys.argv) != 4:
        print("usage: gmc_options_migrate.py OPTIONS_JSON DEVICES_OUT DUAL_OUT", file=sys.stderr)
        return 2

    source = Path(sys.argv[1])
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read app options: {exc}", file=sys.stderr)
        return 3

    migrated, changed = merge_single_and_dual_device_options(payload)
    Path(sys.argv[2]).write_text(
        json.dumps(migrated.get("devices", []), ensure_ascii=False, separators=(",", ":")),
        encoding="utf-8",
    )
    Path(sys.argv[3]).write_text(
        json.dumps(
            migrated.get("dual_tube_devices", []),
            ensure_ascii=False,
            separators=(",", ":"),
        ),
        encoding="utf-8",
    )

    if not changed:
        return 0

    try:
        persist_self_options(
            migrated,
            token=os.environ.get("SUPERVISOR_TOKEN", ""),
        )
    except SupervisorOptionsError as exc:
        print(f"cannot persist migrated app options: {exc}", file=sys.stderr)
        return 11

    return 10


if __name__ == "__main__":
    raise SystemExit(main())
