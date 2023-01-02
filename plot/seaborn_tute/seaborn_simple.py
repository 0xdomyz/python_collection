"""
https://seaborn.pydata.org/tutorial/function_overview.html
"""

import pandas as pd
import seaborn as sns

titanic = pd.read_csv("toydata/titanic.csv")

titanic.head()

list(titanic.select_dtypes("number").columns)
list(titanic.select_dtypes(object).columns)
list(titanic.select_dtypes(bool).columns)

# numeric: ['age', 'fare']
# categorical: ['survived', 'sibsp', 'parch', 'class', 'who', 'deck', 'embark_town', 'adult_male', 'alone']


# statistical relationship

#    scatter
sns.relplot(data=titanic, x="age", y="fare")
sns.relplot(data=titanic, x="age", y="fare", hue="survived")
sns.relplot(data=titanic, x="age", y="fare", col="survived")
sns.relplot(data=titanic, x="age", y="fare", style="survived")
sns.relplot(data=titanic, x="age", y="fare", size="survived")

sns.relplot(
    data=titanic, x="age", y="fare", hue="survived", style="survived", col="class"
)

#    line: continuity
sns.relplot(data=titanic, x="age", y="fare", kind="line")
sns.relplot(
    data=titanic,
    x="age",
    y="fare",
    kind="line",
    hue="survived",
    style="survived",
    col="class",
)


# variable distribution

#    hist

#        continuouse
sns.displot(data=titanic, x="age")
sns.displot(data=titanic, x="age", y="fare")

sns.displot(data=titanic, x="age", hue="class")
sns.displot(data=titanic, x="age", col="alive")
sns.displot(data=titanic, x="age", hue="alive", col="class")

sns.displot(data=titanic, x="age", y="fare", col="alive")

#        discrete
sns.displot(data=titanic, x="alive")
sns.displot(data=titanic, x="class", y="alive")

sns.displot(data=titanic, x="alive", col="class")
sns.displot(data=titanic, x="alive", col="who")
sns.displot(data=titanic, x="alive", col="adult_male")
sns.displot(data=titanic, x="alive", col="alone")
sns.displot(data=titanic, x="alive", col="embark_town")
sns.displot(data=titanic, x="alive", col="parch", col_wrap=3)
sns.displot(data=titanic, x="alive", col="sibsp", col_wrap=3)

sns.displot(data=titanic, x="class", y="alive", col="who")


# categorical data

#    box
sns.catplot(data=titanic, x="alive", y="age", kind="box")
sns.catplot(data=titanic, x="deck", y="age", kind="box")

#    point
sns.catplot(data=titanic, x="alive", y="age")
sns.catplot(data=titanic, x="deck", y="age")

#    bar
sns.catplot(data=titanic, x="alive", kind="count")
sns.catplot(data=titanic, x="alive", col="class", kind="count")
