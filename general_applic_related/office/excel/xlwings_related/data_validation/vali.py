# %%
import xlwings as xw

# %%
wb = xw.Book()

# %%
ws = wb.sheets.add('Tracker')
ws['B5'].name = 'package_selection'

# %%
ws = wb.sheets.add('Dropdown')
ws['A1'].value = 'Packages'
ws['A2'].value = 'package1'
ws['A3'].value = 'package2'
ws['A4'].value = 'package3'
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
