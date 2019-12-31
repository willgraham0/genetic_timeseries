from datetime import datetime, timedelta
from random import random


def random_datetime(start: datetime, end: datetime) -> datetime:
    """Return a random datetime between the specified start and end datetimes."""
    time_delta = (end - start).total_seconds()
    random_time_delta = time_delta * random()
    return start + timedelta(seconds=random_time_delta)
