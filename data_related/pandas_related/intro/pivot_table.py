import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'Region': ['North', 'South', 'North', 'East', 'South', 'East', 'West', 'West'],
    'Category': ['A', 'B', 'A', 'B', 'A', 'A', 'B', 'A'],
    'Sales': [200, 150, 300, 400, 250, 100, 300, 500],
    'Discount': [0.1, 0.2, 0.15, 0.05, 0.1, 0.2, 0.25, 0.1],
    'Year': [2023, 2023, 2024, 2023, 2024, 2023, 2024, 2023]
})

# Pivot-style summary: total sales and average discount by Region and Category for 2023
summary = (
    df
    .loc[lambda d: d['Year'] == 2023]  # filter for year
    .assign(SalesAfterDiscount=lambda d: d['Sales'] * (1 - d['Discount']))  # new column
    .groupby(['Region', 'Category'], as_index=False)
    .agg(
        TotalSales=('SalesAfterDiscount', 'sum'),
        AvgDiscount=('Discount', 'mean'),
        Count=('Sales', 'size')
    )
    .pivot_table(index='Region', columns='Category', values='TotalSales', fill_value=0)
    .round(2)
)

print(summary)