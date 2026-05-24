# %%

import xlwings as xw

# %%
wb = xw.Book(r"xxx.xlsx")
wb.sheet_names

# %%
sheet_name = "xxx"
input_column_top_range = "Y5"
output_column_top_range = "Z5"

model_input_cell = "M14"
model_output_cells = ["E12", "E28"]


# %%
sht = wb.sheets[sheet_name]

input_vals = sht.range(input_column_top_range).expand("down").value

out_rows = []

for v in input_vals:
    sht[model_input_cell].value = v
    wb.app.calculate()
    print(f"{v = }")
    out_rows.append([sht[cell].value for cell in model_output_cells])

sht[output_column_top_range].value = out_rows

# %%
