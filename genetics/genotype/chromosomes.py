"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import sys
from copy import copy
from random import Random
from typing import Any, Dict, Generic, List, Optional, Tuple

from genetics.genotype.genes import DNA, GenericGene
from genetics.utils import create_offsprings


class GenotypeException(Exception):
    def __init__(self, msg: str):
        super(GenotypeException, self).__init__(msg)


class GenericChromosome(Generic[DNA]):
    """ A chromosome is represented as a list of genes. """
    __alphabet: Dict[Any, DNA]
    __genotype: List[GenericGene[DNA]]
    __rng: Random
    __size: int

    def __init__(self, size: int, alphabet: Dict[Any, DNA], rng: Random = Random(),
                 genes: Optional[List[GenericGene[DNA]]] = None) -> None:
        """
        Creates a new chromosome with genes of type ``DNA``.

        Args:
            size:
                the length of the chromosome.
            alphabet:
                the domain of the genes.
            rng:
                a random number generator.
            genes:
                the list of genes of the chromosome (to create a new chromosome from an existing
                one).
        """
        self.__alphabet = alphabet
        self.__rng = rng
        self.__size = size
        self.__genotype = genes if genes else [GenericGene(alphabet, rng=rng) for _ in
                                               range(0, size)]
        if len(self.__genotype) != self.__size:
            raise GenotypeException("Chromosome size doesn't match the number of genes.\n"
                                    f"Expected: {size}\n"
                                    f"Actual: {len(self.__genotype)}")

    def mutate(self, mutation_rate: float) -> None:
        """Mutates the chromosome according to it's mutation rate."""
        for gene_idx in range(0, self.__size):
            if self.__rng.random() < mutation_rate:
                self.__genotype[gene_idx] = GenericGene(self.__alphabet)

    def crossover(self, other: 'GenericChromosome') \
            -> Tuple['GenericChromosome', 'GenericChromosome']:
        """
        Performs a crossover with another chromosome.

        Args:
            other: the chromosome to be used for crossover.
        Returns:
            A pair with the offsprings generated in the crossover.
        """
        return create_offsprings(self, other)

    # region : Utility

    def __copy__(self):
        genes_copy = [copy(gene) for gene in self.__genotype]
        return GenericChromosome(self.__size, self.__alphabet, genes=genes_copy)

    def __eq__(self, other) -> bool:
        return isinstance(other,
                          GenericChromosome) and other.__alphabet == self.__alphabet and \
               other.__genotype == self.__genotype

    def __len__(self):
        return self.__size

    def __setitem__(self, index: int, value: GenericGene[DNA]) -> None:
        self.__genotype[index] = copy(value)

    def __str__(self):
        return str(self.__genotype)

    def __getitem__(self, item: int) -> GenericGene:
        return self.__genotype[item]

    # endregion

    # region : properties
    @property
    def genes(self) -> List[GenericGene]:
        return copy(self.__genotype)

    # endregion


class ChromosomeFactory(Generic[DNA]):
    """A factory to ease the creation of chromosomes."""

    def __init__(self, alphabet: Dict[Any, DNA], max_size: Optional[int]):
        """
        Initializes a new factory.

        Args:
            alphabet:
                the alphabet from which the chromosome genes are going to be created.
            max_size:
                the maximum length of the chromosome.
        """
        self.__alphabet = alphabet
        self.__max_size = max_size if max_size > 0 else sys.maxsize

    def make(self) -> GenericChromosome[DNA]:
        """Returns a new chromosome."""
        return GenericChromosome(self.__max_size, self.__alphabet)
