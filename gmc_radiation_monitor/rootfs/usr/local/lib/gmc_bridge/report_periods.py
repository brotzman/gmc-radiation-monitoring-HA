from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, date, datetime, timedelta
from datetime import time as dt_time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

@dataclass(frozen=True)
class ReportPeriod:
    kind: str
    label: str
    start_local: datetime
    end_local: datetime

    @property
    def start_utc(self) -> datetime:
        return self.start_local.astimezone(UTC)

    @property
    def end_utc(self) -> datetime:
        return self.end_local.astimezone(UTC)

    @property
    def filename_label(self) -> str:
        if self.kind == "daily":
            return self.start_local.strftime("%Y-%m-%d")
        if self.kind == "weekly":
            iso = self.start_local.isocalendar()
            return f"{iso.year}-W{iso.week:02d}"
        if self.kind == "monthly":
            return self.start_local.strftime("%Y-%m")
        if self.kind in {"rolling24", "rolling7"}:
            return self.label.replace(" ", "-").replace(":", "")
        return f"{self.start_local:%Y-%m-%d}_{(self.end_local - timedelta(microseconds=1)):%Y-%m-%d}"


def load_timezone(name: str) -> ZoneInfo:
    try:
        return ZoneInfo(name)
    except ZoneInfoNotFoundError as exc:
        raise ValueError(f"Unknown IANA timezone: {name}") from exc


def resolve_period(
    *,
    kind: str,
    selection: str,
    tz: ZoneInfo,
    now: datetime | None = None,
    date_value: str | None = None,
    week_value: str | None = None,
    month_value: str | None = None,
    start_value: str | None = None,
    end_value: str | None = None,
) -> ReportPeriod:
    current = (now or datetime.now(tz)).astimezone(tz)
    if kind == "daily":
        if selection == "today":
            chosen = current.date()
        elif selection == "previous":
            chosen = current.date() - timedelta(days=1)
        elif selection == "specific":
            if not date_value:
                raise ValueError("A date is required for a specific daily report")
            chosen = date.fromisoformat(date_value)
        else:
            raise ValueError(f"Unsupported daily selection: {selection}")
        start = datetime.combine(chosen, dt_time.min, tzinfo=tz)
        end = start + timedelta(days=1)
        return ReportPeriod("daily", chosen.isoformat(), start, end)

    if kind == "weekly":
        if selection in {"current", "previous"}:
            monday = current.date() - timedelta(days=current.weekday())
            if selection == "previous":
                monday -= timedelta(days=7)
        elif selection == "specific":
            if not week_value:
                raise ValueError("An ISO week is required for a specific weekly report")
            try:
                year_text, week_text = week_value.upper().split("-W", 1)
                monday = date.fromisocalendar(int(year_text), int(week_text), 1)
            except (TypeError, ValueError) as exc:
                raise ValueError("ISO week must use the form YYYY-Www") from exc
        else:
            raise ValueError(f"Unsupported weekly selection: {selection}")
        start = datetime.combine(monday, dt_time.min, tzinfo=tz)
        end = start + timedelta(days=7)
        iso = monday.isocalendar()
        return ReportPeriod("weekly", f"{iso.year}-W{iso.week:02d}", start, end)

    if kind == "monthly":
        if selection == "current":
            first_day = current.date().replace(day=1)
        elif selection == "previous":
            previous_month_end = current.date().replace(day=1) - timedelta(days=1)
            first_day = previous_month_end.replace(day=1)
        elif selection == "specific":
            if not month_value:
                raise ValueError("A month is required for a specific monthly report")
            try:
                year_text, month_text = month_value.split("-", 1)
                first_day = date(int(year_text), int(month_text), 1)
            except (TypeError, ValueError) as exc:
                raise ValueError("Month must use the form YYYY-MM") from exc
        else:
            raise ValueError(f"Unsupported monthly selection: {selection}")
        next_month = (first_day.replace(day=28) + timedelta(days=4)).replace(day=1)
        start = datetime.combine(first_day, dt_time.min, tzinfo=tz)
        end = datetime.combine(next_month, dt_time.min, tzinfo=tz)
        return ReportPeriod("monthly", first_day.strftime("%Y-%m"), start, end)

    if kind in {"rolling24", "rolling7"}:
        end = current
        delta = timedelta(hours=24) if kind == "rolling24" else timedelta(days=7)
        start = end - delta
        label = (
            f"last-24-hours-{end:%Y%m%d-%H%M}"
            if kind == "rolling24"
            else f"last-7-days-{end:%Y%m%d-%H%M}"
        )
        return ReportPeriod(kind, label, start, end)

    if kind == "custom":
        if not start_value or not end_value:
            raise ValueError("A start and end date are required for a custom report")
        try:
            start_date = date.fromisoformat(start_value)
            end_date = date.fromisoformat(end_value)
        except ValueError as exc:
            raise ValueError("Custom dates must use the form YYYY-MM-DD") from exc
        if end_date < start_date:
            raise ValueError("The report end date must not be before the start date")
        start = datetime.combine(start_date, dt_time.min, tzinfo=tz)
        end = datetime.combine(end_date + timedelta(days=1), dt_time.min, tzinfo=tz)
        return ReportPeriod("custom", f"{start_date.isoformat()} to {end_date.isoformat()}", start, end)

    raise ValueError(f"Unsupported report period: {kind}")


def expected_samples(period: ReportPeriod, scan_interval_seconds: int) -> int:
    effective_end = min(period.end_utc, datetime.now(UTC))
    duration = max(0.0, (effective_end - period.start_utc).total_seconds())
    return max(1, round(duration / scan_interval_seconds))
