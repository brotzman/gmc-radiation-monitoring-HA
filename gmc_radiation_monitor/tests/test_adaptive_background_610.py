from datetime import UTC, datetime, timedelta

from gmc_bridge.adaptive_background import build_adaptive_background
from gmc_bridge.history import HistoryRow


def row(ts, cpm, temp=20.0):
    return HistoryRow("s", int(ts.timestamp()), cpm, temp, None, None, None, None, "accepted")


def test_weekday_hour_profile_and_temperature():
    now = datetime(2026, 7, 14, 14, 0, tzinfo=UTC)  # Tuesday
    rows = []
    for weeks in range(8, 0, -1):
        ts = now - timedelta(weeks=weeks)
        rows.append(row(ts, 20 + (weeks % 2), 21.0))
    rows.append(row(now, 24, 21.0))
    result = build_adaptive_background(rows, timezone_name="UTC", now_utc=int(now.timestamp()))
    assert result["available"]
    assert result["reference_source"] == "weekday_hour"
    assert result["typical_cpm"] is not None
    assert result["deviation_percent"] > 10
    assert result["temperature_typical_cpm"] is not None


def test_learning_without_enough_slot_samples():
    now = datetime(2026, 7, 14, 14, 0, tzinfo=UTC)
    result = build_adaptive_background([row(now, 16)], timezone_name="UTC", now_utc=int(now.timestamp()))
    assert result["learning"] is True
