# %%
from functools import partial

import pandas as pd
import seaborn as sns
import xlwings as xw

# %% [markdown]
# ### helpers

# %%
XL_FUNC = {
    "count": -4112,  # xlCount
    "sum": -4157,  # xlSum
    "average": -4106,  # xlAverage
    "max": -4136,  # xlMax
    "min": -4139,  # xlMin
}


def grid_positions(
    ncols=2, col_width=430, row_height=330, top_offset=60, left_offset=0
):
    """Infinite generator yielding (left, top) pixel positions in a grid."""
    col, row = 0, 0
    while True:
        yield left_offset + col * col_width, top_offset + row * row_height
        col += 1
        if col >= ncols:
            col, row = 0, row + 1


def pivot_dest_refs(col="Z", start_row=5, row_step=15, ncols=1, col_step=12):
    """Infinite generator yielding Excel cell refs (e.g. 'Z5') for pivot placement."""

    def col_to_idx(c: str) -> int:
        idx = 0
        for ch in c.upper():
            idx = idx * 26 + (ord(ch) - ord("A") + 1)
        return idx

    def idx_to_col(idx: int) -> str:
        result = ""
        while idx > 0:
            idx, r = divmod(idx - 1, 26)
            result = chr(r + ord("A")) + result
        return result

    base_idx = col_to_idx(col)
    row = start_row
    while True:
        for c in range(ncols):
            yield f"{idx_to_col(base_idx + c * col_step)}{row}"
        row += row_step


def make_pivot(
    pivot_cache,
    ws_pivot,
    dest,
    name,
    row_field,
    col_field="survived",
    data_field="fare",
    data_label="Count of Fare",
    xl_func=-4112,  # xlCount; pass int or XL_FUNC key string
):
    if isinstance(xl_func, str):
        xl_func = XL_FUNC[xl_func]
    pt = pivot_cache.CreatePivotTable(
        TableDestination=ws_pivot[dest].api, TableName=name
    )
    pt.PivotFields(row_field).Orientation = 1  # xlRowField
    pt.PivotFields(col_field).Orientation = 2  # xlColumnField
    pt.AddDataField(pt.PivotFields(data_field), data_label, xl_func)
    return pt


def make_chart(
    ws_pivot,
    source_ref,
    left,
    top,
    title,
    width=400,
    height=300,
    chart_type="bar_clustered",
):
    chart = ws_pivot.charts.add(left=left, top=top, width=width, height=height)
    chart.set_source_data(ws_pivot[source_ref].expand())
    chart.chart_type = chart_type
    chart_com = chart.api[1]  # (Shape, Chart) tuple on Windows
    chart_com.HasTitle = True
    chart_com.ChartTitle.Text = title
    return chart


# %%
# data
df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())

# %% [markdown]
# ### write named table

# %%
wb = xw.Book()
ws = wb.sheets[0]
ws.name = "Data"

ws["A1"].value = df
ws.tables.add(source=ws["A1"].expand(), name="titanic_table")

# %% [markdown]
# ### make pivot cache

# %%
ws_pivot = wb.sheets.add("Pivot")
pivot_cache = wb.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="titanic_table",
)

# %% [markdown]
# ### make pivot tables and charts

# %%
PIVOT_CONFIGS = [
    ("TitanicPivot", "who", "Volume by Who and Survival"),
    ("TitanicPivot2", "embark_town", "Volume by Embark Town and Survival"),
    ("TitanicPivot3", "adult_male", "Volume by Adult Male and Survival"),
    ("TitanicPivot4", "sex", "Volume by Sex and Survival"),
]

two_col_grid = partial(grid_positions, ncols=2, col_width=430, row_height=330)
two_col_dests = partial(
    pivot_dest_refs, ncols=2, col="Z", start_row=5, row_step=15, col_step=7
)

for (name, row_field, title), dest, (left, top) in zip(
    PIVOT_CONFIGS, two_col_dests(), two_col_grid()
):
    make_pivot(pivot_cache, ws_pivot, dest, name, row_field)
    make_chart(ws_pivot, dest, left=left, top=top, title=title, width=400, height=300)

# %% [markdown]
# ### refresh table data with diff sizes

# %%
# data2
df2 = df.copy()
df2["age_group"] = pd.cut(df2["age"], bins=[0, 18, 40, 80]).astype(str)
print(f"{df2.shape = }")
print(df2.head().to_string())

# %%
tbl = ws.tables["titanic_table"]
tbl.api.Unlist()
ws.clear()

ws["A1"].value = df2
ws.tables.add(source=ws["A1"].expand(), name="titanic_table")

new_cache = wb.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="titanic_table",
)
new_cache_index = wb.api.PivotCaches().count + 1

# %%
for i, (name, _, _) in enumerate(PIVOT_CONFIGS):
    pt_com = ws_pivot.api.PivotTables(name)
    if i == 0:
        pt_com.ChangePivotCache(new_cache)  # first: swap cache and refresh count
    else:
        pt_com.CacheIndex = new_cache_index  # rest: point to new index
    pt_com.RefreshTable()

# %% [markdown]
# ### save

# %%
wb.save(r"output.xlsx")
wb.close()
wb.close()
