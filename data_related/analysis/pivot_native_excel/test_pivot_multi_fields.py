import sys
import time
import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pandas as pd
import win32com.client as win32

MODULE_PATH = Path(__file__).resolve().parent / "pivot.py"
SPEC = spec_from_file_location("pivot_module", MODULE_PATH)
pivot_module = module_from_spec(SPEC)
SPEC.loader.exec_module(pivot_module)

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.insert(0, str(CURRENT_DIR))

from process_isolation import run_in_isolated_process

ARTIFACT_DIR = Path(__file__).resolve().parent / "test_artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


def _run_multi_fields_scenario(output_file):
    df_multi = pd.DataFrame(
        {
            "Region": ["North", "North", "South", "South", "East", "East"],
            "Country": ["US", "CA", "US", "MX", "JP", "KR"],
            "Product": ["A", "B", "A", "B", "A", "B"],
            "Quarter": ["Q1", "Q1", "Q2", "Q2", "Q1", "Q2"],
            "Date": [
                "2025-01-01",
                "2025-01-15",
                "2025-02-01",
                "2025-02-15",
                "2025-03-01",
                "2025-03-15",
            ],
            "Sales": [120, 180, 150, 140, 170, 160],
            "Quantity": [12, 18, 15, 14, 17, 16],
        }
    )

    pivot_module.create_native_excel_pivot(
        df=df_multi,
        output_file=output_file,
        row_field=["Region", "Country"],
        col_field=["Product", "Quarter"],
        value_field=["Sales", "Quantity"],
        filter_fields=["Date"],
    )

    excel = None
    workbook = None
    pivot_table = None
    try:
        excel = win32.DispatchEx("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        workbook = excel.Workbooks.Open(str(output_file))
        pivot_table = workbook.Worksheets("Pivot").PivotTables("PivotTable1")

        if pivot_table.PivotFields("Region").Orientation != 1:
            raise AssertionError("Region field is not set as row field")
        if pivot_table.PivotFields("Country").Orientation != 1:
            raise AssertionError("Country field is not set as row field")
        if pivot_table.PivotFields("Product").Orientation != 2:
            raise AssertionError("Product field is not set as column field")
        if pivot_table.PivotFields("Quarter").Orientation != 2:
            raise AssertionError("Quarter field is not set as column field")
        if pivot_table.DataFields.Count < 2:
            raise AssertionError("Expected at least two data fields in pivot")
        if pivot_table.PivotFields("Date").Orientation != 3:
            raise AssertionError("Date field is not set as page filter")
    finally:
        pivot_table = None
        if workbook is not None:
            try:
                workbook.Close(SaveChanges=False)
            except Exception:
                pass
        workbook = None
        if excel is not None:
            try:
                excel.Quit()
            except Exception:
                pass
        excel = None
        time.sleep(0.5)


class TestNativeExcelPivotMultiFields(unittest.TestCase):
    def test_native_pivot_with_multiple_fields(self):
        output_file = ARTIFACT_DIR / "pivot_multi_fields.xlsx"

        ok, message = run_in_isolated_process(
            _run_multi_fields_scenario,
            str(output_file),
            timeout=120,
            attempts=3,
        )
        self.assertTrue(ok, message)

        self.assertTrue(output_file.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
