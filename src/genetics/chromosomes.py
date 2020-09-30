"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from random import Random
from typing import Any, Dict, Generic, List

from genetics.genes import DNA, GenericGene


class GenericChromosome(Generic[DNA]):
    """ A chromosome is represented as a list of genes. """
    __genes: List[GenericGene[DNA]]
    __rng: Random
    __size: int
    __alphabet: Dict[Any, DNA]

    def __init__(self, size: int, alphabet: Dict[Any, DNA], rng: Random = Random()):
        """
        Creates a new chromosome from a list of genes generated from an alphabet.
        """
        self.__genes = []
        self.__rng = rng
        self.__size = size
        self.__alphabet = alphabet
        for _ in range(0, size):
            self.__genes.append(GenericGene(alphabet))

    def mutate(self, mutation_rate: float):
        for gene_idx in range(0, self.__size):
            if self.__rng.random() < mutation_rate:
                self.__genes[gene_idx] = GenericGene(self.__alphabet)

    # region : Utility
    def __setitem__(self, index: int, value: GenericGene[DNA]):
        self.__genes[index] = value.copy()
    # endregion
