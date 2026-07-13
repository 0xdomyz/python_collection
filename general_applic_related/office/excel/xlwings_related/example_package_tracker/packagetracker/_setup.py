# %%
import xlwings as xw

# %%
wb = xw.Book()

# %%
ws = wb.sheets.add('Tracker')
ws['B4'].value = 'Package Name'
ws['B5'].name = 'package_selection'
ws['B10'].value = 'Latest release'
ws['B11'].name = 'latest_release'

shape = ws.api.Shapes.AddShape(5, 250, 50, 200, 50)  # 5 = msoShapeRoundedRectangle
shape.TextFrame.Characters().Text = 'Show history'

# %%
ws = wb.sheets.add('Database')
ws['B2'].value = 'Add new package to database'
ws['B4'].value = 'Package Name'
ws['B5'].name = 'new_package'
ws['B12'].value = 'Update Database from pypi'
ws['B13'].name = 'update_at'
ws['B17'].value = 'Log'
ws['B18'].name = 'log'

shape = ws.api.Shapes.AddShape(5, 250, 50, 200, 50)  # 5 = msoShapeRoundedRectangle
shape.TextFrame.Characters().Text = 'Add package'
shape2 = ws.api.Shapes.AddShape(5, 250, 150, 200, 50)  # 5 = msoShapeRoundedRectangle
shape2.TextFrame.Characters().Text = 'Update Database'

# %%
ws = wb.sheets.add('Dropdown')
ws['A1'].value = 'Packages'
ws.tables.add( source=ws['A1'].expand(), name='dropdown_content', table_style_name='TableStyleMedium2' )

# %%
target = wb.names['package_selection'].refers_to_range
validation = target.api.Validation
validation.Delete()
validation.Add(
    Type=xw.constants.DVType.xlValidateList,
    AlertStyle=xw.constants.DVAlertStyle.xlValidAlertStop,
    Operator=xw.constants.FormatConditionOperator.xlBetween,
    Formula1='=INDIRECT("dropdown_content[Packages]")'
)

# %%
wb.save(r"pac_tracker.xlsm")