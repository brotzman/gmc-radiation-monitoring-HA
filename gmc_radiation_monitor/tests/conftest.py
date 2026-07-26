from __future__ import annotations

import os
import signal
from pathlib import Path
from collections.abc import Generator

import pytest

SERIAL_TEST_TIMEOUT_SECONDS = 30

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def stable_project_working_directory() -> Generator[None, None, None]:
    """Keep legacy path-based tests independent of test execution order."""
    os.chdir(PROJECT_ROOT)
    try:
        yield
    finally:
        os.chdir(PROJECT_ROOT)



class SerialTestTimeout(TimeoutError):
    pass


def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "serial: test that exercises serial or PTY behavior")


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    for item in items:
        if "serial" in item.path.name:
            item.add_marker("serial")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item: pytest.Item) -> Generator[None, None, None]:
    if item.get_closest_marker("serial") is None or not hasattr(signal, "SIGALRM"):
        yield
        return

    def timeout_handler(_signum: int, _frame: object) -> None:
        raise SerialTestTimeout(
            f"serial test exceeded the fixed {SERIAL_TEST_TIMEOUT_SECONDS}-second timeout"
        )

    previous_handler = signal.getsignal(signal.SIGALRM)
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.setitimer(signal.ITIMER_REAL, SERIAL_TEST_TIMEOUT_SECONDS)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
