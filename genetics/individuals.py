"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
from typing import Callable, List, Tuple

from genetics.chromosomes import GenericChromosome


class Individual:
    __fitness: float
    __fitness_function: Callable[['Individual'], float]
    __genotype: List[GenericChromosome]
    __mutation_rate: float

    def __init__(self, chromosomes: List[GenericChromosome], mutation_rate: float,
                 fitness_function: Callable[['Individual'], float]) -> None:
        self.__genotype = chromosomes
        self.__fitness_function = fitness_function
        self.__mutation_rate = mutation_rate
        self.__fitness = self.__update_fitness()

    def crossover(self, other: 'Individual', cut_points: List[int]) \
            -> Tuple['Individual', 'Individual']:
        """
        Performs a k-point crossover with another individual.

        Args:
            other:
                the individual used for the crossover
            cut_points:
                the points to do the crossover
        Returns:

        """
        cut_points.sort()
        offspring_1 = []
        offspring_2 = []
        i = 0
        start = 0
        while i < len(cut_points):
            end = cut_points[i]
            for chromosome_idx in range(start, end):
                new_chromosomes = self.__genotype[chromosome_idx].crossover(
                    other.__genotype[chromosome_idx])
                offspring_1.append(new_chromosomes[0])
                offspring_2.append(new_chromosomes[1])
            i += 1
        return self.__init__(offspring_1, self.__mutation_rate,
                             self.__fitness_function), self.__init__(offspring_2,
                                                                     self.__mutation_rate,
                                                                     self.__fitness_function)

    def __update_fitness(self) -> float:
        pass

    def __len__(self) -> int:
        return len(self.__genotype)
