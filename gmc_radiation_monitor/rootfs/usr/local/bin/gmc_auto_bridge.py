#!/usr/bin/env python3
"""Automatic serial discovery wrapper for the GMC bridge."""
from __future__ import annotations

import json
import logging
import os
import sys
from pathlib import Path

LIB_DIR = Path(__file__).resolve().parents[1] / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from gmc_bridge.security_logging import configure_secure_logging  # noqa: E402
from gmc_bridge.serial_autoconfig import AutomaticSerialBridge  # noqa: E402


def main() -> int:
    level_name = os.environ.get("LOG_LEVEL", "info").upper()
    configure_secure_logging(
        level=getattr(logging, level_name, logging.INFO),
        format_string="%(asctime)s %(levelname)s %(message)s",
    )
    try:
        raw = json.loads(os.environ.get("DEVICES_JSON", "[]"))
    except json.JSONDecodeError as exc:
        raise ValueError("DEVICES_JSON must be valid JSON") from exc
    if not isinstance(raw, list):
        raise ValueError("DEVICES_JSON must contain a list")
    return AutomaticSerialBridge(raw).run()


if __name__ == "__main__":
    raise SystemExit(main())
