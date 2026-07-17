from gmc_bridge.device_health import DeviceHealthMonitor


def test_prolonged_zero_sequence_warns():
    monitor = DeviceHealthMonitor(zero_limit=6, constant_limit=8)
    result = None
    for _ in range(6):
        result = monitor.update({"cpm": 0})
    assert result is not None
    assert result.status == "warning"
    assert result.reason == "prolonged_zero_cpm"


def test_dual_tube_imbalance_warns():
    result = DeviceHealthMonitor().update({"cpm": 40, "tube_low_cpm": 40, "tube_high_cpm": 0})
    assert result.status == "warning"
    assert result.reason == "dual_tube_imbalance"
