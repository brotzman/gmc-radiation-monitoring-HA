#!/usr/bin/env python3
"""Run release-level checks without requiring the Home Assistant runtime."""
from __future__ import annotations

import argparse
import compileall
import os
import subprocess
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-browser", action="store_true")
    parser.add_argument("--chromium", default=os.environ.get("CHROMIUM_PATH"))
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    addon = repo_root / "gmc_radiation_monitor"
    library = addon / "rootfs/usr/local/lib"
    package = library / "gmc_bridge"
    css = package / "static/dashboard.css"

    if not compileall.compile_dir(package, quiet=1, force=True):
        print("Python compilation failed", file=sys.stderr)
        return 1

    sys.path.insert(0, str(library))
    from gmc_bridge.i18n import validate_catalogs
    from gmc_bridge.report_web import ReportApplication

    issues = validate_catalogs()
    if issues:
        print("Translation catalogue validation failed:", file=sys.stderr)
        print("\n".join(issues), file=sys.stderr)
        return 1
    if ReportApplication.status.__module__ != "gmc_bridge.report_web_status":
        print("Report status mixin is not active", file=sys.stderr)
        return 1
    if ReportApplication._render_devices_section.__module__ != "gmc_bridge.report_web_devices":
        print("Report device view mixin is not active", file=sys.stderr)
        return 1

    css_text = css.read_text(encoding="utf-8")
    forbidden = (
        ".jump-links { flex-wrap:nowrap; overflow-x:auto",
        ".language-switcher { width:100%; min-width:0; flex-wrap:nowrap; overflow-x:auto",
        "10.0.1 mobile layout hardening",
        "10.0.1 mobile follow-up",
    )
    found = [item for item in forbidden if item in css_text]
    if found:
        print(f"Obsolete responsive CSS found: {found}", file=sys.stderr)
        return 1
    if "10.0.2 responsive layout contract" not in css_text:
        print("Responsive CSS contract is missing", file=sys.stderr)
        return 1

    if not args.skip_browser:
        command = [sys.executable, str(Path(__file__).with_name("mobile_layout_regression.py")), "--css", str(css)]
        if args.chromium:
            command.extend(["--chromium", args.chromium])
        completed = subprocess.run(command, check=False)
        if completed.returncode:
            return completed.returncode

    print("Quality checks passed: Python, split web modules, translations and responsive layout")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
