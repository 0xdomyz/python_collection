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


class TestNativeExcelPivotSlicers(unittest.TestCase):
    def test_slicer_fields_enable_multi_select(self):
        """slicer_fields enables multi-page (multi-select) filtering on pivot fields.

        Visual slicer UI cannot be created via COM automation; this fallback enables
        interactive multi-select filtering through pivot field dropdown menus.
        See SLICER_LIMITATION.md for full details.
        """
        df = pd.DataFrame(
            {
                "Region": ["North", "South", "East", "West", "North", "East"],
                "Product": ["A", "A", "B", "B", "B", "A"],
                "Channel": ["Retail", "Online", "Retail", "Online", "Retail", "Online"],
                "Date": [
                    "2025-01-01",
                    "2025-01-15",
                    "2025-02-01",
                    "2025-02-15",
                    "2025-03-01",
                    "2025-03-15",
                ],
                "Sales": [100, 120, 130, 140, 150, 160],
            }
        )

        output_file = ARTIFACT_DIR / "pivot_slicer_multiselect.xlsx"

        pivot_module.create_native_excel_pivot(
            df=df,
            output_file=output_file,
            row_field="Date",
            col_field="Product",
            value_field="Sales",
            slicer_fields=[
                "Channel",
                "Date",
                "Region",
            ],
        )

        self.assertTrue(output_file.exists())

        excel = win32.Dispatch("Excel.Application")
        excel.Visible = False
        excel.DisplayAlerts = False
        workbook = None
        try:
            workbook = excel.Workbooks.Open(str(output_file))
            pivot_table = workbook.Worksheets("Pivot").PivotTables("PivotTable1")

            # Verify multi-select is enabled for all slicer fields (Channel + Date + Region)
            for field_name in ["Channel", "Date", "Region"]:
                self.assertTrue(
                    pivot_table.PivotFields(field_name).EnableMultiplePageItems,
                    f"Multi-select not enabled for slicer field: {field_name}",
                )
        finally:
            if workbook is not None:
                workbook.Close(SaveChanges=False)
            excel.Quit()


if __name__ == "__main__":
    unittest.main(verbosity=2)
