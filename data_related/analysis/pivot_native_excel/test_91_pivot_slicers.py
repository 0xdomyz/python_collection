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


class TestNativeExcelPivotSlicers(unittest.TestCase):
    def test_native_pivot_with_single_slicer_field(self):
        """Test that slicer_fields parameter enables multi-page filtering on pivot.

        Note: The slicer feature enables interactive filtering through enable multi-page
        items on pivot fields, allowing users to filter via dropdown menus in Excel.
        """
        df_slicer = pd.DataFrame(
            {
                "Region": ["North", "South", "East", "West", "North", "East"],
                "Product": ["A", "A", "B", "B", "B", "A"],
                "Channel": ["Retail", "Online", "Retail", "Online", "Retail", "Online"],
                "Sales": [100, 120, 130, 140, 150, 160],
            }
        )

        output_file = ARTIFACT_DIR / "pivot_with_single_slicer_field.xlsx"

        pivot_module.create_native_excel_pivot(
            df=df_slicer,
            output_file=output_file,
            row_field="Region",
            col_field="Product",
            value_field="Sales",
            slicer_fields=["Channel"],
        )

        self.assertTrue(output_file.exists())

        excel = win32.gencache.EnsureDispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        workbook = None
        try:
            workbook = excel.Workbooks.Open(str(output_file))
            ws_pivot = workbook.Worksheets("Pivot")
            pivot_table = ws_pivot.PivotTables("PivotTable1")

            # Verify multi-page filtering is enabled for the slicer field
            channel_field = pivot_table.PivotFields("Channel")
            self.assertTrue(
                channel_field.EnableMultiplePageItems,
                "Multi-page filtering should be enabled on slicer field",
            )

        finally:
            if workbook is not None:
                workbook.Close(SaveChanges=False)
            excel.Quit()

    def test_native_pivot_with_multiple_slicer_fields(self):
        """Test that multiple slicer_fields all have multi-page filtering enabled."""
        df_multi_slicer = pd.DataFrame(
            {
                "Region": ["North", "North", "South", "South", "East", "East"],
                "Product": ["A", "B", "A", "B", "A", "B"],
                "Channel": ["Retail", "Retail", "Online", "Online", "Retail", "Online"],
                "Year": [2025, 2025, 2025, 2026, 2026, 2026],
                "Sales": [100, 120, 130, 140, 150, 160],
            }
        )

        output_file = ARTIFACT_DIR / "pivot_with_multiple_slicer_fields.xlsx"

        pivot_module.create_native_excel_pivot(
            df=df_multi_slicer,
            output_file=output_file,
            row_field="Region",
            col_field="Product",
            value_field="Sales",
            slicer_fields=["Channel", "Year"],
        )

        self.assertTrue(output_file.exists())

        excel = win32.gencache.EnsureDispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        workbook = None
        try:
            workbook = excel.Workbooks.Open(str(output_file))
            ws_pivot = workbook.Worksheets("Pivot")
            pivot_table = ws_pivot.PivotTables("PivotTable1")

            # Verify multi-page filtering is enabled for all slicer fields
            for field_name in ["Channel", "Year"]:
                field = pivot_table.PivotFields(field_name)
                self.assertTrue(
                    field.EnableMultiplePageItems,
                    f"Multi-page filtering not enabled for {field_name}",
                )

        finally:
            if workbook is not None:
                workbook.Close(SaveChanges=False)
            excel.Quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
