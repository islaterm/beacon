import unittest

import pytest

from src.genetics.genes import DNAException, GenericGene


def test_empty_gene(empty_alphabet_error_msg: str) -> None:
    with pytest.raises(DNAException) as dna_error:
        _ = GenericGene({ })
        assert empty_alphabet_error_msg in dna_error.value


@pytest.mark.repeat(8)
def test_random_gene(generic_gene: GenericGene[int]) -> None:
    pass


@pytest.fixture
def generic_gene() -> GenericGene[int]:
    return GenericGene({ True: 1, False: 0 })


@pytest.fixture
def empty_alphabet_error_msg() -> str:
    return "Alphabet cannot be empty."


if __name__ == '__main__':
    unittest.main()
