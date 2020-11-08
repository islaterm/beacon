"""
"Beacon" (c) by Ignacio Slater M.
"Beacon" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import random
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
    __target_exception: Exception

    def __init__(self, module, target):
        self.__statements = [fun[1] for fun in
                             filter(lambda m: isinstance(m[1], FunctionType), getmembers(module))]
        self.__target_exception = target

    def __fitness_function(self) -> float:
        try:
            for statement in self.__statements:
                statement()
        except Exception as e:
            return 1 if isinstance(e, self.__target_exception.__class__) else 0
        return 0

    def __instruction_generator(self) -> Callable:
        return random.choice(self.__statements)

    def run(self) -> None:
        statement_factory = GeneFactory(self)
        statement_factory.generator = self.__instruction_generator
        engine = GenyalEngine(fitness_function=self.__fitness_function)
        engine.create_population(10, 3, statement_factory)
        engine.evolve()
        print(engine.fittest)


if __name__ == '__main__':
    Tracer(dummy, NotImplementedError).run()
