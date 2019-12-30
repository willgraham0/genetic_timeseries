from datetime import datetime, timedelta
from itertools import tee
from typing import List


def pairwise(iterable):
    """
    From the itertools cookbook.
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def generate_sp_range(start: datetime, end: datetime) -> List[float]:
    """Returns a list of half hourly settlement period timestamps between start and end."""
    step = timedelta(minutes=30)
    sp_count = int((end - start).total_seconds() / step.seconds)
    return [(start + step * sp).timestamp() for sp in range(0, sp_count)]
