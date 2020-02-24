# Genetic Time Series

## Introduction

Genetic algorithms can be used to find optimised solutions in good
time to problems where there are a very large number of variables.

This repo is an experiment in using a genetic algorithm to try to
generate, as closely as possible, a target time series from an initial
generation of randomly generated time series.
 
## The Algorithm

## Methodology

The time series object we are building is a `GeneticTimeSeries`. It is
composed of `Point` objects specifying a `datetime` and a value. 

### Executing the Algorithm

Import the required objects and create a target `GeneticTimeSeries`
that the algorithm will try to generate. Set this target using the 
`GeneticTimeSeries.configure` method.

```python
from datetime import datetime

from environment import Environment
from genetic_ts import GeneticTimeSeries
from point import Point


# Create the target.
target = GeneticTimeSeries(
    [
        Point(datetime(2019, 1, 1, 9), 0),
        Point(datetime(2019, 1, 1, 9, 15), 5),
        Point(datetime(2019, 1, 1, 9, 30), 10),
        Point(datetime(2019, 1, 1, 10), 10),
        Point(datetime(2019, 1, 1, 10, 15), 5),
        Point(datetime(2019, 1, 1, 10, 30), 0),
    ]
)

# Set the target.
GeneticTimeSeries.configure(target)
```

Create an initial population of 100 randomly generated
`GeneticTimeSeries` instances.

```python
initial_population = [GeneticTimeSeries.random_instance() for _ in range(100)]
```

Specify the environmental conditions. These are:
- the initial population;
- the threshold fitness at which the algorithm should cease;
- the maximum number of generations;
- the propability of mutation; and,
- the probability of crossover.

```python
# Execute the genetic algorithm.
natural_selection = Environment(
    initial_population=initial_population,
    threshold=1,
    max_generations=1000,
    mutation_chance=0.8,
    crossover_chance=0.6
)

best_result = natural_selection.run()
```

To plot all of the results of each generation up until one that 
satisfies the threshold, capture all the results by casting the 
generator method as a list and then use with a plotting library such
as matplotlib.

```python
results = list(natural_selection.run())
```

### Result

The gif below shows the evolution of the `GeneticTimeseries` after each
generation given the environmental conditions defined above. 

![evolution_gif]

After approximately the 875th generation the derived time series
resembles the target quite well and remains stable thereafter. 

## Conclusion
 
 
## References

Kopec D. Classic Computer Science Problems in Python. Manning Publications. 20th May 2019.

[evolution_gif]: evolution.gif "evolution_gif"
 