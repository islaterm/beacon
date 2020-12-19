def foo(i=0):
    a = [1, 2, 3]
    return a[i]


def positive_sum(a, b):
    is_positive(a + b)


def is_positive(n):
    assert n > 0, "n must be positive"
