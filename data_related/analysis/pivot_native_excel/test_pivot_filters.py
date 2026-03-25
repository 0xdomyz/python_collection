import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pandas as pd
import win32com.client as win32

MODULE_PATH = Path(__file__).resolve().parent / "pivot.py"
SPEC = spec_from_file_location("pivot_module", MODULE_PATH)
pivot_module = module_from_spec(SPEC)
SPEC.loader.exec_module(pivot_module)

ARTIFACT_DIR = Path(__file__).resolve().parent / "test_artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


class TestNativeExcelPivotFilters(unittest.TestCase):
    def test_native_pivot_with_filter_fields(self):
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

        output_file = ARTIFACT_DIR / "pivot_with_filters.xlsx"

        pivot_module.create_native_excel_pivot(
            df=df_filters,
            output_file=output_file,
            row_field="Region",
            col_field="Product",
            value_field="Sales",
            filter_fields=["Channel", "Year", "Date"],
        )

        self.assertTrue(output_file.exists())

        excel = win32.gencache.EnsureDispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        workbook = None
        try:
            workbook = excel.Workbooks.Open(str(output_file))
            pivot_table = workbook.Worksheets("Pivot").PivotTables("PivotTable1")

            self.assertEqual(
                pivot_table.PivotFields("Channel").Orientation,
                3,
            )
            self.assertEqual(
                pivot_table.PivotFields("Year").Orientation,
                3,
            )
            self.assertEqual(
                pivot_table.PivotFields("Date").Orientation,
                3,
            )
        finally:
            if workbook is not None:
                workbook.Close(SaveChanges=False)
            excel.Quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
