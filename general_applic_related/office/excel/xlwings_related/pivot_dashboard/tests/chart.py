# %%
import pandas as pd
import seaborn as sns
import xlwings as xw

# %%
# data
df = sns.load_dataset("healthexp")
print(f"{df.shape = }")
print(df.head().to_string())
df.describe()

# %%
df["category"] = "A"
df.loc[df["Country"].isin(["Great Britain", "Japan"]), "category"] = "B"
df.loc[df["Country"].isin(["USA", "Canada"]), "category"] = "C"
df["Country"] = df["Country"].map(
    {
        "Germany": "Germany",
        "France": "France",
        "Great Britain": "Germany",
        "Japan": "France",
        "USA": "Germany",
        "Canada": "France",
    }
)

# %%
df.loc[df["category"] == "A", :].pivot(
    index="Year", columns="Country", values="Spending_USD"
).plot()

# %%
df.loc[df["category"] == "B", :].pivot(
    index="Year", columns="Country", values="Spending_USD"
).plot()

# %%
df.loc[df["category"] == "C", :].pivot(
    index="Year", columns="Country", values="Spending_USD"
).plot()

# %%
import xlwings as xw
from pivot_dashboard.xlwings_pivot_dashboard import PivotDashboard

wb = xw.Book()
dashboard = PivotDashboard(wb)
dashboard.write_table(df, sql="")

pivot_configs = [
    # fmt: off
    dict(row_field='Year',col_field='Country',data_field="Spending_USD",chart_type="line",xl_func='max'),
    # fmt: on
]
dashboard.add_pivots(pivot_configs)

dashboard.add_slicers(
    fields=df.columns.tolist(),
)
