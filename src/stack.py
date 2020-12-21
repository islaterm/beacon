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
from inspect import getmembers, signature
from pprint import pprint
from types import FunctionType
from typing import Any, Callable, List, Type, Union

from genyal.engine import GenyalEngine
from genyal.genotype import GeneFactory

from src.beacons import InputFactory, Variable

Instruction = Union[tuple[Callable, str, dict[str, Any]], Callable]


# noinspection PyBroadException
class Tracer:
    """
    The job of Tracer is to generate sequences of instructions to replicate a desired stack trace.
    """
    __fn_name: str
    __engine: GenyalEngine
    __exc_msg: str
    __in_factory: InputFactory
    __statement_factory: GeneFactory
    __statements: list[Instruction]
    __target_exception: Type[Exception]

    def __init__(self, module_name: str, target: Type[Exception], target_msg: str = "",
                 fn_name: str = ""):
        """
        Tracer gets all functions from a Python module and generates the sequence of instructions
        that will lead to a minimal crash reproduction given a desired exception type.

        Args:
            module_name:
                the name of the module in which Tracer is going to look for functions.
            target:
                the desired exception's type.
            target_msg:
                (Optional) a string that should be contained in the raised exception's arguments;
                defaults to blank.
            fn_name:
                (Optional) a function that should be present on the runtime stack of the crash;
                defaults to blank.
        """
        module = import_module(module_name)
        self.__in_factory = InputFactory()
        self.__statements = []
        for fun in filter(lambda m: isinstance(m[1], FunctionType), getmembers(module)):
            self.__statements.append((fun[1], fun[0], { }))
        self.__target_exception = target
        self.__exc_msg = target_msg
        self.__fn_name = fn_name
        self.__statement_factory = GeneFactory(self)
        self.__statement_factory.generator = self.instruction_generator
        self.__statement_factory.generator_args = (random.Random(), self.__statements)
        self.__engine = GenyalEngine(fitness_function=Tracer.fitness_function,
                                     terminating_function=Tracer.run_until)
        self.__engine.fitness_function_args = (
            self.__target_exception, self.__exc_msg, self.__fn_name)

    @staticmethod
    def fitness_function(statements: List[Instruction], target_exception: Type[Exception],
                         target_message: str, target_fn: str) -> float:
        fitness = 0
        try:
            Tracer.execute(statements)
        except target_exception as e:
            exc_info = sys.exc_info()
            stack = traceback.extract_tb(exc_info[2])
            fitness += 2
            if not target_message:
                fitness += 1
            else:
                for arg in e.args:
                    fitness += 1 if target_message in arg else 0
        except Exception:
            exc_info = sys.exc_info()
            stack = traceback.extract_tb(exc_info[2])
        else:
            return 0
        fitness += 2 if not target_fn or list(
            filter(lambda frame: frame.name == target_fn, stack)) else 0
        return fitness

    def instruction_generator(self, random_generator: random.Random,
                              statements: list[Instruction]) -> Instruction:
        instruction = random_generator.choice(statements)
        fn_params = { }
        for param in signature(instruction[0]).parameters:
            fn_params[param] = self.__in_factory.get()
        return instruction[0], instruction[1], fn_params

    @staticmethod
    def run_until(engine: GenyalEngine) -> bool:
        return engine.fittest.fitness == 5

    def __minimize(self):
        """
        Reduces the fittest sequence of instructions to the shortest one which raises the exception.
        """
        fittest = self.__engine.fittest
        minimal_test = fittest.genes
        for instruction in fittest.genes:
            candidate = copy(minimal_test)
            candidate.remove(instruction)
            if Tracer.fitness_function(candidate, self.__target_exception,
                                       self.__exc_msg, self.__fn_name) >= fittest.fitness:
                minimal_test = candidate
        return minimal_test

    def run(self) -> None:
        self.__engine.create_population(50, 5, self.__statement_factory)
        self.__engine.evolve()
        instructions = self.__minimize()
        try:
            Tracer.execute(instructions)
        except Exception:
            exc_info = sys.exc_info()
            print(exc_info[0])
            print(f"{exc_info[1]} occurred at functions:")
            for i in instructions:
                d: dict = i[2]
                args = [f"{arg[0]} = {arg[1]}" for arg in d.items()]
                print(f"\t{i[1]}({', '.join(args)})")
            pprint(traceback.extract_tb(exc_info[2]))

    @staticmethod
    def execute(statements):
        results = []
        for statement in statements:
            parameters = copy(statement[2])
            j = len(results)
            for key, val in parameters.items():
                if val == Variable:
                    j -= 1
                    parameters[key] = results[j]
            results.append(statement[0](**parameters))


if __name__ == '__main__':
    tracer = Tracer("dummy", AssertionError)
    tracer.run()
