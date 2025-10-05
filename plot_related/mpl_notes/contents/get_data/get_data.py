from pathlib import Path
import pandas as pd

HERE = Path(__file__).parent


def get_snp_data():
    import yfinance as yf

    asset = "ES=F"
    tk = yf.Ticker(asset)
    hist = tk.history(period="max", interval="1mo", auto_adjust=False)[
        ["Close"]
    ]  # [['Open', 'High', 'Low', 'Close', 'Volume']]
    hist.columns = [c.lower() for c in hist.columns]
    hist["r_12m"] = hist["close"].pct_change(12)

    print(f"{hist.shape = }")
    print(hist.head().to_string())

    return hist


def get_titanic_data():
    df = pd.read_csv(HERE / "titanic.csv")
    print(df.shape)
    print(df.head().to_string())
    return df


def get_taxis_data():
    df = pd.read_csv(HERE / "taxis.csv")
    print(df.shape)
    print(df.head().to_string())
    return df


def get_flights_data():
    df = pd.read_csv(HERE / "flights.csv")
    print(df.shape)
    print(df.head().to_string())
    return df


def get_titanic_summary_data():
    df = get_titanic_data()

    df["age_bin"] = pd.qcut(df["age"], q=10)

    grp_dict = {
        "n": ("age_bin", "size"),
        "survival_rate": ("survived", "mean"),
    }
    for who in df["who"].unique():
        grp_dict[f"survival_rate_{who}"] = (
            "survived",
            lambda x, w=who: df.loc[x.index]
            .loc[lambda y: y["who"] == w, "survived"]
            .mean(),
        )

    pdf = df.groupby("age_bin", observed=False, as_index=False).agg(**grp_dict)
    print(pdf.head().to_string())

    return pdf
