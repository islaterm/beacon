from pprint import pprint

from genetics.genotype.chromosomes import ChromosomeFactory
from genetics.individuals import Individual, IndividualFactory
from genetics.population import Population

target = [1, 0, 1, 1, 0]


def fitness_function(individual: Individual):
    """"""
    fitness = 0
    for chromosome in individual.genotype:
        chromosome_fitness = 0
        for i in range(0, min(len(chromosome), len(target))):
            if chromosome.genes[i].dna == target[i]:
                chromosome_fitness += 1
        
        fitness += chromosome_fitness / max(len(target), len(chromosome))
    return fitness


binary_alphabet = { True: 1, False: 0 }
individual_factory = IndividualFactory(0.3, fitness_function,
                                       [ChromosomeFactory(binary_alphabet, 1)])

population = Population(100, individual_factory)
if __name__ == '__main__':
    for _ in range(0, 50):
        population.evolve()
    print(target)
    pprint([f"{str(individual)} fitness: {individual.fitness}" for individual in
            population.get_fittest(3)])
