# %%
# set up manually with macro
import xlwings as xw

bk = xw.Book()
bk.save('test.xlsm') # save the new book as test.xlsm
bk.close()

# %%
# main
import xlwings as xw

vba_book = xw.Book('test.xlsm') # open the book

# %%
mysum = vba_book.macro("Module1.MySum")
mysum
# %%
# Call a VBA function
mysum(5, 4)
# %%
show_msgbox = vba_book.macro("Module1.ShowMsgBox")
show_msgbox
# %%
show_msgbox("Hello from Python!")
# %%
vba_book.close()