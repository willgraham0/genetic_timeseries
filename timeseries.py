from __future__ import annotations
from datetime import datetime
from math import sqrt

from utils import pairwise


class Point:
    """A datetime and value representation."""

    def __init__(self, time: datetime, value: float):
        self.time = time
        self.value = value

    def distance(self, other: Point):
        """Return a value that represents the vector distance between two points."""
        return sqrt(((self.time - other.time).total_seconds())**2 + (self.value - other.value)**2)

    def __str__(self):
        return f"<Point: time={self.time} value={self.value}>"


class TimeSeries:
    """A chronologically ordered iterable of Points."""

    def __init__(self, points) -> None:
        self.points = tuple(
            Point(*point)
            for point in sorted(points, key=lambda x: x.time)
        )

    @property
    def area(self) -> float:
        """Return the area under the time series."""
        return (
            sum(
                (point.value + next_point.value)
                * (next_point.time - point.time).total_seconds()
                for point, next_point in pairwise(self.points)
            )
            / 2.0
        )
