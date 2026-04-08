# %%
import pandas as pd
import seaborn as sns
import xlwings as xw
from xlwings_pivot_dashboard import PivotDashboard

# %%
# initial data
df = sns.load_dataset("titanic")

# %%
# group up continuous variables into bins
df["age_group"] = pd.cut(
    df["age"],
    bins=[-1, 10, 20, 30, 40, 50, 60, 70, 80],
).astype(str)
df["fare_group"] = pd.cut(df["fare"], bins=[0, 10, 20, 30, 40, 50, 100, 600]).astype(
    str
)
df = df.sort_values(df.columns.tolist())

# %%
print(f"{df.shape = }")
print(df.head().to_string())
df.describe(include="all").T

# %% [markdown]
# ### build dashboard

# %%
wb = xw.Book()
dashboard = PivotDashboard(wb, data_sheet="Data", pivot_sheet="Pivot")

# %%
SQL = """
select *
from titanic
"""

dashboard.write_table(df, sql=SQL, table_name="titanic_table")

# %%
PIVOT_CONFIGS = [
    dict(
        name="Pvt1",
        row_field="who",
        col_field="survived",
        data_field="fare",
        xl_func="count",
        chart_type="column_clustered",
        title="Volume by Who and Survival",
    ),
    dict(
        name="Pvt2",
        row_field="age_group",
        col_field="who",
        data_field="survived",
        xl_func="count",
        chart_type="area_stacked",
        title="Volume by Age and Who",
    ),
    dict(
        name="Pvt3",
        row_field="embark_town",
        col_field="survived",
        data_field="fare",
        xl_func="sum",
        chart_type="bar_stacked_100",
        title="Fare Sum by Embark Town and Survival",
    ),
]

dashboard.add_pivots(
    PIVOT_CONFIGS,
)

# %%
dashboard.add_slicers(
    fields=[
        "survived",
        "pclass",
        "sex",
        "age_group",
        "fare_group",
        "embark_town",
        "who",
    ],
)

# %% [markdown]
# ### refresh with extended data

# %%
df2 = df.copy()
df2["age_group"] = pd.cut(df2["age"], bins=[0, 18, 40, 80]).astype(str)
print(f"{df2.shape = }")
print(df2.head().to_string())

# %%
SQL2 = """
select
    *,
    case
        when age between 0  and 18 then '0-18'
        when age between 18 and 40 then '18-40'
        else '40+'
    end as age_group
from titanic
"""

dashboard.refresh(df2, sql=SQL2)

# %% [markdown]
# ### save

# %%
wb.save(r"output.xlsx")
wb.close()

# %% [markdown]
# ### refresh from an existing workbook
# %%
wb = xw.Book("Output.xlsx")
dashboard = PivotDashboard.from_workbook(wb, data_sheet="Data", pivot_sheet="Pivot")
print(dashboard)

# %%
df3 = df.copy()
df3["age_group2"] = pd.cut(df3["age"], bins=[0, 25, 50, 80]).astype(str)
print(f"{df3.shape = }")
print(df3.head().to_string())
# %%
SQL3 = """
select
    *,
    case
        when age between 0  and 25 then '0-25'
        when age between 25 and 50 then '25-50'
        else '50+'
    end as age_group2
from titanic
"""
dashboard.refresh(df3, sql=SQL3, table_name="titanic_table")

# %%
wb.save(r"output.xlsx")
wb.close()
