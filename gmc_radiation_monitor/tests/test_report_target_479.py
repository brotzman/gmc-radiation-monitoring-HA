import pytest
from gmc_bridge.report_web import (
    REPORT_TARGET_COMBINED,
    _decode_report_target,
    _encode_report_target,
)


def test_report_target_tokens_are_explicit():
    assert _encode_report_target("SERIAL-500") == "device:SERIAL-500"
    assert _encode_report_target(combined=True) == REPORT_TARGET_COMBINED
    assert _decode_report_target("device:SERIAL-500", {"SERIAL-320", "SERIAL-500"}) == (False, "SERIAL-500")
    assert _decode_report_target("combined", {"SERIAL-320", "SERIAL-500"}) == (True, None)


def test_missing_or_unknown_target_never_falls_back_to_combined():
    with pytest.raises(ValueError):
        _decode_report_target("", {"SERIAL-320", "SERIAL-500"})
    with pytest.raises(ValueError):
        _decode_report_target("device:UNKNOWN", {"SERIAL-320", "SERIAL-500"})
