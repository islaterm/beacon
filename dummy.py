import sys
import traceback
from traceback import StackSummary


def foo(i=0):
    a = [1, 2, 3]
    return a[i]


def foo2():
    foo(3)


if __name__ == '__main__':
    try:
        foo2()
    except:
        stack = sys.exc_info()
        trace = traceback.extract_tb(sys.exc_info()[-1])
        print(trace)
