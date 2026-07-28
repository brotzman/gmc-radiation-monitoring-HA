#!/usr/bin/env python3
"""Run repeatable release checks without requiring Home Assistant hardware."""
from __future__ import annotations

import argparse
import compileall
import os
import subprocess
import sys
import unittest
from pathlib import Path


def _run(command: list[str], *, env: dict[str, str]) -> int:
    completed = subprocess.run(command, check=False, env=env)
    return int(completed.returncode)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--skip-browser", action="store_true")
    parser.add_argument("--skip-unit", action="store_true")
    parser.add_argument("--chromium", default=os.environ.get("CHROMIUM_PATH"))
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parents[1]
    addon = repo_root / "gmc_radiation_monitor"
    library = addon / "rootfs/usr/local/lib"
    package = library / "gmc_bridge"
    css = package / "static/dashboard.css"
    i18n_dir = package / "i18n"

    if not compileall.compile_dir(package, quiet=1, force=True):
        print("Python compilation failed", file=sys.stderr)
        return 1

    sys.path.insert(0, str(library))
    from gmc_bridge.history import HistoryRow
    from gmc_bridge.i18n import validate_catalogs
    from gmc_bridge.i18n.catalog import CATALOG_SOURCE_PATH
    from gmc_bridge.report_periods import ReportPeriod
    from gmc_bridge.report_web import ReportApplication
    from gmc_bridge.service_metrology import enrich_metrology_state

    issues = validate_catalogs()
    if issues:
        print("Translation catalogue validation failed:", file=sys.stderr)
        print("\n".join(issues), file=sys.stderr)
        return 1

    split_contract = {
        "report status mixin": ReportApplication.status.__module__ == "gmc_bridge.report_web_status",
        "report device mixin": ReportApplication._render_devices_section.__module__ == "gmc_bridge.report_web_devices",
        "report periods": ReportPeriod.__module__ == "gmc_bridge.report_periods",
        "history models": HistoryRow.__module__ == "gmc_bridge.history_models",
        "service metrology": enrich_metrology_state.__module__ == "gmc_bridge.service_metrology"
        and "from .service_metrology import enrich_metrology_state as _enrich_metrology_state"
        in (package / "service.py").read_text(encoding="utf-8"),
    }
    inactive = [name for name, active in split_contract.items() if not active]
    if inactive:
        print(f"Module split contract is inactive: {inactive}", file=sys.stderr)
        return 1

    if not CATALOG_SOURCE_PATH.is_file():
        print("Canonical translation source is missing", file=sys.stderr)
        return 1
    obsolete_i18n = [
        i18n_dir / f"{language}.py"
        for language in ("en", "de", "fr", "es", "it", "nl", "pl", "hr")
        if (i18n_dir / f"{language}.py").exists()
    ]
    obsolete_i18n.extend(i18n_dir.glob("release_*.json"))
    if obsolete_i18n:
        print(f"Obsolete translation sources found: {obsolete_i18n}", file=sys.stderr)
        return 1

    css_text = css.read_text(encoding="utf-8")
    forbidden = (
        ".jump-links { flex-wrap:nowrap; overflow-x:auto",
        ".language-switcher { width:100%; min-width:0; flex-wrap:nowrap; overflow-x:auto",
        "10.0.1 mobile layout hardening",
        "10.0.1 mobile follow-up",
        ".dashboard-controls { position:static",
    )
    found = [item for item in forbidden if item in css_text]
    if found:
        print(f"Obsolete responsive CSS found: {found}", file=sys.stderr)
        return 1
    for contract in ("Base responsive layout contract", "10.0.3 full-page responsive contract"):
        if contract not in css_text:
            print(f"Responsive CSS contract is missing: {contract}", file=sys.stderr)
            return 1

    env = dict(os.environ)
    env["PYTHONPATH"] = str(library) + os.pathsep + env.get("PYTHONPATH", "")

    unit_test_count = unittest.defaultTestLoader.discover(str(repo_root / "quality/tests")).countTestCases()
    if not args.skip_unit:
        command = [sys.executable, "-m", "unittest", "discover", "-s", str(repo_root / "quality/tests"), "-v"]
        if _run(command, env=env):
            return 1

    if not args.skip_browser:
        browser_commands = [
            [sys.executable, str(repo_root / "quality/mobile_layout_regression.py"), "--css", str(css)],
            [sys.executable, str(repo_root / "quality/full_app_e2e.py"), "--package-root", str(repo_root)],
        ]
        for command in browser_commands:
            if args.chromium:
                command.extend(["--chromium", args.chromium])
            if _run(command, env=env):
                return 1

    browser_summary = "browser regressions skipped" if args.skip_browser else "sticky responsive browser regressions"
    unit_summary = "unit/integration tests skipped" if args.skip_unit else f"{unit_test_count} unit/integration tests"
    print(
        f"Quality checks passed: compilation, {unit_summary}, module splits, "
        f"single-source translations and {browser_summary}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
