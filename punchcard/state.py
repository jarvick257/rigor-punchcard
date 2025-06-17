import json
import calendar
from pathlib import Path
from datetime import datetime, timedelta, date
from typing import List

from .period import Period


class PunchcardState:
    def __init__(self, title: str, log_file_path: str):
        self.title = title
        self.log_file: Path = Path(log_file_path)
        self.hist: List[Period] = self._load()

    @property
    def punched_in(self) -> bool:
        return len(self.hist) > 0 and self.hist[-1].end is None

    def _load(self) -> List[Period]:
        if not self.log_file.exists():
            return []
        with open(self.log_file, "r") as fp:
            hist = json.load(fp)
        d = [
            Period(
                start=datetime.fromisoformat(r["start"]),
                end=datetime.fromisoformat(r["end"]) if r["end"] is not None else None,
            )
            for r in hist
        ]
        return d

    def _save(self) -> None:
        d = [
            dict(
                start=p.start.isoformat(),
                end=p.end.isoformat() if p.end is not None else None,
            )
            for p in self.hist
        ]
        with open(self.log_file, "w") as fp:
            json.dump(d, fp)

    def punched_in_since(self) -> timedelta:
        if not self.punched_in:
            return timedelta(0)
        return datetime.now() - self.hist[-1].start

    def punched_out_since(self) -> timedelta:
        if self.punched_in:
            return timedelta(0)
        assert self.hist[-1].end is not None
        return datetime.now() - self.hist[-1].end

    def _get_time_in_period(self, period: Period) -> timedelta:
        overlap = [r.intersect(period) for r in self.hist]
        overlap = [o.length_in_seconds() for o in overlap if o is not None]
        return timedelta(seconds=sum(overlap))

    def time_today(self) -> timedelta:
        t = datetime.today()
        start = datetime(t.year, t.month, t.day, 0, 0, 0)
        end = start + timedelta(days=1)
        return self._get_time_in_period(Period(start, end))

    def time_this_week(self) -> timedelta:
        today = date.today()
        month = calendar.Calendar().monthdatescalendar(today.year, today.month)
        for week in month:
            for day in week:
                if day != today:
                    continue
                start = datetime.combine(week[0], datetime.min.time())
                end = datetime.combine(
                    week[-1] + timedelta(days=1), datetime.min.time()
                )
                return self._get_time_in_period(Period(start, end))
        return timedelta(0)

    def time_this_month(self) -> timedelta:
        t = date.today()
        start = datetime(t.year, t.month, 1, 0, 0, 0)
        _, num_days = calendar.monthrange(t.year, t.month)
        end = start + timedelta(days=num_days)
        return self._get_time_in_period(Period(start, end))

    def time_total(self) -> timedelta:
        return timedelta(seconds=sum([p.length_in_seconds() for p in self.hist]))

    def punch_in(self) -> None:
        if not self.punched_in:
            print(f"Punched in at {self.title}")
            self.hist.append(Period(start=datetime.now(), end=None))
            self._save()

    def punch_out(self) -> None:
        if self.punched_in:
            print(f"Punched out at {self.title}")
            self.hist[-1].end = datetime.now()
            self._save()

    def toggle(self) -> None:
        if self.punched_in:
            self.punch_out()
        else:
            self.punch_in()
