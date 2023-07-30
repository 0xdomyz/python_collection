def divide(x, y):
    try:
        return x / y
    except ZeroDivisionError as e:
        raise ValueError("Invalid arguments") from e

divide(1, 0)
