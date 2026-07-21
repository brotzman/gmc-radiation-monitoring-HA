from __future__ import annotations

import json
from pathlib import Path
from urllib.request import Request

import pytest
from gmc_bridge.supervisor_options import (
    SUPERVISOR_OPTIONS_URL,
    SupervisorOptionsError,
    build_options_payload,
    persist_self_options,
)

ROOT = Path(__file__).parents[1]


class FakeResponse:
    status = 200

    def __init__(self, body: bytes = b'{"result":"ok","data":{}}') -> None:
        self.body = body

    def __enter__(self) -> FakeResponse:
        return self

    def __exit__(self, exc_type: object, exc: object, traceback: object) -> None:
        return None

    def read(self) -> bytes:
        return self.body


def _problematic_options() -> dict[str, object]:
    return {
        "devices": [
            {
                "name": "GMC-320",
                "scan_interval": 120,
                "cpm_per_usvh": 154.0,
                "calibration_reference": (
                    'GQ GMC-320 Plus V4 Benutzerhandbuch; "M4011"; '
                    "154 CPM/(µSv/h); Reproduzierbarkeit 20 %."
                ),
                "detector_profile": "gmc_320_plus_v4",
            }
        ],
        "dual_tube_devices": [
            {
                "name": "GMC-500+",
                "detector_profile": "gmc_500_plus",
                "dual_tube_mode": "separate",
                "high_dose_tube_model": "SI-3BG",
                "high_dose_calibration_reference": (
                    'No verified "SI-3BG" dose factor; CPM display only'
                ),
            }
        ],
        "interface": {"ui_language": "de"},
    }


def test_payload_preserves_arrays_quotes_and_unicode() -> None:
    options = _problematic_options()
    decoded = json.loads(build_options_payload(options).decode("utf-8"))
    assert decoded == {"options": options}
    assert isinstance(decoded["options"]["devices"], list)
    assert "µSv/h" in decoded["options"]["devices"][0]["calibration_reference"]
    assert decoded["options"]["dual_tube_devices"][0]["name"] == "GMC-500+"


def test_persist_uses_one_structured_supervisor_request() -> None:
    captured: dict[str, object] = {}

    def opener(request: Request, *, timeout: float) -> FakeResponse:
        captured["url"] = request.full_url
        captured["method"] = request.get_method()
        captured["authorization"] = request.get_header("Authorization")
        captured["content_type"] = request.get_header("Content-type")
        captured["timeout"] = timeout
        captured["payload"] = json.loads(request.data.decode("utf-8"))
        return FakeResponse()

    options = _problematic_options()
    persist_self_options(options, token="test-token", opener=opener)

    assert captured["url"] == SUPERVISOR_OPTIONS_URL
    assert captured["method"] == "POST"
    assert captured["authorization"] == "Bearer test-token"
    assert captured["content_type"] == "application/json"
    assert captured["payload"] == {"options": options}


def test_persist_requires_supervisor_token() -> None:
    with pytest.raises(SupervisorOptionsError, match="SUPERVISOR_TOKEN"):
        persist_self_options(_problematic_options(), token="")


def test_start_script_never_injects_json_into_bashio_or_jq() -> None:
    run_script = (ROOT / "rootfs/etc/services.d/gmc/run").read_text(encoding="utf-8")
    assert "bashio::addon.option" not in run_script
    assert "bashio::app.option" not in run_script
    assert "jq " not in run_script
    assert "gmc_options_migrate.py" in run_script
