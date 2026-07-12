# %%
import xlwings as xw

# %%
xw.Book()
ws = xw.sheets.active
# ws = xw.Book().sheets['Sheet1']

# %%
shape = ws.api.Shapes.AddShape(5, 189, 153, 183.75, 53.25)  # 5 = msoShapeRoundedRectangle
shape.TextFrame.Characters().Text = 'Show history Button 2'
# shape.Delete()
