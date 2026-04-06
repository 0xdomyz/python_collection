# %%
import pandas as pd
import seaborn as sns
import xlwings as xw
from xlwings_pivot_dashboard import PivotDashboard

# %%
# initial data
df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())

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
        name="PvtWho",
        row_field="who",
        col_field="survived",
        data_field="fare",
        title="Volume by Who and Survival",
    ),
    dict(
        name="PvtTown",
        row_field="embark_town",
        col_field="survived",
        data_field="fare",
        title="Volume by Embark Town and Survival",
    ),
    dict(
        name="PvtMale",
        row_field="adult_male",
        col_field="survived",
        data_field="fare",
        title="Volume by Adult Male and Survival",
    ),
    dict(
        name="PvtSex",
        row_field="sex",
        col_field="survived",
        data_field="fare",
        title="Volume by Sex and Survival",
    ),
]

dashboard.add_pivots(
    PIVOT_CONFIGS,
    chart_layout={
        "ncols": 2,
        "col_width": 430,
        "row_height": 330,
        "top_offset": 60,
        "left_offset": 0,
        "chart_width": 400,
        "chart_height": 300,
    },
    dest_layout={
        "col": "Z",
        "start_row": 5,
        "row_step": 15,
        "ncols": 2,
        "col_step": 6,
    },
)

# %%
dashboard.add_slicers(
    fields=["survived", "pclass", "sex"],
    layout={
        "ncols": 2,
        "col_width": 150,
        "row_height": 230,
        "top_offset": 60,
        "left_offset": 900,
        "width": 120,
        "height": 200,
    },
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
# ### refresh existing
# %%
wb = xw.Book("Output.xlsx")
dashboard = PivotDashboard(wb, data_sheet="Data", pivot_sheet="Pivot")
