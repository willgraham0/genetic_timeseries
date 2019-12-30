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


def generate_hh_range(start: datetime, end: datetime) -> List[datetime]:
    """Returns a list of half hourly date-times between start and end."""
    step = timedelta(minutes=30)
    hh_count = int((end - start).total_seconds() / step.seconds)
    return [(start + step * hh) for hh in range(0, hh_count)]
