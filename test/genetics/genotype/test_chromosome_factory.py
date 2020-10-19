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

from genetics.genotype.chromosomes import ChromosomeFactory, GenericChromosome


@pytest.mark.repeat(16)
def test_factory_init(chromosome_factory: ChromosomeFactory[str], ascii_alphabet: Dict[int, str],
                      chromosome_size: int):
    expected_factory = ChromosomeFactory(ascii_alphabet, chromosome_size)
    assert expected_factory == chromosome_factory


@pytest.mark.repeat(16)
def test_factory_make(chromosome_factory: ChromosomeFactory[str], chromosome_size: int,
                      ascii_alphabet: Dict[int, str], random_seed: int) -> None:
    expected_chromosome = GenericChromosome(chromosome_size, ascii_alphabet,
                                            rng=Random(random_seed))
    actual_chromosome = chromosome_factory.make(chromosome_size)
    assert actual_chromosome == expected_chromosome


@pytest.fixture
def chromosome_factory(ascii_alphabet: Dict[int, str], chromosome_size: int, random_seed) \
        -> ChromosomeFactory[str]:
    """"""
    return ChromosomeFactory(ascii_alphabet, chromosome_size, rng=Random(random_seed))


@pytest.fixture()
def chromosome_size(random_seed: int) -> int:
    return Random(random_seed).randint(1, 256)


@pytest.fixture()
def ascii_alphabet() -> Dict[int, str]:
    """"""
    return dict([n for n in enumerate(string.ascii_letters)])


@pytest.fixture()
def random_seed() -> int:
    return randint(-sys.maxsize, sys.maxsize)


if __name__ == '__main__':
    unittest.main()
