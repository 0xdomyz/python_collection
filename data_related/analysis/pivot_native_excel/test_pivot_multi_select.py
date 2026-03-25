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


def _run_slicer_multi_select_scenario(output_file):
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

    pivot_module.create_native_excel_pivot(
        df=df,
        output_file=output_file,
        row_field="Date",
        col_field="Product",
        value_field="Sales",
        slicer_fields=["Channel", "Date", "Region"],
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

        for field_name in ["Channel", "Date", "Region"]:
            if not pivot_table.PivotFields(field_name).EnableMultiplePageItems:
                raise AssertionError(
                    f"Multi-select not enabled for slicer field: {field_name}"
                )
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


class TestNativeExcelPivotSlicers(unittest.TestCase):
    def test_slicer_fields_enable_multi_select(self):
        """slicer_fields enables multi-page (multi-select) filtering on pivot fields.

        Visual slicer UI cannot be created via COM automation; this fallback enables
        interactive multi-select filtering through pivot field dropdown menus.
        See SLICER_LIMITATION.md for full details.
        """
        output_file = ARTIFACT_DIR / "pivot_slicer_multiselect.xlsx"

        ok, message = run_in_isolated_process(
            _run_slicer_multi_select_scenario,
            str(output_file),
            timeout=120,
            attempts=3,
        )
        self.assertTrue(ok, message)

        self.assertTrue(output_file.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
