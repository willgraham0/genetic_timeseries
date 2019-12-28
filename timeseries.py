from datetime import datetime
from typing import NamedTuple

from utils import pairwise


class Point(NamedTuple):
    """A tuple of datetime and value."""
    time: datetime
    value: float


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
