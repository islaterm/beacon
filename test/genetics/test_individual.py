"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import string
import sys
import unittest
from random import Random, randint
from typing import Dict

import pytest

from genetics.genotype.chromosomes import ChromosomeFactory
from genetics.individuals import Individual, IndividualFactory


@pytest.mark.repeat(16)
def test_factory_init(individual_factory: IndividualFactory, random_seed: int,
                      binary_factory: ChromosomeFactory[int],
                      ascii_factory: ChromosomeFactory[str]) -> None:
    expected_factory = IndividualFactory(Random(random_seed).random(), fitness_function,
                                         [binary_factory, ascii_factory])
    assert individual_factory == expected_factory


def test_factory_make(individual_factory: IndividualFactory, mutation_rate: float,
                      ascii_alphabet: Dict[int, str], binary_alphabet: Dict[bool, int],
                      random_seed: int) -> None:
    chromosome_size = Random(random_seed).randint(1, 50)
    expected_genotype = [
        ChromosomeFactory(ascii_alphabet, chromosome_size, rng=Random(random_seed)).make(
            chromosome_size),
        ChromosomeFactory(binary_alphabet, chromosome_size, rng=Random(random_seed)).make(
            chromosome_size)]
    expected_individual = Individual(expected_genotype, mutation_rate, fitness_function)
    actual_individual = individual_factory.make(chromosome_size)
    assert actual_individual == expected_individual


@pytest.fixture()
def individual_factory(mutation_rate: float, binary_factory: ChromosomeFactory,
                       ascii_factory: ChromosomeFactory) -> IndividualFactory:
    return IndividualFactory(mutation_rate, fitness_function,
                             [ascii_factory, binary_factory])


@pytest.fixture()
def mutation_rate(random_seed: int) -> float:
    return Random(random_seed).random()


@pytest.fixture
def binary_factory(binary_alphabet: Dict[bool, int], chromosome_size: int, random_seed) \
        -> ChromosomeFactory[int]:
    return ChromosomeFactory(binary_alphabet, chromosome_size, rng=Random(random_seed))


@pytest.fixture
def ascii_factory(ascii_alphabet: Dict[int, str], chromosome_size: int, random_seed) \
        -> ChromosomeFactory[str]:
    return ChromosomeFactory(ascii_alphabet, chromosome_size, rng=Random(random_seed))


@pytest.fixture
def chromosome_size(random_seed: int) -> int:
    return Random(random_seed).randint(1, 256)


@pytest.fixture
def binary_alphabet() -> Dict[bool, int]:
    return { True: 1, False: 0 }


@pytest.fixture()
def ascii_alphabet() -> Dict[int, str]:
    return dict([n for n in enumerate(string.ascii_letters)])


@pytest.fixture()
def random_seed() -> int:
    return randint(-sys.maxsize, sys.maxsize)


def fitness_function(_: Individual) -> float:
    return 0


if __name__ == '__main__':
    unittest.main()
