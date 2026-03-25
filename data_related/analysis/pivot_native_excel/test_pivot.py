# %%
from pathlib import Path

import pandas as pd
from pivot import create_native_excel_pivot

# %%
# remove old artifact if exists
artifact_path = Path("test_artifacts") / "pivot_single_complex.xlsx"
if artifact_path.exists():
    artifact_path.unlink()

# %%
df = pd.DataFrame(
    {
        "Region": ["North", "North", "South", "South", "East", "East"],
        "Country": ["US", "CA", "US", "MX", "JP", "KR"],
        "Product": ["A", "B", "A", "B", "A", "B"],
        "Quarter": ["Q1", "Q1", "Q2", "Q2", "Q1", "Q2"],
        "Channel": ["Retail", "Online", "Retail", "Online", "Retail", "Online"],
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

create_native_excel_pivot(
    df=df,
    output_file=artifact_path,
    row_field=["Date"],
    col_field=["Product"],
    value_field=["Sales", "Quantity"],
    filter_fields=[
        "Channel",
        "Region",
        "Country",
        "Quarter",
    ],
)
