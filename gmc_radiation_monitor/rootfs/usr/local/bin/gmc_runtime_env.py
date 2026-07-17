#!/usr/bin/env python3
from __future__ import annotations

import os
import sys
from pathlib import Path

LIB_DIR = Path(__file__).resolve().parents[1] / "lib"
if str(LIB_DIR) not in sys.path:
    sys.path.insert(0, str(LIB_DIR))

from gmc_bridge.runtime_options import load_options, runtime_environment  # noqa: E402


def main() -> int:
    service = sys.argv[1] if len(sys.argv) > 1 else ""
    options_path = os.environ.get("CONFIG_PATH", "/data/options.json")
    environment = runtime_environment(load_options(options_path), service)
    output = sys.stdout.buffer
    for key, value in sorted(environment.items()):
        output.write(key.encode("ascii"))
        output.write(b"\0")
        output.write(str(value).encode("utf-8"))
        output.write(b"\0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
