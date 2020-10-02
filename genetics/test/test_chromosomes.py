import string
import unittest
from typing import Dict

import pytest

from genetics.chromosomes import GenericChromosome, GenotypeException
from genetics.genes import GenericGene


def test_empty_chromosome(binary_alphabet: Dict) -> None:
    generic_chromosome = GenericChromosome(0, binary_alphabet, genes=[])
    assert not len(generic_chromosome)


def test_size_mismatch_chromosome(binary_alphabet: Dict, size_mismatch_error_msg: str) -> None:
    with pytest.raises(GenotypeException) as genotype_error:
        _ = GenericChromosome(0, binary_alphabet, genes=[GenericGene(binary_alphabet)])
        assert size_mismatch_error_msg in genotype_error.value


@pytest.fixture()
def binary_alphabet() -> Dict[bool, int]:
    return { True: 1, False: 0 }


@pytest.fixture()
def ascii_alphabet() -> Dict[int, str]:
    return dict([n for n in enumerate(string.ascii_letters)])


@pytest.fixture()
def size_mismatch_error_msg() -> str:
    return "Chromosome size doesn't match the number of genes.\n" \
           "Expected: 0\n" \
           "Actual: 1"


if __name__ == '__main__':
    unittest.main()
