from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd
import seaborn as sns
import sklearn.datasets

# _DATA_DIR = Path(__file__).parent / "toydata"
_DATA_DIR = Path("").resolve() / "data" / "toydata"


def sklearn_data(name: str, bunch):
    df: pd.DataFrame = bunch["frame"]
    desc = bunch["DESCR"]

    with open(_DATA_DIR / f"{name}_desc.txt", "w") as f:
        f.write(desc)

    # print(f"shape:\n{df.shape}")
    # print(f"head:\n{df.head()}")
    # print(f"first row:\n{df.iloc[0,:]}")

    df.to_csv(_DATA_DIR / f"{name}.csv", index=False)


def sns_data(name: str):
    df: pd.DataFrame = sns.load_dataset(name)
    df.to_csv(_DATA_DIR / f"{name}.csv", index=False)


if __name__ == "__main__":
    sklearn_data("diabetes", sklearn.datasets.load_diabetes(as_frame=True))
    sklearn_data("iris", sklearn.datasets.load_iris(as_frame=True))
    sklearn_data("wine", sklearn.datasets.load_wine(as_frame=True))

    # sns.get_dataset_names()
    names = [
        "anagrams",
        "anscombe",
        "attention",
        "brain_networks",
        "car_crashes",
        "diamonds",
        "dots",
        "exercise",
        "flights",
        "fmri",
        "gammas",
        "geyser",
        # "iris",
        "mpg",
        "penguins",
        "planets",
        "taxis",
        "tips",
        "titanic",
    ]

    for name in names:
        sns_data(name)

    url = "https://archive.ics.uci.edu/ml/machine-learning-databases/00350/default%20of%20credit%20card%20clients.xls"
    urlretrieve(url, _DATA_DIR / "uci_credit_card.xls")
