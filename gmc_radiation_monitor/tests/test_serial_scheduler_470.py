from __future__ import annotations

import threading
import time

from gmc_bridge.serial_scheduler import SerialScheduler


def test_scheduler_serializes_windows_and_applies_gap() -> None:
    scheduler = SerialScheduler(enabled=True, minimum_gap_seconds=0.05)
    stop = threading.Event()
    entries: list[tuple[str, float]] = []

    def worker(index: int) -> None:
        with scheduler.window(index, "READ", stop):
            entries.append((f"start-{index}", time.monotonic()))
            time.sleep(0.03)
            entries.append((f"end-{index}", time.monotonic()))

    first = threading.Thread(target=worker, args=(0,))
    second = threading.Thread(target=worker, args=(1,))
    first.start()
    time.sleep(0.005)
    second.start()
    first.join(timeout=2.0)
    second.join(timeout=2.0)
    assert not first.is_alive()
    assert not second.is_alive()

    times = dict(entries)
    assert times["start-1"] >= times["end-0"] + 0.04


def test_preconfigured_devices_expose_frame_debug_options() -> None:
    from pathlib import Path

    import yaml

    config = yaml.safe_load(Path("config.yaml").read_text())
    assert config["version"] == "8.2.1"
    assert config["options"]["system"]["serial_scheduler_enabled"] is True
    assert config["options"]["system"]["serial_scheduler_gap_seconds"] == 2.0
    for device in config["options"]["devices"]:
        assert device["serial_debug"] is False
        assert device["serial_debug_max_bytes"] == 64
