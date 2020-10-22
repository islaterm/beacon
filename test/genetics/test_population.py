import string
import unittest
from random import Random, randint
from typing import Dict

import pytest

from genetics.genotype.chromosomes import ChromosomeFactory
from genetics.individuals import Individual, IndividualFactory
from genetics.population import Population, PopulationError


def fitness_function(_: Individual) -> float:
    return 0


# region : Tests
@pytest.mark.repeat(16)
def test_wrong_population(invalid_size: int, individual_factory: IndividualFactory):
    """Creates a population with an invalid size and checks that it raises a PopulationError."""
    with pytest.raises(PopulationError) as error:
        _ = Population(invalid_size, individual_factory)
        assert expected_wrong_init_error == error


@pytest.mark.repeat(16)
def test_population_init(population: Population, population_size: int, mutation_rate: float,
                         ascii_alphabet: Dict[int, str], random_seed: int) -> None:
    expected_ind_factory = IndividualFactory(mutation_rate, fitness_function,
                                             [ChromosomeFactory(ascii_alphabet, max_size=3,
                                                                rng=Random(random_seed))])
    expected_population = Population(population_size, expected_ind_factory)
    assert population == expected_population


# endregion

# region : fixtures
#   region : Population
@pytest.fixture()
def population(population_size: int, individual_factory: IndividualFactory) -> Population:
    return Population(population_size, individual_factory)


@pytest.fixture()
def population_size() -> int:
    return Random(random_seed).randint(2, 4)


@pytest.fixture()
def mutation_rate(random_seed: int) -> float:
    return Random(random_seed).random()


#   endregion
#   region : Individuals
@pytest.fixture()
def individual_factory(mutation_rate: float,
                       ascii_chromosome_factory: ChromosomeFactory[str]) -> IndividualFactory:
    return IndividualFactory(mutation_rate, fitness_function, [ascii_chromosome_factory])


#   endregion
#   region : Chromosomes
@pytest.fixture()
def ascii_chromosome_factory(ascii_alphabet: Dict[int, str], random_seed: int) \
        -> ChromosomeFactory[str]:
    return ChromosomeFactory(ascii_alphabet, max_size=3, rng=Random(random_seed))


#   endregion
#   region : Wrong data
@pytest.fixture
def expected_wrong_init_error(invalid_size: int):
    return PopulationError(
        f"Invalid size {invalid_size}. The population must have at least 2 individuals")


@pytest.fixture
def invalid_size(random_seed):
    return Random(random_seed).randint(-10, 1)


#   endregion


@pytest.fixture()
def ascii_alphabet() -> Dict[int, str]:
    return dict([n for n in enumerate(string.ascii_letters)])


@pytest.fixture()
def random_seed():
    return randint(1, 100)


# endregion

if __name__ == '__main__':
    unittest.main()
