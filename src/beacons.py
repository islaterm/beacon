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
from typing import Any, Type


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
    __types: dict[Type, Type[BeaconType]]
    __type_list: list[Type]
    __constructor_arguments: dict[Type, dict[str, Any]]

    def __init__(self, constructors_args=None):
        if constructors_args is None:
            constructors_args = { }
        self.__types = { int: Integer, str: String }
        self.__type_list = [int, str]
        self.__constructor_arguments = constructors_args

    def set(self, in_type: Type, type_constructor: Type[BeaconType]) -> None:
        """
        Adds a new type mapping to the factory.

        Args:
            in_type:
                the concrete type that's gonna be created with the factory.
            type_constructor:
                a class that extends [BeaconType] with a specification of how to create the
                elements used in [Tracer].
        """
        self.__types[in_type] = type_constructor
        self.__type_list.append(in_type)

    def get(self) -> Any:
        """
        Returns a new random value generated from the input factory types.
        """
        return_type = random.choice(self.__type_list)
        return self.__types[return_type].make(
            **(self.__constructor_arguments[
                   return_type] if return_type in self.__constructor_arguments else { }))

