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
from typing import Dict

import pytest

from genetics.genes import DNAException, GenericGene


# region : Constructor tests
def test_empty_gene(empty_alphabet_error_msg: str) -> None:
    with pytest.raises(DNAException) as dna_error:
        _ = GenericGene({ })
        assert empty_alphabet_error_msg in dna_error.value


def test_wrong_key(binary_alphabet: Dict[bool, int], wrong_key_error_msg: str) -> None:
    with pytest.raises(DNAException) as dna_error:
        _ = GenericGene(binary_alphabet, key="A")
        assert wrong_key_error_msg in dna_error.value


@pytest.mark.repeat(8)
def test_binary_gene(binary_gene: GenericGene[int], binary_alphabet: Dict[bool, int],
                     random_seed: int) -> None:
    rng = random.Random(random_seed)
    assert binary_gene.dna == binary_alphabet[rng.choice(list(binary_alphabet.keys()))]


@pytest.mark.repeat(100)
def test_ascii_gene(ascii_gene: GenericGene[str], ascii_alphabet: Dict[bool, str],
                    random_seed: int) -> None:
    rng = random.Random(random_seed)
    assert ascii_gene.dna == ascii_alphabet[rng.choice(list(ascii_alphabet.keys()))]


# endregion

# region : Utility tests
@pytest.mark.repeat(100)
def test_gene_copy(ascii_gene: GenericGene[str], random_seed: int):
    new_gene = copy(ascii_gene)
    assert new_gene == ascii_gene, f"Test failed with seed {random_seed}"


# endregion
# region : Parameters
@pytest.fixture
def binary_gene(random_seed: int, binary_alphabet: Dict[bool, int]) -> GenericGene[int]:
    return GenericGene(binary_alphabet, rng=random.Random(random_seed))


@pytest.fixture
def ascii_gene(random_seed: int, ascii_alphabet: Dict[bool, str]) -> GenericGene[str]:
    return GenericGene(ascii_alphabet, rng=random.Random(random_seed))


@pytest.fixture()
def random_seed():
    return random.randint(-50, 50)


@pytest.fixture()
def binary_alphabet() -> Dict[bool, int]:
    return { True: 1, False: 0 }


@pytest.fixture()
def ascii_alphabet() -> Dict[int, str]:
    return dict([n for n in enumerate(string.ascii_letters)])


# region : Error messages
@pytest.fixture
def empty_alphabet_error_msg() -> str:
    return "Alphabet cannot be empty."


@pytest.fixture
def wrong_key_error_msg(binary_alphabet: Dict[bool, int]) -> str:
    return f"A is not part of the alphabet {binary_alphabet}"


# endregion
# endregion


if __name__ == '__main__':
    unittest.main()
