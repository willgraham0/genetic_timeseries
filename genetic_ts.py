from __future__ import annotations
from copy import deepcopy
from datetime import datetime
from typing import Tuple, Type
from random import randint

from environment import Environment
from timeseries import Point
from replicator import Replicator
from utils import random_datetime


class GeneticTimeSeries(Replicator):

    ideal: GeneticTimeSeries = None

    def __init__(self, points) -> None:
        if self.ideal:
            if len(points) != len(self.ideal.points):
                raise ValueError("The number of points is not the same as in the ideal time series.")
        self.points = tuple(Point(*point) for point in sorted(points, key=lambda x: x.time))

    @classmethod
    def is_configured(cls, func):
        if not cls.ideal:
            raise ValueError("This class must be configured before an instance can be created.")
        return func

    @property
    def max_value(self) -> float:
        """Return the largest value in the genetic time series."""
        return max(point.value for point in self.points)

    @property
    def min_value(self) -> float:
        """Return the smallest value in the genetic time series."""
        return min(point.value for point in self.points)

    @property
    def latest_time(self) -> datetime:
        """Return the latest time in the genetic time series."""
        return max(point.time for point in self.points)

    @property
    def earliest_time(self) -> datetime:
        """Return the earliest time in the genetic time series."""
        return min(point.time for point in self.points)

    @is_configured
    def fitness(self) -> float:
        """Return the maximum of the distances between elbow points of this time series and the ideal."""
        return max(p1.distance(p2) for p1, p2 in zip(self.ideal.points, self.points))

    def mutate(self) -> None:
        pass

    def crossover(self, other: GeneticTimeSeries) -> Tuple[GeneticTimeSeries, GeneticTimeSeries]:
        """Create children by mixing datetimes and values."""
        father, mother = self, other
        child1 = deepcopy(father)
        child2 = deepcopy(mother)
        # Child 1 (clone of father) gets values of mother.
        for point in mother.points:
            for child1_point in child1.points:
                child1_point.value = point.value
        # Child 2 (clone of mother) gets values of father.
        for point in father.points:
            for child2_point in child2.points:
                child2_point.time = point.time
        return child1, child2

    @classmethod
    @is_configured
    def random_instance(cls: Type[GeneticTimeSeries]) -> GeneticTimeSeries:
        """Return a random genetic time series that had times and values within the time and value ranges of `ideal`."""
        time = random_datetime(cls.ideal.earliest_time, cls.ideal.latest_time)
        value = randint(cls.ideal.min_value, cls.ideal.max_value)
        return cls((time, value) for _ in range(len(cls.ideal.points)))

    @classmethod
    def configure(cls, ideal: GeneticTimeSeries) -> None:
        cls.ideal = ideal


if __name__ == "__main__":
    initial_population = [GeneticTimeSeries.random_instance() for _ in range(20)]
    natural_selection = Environment(
        initial_population=initial_population,
        threshold=13.0,
        max_generations=100,
        mutation_chance=0.1,
        crossover_chance=0.7
    )
    result = natural_selection.run()
    print(result)
