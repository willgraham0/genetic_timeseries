from datetime import datetime, timedelta
from itertools import tee
from random import random


def pairwise(iterable):
    """
    From the itertools cookbook.
    s -> (s0,s1), (s1,s2), (s2, s3), ...
    """
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


def random_datetime(start: datetime, end: datetime) -> datetime:
    """Return a random datetime between the specified start and end datetimes."""
    time_delta = (end - start).total_seconds()
    random_time_delta = time_delta * random()
    return start + timedelta(seconds=random_time_delta)
