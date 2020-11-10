"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
from copy import copy
from inspect import getmembers, signature
from types import FunctionType
from typing import Callable, List

from genyal.engine import GenyalEngine
from genyal.genotype import GeneFactory

import dummy


class Tracer:
    """
    The job of Tracer is to generate sequences of instructions to replicate a desired stack trace.
    """
    __statements: List[Callable]
    __target_exception: Exception

    def __init__(self, module, target):
        self.__statements = [fun[1] for fun in
                             filter(lambda m: isinstance(m[1], FunctionType), getmembers(module))]
        self.__target_exception = target
        self.__statement_factory = GeneFactory(self)
        self.__statement_factory.generator = Tracer.instruction_generator
        self.__statement_factory.generator_args = (random.Random(), self.__statements)
        self.__engine = GenyalEngine(fitness_function=Tracer.fitness_function,
                                     terminating_function=Tracer.run_until)
        self.__engine.fitness_function_args = (self.__target_exception,)

    @staticmethod
    def fitness_function(statements: List[Callable], target_exception: Exception) -> float:
        try:
            for statement in statements:
                statement()
        except Exception as e:
            return 1 if type(e) == target_exception else 0
        return 0

    @staticmethod
    def instruction_generator(random_generator: random.Random,
                              statements: list[tuple[Callable, tuple]]) -> tuple[Callable, tuple]:
        return random_generator.choice(statements)

    @staticmethod
    def run_until(engine: GenyalEngine) -> bool:
        return engine.fittest.fitness == 1

    def __minimize(self):
        """
        Reduces the fittest sequence of instructions to the shortest one that raises the exception.
        """
        fittest = self.__engine.fittest
        minimal_test = fittest.genes
        for instruction in fittest.genes:
            candidate = copy(minimal_test)
            candidate.remove(instruction)
            if Tracer.fitness_function(candidate, self.__target_exception) >= fittest.fitness:
                minimal_test = candidate
        return minimal_test

    def run(self) -> None:
        self.__engine.create_population(50, 3, self.__statement_factory)
        self.__engine.evolve()
        print(self.__minimize())


if __name__ == '__main__':
    Tracer(dummy, ValueError).run()
