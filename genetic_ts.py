from __future__ import annotations
from datetime import datetime
from typing import List, Tuple, Type

from environment import Environment
from timeseries import Point
from replicator import Replicator


class GeneticTimeSeries(Replicator):

    ideal: List[Point] = None

    @classmethod
    def is_configured(cls, func):
        if not cls.ideal:
            raise ValueError("This class must be configured before an instance can be created.")
        return func

    @is_configured
    def __init__(self, points) -> None:
        if len(points) != len(self.ideal):
            raise ValueError("The number of points is not the same as in the ideal time series.")

        self.points = tuple(
            Point(*point)
            for point in sorted(points, key=lambda x: x.time)
        )

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
        """Return the maximum of the distances between elbow points of this time series and the ideal."""
        return max(p1.distance(p2) for p1, p2 in zip(self.ideal, self.points))

    def mutate(self) -> None:
        pass

    def crossover(self, other: GeneticTimeSeries) -> Tuple[GeneticTimeSeries, GeneticTimeSeries]:
        pass

    @classmethod
    def random_instance(cls: Type[GeneticTimeSeries]) -> GeneticTimeSeries:
        pass

    @classmethod
    def configure(cls, ideal: List[Point]) -> None:
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
