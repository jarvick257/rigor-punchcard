from typing import Optional
from datetime import datetime


class Period:
    def __init__(self, start: datetime, end: datetime | None = None):
        self.start: datetime = start
        self.end: datetime | None = end

    def is_valid(self) -> bool:
        if self.end is None:
            return True
        return self.start <= self.end

    def length_in_seconds(self) -> float:
        return ((self.end or datetime.now()) - self.start).total_seconds()

    def intersect(self, other: "Period") -> Optional["Period"]:
        my_end = self.end or datetime.now()
        assert self
        intersection = Period(
            start=max(self.start, other.start),
            end=min(my_end, other.end or my_end),
        )
        if not intersection.is_valid() or intersection.length_in_seconds() == 0:
            return None
        # intersection can only shrink
        assert intersection.length_in_seconds() <= min(
            self.length_in_seconds(), other.length_in_seconds()
        )
        return intersection

    def __str__(self) -> str:
        end = str(self.end) if self.end is not None else "inf"
        return f"{self.start} -> {end}"
