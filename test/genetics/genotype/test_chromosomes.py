"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
import string
import unittest
from copy import copy
from random import Random
from typing import Dict

import pytest

from genetics.genotype.chromosomes import GenericChromosome, GenotypeException
from genetics.genotype.genes import GenericGene


@pytest.mark.repeat(32)
def test_basic_operations(ascii_chromosome: GenericChromosome, ascii_alphabet: Dict[int, str],
                          random_seed: int) -> None:
    gene = GenericGene(ascii_alphabet)
    idx = random.Random(random_seed).randint(0, len(ascii_chromosome) - 1)
    print(idx)
    ascii_chromosome[idx] = gene
    assert ascii_chromosome[idx] == gene

    genes_str = str(ascii_chromosome.genes)
    assert str(ascii_chromosome) == genes_str


def test_empty_chromosome(binary_alphabet: Dict) -> None:
    generic_chromosome = GenericChromosome(0, binary_alphabet, genes=[])
    assert not len(generic_chromosome)


def test_size_mismatch_chromosome(binary_alphabet: Dict, size_mismatch_error_msg: str) -> None:
    with pytest.raises(GenotypeException) as genotype_error:
        _ = GenericChromosome(0, binary_alphabet, genes=[GenericGene(binary_alphabet)])
        assert size_mismatch_error_msg in genotype_error.value


@pytest.mark.repeat(100)
def test_binary_chromosome(binary_alphabet: Dict, binary_chromosome: GenericChromosome,
                           chromosome_size: int, random_seed: int) -> None:
    rng = Random(random_seed)
    expected_chromosome = GenericChromosome(chromosome_size, binary_alphabet, rng)
    assert expected_chromosome == binary_chromosome


@pytest.mark.repeat(100)
def test_ascii_chromosome(ascii_alphabet: Dict, ascii_chromosome: GenericChromosome,
                          chromosome_size: int, random_seed: int) -> None:
    rng = Random(random_seed)
    expected_chromosome = GenericChromosome(chromosome_size, ascii_alphabet, rng)
    assert expected_chromosome == ascii_chromosome


@pytest.mark.repeat(16)
def test_chromosome_copy(binary_chromosome: GenericChromosome,
                         ascii_chromosome: GenericChromosome) -> None:
    binary_chromosome_copy = copy(binary_chromosome)
    assert binary_chromosome == binary_chromosome_copy
    ascii_chromosome_copy = copy(ascii_chromosome)
    assert ascii_chromosome == ascii_chromosome_copy


@pytest.fixture()
def binary_chromosome(binary_alphabet: Dict[bool, int], chromosome_size: int,
                      random_seed: int) -> GenericChromosome:
    chromosome_rng = Random(random_seed)
    return GenericChromosome(chromosome_size, binary_alphabet, chromosome_rng)


@pytest.fixture()
def ascii_chromosome(ascii_alphabet: Dict[bool, int], chromosome_size: int,
                     random_seed: int) -> GenericChromosome:
    chromosome_rng = Random(random_seed)
    return GenericChromosome(chromosome_size, ascii_alphabet, chromosome_rng)


@pytest.fixture()
def chromosome_size():
    return random.randint(1, 100)


@pytest.fixture()
def binary_alphabet() -> Dict[bool, int]:
    return { True: 1, False: 0 }


@pytest.fixture()
def ascii_alphabet() -> Dict[int, str]:
    return dict([n for n in enumerate(string.ascii_letters)])


@pytest.fixture()
def random_seed():
    return random.randint(-50, 50)


@pytest.fixture()
def size_mismatch_error_msg() -> str:
    return "Chromosome size doesn't match the number of genes.\n" \
           "Expected: 0\n" \
           "Actual: 1"


if __name__ == '__main__':
    unittest.main()
