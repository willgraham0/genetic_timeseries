from __future__ import annotations
from copy import deepcopy
from datetime import datetime
from typing import List, Tuple, Type
from random import gauss, randint

from environment import Environment
from point import Point
from replicator import Replicator
from utils import random_datetime


class GeneticTimeSeries(Replicator):

    ideal: GeneticTimeSeries = None

    def __init__(self, points: List[Point]) -> None:
        if self.ideal:
            if len(points) != len(self.ideal.points):
                raise ValueError("The number of points is not the same as in the ideal time series.")
        self.points = list(sorted(points, key=lambda x: x.time))

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

    def fitness(self) -> float:
        """Return the reciprocal of the maximum of the distances between elbow points of this time series and the ideal.
        """
        if not self.ideal:
            raise ValueError("This class must be configured before an instance can be created.")
        return 1 / max(p1.distance(p2) for p1, p2 in zip(self.ideal.points, self.points))

    def mutate(self) -> None:
        """Modify the value and time of each point in the time series using a Gaussian distribution."""
        sig = 1.2
        for point in self.points:
            point.value = gauss(point.value, sig)
            point.time = datetime.fromtimestamp(gauss(point.time.timestamp(), sig))

    def crossover(self, other: GeneticTimeSeries) -> Tuple[GeneticTimeSeries, GeneticTimeSeries]:
        """Create children by mixing datetimes and values."""
        father, mother = self, other
        child1 = deepcopy(father)
        child2 = deepcopy(mother)
        # Child 1 (initially a clone of the father) gets values of mother.
        for point in mother.points:
            for child1_point in child1.points:
                child1_point.value = point.value
        # Child 2 (initially a clone of the mother) gets times of father.
        for point in father.points:
            for child2_point in child2.points:
                child2_point.time = point.time
        return child1, child2

    @classmethod
    def random_instance(cls: Type[GeneticTimeSeries]) -> GeneticTimeSeries:
        """Return a random genetic time series that had times and values within the time and value ranges of `ideal`."""
        if not cls.ideal:
            raise ValueError("This class must be configured before an instance can be created.")
        new_points = []
        for _ in range(len(cls.ideal.points)):
            time = random_datetime(cls.ideal.earliest_time, cls.ideal.latest_time)
            value = randint(cls.ideal.min_value, cls.ideal.max_value)
            new_points.append(Point(time, value))
        return cls(new_points)

    @classmethod
    def configure(cls, ideal: GeneticTimeSeries) -> None:
        cls.ideal = ideal


if __name__ == "__main__":
    # Goal.
    goal = GeneticTimeSeries(
        [
            Point(datetime(2019, 1, 1, 9), 0),
            Point(datetime(2019, 1, 1, 9, 15), 5),
            Point(datetime(2019, 1, 1, 9, 30), 10),
            Point(datetime(2019, 1, 1, 10), 10),
            Point(datetime(2019, 1, 1, 10, 15), 5),
            Point(datetime(2019, 1, 1, 10, 30), 0),
        ]
    )

    # Set goal.
    GeneticTimeSeries.configure(goal)

    # Start evolution.
    initial_population = [GeneticTimeSeries.random_instance() for _ in range(100)]
    natural_selection = Environment(
        initial_population=initial_population,
        threshold=0.9,
        max_generations=1000,
        mutation_chance=0.8,
        crossover_chance=0.8
    )
    result = natural_selection.run()

    print("Ideal")
    for i in goal.points:
        print(i)
    print("Result")
    for j in result.points:
        print(j)
