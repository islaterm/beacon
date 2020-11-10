import sys
import traceback
from random import random


def not_implemented():
    raise NotImplementedError()


def value_error():
    raise ValueError()


def value_error_2():
    if random() > 0.5:
        raise ValueError()
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    value_error()
