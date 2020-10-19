"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from copy import copy
from typing import Callable, List, Tuple

from genetics.genotype.chromosomes import ChromosomeFactory, GenericChromosome
from genetics.utils import create_offsprings

FitnessFunction = Callable[['Individual'], float]


class Individual:
    __fitness: float
    __fitness_function: FitnessFunction
    __genotype: List[GenericChromosome]
    __mutation_rate: float

    def __init__(self, chromosomes: List[GenericChromosome], mutation_rate: float,
                 fitness_function: FitnessFunction) -> None:
        self.__genotype = chromosomes
        self.__fitness_function = fitness_function
        self.__mutation_rate = mutation_rate
        self.__update_fitness()

    def crossover(self, other: 'Individual') -> Tuple['Individual', 'Individual']:
        """
        Performs a random k-point crossover with another individual.

        Returns:
            a pair with the new individuals.
        """
        return create_offsprings(self, other)

    def mutate(self) -> None:
        """
        Mutates this individual according to its mutation rate.
        """
        for chromosome in self.__genotype:
            chromosome.mutate(self.__mutation_rate)
        self.__update_fitness()

    def __update_fitness(self) -> None:
        self.__fitness = self.__fitness_function(self)

    @property
    def fitness(self) -> float:
        return self.__fitness

    @property
    def genotype(self) -> List[GenericChromosome]:
        return copy(self.__genotype)

    # region : Built-ins
    def __len__(self) -> int:
        return len(self.__genotype)

    def __lt__(self, other: 'Individual') -> bool:
        """Compares this individual with another according to their fitness."""
        return self.__fitness < other.__fitness

    def __copy__(self) -> 'Individual':
        return Individual(self.__genotype, self.__mutation_rate, self.__fitness_function)

    def __setitem__(self, index: int, value: GenericChromosome) -> None:
        self.__genotype[index] = value

    def __str__(self) -> str:
        return str([str(chromosome) for chromosome in self.__genotype])
    # endregion


class IndividualFactory:
    """A factory to ease the creation of new individuals."""
    __factories: List[ChromosomeFactory]
    __fitness_function: FitnessFunction
    __mutation_rate: float

    def __init__(self, mutation_rate: float, fitness_function: FitnessFunction,
                 chromosome_factories: List[ChromosomeFactory]):
        """
        Initializes a new factory.

        Args:
            mutation_rate:
                the probability to mutate the chromosomes of the individual.
            fitness_function:
                the function to be optimized.
            chromosome_factories:
                a list of factories to create the chromosomes of the individual.
        """
        self.__factories = chromosome_factories
        self.__fitness_function = fitness_function
        self.__mutation_rate = mutation_rate

    def make(self) -> Individual:
        """Creates a new individual."""
        genotype = [factory.make() for factory in self.__factories]
        return Individual(genotype, self.__mutation_rate, self.__fitness_function)
