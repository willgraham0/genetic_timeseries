from __future__ import annotations
from datetime import datetime
from math import sqrt


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
