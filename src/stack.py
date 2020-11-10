"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
import sys
import traceback
from inspect import getmembers
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
    __target_method: Exception

    def __init__(self, module, target):
        self.__statements = [fun[1] for fun in
                             filter(lambda m: isinstance(m[1], FunctionType), getmembers(module))]
        self.__target_method = target
        self.__statement_factory = GeneFactory(self)
        self.__statement_factory.generator = Tracer.instruction_generator
        self.__statement_factory.generator_args = (random.Random(), self.__statements)
        self.__engine = GenyalEngine(fitness_function=Tracer.fitness_function,
                                     terminating_function=Tracer.run_until)
        self.__engine.fitness_function_args = (self.__target_method, 10)

    @staticmethod
    def fitness_function(statements: List[Callable], method_name: str,
                         engine: GenyalEngine) -> float:
        try:
            for statement in statements:
                statement()
        except Exception as e:
            stacktrace = traceback.extract_tb(sys.exc_info()[2])
            return 1 if method_name == stacktrace[1].name else 0
        return 0

    @staticmethod
    def instruction_generator(random_generator: random.Random,
                              statements: list[tuple[Callable, tuple]]) -> tuple[Callable, tuple]:
        return random_generator.choice(statements)

    @staticmethod
    def run_until(engine: GenyalEngine) -> bool:
        return engine.fittest.fitness == 1

    def run(self) -> None:
        self.__engine.create_population(50, 3, self.__statement_factory)
        self.__engine.evolve()
        print(self.__engine.fittest.genes)


if __name__ == '__main__':
    Tracer(dummy, "value_error_2").run()
