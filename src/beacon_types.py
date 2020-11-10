import random
import sys


class Integer:
    @staticmethod
    def make(lo: int = -sys.maxsize, hi: int = sys.maxsize) -> int:
        return random.randrange(lo, hi)


arg_types = { int: Integer }
