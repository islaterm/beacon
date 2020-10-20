from random import randrange
from typing import List

from genetics.individuals import Individual, IndividualFactory


class PopulationError(Exception):
    """Error raised when an operation on the population is invalid."""

    def __init__(self, cause: str):
        super(PopulationError, self).__init__(cause)


class Population:
    """A population is a set of individuals that can evolve over time."""
    __individuals: List[Individual]

    def __init__(self, size: int, individual_factory: IndividualFactory):
        """Creates a population of a given size using a factory to create the individuals."""
        if size < 2:
            raise PopulationError(
                f"Invalid size {size}. The population must have at least 2 individuals")
        self.__individuals = [individual_factory.make() for _ in range(0, size)]
        self.__individuals.sort()

    def evolve(self) -> None:
        """Evolves the population to the next generation."""
        pop_size = self.__len__()
        offsprings = []
        survivors = pop_size / 4
        i = 0
        while len(offsprings) < pop_size:
            if i < pop_size - survivors - 1:
                # Crossover
                parents = (tournament_selection(self), tournament_selection(self))
                it_offsprings = parents[0].crossover(parents[1])
                # Mutation
                it_offsprings[0].mutate()
                offsprings.append(it_offsprings[0])
                it_offsprings[1].mutate()
                offsprings.append(it_offsprings[1])
                i += 2
            else:
                # The individual survived :D
                offsprings.append(self.__individuals[i])
                i += 1
        # Assigns the new generation
        self.__individuals = offsprings
        self.__individuals.sort()

    def get_fittest(self, n: int) -> List[Individual]:
        """Gets the n fittest individuals of the population."""
        return self.__individuals[-n:]

    def __len__(self) -> int:
        """The size of the population."""
        return len(self.__individuals)

    @property
    def individuals(self) -> List[Individual]:
        """The individuals of the population."""
        return self.__individuals


def tournament_selection(population: Population) -> Individual:
    """
    Selects the fittest individual from 2 candidates.
    Individuals of a population are sorted in such a way that the elements with greater index have a
    higher fitness.
    """
    winner = max(randrange(0, len(population)), randrange(0, len(population)))
    return population.individuals[winner]
