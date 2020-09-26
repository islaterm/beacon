"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
from typing import Dict, Generic, TypeVar

DNA = TypeVar("DNA")


class DNAException(Exception):
    def __init__(self, msg: str):
        super(DNAException, self).__init__(msg)


class GenericGene(Generic[DNA]):
    """ A gene is the more basic unit of a genotype.    """
    __alphabet: Dict[str, DNA]
    __dna: DNA
    __key: str

    def __init__(self, alphabet: Dict[str, DNA], key: str = ""):
        """ Creates a random gene from a DNA alphabet.  """
        self.__alphabet = alphabet
        self.__key = key if key else random.choice(list(alphabet.keys()))
        try:
            self.__dna = alphabet[self.__key]
        except KeyError:
            raise DNAException(f"{self.__key} is not part of the alphabet {alphabet}")

    def copy(self) -> 'GenericGene[DNA]':
        """ Returns a copy of this gene.    """
        return GenericGene(self.__alphabet, self.__key)

    def copy_to(self, other: 'GenericGene[DNA]') -> None:
        """ Copies the DNA of this gene into another.   """
        other.__dna = self.__dna
        other.__key = self.__key
        other.__alphabet = self.__alphabet
