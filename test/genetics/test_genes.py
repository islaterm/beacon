"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
import unittest
from typing import Dict

import pytest

from src.genetics.genes import DNAException, GenericGene


def test_empty_gene(empty_alphabet_error_msg: str) -> None:
    with pytest.raises(DNAException) as dna_error:
        _ = GenericGene({ })
        assert empty_alphabet_error_msg in dna_error.value


@pytest.mark.repeat(8)
def test_random_gene(binary_gene: GenericGene[int], binary_alphabet: Dict[bool, int],
                     random_seed: int) -> None:
    rng = random.Random(random_seed)
    assert binary_gene.dna == binary_alphabet[rng.choice(list(binary_alphabet.keys()))]


@pytest.fixture
def binary_gene(random_seed: int, binary_alphabet: Dict[bool, int]) -> GenericGene[int]:
    return GenericGene(binary_alphabet, rng=random.Random(random_seed))


# region : Parameters
@pytest.fixture()
def random_seed():
    return random.randint(-50, 50)


@pytest.fixture()
def binary_alphabet() -> Dict[bool, int]:
    return { True: 1, False: 0 }


# endregion

@pytest.fixture
def empty_alphabet_error_msg() -> str:
    return "Alphabet cannot be empty."


if __name__ == '__main__':
    unittest.main()
