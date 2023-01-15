import janitor
import pandas as pd

df = pd.DataFrame.from_dict(
    {
        "Name": [
            "Jane",
            "Melissa",
            "John",
            "Matt",
            "Abernethy",
            "Annie",
            "Brook",
            "Brian",
            "Carrie",
        ],
        "Tag": [
            "tag1,tag2",
            "tag1",
            "tag4,tag3,tag7",
            "tag2,tag9",
            "tag1,tag3",
            "tag3,tag4",
            "tag9,tag2",
            "tag3,tag2",
            "tag1,tag5",
        ],
    }
)

df.case_when(
    df.Tag.str.contains("tag1"),
    "tag1",  # condition, result
    df.Tag.str.contains("tag2"),
    "tag2",
    df.Tag.str.contains("tag3"),
    "tag3",
    df.Tag.str.contains("tag4"),
    "tag4",
    df.Tag.str.contains("tag5"),
    "tag5",
    df.Tag.str.contains("tag_wrong1"),
    "tag_right1",
    df.Tag,  # default if none of the conditions evaluate to True
    column_name="Tag_after",
)
