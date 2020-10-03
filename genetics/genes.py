"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
from typing import Any, Dict, Generic, TypeVar

DNA = TypeVar("DNA")


class DNAException(Exception):
    def __init__(self, msg: str):
        super(DNAException, self).__init__(msg)


class GenericGene(Generic[DNA]):
    """ A gene is the more basic unit of a genotype.    """
    __alphabet: Dict[Any, DNA]
    __dna: DNA
    __key: str

    def __init__(self, alphabet: Dict[Any, DNA], key: str = "",
                 rng: random.Random = random.Random()):
        """ Creates a random gene from a DNA alphabet.  """
        if alphabet:
            self.__alphabet = alphabet
            self.__key = key if key else rng.choice(list(alphabet.keys()))
            try:
                self.__dna = alphabet[self.__key]
            except KeyError:
                raise DNAException(f"{self.__key} is not part of the alphabet {alphabet}")
        else:
            raise DNAException("Alphabet cannot be empty.")

    # region : Properties
    @property
    def dna(self):
        """ The content of this gene.   """
        return self.__dna

    # endregion

    # region : Utility
    def __copy__(self) -> 'GenericGene[DNA]':
        """ Returns a copy of this gene.    """
        return GenericGene(self.__alphabet, self.__key)

    def __eq__(self, other) -> bool:
        return isinstance(other,
                          GenericGene) and other.__alphabet == self.__alphabet and other.__key == \
               self.__key and other.__dna == self.__dna

    def __repr__(self) -> str:
        return self.__str__()

    def __str__(self) -> str:
        return f"{str(self.__key)}: {str(self.__dna)}"

    def copy_to(self, other: 'GenericGene[DNA]') -> None:
        """ Copies the DNA of this gene into another.   """
        other.__dna = self.__dna
        other.__key = self.__key
        other.__alphabet = self.__alphabet
    # endregion
