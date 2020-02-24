# Genetic Time Series

## Introduction

Genetic algorithms can be used to find optimised solutions to problems
where there are a very large number of variables.
 
## Time Series

### Executing the algorithm

```python
from datetime import datetime

from environment import Environment
from genetic_ts import GeneticTimeSeries
from point import Point


# Create the goal.
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

# Set the goal.
GeneticTimeSeries.configure(goal)

# Execute the genetic algorithm.
initial_population = [GeneticTimeSeries.random_instance() for _ in range(100)]
natural_selection = Environment(
    initial_population=initial_population,
    threshold=1,
    max_generations=1000,
    mutation_chance=0.8,
    crossover_chance=0.6
)

best_result = natural_selection.run()
```

### Result

![evolution_gif]

## Conclusion
 
 
[evolution_gif]: evolution.gif "evolution_gif"
 