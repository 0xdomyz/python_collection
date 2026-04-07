# %%
import time

import pandas as pd
import seaborn as sns
import xlwings as xw

# %%
# data
df = sns.load_dataset("healthexp")
print(f"{df.shape = }")
print(df.head().to_string())
df.describe()

# %% [markdown]
# ### Make new test workbook

# %%
wb = xw.Book()
ws = wb.sheets[0]
ws.name = "Data"
ws2 = wb.sheets.add("Data2")
# %% [markdown]
# ### simulate something big
# %%
ws.range("A1").value = df
nrows = len(df)

# add a formula column header
ws.range("F1").value = "spend_pct"

t0 = time.perf_counter()
for i in range(2, nrows + 2):
    cell_country = ws.range(f"C{i}")
    cell_spend = ws.range(f"D{i}")
    cell_formula = ws.range(f"F{i}")
    cell_formula2 = ws.range(f"G{i}")
    country = cell_country.value
    # formula triggers recalculation on every iteration without manual mode
    cell_formula.formula = f"=D{i}/SUM($D$2:$D${nrows + 1})*100"
    cell_formula2.formula = f"=rand()*100"
    # row colour
    color = (198, 224, 180) if country.strip() == "USA" else (255, 199, 206)
    for col in "ABCDEFG":
        ws.range(f"{col}{i}").color = color
    # bold the country name
    cell_country.font.bold = True
    # number format on spend
    cell_spend.number_format = "#,##0.00"
t1 = time.perf_counter()
print(f"without stop_upd: {t1 - t0:.2f}s")

# %% [markdown]
# ### repeat but with stop upd incl
# %%
ws2.range("A1").value = df
ws2.range("F1").value = "spend_pct"

app = wb.app
app.screen_updating = False
app.calculation = "manual"
app.enable_events = False
app.display_status_bar = False
try:
    t0 = time.perf_counter()
    for i in range(2, nrows + 2):
        cell_country = ws2.range(f"C{i}")
        cell_spend = ws2.range(f"E{i}")
        cell_formula = ws2.range(f"F{i}")
        cell_formula2 = ws2.range(f"G{i}")
        country = cell_country.value
        cell_formula.formula = f"=E{i}/SUM($E$2:$E${nrows + 1})*100"
        cell_formula2.formula = f"=rand()*100"
        color = (198, 224, 180) if country.strip() == "USA" else (255, 199, 206)
        for col in "ABCDEFG":
            ws2.range(f"{col}{i}").color = color
        cell_country.font.bold = True
        cell_spend.number_format = "#,##0.00"
    t1 = time.perf_counter()
    print(f"with stop_upd:    {t1 - t0:.2f}s")
finally:
    app.screen_updating = True
    app.calculation = "automatic"
    app.enable_events = True
    app.display_status_bar = True


# %% [markdown]
# ### save close
# %%
wb.save(r"output.xlsx")
wb.close()
wb.close()
