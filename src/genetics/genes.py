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


class Gene(Generic[DNA]):
    """ A gene is the more basic unit of a genotype.    """
    __alphabet: Dict[str, DNA]
    __dna: DNA
    __key: str

    def __init__(self, alphabet: Dict[str, DNA], key: str = ""):
        """ Creates a random gene from a DNA alphabet.  """
        self.__alphabet = alphabet
        self.__key = key if key else random.choice(list(alphabet.keys()))
        self.__dna = alphabet[self.__key]

    def copy(self) -> 'Gene[DNA]':
        """ Returns a copy of this gene.    """
        return Gene(self.__alphabet, self.__key)


class Chromosome:
    """ A chromosome made from a sequence of objects.   """

    def __init__(self, alphabet: Dict[str, DNA]):
        pass
