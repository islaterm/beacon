import string
import unittest
from random import Random, randint
from typing import Dict

import pytest

from genetics.genotype.chromosomes import ChromosomeFactory
from genetics.individuals import Individual, IndividualFactory
from genetics.population import Population, PopulationError


@pytest.mark.repeat(10)
def test_wrong_population(invalid_size: int, individual_factory: IndividualFactory):
    with pytest.raises(PopulationError) as error:
        _ = Population(invalid_size, individual_factory)
        assert expected_wrong_init_error == error


@pytest.fixture()
def individual_factory(mutation_rate: float) -> IndividualFactory:
    """"""
    return IndividualFactory(mutation_rate, fitness_function, ascii_chromosome_factory)


@pytest.fixture()
def fitness_function(individual: Individual) -> float:
    return 0


@pytest.fixture()
def ascii_chromosome_factory(ascii_alphabet: Dict[int, str]) -> ChromosomeFactory[str]:
    """"""
    return ChromosomeFactory(ascii_alphabet)


@pytest.fixture()
def ascii_alphabet() -> Dict[int, str]:
    return dict([n for n in enumerate(string.ascii_letters)])


@pytest.fixture()
def mutation_rate(random_seed: int) -> float:
    return Random(random_seed).random()


@pytest.fixture
def expected_wrong_init_error(invalid_size: int):
    return PopulationError(
        f"Invalid size {invalid_size}. The population must have at least 2 individuals")


@pytest.fixture
def invalid_size(random_seed):
    return Random(random_seed).randint(-10, 1)


@pytest.fixture()
def random_seed():
    return randint(1, 100)


if __name__ == '__main__':
    unittest.main()
