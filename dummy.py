def not_implemented():
    raise NotImplementedError()


def value_error(val):
    if val < 0:
        raise ValueError("Value can't be negative")
