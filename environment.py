from __future__ import annotations
from enum import Enum
from heapq import nlargest
from random import choices, random
from statistics import mean
from typing import TypeVar, Generic, List, Tuple, Callable

from replicator import Replicator

C = TypeVar('C', bound=Replicator)


class SelectionType(Enum):
    ROULETTE = "ROULETTE"
    TOURNAMENT = "TOURNAMENT"


class Environment(Generic[C]):
    def __init__(
        self,
        initial_population: List[C],
        threshold: float,
        max_generations: int = 100,
        mutation_chance: float = 0.01,
        crossover_chance: float = 0.7,
        selection_type: SelectionType = SelectionType.TOURNAMENT
    ):
        self._population = initial_population
        self._threshold = threshold
        self._max_generations = max_generations
        self._mutation_chance = mutation_chance
        self._crossover_chance = crossover_chance
        self._selection_type = selection_type
        self._fitness_key: Callable = type(self._population[0]).fitness

    def _pick_roulette(self, wheel: List[float]) -> Tuple[C, C]:
        """Pick two parents using the probability distribution wheel.

        Note: will not work with negative fitness results.
        """
        return tuple(choices(self._population, weights=wheel, k=2))

    def _pick_tournament(self, num_participants: int) -> Tuple[C, C]:
        """Pick two parents that have the best fitness from a sample size of `num_participants`."""
        participants: List[C] = choices(self._population, k=num_participants)
        return tuple(nlargest(2, participants, key=self._fitness_key))

    def _reproduce_and_replace(self) -> None:
        """Replace the population with a new generation of individuals."""
        new_population: List[C] = []

        # Continue until the new generation is the same size of the previous.
        while len(new_population) < len(self._population):
            # Pick the 2 parents.
            if self._selection_type == SelectionType.ROULETTE:
                parents = self._pick_roulette([individual.fitness() for individual in self._population])
            else:
                parents = self._pick_tournament(len(self._population) // 2)

            # Replicate or clone.
            if random() < self._crossover_chance:
                father, mother = parents
                children = father.crossover(mother)
                new_population.extend(children)
            else:
                new_population.extend(parents)

        # Ensure the size of the new population is the same as the previous.
        if len(new_population) > len(self._population):
            new_population.pop()

        self._population = new_population

