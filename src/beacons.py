"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
import string
import sys
from abc import ABC, abstractmethod
from random import Random


class BeaconType(ABC):
    """
    Base type for all beacons.

    A beacon defines a type of input that'll be used as function parameter for Tracer.
    All beacons must implement the class method ``make`` that will serve as the generator for values
    of this* type.

        * whenever we refer to _this_ in the context of Beacon we're refering to the type
        represented by the class. For example: ``Integer`` represents the type ``int``
    """
    rng: Random

    def __init__(self, rng: random.Random = random.Random()):
        """
        Defines a new type of Beacon to use as a function parameter in Tracer.

        Args:
            rng:    a random number generator used for value generation.
        """
        self.rng = rng

    @classmethod
    @abstractmethod
    def make(cls, **kwargs):
        """
        Generates a new value of this type
        Args:
            **kwargs:   named parameters used for the value generation.

        Returns:
            a value of this type
        """
        raise NotImplementedError("Abstract method can't be called")


class Integer(BeaconType):
    """

    """
    @classmethod
    def make(cls, lo: int = -sys.maxsize, hi: int = sys.maxsize) -> int:
        return random.randrange(lo, hi)


class String(BeaconType):
    @classmethod
    def make(cls, characters: str = string.printable, max_len: int = 50, min_len: int = 0):
        str_len = random.randint(min_len, max_len)
        return "".join([random.choice(characters) for _ in range(min_len, str_len)])


arg_types = { int: Integer }


class InputFactory:
    def __init__(self):
        self.__types = { int: Integer, str: String }

    def set(self, in_type, type_constructor):
        self.__types[in_type] = type_constructor
