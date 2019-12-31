from __future__ import annotations
from typing import Tuple, Type

from environment import Environment
from timeseries import TimeSeries
from replicator import Replicator


class GeneticTimeSeries(Replicator):

    ideal: TimeSeries = None

    @classmethod
    def configure(cls, ideal: TimeSeries) -> None:
        cls.ideal = ideal

    @classmethod
    def is_configured(cls, func):
        if not cls.ideal:
            raise ValueError("Class must be configured before this method can be called.")
        return func

    @is_configured
    def fitness(self) -> float:
        pass

    @is_configured
    def mutate(self) -> None:
        pass

    @is_configured
    def crossover(
        self: GeneticTimeSeries,
        other: GeneticTimeSeries
    ) -> Tuple[GeneticTimeSeries, GeneticTimeSeries]:
        pass

    @classmethod
    @is_configured
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
