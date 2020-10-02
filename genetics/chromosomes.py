"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from copy import copy
from random import Random
from typing import Any, Dict, Generic, List, Optional

from genetics.genes import DNA, GenericGene


class GenotypeException(Exception):
    def __init__(self, msg: str):
        super(GenotypeException, self).__init__(msg)


class GenericChromosome(Generic[DNA]):
    """ A chromosome is represented as a list of genes. """
    __alphabet: Dict[Any, DNA]
    __genes: List[GenericGene[DNA]]
    __rng: Random
    __size: int

    def __init__(self, size: int, alphabet: Dict[Any, DNA], rng: Random = Random(),
                 genes: Optional[List[GenericGene[DNA]]] = None) -> None:
        """
        Creates a new chromosome from a list of genes generated from an alphabet.
        """
        self.__alphabet = alphabet
        self.__rng = rng
        self.__size = size
        self.__genes = genes if genes else [GenericGene(alphabet) for _ in range(0, size)]
        if len(self.__genes) != self.__size:
            raise GenotypeException("Chromosome size doesn't match the number of genes.\n"
                                    f"Expected: {size}\n"
                                    f"Actual: {len(self.__genes)}")

    def mutate(self, mutation_rate: float) -> None:
        for gene_idx in range(0, self.__size):
            if self.__rng.random() < mutation_rate:
                self.__genes[gene_idx] = GenericGene(self.__alphabet)

    # region : Utility

    def __copy__(self):
        genes_copy = [copy(gene) for gene in self.__genes]
        return GenericChromosome(self.__size, self.__alphabet, genes=genes_copy)

    def __len__(self):
        return self.__size

    def __setitem__(self, index: int, value: GenericGene[DNA]) -> None:
        self.__genes[index] = copy(value)

    def __str__(self):
        return str(self.__genes)
    # endregion
