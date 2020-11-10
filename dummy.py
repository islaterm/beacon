a = 0


def not_implemented():
    raise NotImplementedError()


def value_error():
    if a > 1:
        raise ValueError()


def other_error():
    global a
    a += 1
