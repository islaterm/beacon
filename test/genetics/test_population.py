import unittest
from random import Random, randint

import pytest

from genetics.population import PopulationError


def test_wrong_population():
    with pytest.raises(PopulationError) as error:
        ""


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
