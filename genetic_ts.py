from timeseries import TimeSeries
from replicator import Replicator


class GeneticTimeSeries(Replicator):

    ideal: TimeSeries = None

    @classmethod
    def configure(cls, ideal: TimeSeries) -> None:
        cls.ideal = ideal

    def is_configured(self, func):
        if not self.ideal:
            raise ValueError("Class must be configured before this method can be called.")
        return func

    @is_configured
    def fitness(self) -> float:
        pass

