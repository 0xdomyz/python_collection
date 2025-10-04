import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Sample data
np.random.seed(0)
df = pd.DataFrame({
    'Category': np.repeat(['A', 'B', 'C'], 50),
    'Value': np.concatenate([
        np.random.normal(loc=5, scale=1, size=50),
        np.random.normal(loc=7, scale=1.5, size=50),
        np.random.normal(loc=6, scale=0.5, size=50)
    ])
})

# Group values by category
grouped = [df[df['Category'] == cat]['Value'].values for cat in sorted(df['Category'].unique())]

# Create figure and axes
fig, ax = plt.subplots(figsize=(8, 5))

# Boxplot
ax.boxplot(grouped, patch_artist=True)

# Label x-axis with category names
ax.set_xticklabels(sorted(df['Category'].unique()))
ax.set_title("Boxplot by Category")
ax.set_xlabel("Category")
ax.set_ylabel("Value")

plt.tight_layout()
plt.show()