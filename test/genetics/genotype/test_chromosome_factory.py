"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import string
import unittest
from typing import Dict

import pytest

from genetics.genotype.chromosomes import ChromosomeFactory


def test_factory_init(chromosome_factory: ChromosomeFactory[str], ascii_alphabet: Dict[int, str]):
    expected_factory = ChromosomeFactory(ascii_alphabet, 100)
    assert expected_factory == chromosome_factory


def test_factory_make():
    assert False


@pytest.fixture
def chromosome_factory(ascii_alphabet: Dict[int, str]) -> ChromosomeFactory[str]:
    """"""
    return ChromosomeFactory(ascii_alphabet, 100)


@pytest.fixture()
def ascii_alphabet() -> Dict[int, str]:
    """"""
    return dict([n for n in enumerate(string.ascii_letters)])


if __name__ == '__main__':
    unittest.main()
