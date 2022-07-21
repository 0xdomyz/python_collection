# Libraries
import numpy as np
import pandas as pd
import janitor

# Sample Data curated for this example
company_sales = {
    'SalesMonth': ['Jan', 'Feb', 'Mar', 'April'],
    'Company1': [150.0, 200.0, 300.0, 400.0],
    'Company2': [180.0, 250.0, np.nan, 500.0],
    'Company3': [400.0, 500.0, 600.0, 675.0]
}

# The Pandas Way

# 1. Create a pandas DataFrame from the company_sales dictionary
df = pd.DataFrame.from_dict(company_sales)

# 2. Delete a column from the DataFrame. Say 'Company1'
del df['Company1']

# 3. Drop rows that have empty values in columns 'Company2' and 'Company3'
df = df.dropna(subset=['Company2', 'Company3'])

# 4. Rename 'Company2' to 'Amazon' and 'Company3' to 'Facebook'
df = df.rename(
    {
        'Company2': 'Amazon',
        'Company3': 'Facebook',
    },
    axis=1,
)

# 5. Let's add some data for another company. Say 'Google'
df['Google'] = [450.0, 550.0, 800.0]

df
# Output looks like this:
# Out[15]:
#   SalesMonth  Amazon  Facebook  Google
# 0        Jan   180.0     400.0   450.0
# 1        Feb   250.0     500.0   550.0
# 3      April   500.0     675.0   800.0

df = (
    pd.DataFrame(company_sales)
    .drop(columns="Company1")
    .dropna(subset=["Company2", "Company3"])
    .rename(columns={"Company2": "Amazon", "Company3": "Facebook"})
    .assign(Google=[450.0, 550.0, 800.0])
)

df
# The output is the same as before, and looks like this:
# Out[15]:
#   SalesMonth  Amazon  Facebook  Google
# 0        Jan   180.0     400.0   450.0
# 1        Feb   250.0     500.0   550.0
# 3      April   500.0     675.0   800.0

df = (
    pd.DataFrame.from_dict(company_sales)
    .remove_columns(["Company1"])
    .dropna(subset=["Company2", "Company3"])
    .rename_column("Company2", "Amazon")
    .rename_column("Company3", "Facebook")
    .add_column("Google", [450.0, 550.0, 800.0])
)

df
# Output looks like this:
# Out[15]:
#   SalesMonth  Amazon  Facebook  Google
# 0        Jan   180.0     400.0   450.0
# 1        Feb   250.0     500.0   550.0
# 3      April   500.0     675.0   800.0


#examples
df = pd.DataFrame.from_dict(company_sales)
df

df.remove_columns("Company2")
df.dropna(subset=["Company2", "Company3"])
df.rename_column("Company2", "Amazon")
df.rename_column("Company3", "Facebook")
df.add_column("Google", [450.0, 550.0, 800.0,1])

#to-do add functionality examples
# Cleaning columns name (multi-indexes are possible!)
# Removing empty rows and columns
# Identifying duplicate entries
# Encoding columns as categorical
# Splitting your data into features and targets (for machine learning)
# Adding, removing, and renaming columns
# Coalesce multiple columns into a single column
# Date conversions (from matlab, excel, unix) to Python datetime format
# Expand a single column that has delimited, categorical values into dummy-encoded variables
# Concatenating and deconcatenating columns, based on a delimiter
# Syntactic sugar for filtering the dataframe based on queries on a column
# Experimental submodules for finance, biology, chemistry, engineering, and pyspark

import janitor  # upon import, functions are registered as part of pandas.

# This cleans the column names as well as removes any duplicate rows
df = pd.DataFrame.from_dict(company_sales).clean_names().remove_empty()

from janitor import clean_names, remove_empty

df = pd.DataFrame.from_dict(company_sales)
df = clean_names(df)
df = remove_empty(df)

from janitor import clean_names, remove_empty
df = (
    pd.DataFrame.from_dict(company_sales)
    .pipe(clean_names)
    .pipe(remove_empty)
)
df



