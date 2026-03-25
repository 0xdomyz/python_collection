import unittest
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pandas as pd
import win32com.client as win32

MODULE_PATH = Path(__file__).resolve().parent / "91_pivot.py"
SPEC = spec_from_file_location("pivot_module", MODULE_PATH)
pivot_module = module_from_spec(SPEC)
SPEC.loader.exec_module(pivot_module)

ARTIFACT_DIR = Path(__file__).resolve().parent / "test_artifacts"
ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)


class TestNativeExcelPivotMultiFields(unittest.TestCase):
    def test_native_pivot_with_multiple_fields(self):
        df_multi = pd.DataFrame(
            {
                "Region": ["North", "North", "South", "South", "East", "East"],
                "Country": ["US", "CA", "US", "MX", "JP", "KR"],
                "Product": ["A", "B", "A", "B", "A", "B"],
                "Quarter": ["Q1", "Q1", "Q2", "Q2", "Q1", "Q2"],
                "Sales": [120, 180, 150, 140, 170, 160],
                "Quantity": [12, 18, 15, 14, 17, 16],
            }
        )

        output_file = ARTIFACT_DIR / "pivot_multi_fields.xlsx"

        pivot_module.create_native_excel_pivot(
            df=df_multi,
            output_file=output_file,
            row_field=["Region", "Country"],
            col_field=["Product", "Quarter"],
            value_field=["Sales", "Quantity"],
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
                pivot_table.PivotFields("Region").Orientation,
                1,
            )
            self.assertEqual(
                pivot_table.PivotFields("Country").Orientation,
                1,
            )
            self.assertEqual(
                pivot_table.PivotFields("Product").Orientation,
                2,
            )
            self.assertEqual(
                pivot_table.PivotFields("Quarter").Orientation,
                2,
            )
            self.assertGreaterEqual(pivot_table.DataFields.Count, 2)
        finally:
            if workbook is not None:
                workbook.Close(SaveChanges=False)
            excel.Quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
