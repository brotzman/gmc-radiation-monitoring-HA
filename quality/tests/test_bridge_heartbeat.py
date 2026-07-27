from __future__ import annotations

import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch

from gmc_bridge.bridge_heartbeat import BridgeHeartbeatReporter, read_bridge_heartbeat


class BridgeHeartbeatTests(unittest.TestCase):
    def test_atomic_writes_use_a_fresh_temporary_file_each_time(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "gmc_bridge_heartbeat.json"
            reporter = BridgeHeartbeatReporter(path)
            sources: list[Path] = []
            real_replace = os.replace

            def recording_replace(source: str | os.PathLike[str], destination: str | os.PathLike[str]) -> None:
                sources.append(Path(source))
                real_replace(source, destination)

            with patch("gmc_bridge.bridge_heartbeat.os.replace", side_effect=recording_replace):
                reporter.write_now()
                reporter.update(state="discovering")

            self.assertEqual(len(sources), 2)
            self.assertEqual(len(set(sources)), 2)
            self.assertTrue(all(source.parent == path.parent for source in sources))
            self.assertFalse(any(path.parent.glob(f".{path.name}.*.tmp")))
            self.assertEqual(read_bridge_heartbeat(path)["state"], "discovering")

    def test_concurrent_writes_do_not_lose_the_atomic_source_file(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "gmc_bridge_heartbeat.json"
            reporter = BridgeHeartbeatReporter(path)
            worker_count = 24
            start = threading.Barrier(worker_count)
            failures: list[BaseException] = []
            failures_lock = threading.Lock()

            def worker(index: int) -> None:
                try:
                    start.wait(timeout=5)
                    reporter.update(state="running", assigned_devices=index)
                except BaseException as exc:  # capture thread failures for the assertion
                    with failures_lock:
                        failures.append(exc)

            threads = [threading.Thread(target=worker, args=(index,)) for index in range(worker_count)]
            for thread in threads:
                thread.start()
            for thread in threads:
                thread.join(timeout=10)

            self.assertFalse(any(thread.is_alive() for thread in threads))
            self.assertEqual(failures, [])
            payload = read_bridge_heartbeat(path)
            self.assertEqual(payload["state"], "running")
            self.assertIn(payload["assigned_devices"], range(worker_count))
            self.assertEqual(reporter.snapshot()["write_error_count"], 0)
            self.assertFalse(any(path.parent.glob(f".{path.name}.*.tmp")))


if __name__ == "__main__":
    unittest.main()
