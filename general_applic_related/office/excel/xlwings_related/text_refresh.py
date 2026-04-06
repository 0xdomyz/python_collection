# %%
import pandas as pd
import seaborn as sns
import xlwings as xw

# %%
# data
df = sns.load_dataset("titanic")
print(f"{df.shape = }")
print(df.head().to_string())

# %% [markdown]
# ### Make new workbook and write text to a tab

# %%
# Open a new workbook (visible=False to run headless)
wb = xw.Book()
ws = wb.sheets[0]
ws.name = "SQL"

# %%
sql = """
select 
    *
from titanic
where age > 30
"""

# %%
# Split into lines and write one line per row so indentation is preserved.
# Each element is wrapped in a list to write as a single-column range.
lines = sql.split("\n")
ws["A1"].value = [[line or " "] for line in lines]

# %% [markdown]
# ### refresh with new sql
# %%
sql2 = """
select 
    case when age > 30 then 'old' else 'young' end as age_group,
    count(*) as count
from titanic a

where age > 30
group by age_group
"""
# %%
lines2 = sql2.split("\n")
ws["A1"].expand().clear()  # wipe old content before writing shorter sql
ws["A1"].value = [[line or " "] for line in lines2]

# %%
sql3 = """
select 
    *
from titanic
"""
# %%
lines3 = sql3.split("\n")
ws["A1"].expand().clear()  # wipe old content before writing shorter sql
ws["A1"].value = [[line or " "] for line in lines3]


# %% [markdown]
# ### save

# %%
wb.save(r"output.xlsx")
wb.close()
