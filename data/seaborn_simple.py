"""
https://seaborn.pydata.org/tutorial/function_overview.html
"""

import pandas as pd
import seaborn as sns

titanic = pd.read_csv("toydata/titanic.csv")

list(titanic.select_dtypes("number").columns)
#['survived', 'pclass', 'age', 'sibsp', 'parch', 'fare']
list(titanic.select_dtypes(object).columns)
#['sex', 'embarked', 'class', 'who', 'deck', 'embark_town', 'alive']


#relational

#    scatter

#    line


#distributions

#    hist


#categorical

#    box

#    point

#    bar


#univariate

#    continuouse/numerical
sns.displot(data=titanic,x="pclass")
sns.displot(data=titanic,x="age")
sns.displot(data=titanic,x="fare")

#    discrete/categorical
sns.catplot(data=titanic, x="alive", col="deck", kind="count")


#bi-variate

#    continuous vs continuous
sns.relplot(data=titanic, x="age", y="fare")
sns.displot(data=titanic, x="age", y="fare")

#    discrete vs continuous
sns.catplot(data=titanic, x="alive", y="age")

#    distcret vs discrete
sns.displot(data=titanic, x="alive", y="class")

