import random
from inspect import getmembers
from pprint import pprint
from typing import Callable, List, Tuple

import dummy


def generate_population(individuals: int) -> List[List[Tuple[str, Callable]]]:
    """ Generates an initial population of random statements.

    :param individuals:
        the size of the population
    :return:
        a list of tuples with the function name and a direct reference to the callable function
    """
    members = getmembers(dummy)
    functions = []
    for member in members:
        member_val = member[1]
        if callable(member_val):
            fun = member_val
            functions.append((fun.__name__, fun))
    population = []
    for _ in range(0, individuals):
        individual = []
        while random.random() < 0.75:
            individual.append(random.choice(functions))
        population.append(individual)
    return population


def get_fitness(statements: List[Tuple[str, Callable]], expected_exeption: Exception):
    try:
        for call in statements:
            call[1]()
    except Exception as e:
        return (1 if e.__class__ == expected_exeption.__class__ else 0) + 1 / (10 * len(statements))
    return 0


if __name__ == '__main__':
    generated_pop = generate_population(10)
    expected_error = NotImplementedError()
    population_fitness = []
    for ind in generated_pop:
        population_fitness.append((get_fitness(ind, expected_error), ind))
    population_fitness.sort(key=lambda i: i[0])
    print(f"Expected exception: {expected_error.__class__}")
    pprint(population_fitness[-3:])
