import xlwings as xw
from xlwings import func


@func
def hello(name):
    return f"Hello {name}!"
