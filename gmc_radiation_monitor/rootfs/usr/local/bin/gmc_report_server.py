#!/usr/bin/env python3
"""GMC scientific report Ingress server launcher."""
from __future__ import annotations

import sys
from pathlib import Path

LIB_DIR = Path(__file__).resolve().parents[1] / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from gmc_bridge.report_web import run_report_server  # noqa: E402

if __name__ == "__main__":
    run_report_server()
