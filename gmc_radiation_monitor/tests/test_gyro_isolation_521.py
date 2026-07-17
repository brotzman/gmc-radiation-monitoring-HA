from __future__ import annotations

from types import SimpleNamespace
from unittest import mock

from gmc_bridge.errors import GmcProtocolError, GmcTimeout
from gmc_bridge.serial_device import read_sample


def _device(gyro):
    return SimpleNamespace(
        get_cpm=lambda: 17,
        get_temperature_c=lambda: 26.8,
        get_voltage_v=lambda: 4.2,
        get_gyro=gyro,
        recover_protocol_stream=mock.Mock(),
    )


def test_malformed_gyro_is_resynchronized_and_retried_once():
    gyro = mock.Mock(side_effect=[GmcProtocolError("bad terminator"), (1, 2, 3)])
    device = _device(gyro)
    result = read_sample(device, True)
    assert result.state["cpm"] == 17
    assert result.state["gyro_x"] == 1
    assert result.available["gyro"] is True
    assert result.reconnect_required is False
    assert result.optional_errors == []
    device.recover_protocol_stream.assert_called_once_with()
    assert gyro.call_count == 2


def test_two_malformed_gyro_frames_do_not_reconnect_whole_device():
    gyro = mock.Mock(side_effect=[GmcProtocolError("bad 1"), GmcProtocolError("bad 2")])
    device = _device(gyro)
    result = read_sample(device, True)
    assert result.state["cpm"] == 17
    assert result.available["gyro"] is False
    assert result.reconnect_required is False
    assert len(result.optional_errors) == 1
    assert result.optional_errors[0].sensor == "gyro"


def test_gyro_timeout_still_requests_normal_device_recovery():
    gyro = mock.Mock(side_effect=GmcTimeout("timeout"))
    result = read_sample(_device(gyro), True)
    assert result.state["cpm"] == 17
    assert result.reconnect_required is True
