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


def _run_filter_fields_scenario(output_file):
    df_filters = pd.DataFrame(
        {
            "Region": ["North", "South", "East", "West", "North", "East"],
            "Product": ["A", "A", "B", "B", "B", "A"],
            "Channel": ["Retail", "Retail", "Online", "Online", "Retail", "Online"],
            "Date": [
                "2025-01-01",
                "2025-01-15",
                "2025-02-01",
                "2025-02-15",
                "2025-03-01",
                "2025-03-15",
            ],
            "Year": [2025, 2025, 2025, 2026, 2026, 2026],
            "Sales": [100, 120, 130, 140, 150, 160],
        }
    )

    pivot_module.create_native_excel_pivot(
        df=df_filters,
        output_file=output_file,
        row_field="Region",
        col_field="Product",
        value_field="Sales",
        filter_fields=["Channel", "Year", "Date"],
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

        if pivot_table.PivotFields("Channel").Orientation != 3:
            raise AssertionError("Channel field is not set as a page filter")
        if pivot_table.PivotFields("Year").Orientation != 3:
            raise AssertionError("Year field is not set as a page filter")
        if pivot_table.PivotFields("Date").Orientation != 3:
            raise AssertionError("Date field is not set as a page filter")
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


class TestNativeExcelPivotFilters(unittest.TestCase):
    def test_native_pivot_with_filter_fields(self):
        output_file = ARTIFACT_DIR / "pivot_with_filters.xlsx"

        ok, message = run_in_isolated_process(
            _run_filter_fields_scenario,
            str(output_file),
            timeout=120,
            attempts=3,
        )
        self.assertTrue(ok, message)

        self.assertTrue(output_file.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
