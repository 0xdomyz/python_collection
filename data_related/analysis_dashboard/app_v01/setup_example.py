"""Quick start example using sample data."""

import os

import pandas as pd

# Check if example CSV exists
example_path = os.path.join(os.path.dirname(__file__), "example_titanic.csv")

if not os.path.exists(example_path):
    try:
        import seaborn as sns

        df = sns.load_dataset("titanic")
        df.to_csv(example_path, index=False)
        print(f"✓ Created example data: {example_path}")
    except ImportError:
        print("To create example data, install seaborn: pip install seaborn")
else:
    print(f"✓ Example data exists: {example_path}")
    print("Use this path in the dashboard: example_titanic.csv")
    print("Use this path in the dashboard: example_titanic.csv")
