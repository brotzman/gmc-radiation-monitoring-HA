from __future__ import annotations

import ast
from pathlib import Path

from gmc_bridge.report_web import ReportRequestHandler
from gmc_bridge.report_web_http import ReportRequestHandler as SplitHandler

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = ROOT.parent


def test_http_handler_is_split_without_breaking_public_import() -> None:
    report_web = ROOT / "rootfs/usr/local/lib/gmc_bridge/report_web.py"
    report_http = ROOT / "rootfs/usr/local/lib/gmc_bridge/report_web_http.py"
    assert ReportRequestHandler is SplitHandler
    assert report_http.is_file()
    assert len(report_web.read_text(encoding="utf-8").splitlines()) < 1800
    assert len(report_http.read_text(encoding="utf-8").splitlines()) < 1000
    module = ast.parse(report_web.read_text(encoding="utf-8"))
    assert not any(
        isinstance(node, ast.ClassDef) and node.name == "ReportRequestHandler" for node in module.body
    )


def test_quality_gates_are_release_blocking() -> None:
    workflow = (REPO_ROOT / ".github/workflows/quality.yml").read_text(encoding="utf-8")
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert "pytest-cov" in workflow
    assert "coverage report" in workflow
    assert "fail_under = 70" in pyproject
    assert "mypy" in workflow
    assert "ruff check rootfs/usr/local/bin rootfs/usr/local/lib/gmc_bridge tests" in workflow


def test_browser_and_simulated_hardware_matrices_are_present() -> None:
    workflow = (REPO_ROOT / ".github/workflows/quality.yml").read_text(encoding="utf-8")
    assert "chromium firefox webkit" in workflow
    assert 'GMC_REQUIRE_ALL_BROWSERS: "1"' in workflow
    assert "test_responsive_browser_matrix_8011.py" in workflow
    assert (ROOT / "tests/test_simulated_hardware_matrix_8011.py").is_file()
