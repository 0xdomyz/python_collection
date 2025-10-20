df2["age_of_lowest_fare_in_who"] = (
    df2.sort_values(["fare", "id"], na_position="last")
    .groupby("who", dropna=False)["age"]
    .transform("first")
)
