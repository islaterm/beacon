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
from copy import copy
from importlib import import_module
from inspect import Signature, getmembers, signature
from pprint import pprint
from types import FunctionType
from typing import Callable, List

from genyal.engine import GenyalEngine
from genyal.genotype import GeneFactory

Instruction = tuple[Callable, str, Signature]


# noinspection PyBroadException
class Tracer:
    """
    The job of Tracer is to generate sequences of instructions to replicate a desired stack trace.
    """
    __statements: list[Instruction]
    __target_exception: Exception

    def __init__(self, module_name: str, target):
        module = import_module(module_name)
        self.__statements = []
        for fun in filter(lambda m: isinstance(m[1], FunctionType), getmembers(module)):
            self.__statements.append((fun[1], fun[0], signature(fun[1])))
        self.__target_exception = target
        self.__statement_factory = GeneFactory(self)
        self.__statement_factory.generator = self.instruction_generator
        self.__statement_factory.generator_args = (random.Random(), self.__statements)
        self.__engine = GenyalEngine(fitness_function=Tracer.fitness_function,
                                     terminating_function=Tracer.run_until)
        self.__engine.fitness_function_args = (self.__target_exception,)

    @staticmethod
    def fitness_function(statements: List[Instruction], target_exception: Exception) -> float:
        fitness = 0
        try:
            for statement in statements:
                statement[0]()
        except Exception as e:
            fitness += 1 if type(e) == target_exception else 0
        return fitness

    def instruction_generator(self, random_generator: random.Random,
                              statements: list[tuple[Callable, str, Signature]]) \
            -> tuple[Callable, str, tuple]:
        statement = random_generator.choice(statements)
        params = [self.__new_value() for _ in statement[2].parameters]
        return statement[0], statement[1], tuple(params)

    @staticmethod
    def run_until(engine: GenyalEngine) -> bool:
        return engine.fittest.fitness == 1

    def __minimize(self):
        """
        Reduces the fittest sequence of instructions to the shortest one which raises the exception.
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
        instructions = self.__minimize()
        try:
            for instruction in instructions:
                instruction[0]()
        except Exception:
            exc_info = sys.exc_info()
            print(exc_info[0])
            print(f"{exc_info[1]} occurred at functions: \n\t" + '\n\t'.join(
                [i[1] for i in instructions]))
            pprint(traceback.extract_tb(exc_info[2]))

    def add_input_type(self, in_type):
        self.__input_factory.add(in_type)

    def __new_value(self):
        return self.__input_factory.create()


if __name__ == '__main__':
    tracer = Tracer("dummy", IndexError)
    tracer.add_input_type(int)
    tracer.run()
