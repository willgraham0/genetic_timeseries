from __future__ import annotations
from datetime import datetime
from typing import Tuple, Type

from environment import Environment
from timeseries import Point
from replicator import Replicator


class GeneticTimeSeries(Replicator):

    ideal: GeneticTimeSeries = None

    def __init__(self, points) -> None:
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

    @classmethod
    def configure(cls, ideal: GeneticTimeSeries) -> None:
        cls.ideal = ideal

    @classmethod
    def is_configured(cls, func):
        if not cls.ideal:
            raise ValueError("This class must be configured before this method can be called.")
        return func

    @is_configured
    def fitness(self) -> float:
        pass

    def mutate(self) -> None:
        pass

    def crossover(self, other: GeneticTimeSeries) -> Tuple[GeneticTimeSeries, GeneticTimeSeries]:
        pass

    @classmethod
    def random_instance(cls: Type[GeneticTimeSeries]) -> GeneticTimeSeries:
        pass


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
