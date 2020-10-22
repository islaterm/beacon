from pprint import pprint

from genetics.genotype.chromosomes import ChromosomeFactory
from genetics.individuals import Individual, IndividualFactory
from genetics.population import Population

target = [1, 0, 1, 1, 0]


def fitness_function(individual: Individual):
    """"""
    chromosome = individual.genotype[0]
    matches = 0
    for i in range(0, min(len(chromosome), len(target))):
        if chromosome.genes[i].dna == target[i]:
            matches += 1
    return matches / (abs(len(chromosome) - len(target)) + 1)


binary_alphabet = { True: 1, False: 0 }
individual_factory = IndividualFactory(0.3, fitness_function,
                                       [ChromosomeFactory(binary_alphabet, 10)])

population = Population(16, individual_factory)
if __name__ == '__main__':
    print(target)
    while population.get_fittest(1)[0].fitness < 5:
        population.evolve()
        fittest = population.get_fittest(1)[0]
        if fitness_function(fittest) != fittest.fitness:
            print(f"Expected: {fitness_function(fittest)}")
            print(f"Actual: {fittest.fitness}")
    pprint(f"{str(population.get_fittest(3))}")
