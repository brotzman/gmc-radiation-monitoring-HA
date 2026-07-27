from __future__ import annotations

import unittest
from datetime import datetime
from zoneinfo import ZoneInfo

from gmc_bridge.report_periods import resolve_period


class ReportPeriodTests(unittest.TestCase):
    def test_daily_period_respects_dst_short_day(self) -> None:
        tz = ZoneInfo("Europe/Berlin")
        period = resolve_period(
            kind="daily",
            selection="specific",
            tz=tz,
            now=datetime(2026, 3, 29, 12, tzinfo=tz),
            date_value="2026-03-29",
        )
        self.assertEqual((period.end_utc - period.start_utc).total_seconds(), 23 * 3600)
        self.assertEqual(period.filename_label, "2026-03-29")

    def test_custom_period_includes_complete_end_date(self) -> None:
        tz = ZoneInfo("Europe/Berlin")
        period = resolve_period(
            kind="custom",
            selection="specific",
            tz=tz,
            start_value="2026-07-01",
            end_value="2026-07-03",
        )
        self.assertEqual(period.start_local.date().isoformat(), "2026-07-01")
        self.assertEqual(period.end_local.date().isoformat(), "2026-07-04")

    def test_invalid_custom_range_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "must not be before"):
            resolve_period(
                kind="custom",
                selection="specific",
                tz=ZoneInfo("UTC"),
                start_value="2026-07-03",
                end_value="2026-07-01",
            )


if __name__ == "__main__":
    unittest.main()
