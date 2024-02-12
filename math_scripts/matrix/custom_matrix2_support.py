import numpy as np
import pandas as pd
from math_scripts.matrix.custom_matrix import CustomMatrix


def calculate2(left: CustomMatrix, right: CustomMatrix):
    res = left**2 - right * 2 + 2
    return res


def calculate3(left: CustomMatrix, right: CustomMatrix):
    res = left * 2 - right
    return res


import openpyxl


def to_excel_with_color_scale(data: pd.DataFrame) -> openpyxl.Workbook:
    """wb.save(f"{here}/table2.xlsx")"""
    wb = openpyxl.Workbook()
    ws = wb.active

    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            cell = ws.cell(row=i + 2, column=j + 2)
            cell.value = data.iloc[i, j]

    ws.conditional_formatting.add(
        f"B2:E{data.shape[0]+1}",
        openpyxl.formatting.rule.ColorScaleRule(
            start_type="min",
            start_color="00FF0000",
            end_type="max",
            end_color="0000FF00",
        ),
    )

    return wb
