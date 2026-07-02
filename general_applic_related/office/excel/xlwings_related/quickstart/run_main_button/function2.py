import numpy as np
import xlwings as xw


def main():
    wb = xw.Book.caller()
    sheet = wb.sheets[0]
    in1 = sheet["A1"].value
    res1 = np.log(in1+1)
    sheet['B1'].value = res1
