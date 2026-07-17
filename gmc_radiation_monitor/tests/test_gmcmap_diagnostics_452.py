from __future__ import annotations

import tempfile
import time
from pathlib import Path
from urllib.error import URLError

from gmc_bridge.gmcmap import (
    GmcMapConfig,
    GmcMapReading,
    GmcMapUploadCoordinator,
    GmcMapUploader,
    effective_upload_interval,
    response_diagnostic,
    response_rejected,
    staggered_startup_delay,
)
from gmc_bridge.history import HistoryStore
from gmc_bridge.report_web import ReportApplication


def _reading() -> GmcMapReading:
    return GmcMapReading(cpm=15, average_cpm=13.2, dose_rate_usvh=0.075, captured_at_utc=1)


def test_startup_delay_prevents_immediate_first_upload() -> None:
    calls: list[str] = []

    def transport(url: str, timeout: float) -> tuple[int, str]:
        calls.append(url)
        return 200, "OK"

    uploader = GmcMapUploader(
        GmcMapConfig(
            account_id="0230111",
            counter_id="0034021",
            startup_delay_seconds=30.0,
        ),
        transport=transport,
        monotonic=lambda: 100.0,
        wall_time=lambda: 1_800_000_000.0,
    )
    uploader.offer(_reading())
    uploader.start()
    time.sleep(0.05)
    status = uploader.snapshot()
    uploader.stop()

    assert calls == []
    assert status["gmcmap_upload_status"] == "waiting"
    assert status["gmcmap_next_upload_utc"] == "2027-01-15T08:00:30Z"


def test_response_parser_ignores_incidental_error_words_in_html() -> None:
    body = "<html><script>window.onerror=function(){}</script><p>Upload accepted</p></html>"
    assert response_diagnostic(body) == "window.onerror=function(){} Upload accepted"
    assert response_rejected(body) is False


def test_response_parser_rejects_explicit_server_failure() -> None:
    assert response_rejected("Error: invalid GID") is True
    assert response_rejected("Link server failed") is True


def test_success_preserves_last_error_and_resets_consecutive_count() -> None:
    responses: list[object] = [URLError("temporary DNS failure"), (200, "OK")]

    def transport(url: str, timeout: float) -> tuple[int, str]:
        result = responses.pop(0)
        if isinstance(result, Exception):
            raise result
        return result

    uploader = GmcMapUploader(
        GmcMapConfig(account_id="0230111", counter_id="0034021"),
        transport=transport,
        wall_time=lambda: 1_800_000_000.0,
    )
    uploader._attempt_upload(_reading())
    failed = uploader.snapshot()
    assert failed["gmcmap_upload_error_count"] == 1
    assert failed["gmcmap_consecutive_error_count"] == 1
    assert failed["gmcmap_last_error_utc"] == "2027-01-15T08:00:00Z"
    previous_error = failed["gmcmap_last_error"]

    uploader._attempt_upload(_reading())
    succeeded = uploader.snapshot()
    assert succeeded["gmcmap_upload_status"] == "success"
    assert succeeded["gmcmap_consecutive_error_count"] == 0
    assert succeeded["gmcmap_upload_error_count"] == 1
    assert succeeded["gmcmap_last_error"] == previous_error
    assert succeeded["gmcmap_last_error_utc"] == "2027-01-15T08:00:00Z"
    assert succeeded["gmcmap_last_http_status"] == 200
    assert succeeded["gmcmap_last_response"] == "OK"


def test_server_response_diagnostics_redact_account_and_counter_ids() -> None:
    def transport(url: str, timeout: float) -> tuple[int, str]:
        return 200, "Accepted AID=0230111 GID=0034021"

    uploader = GmcMapUploader(
        GmcMapConfig(account_id="0230111", counter_id="0034021"),
        transport=transport,
    )
    uploader._attempt_upload(_reading())
    status = uploader.snapshot()
    assert status["gmcmap_last_response"] == "Accepted AID=*** GID=***"
    assert "0230111" not in str(status)
    assert "0034021" not in str(status)


def test_dashboard_keeps_gmcmap_diagnostics_compact() -> None:
    with tempfile.TemporaryDirectory() as temp_dir:
        store = HistoryStore(Path(temp_dir) / "history.sqlite3")
        store.upsert_device_registry(
            "SERIAL_A",
            {
                "device_model": "GMC-320Re 4.52",
                "port": "/dev/a",
                "gmcmap_enabled": True,
                "gmcmap_configured": True,
                "gmcmap_upload_status": "success",
                "gmcmap_counter_id_masked": "***4021",
                "gmcmap_last_attempt_utc": "2026-07-13T10:12:04Z",
                "gmcmap_last_upload_utc": "2026-07-13T10:12:04Z",
                "gmcmap_next_upload_utc": "2026-07-13T10:17:04Z",
                "gmcmap_upload_success_count": 3,
                "gmcmap_upload_error_count": 3,
                "gmcmap_consecutive_error_count": 0,
                "gmcmap_last_error": "Network error: temporary DNS failure",
                "gmcmap_last_error_utc": "2026-07-13T10:02:04Z",
                "gmcmap_last_http_status": 200,
                "gmcmap_last_response": "OK",
            },
        )
        store.insert_measurement({"cpm": 12}, device_serial="SERIAL_A", timestamp_utc=1_800_000_000)
        app = ReportApplication(
            store=store,
            timezone_name="Europe/Berlin",
            scan_interval_seconds=60,
            read_gyro=False,
            cpm_per_usvh=154.0,
            ui_language="de",
        )
        page = app.render_index(language_override="de", mode_override="advanced").decode("utf-8")

        assert "Zähler-ID" in page
        assert "Letzter Versuch" not in page
        assert "Letzter Upload" in page
        assert "Nächster Upload" not in page
        assert "Erfolgreiche Uploads seit Start" not in page
        assert "Uploadfehler seit Start" not in page
        assert "Aufeinanderfolgende Uploadfehler" not in page
        assert "Letzter HTTP-Status" not in page
        assert "Letzter Uploadfehler" not in page
        assert "Letzte Serverantwort" not in page
        assert "temporary DNS failure" not in page
        assert ">OK<" not in page


def test_two_device_uploads_receive_separate_slots_below_server_deadline() -> None:
    assert effective_upload_interval(300) == 280.0
    assert staggered_startup_delay(0, 2, 300) == 30.0
    assert staggered_startup_delay(1, 2, 300) == 170.0


def test_shared_upload_coordinator_keeps_minimum_connection_gap() -> None:
    clock = [0.0]
    sleeps: list[float] = []

    def monotonic() -> float:
        return clock[0]

    def sleep(seconds: float) -> None:
        sleeps.append(seconds)
        clock[0] += seconds

    coordinator = GmcMapUploadCoordinator(10.0, monotonic=monotonic, sleep=sleep)

    def first() -> tuple[int, str]:
        clock[0] += 2.0
        return 200, "first"

    assert coordinator.execute(first) == (200, "first")
    assert coordinator.execute(lambda: (200, "second")) == (200, "second")
    assert sleeps == [10.0]


def test_success_cadence_is_measured_from_request_start_not_completion() -> None:
    clock = [100.0]

    def transport(url: str, timeout: float) -> tuple[int, str]:
        clock[0] += 8.0
        return 200, "OK"

    uploader = GmcMapUploader(
        GmcMapConfig(account_id="0230111", counter_id="0034021"),
        transport=transport,
        monotonic=lambda: clock[0],
        wall_time=lambda: 1_800_000_000.0,
    )
    uploader._attempt_upload(_reading())
    assert uploader._next_due_monotonic == 380.0
    assert uploader.snapshot()["gmcmap_effective_upload_interval_seconds"] == 280.0


def test_retry_backoff_never_exceeds_effective_deadline_cadence() -> None:
    clock = [100.0]

    def transport(url: str, timeout: float) -> tuple[int, str]:
        raise URLError("temporary")

    uploader = GmcMapUploader(
        GmcMapConfig(account_id="0230111", counter_id="0034021"),
        transport=transport,
        monotonic=lambda: clock[0],
        wall_time=lambda: 1_800_000_000.0,
    )
    for expected_delay in (60.0, 120.0, 240.0, 280.0, 280.0):
        uploader._attempt_upload(_reading())
        assert uploader._next_due_monotonic - clock[0] == expected_delay
