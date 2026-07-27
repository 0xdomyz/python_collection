# %%
import yfinance as yf

df = yf.download(['ASIA.AX', 'VFINX',], start = '2020-01-01', end = '2026-12-31', interval = '1d')
df[[('ret',x) for x in df['Close'].columns]] = df['Close'].ffill().pct_change().add(1).cumprod()
df.columns = [f"{col[1]}_{col[0]}" for col in df.columns]
df
# %%
import xlwings as xw

ws = xw.sheets.active
ws["A1"].value = df
ws.tables.add(source=ws["A1"].expand())
# %%
chart = ws.charts.add(
    top=ws['C5'].top, left=ws['C5'].left,
    width=700, height=400
)
chart.chart_type = 'line'
chart.set_source_data(ws['L1:M1697'])

# %%
import xlwings as xw
xw.Book()