# %%
import seaborn as sns

df = sns.load_dataset('titanic')
print(f"{df.shape = }")
print(df.head().to_string())
# %%
import xlwings as xw

wb = xw.Book()
ws = wb.sheets[0]
ws.name = "Data"

ws.clear()
ws["A1"].value = df
ws.tables.add(source=ws["A1"].expand(), name="Data1")
tbl = ws.tables["Data1"]

# %%
ws_input = wb.sheets.add("pivot")

# %%
# input cell in another location
ws_input["A1"].value = 'inputs'

input_cell = ws_input["A2"]
ws_input["A2"].value = 10

input_cell2 = ws_input["A3"]
ws_input["A3"].value = 20

# %%
# Add a calculated column on the table and fill it for all rows.
tbl.api.ListColumns.Add().Name = "fml"
tbl.api.ListColumns("fml").DataBodyRange.Formula = (
f"""
=IF([@age]<='{ws_input.name}'!{input_cell.address}, \"d0\",
    IF([@age]<='{ws_input.name}'!{input_cell2.address}, \"d1\",
        \"d2\"
    )
)
""".strip()
)

# %%
# make pivot table
pivot_cache = wb.api.PivotCaches().Create(
    SourceType=1,  # xlDatabase
    SourceData="Data1",
)
pt = pivot_cache.CreatePivotTable(
    TableDestination=ws_input["E6"].api,
    TableName="Pivot_1",
)
pt.PivotFields("fml").Orientation = 1  # xlRowField
pt.PivotFields("survived").Orientation = 2  # xlColumnField
pt.AddDataField(pt.PivotFields("age"), "min of Age", -4139)  # xlMin



# %%
pt.TableRange2.Clear()
# %%
wb.close()