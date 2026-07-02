import xlwings as xw
from xlwings import func


def test_func():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    if sheet["A1"].value == "Hello 2 xlwings!":
        sheet["A1"].value = "Bye 2 xlwings!"
    else:
        sheet["A1"].value = "Hello 2 xlwings!"

