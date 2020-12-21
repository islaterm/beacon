def foo(i=0):
    a = [1, 2, 3]
    return a[i]


def positive_sum(a, b):
    is_positive(a + b)


def is_positive(n):
    return n > 0


def error_if_true(p):
    if isinstance(p, bool) and p:
        raise AssertionError()
