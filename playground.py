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
    return matches


binary_alphabet = { True: 1, False: 0 }
individual_factory = IndividualFactory(0.3, fitness_function,
                                       [ChromosomeFactory(binary_alphabet, 10)])

population = Population(5, individual_factory)
if __name__ == '__main__':
    print(target)
    for _ in range(0, 16):
        population.evolve()
        print(
            f"{str(population.get_fittest(1)[0])}\n\tfitness: "
            f"{population.get_fittest(1)[0].fitness}")
    pprint([f"{str(individual)} fitness: {individual.fitness}" for individual in
            population.get_fittest(3)])
