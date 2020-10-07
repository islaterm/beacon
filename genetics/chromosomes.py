"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
from copy import copy
from random import Random
from typing import Any, Dict, Generic, List, Optional, Tuple

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
        self.__genes = genes if genes else [GenericGene(alphabet, rng=rng) for _ in range(0, size)]
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

    def __eq__(self, other) -> bool:
        return isinstance(other,
                          GenericChromosome) and other.__alphabet == self.__alphabet and \
               other.__genes == self.__genes

    def __len__(self):
        return self.__size

    def __setitem__(self, index: int, value: GenericGene[DNA]) -> None:
        self.__genes[index] = copy(value)

    def __str__(self):
        return str(self.__genes)

    # endregion
    def crossover(self, other: 'GenericChromosome') \
            -> Tuple['GenericChromosome', 'GenericChromosome']:
        """
        Performs a crossover with another chromosome.

        Args:
            other: the chromosome to be used for crossover.
        Returns:
            A pair with the offsprings generated in the crossover.
        """
        max_cuts = min(self.__size, other.__size)
        number_of_cuts = random.randint(0, max_cuts)
        mixing_points = [random.randint(0, max_cuts) for _ in range(0, number_of_cuts)]
        mixing_points.sort()
        offsprings = (self.__copy__(), other.__copy__())    # FIXME: There's a bug here!
        i = 0
        start = 0
        while i < len(mixing_points):
            end = mixing_points[i]
            for gene_idx in range(start, end):
                if i % 2 == 0:
                    offsprings[0][gene_idx] = copy(other.__genes[gene_idx])
                    offsprings[1][gene_idx] = copy(self.__genes[gene_idx])
                else:
                    offsprings[0][gene_idx] = copy(self.__genes[gene_idx])
                    offsprings[1][gene_idx] = copy(other.__genes[gene_idx])
            start = end
            i += 1
        return offsprings
