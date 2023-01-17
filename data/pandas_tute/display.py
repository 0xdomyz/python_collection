import numpy as np
import pandas as pd

# example of pd set_option
pd.set_option("display.max_rows", 10)
pd.set_option("display.max_columns", 10)
pd.set_option("display.width", 1000)
pd.set_option("display.max_colwidth", 1000)
pd.set_option("display.precision", 2)
pd.set_option("display.float_format", "{:,.2f}".format)
pd.set_option("display.show_dimensions", True)
pd.set_option("display.colheader_justify", "left")
pd.set_option("display.max_info_columns", 10)
pd.set_option("display.max_info_rows", 10)
pd.set_option("display.notebook_repr_html", True)
pd.set_option("display.html.border", 1)
pd.set_option("display.large_repr", "truncate")
pd.set_option("display.expand_frame_repr", False)
pd.set_option("display.max_seq_items", 10)

# display table as html
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df.to_html("test.html")

# display table as html with css
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df.to_html("test.html", classes="table table-striped table-hover")

# display table with colour-scaled values on cells
#####################################################
df = pd.DataFrame({"a": [1, 2, 3], "b": [4, 5, 6]})
df = df.style.background_gradient(cmap="Blues")

# save as html
df.to_html("test.html")

# example 20 by 20 table
df = pd.DataFrame(np.random.randn(20, 20))
df.style.background_gradient(cmap="Blues").to_html("test.html")

# cmap options
# 'viridis', 'plasma', 'inferno', 'magma', 'cividis'
# 'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
# 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
# 'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn'

# cmap of red to green scale
df = pd.DataFrame(np.random.randn(20, 20))
df = df.style.background_gradient(cmap="RdYlGn")
df.to_html("test.html")

# find out colnames
df.columns

# multiple dataframe on 1 html page
#########################################
df1 = pd.DataFrame(np.random.randn(20, 20))
df2 = pd.DataFrame(np.random.randn(20, 20))
df3 = pd.DataFrame(np.random.randn(20, 20))

df1 = df1.style.background_gradient(cmap="RdYlGn")
df2 = df2.style.background_gradient(cmap="RdYlGn")
df3 = df3.style.background_gradient(cmap="RdYlGn")

html1 = df1.to_html()
html2 = df2.to_html()
html3 = df3.to_html()

# combine html
lst = [html1, html2, html3]
html = "<br>".join(lst)

# add title above each table
html = (
    "<h1>Table 1</h1>"
    + html1
    + "<br><h1>Table 2</h1>"
    + html2
    + "<br><h1>Table 3</h1>"
    + html3
)

# save html
with open("test.html", "w") as f:
    f.write(html)
