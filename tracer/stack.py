"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from inspect import getmembers
from pprint import pprint
from types import FunctionType
from typing import Callable, Dict

import numpy

import dummy
from genetics.genotype.chromosomes import ChromosomeFactory
from genetics.individuals import Individual, IndividualFactory
from genetics.population import Population

expected_exception = ValueError
expected_message = "Value must be positive"


def get_module_functions(module) -> Dict[str, Callable]:
    """
    Get all the functions from a module.

    Returns:
        a list with references to the functions in the module
    """
    members = getmembers(module)
    funs = { }
    for fun in filter(lambda m: isinstance(m[1], FunctionType), members):
        funs[fun[0]] = fun[1]
    return funs


def fitness_function(individual: Individual) -> float:
    try:
        for gene in individual.genotype[0]:
            gene.dna()
        return -numpy.inf
    except Exception as e:
        return (1 if isinstance(e, expected_exception) else 0) + (
            0.5 if expected_message in str(e) else 0) - 0.1 * len(individual.genotype[0])


if __name__ == '__main__':
    functions = get_module_functions(dummy)
    population = Population(100, IndividualFactory(0.2, fitness_function,
                                                   [ChromosomeFactory(functions, max_size=10)]))
    for _ in range(0, 1000):
        population.evolve()
    pprint(population.get_fittest(10))
