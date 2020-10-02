import string
import unittest
from typing import Dict

import pytest

from genetics.chromosomes import GenericChromosome


def test_empty_chromosome(binary_alphabet: Dict):
    test_chromosome = GenericChromosome(0, binary_alphabet, genes=[])
    assert not len(test_chromosome)


@pytest.fixture()
def binary_alphabet() -> Dict[bool, int]:
    return { True: 1, False: 0 }


@pytest.fixture()
def ascii_alphabet() -> Dict[int, str]:
    return dict([n for n in enumerate(string.ascii_letters)])


if __name__ == '__main__':
    unittest.main()
