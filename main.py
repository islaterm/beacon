import random
from inspect import getmembers
from typing import Callable, List

from genyal.engine import GenyalEngine
from genyal.genotype import GeneFactory

import dummy


def gene_generator():
    """ Generates an initial population of random statements.

    :param individuals:
        the size of the population
    :return:
        a list of tuples with the function name and a direct reference to the callable function
    """
    funs = filter(callable, [member[1] for member in getmembers(dummy)])
    return random.choice(list(funs))


def get_fitness(statements: List[Callable]):
    try:
        for call in statements:
            call()
    except Exception as e:
        return 1 if isinstance(e, NotImplementedError) else 0
    return 0


if __name__ == '__main__':
    factory = GeneFactory()
    factory.generator = gene_generator
    engine = GenyalEngine(fitness_function=get_fitness)
    engine.create_population(10, 3, factory)
    print()
    #
    # generated_pop = gene_generator(10)
    # expected_error = NotImplementedError()
    # population_fitness = []
    # for ind in generated_pop:
    #     population_fitness.append((get_fitness(ind), ind))
    # population_fitness.sort(key=lambda i: i[0])
    # print(f"Expected exception: {expected_error.__class__}")
    # pprint(population_fitness[-3:])
