from genetics.chromosomes import GenericChromosome


def not_implemented():
    raise NotImplementedError()


def value_error():
    raise ValueError()


if __name__ == '__main__':
    alphabet = {True: 1, False: 0}
    c1 = GenericChromosome(10, alphabet)
    print(f"C1: {c1}")
    c2 = GenericChromosome(8, alphabet)
    print(f"C2: {c2}")
    c3, c4 = c1.crossover(c2)
    print(f"C3: {c3}")
    print(f"C4: {c4}")
