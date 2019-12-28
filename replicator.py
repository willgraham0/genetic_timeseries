from __future__ import annotations
from typing import TypeVar, Tuple, Type
from abc import ABC, abstractmethod

T = TypeVar('T', bound="Replicator")


class Replicator(ABC):
    """A base class for all replicators."""

    @abstractmethod
    def fitness(self) -> float:
        """Return a metric for determining the fitness of the instance."""
        pass

    @classmethod
    @abstractmethod
    def random_instance(cls: Type[T]) -> T:
        """Return a random instance of the type T."""
        pass

    @abstractmethod
    def crossover(self: T, other: T) -> Tuple[T, T]:
        """Return two child instances that is a combination of self and other."""
        pass

    @abstractmethod
    def mutate(self) -> None:
        """Make random modifications to self."""
        pass
