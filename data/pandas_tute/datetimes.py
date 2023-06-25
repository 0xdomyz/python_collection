import datetime

import pandas as pd

df = pd.DataFrame({"modified": [datetime.datetime(2022, 12, 31), datetime.datetime(2022, 9, 30), datetime.datetime(2022, 6, 30), datetime.datetime(2022, 3, 31), datetime.datetime(2021, 12, 31)]})
df.sort_values(by="modified", inplace=True)
df["modified"] = df["modified"].apply(lambda x: x.replace(hour=0, minute=0, second=0, microsecond=0))
df["modified_week"] = df["modified"].apply(lambda x: x - datetime.timedelta(days=x.weekday()))
df["modified_month"] = df["modified"].apply(lambda x: x.replace(day=1))
df["modified_month_part"] = df["modified"].apply(lambda x: "first" if x.day <= 15 else "second")
df["modified_month_first_or_second_half"] = df["modified_month"].astype(str) + "_" + df["modified_month_part"]

