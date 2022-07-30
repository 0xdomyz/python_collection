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
titanic.head()


#statistical relationship

#    scatter
sns.relplot(data=titanic, x="age", y="fare")
sns.relplot(data=titanic, x="age", y="fare",hue="survived")
sns.relplot(data=titanic, x="age", y="fare",col="survived")
sns.relplot(data=titanic, x="age", y="fare",style="survived")
sns.relplot(data=titanic, x="age", y="fare",size="survived")

sns.relplot(data=titanic, x="age", y="fare",hue="survived",style="survived",col="class")

#    line: continuity
sns.relplot(data=titanic, x="age", y="fare",kind="line")
sns.relplot(data=titanic, x="age", y="fare",kind="line",hue="survived",style="survived",col="class")

#variable distribution

#    hist
sns.displot(data=titanic,x="age")#continuouse
sns.displot(data=titanic,x="class")#discrete
sns.displot(data=titanic,x="age",y="fare")
sns.displot(data=titanic, x="alive", y="class")

sns.displot(data=titanic,x="age",hue="class")
sns.displot(data=titanic,x="age",col="survived")
sns.displot(data=titanic,x="age",hue="survived",col="class")

sns.displot(data=titanic,x="class",hue="survived")
sns.displot(data=titanic,x="class",col="embark_town")
sns.displot(data=titanic,x="class",hue="survived",col="embark_town")

#categorical data

#    box
sns.catplot(data=titanic, x="alive", y="age", kind="box")

#    point
sns.catplot(data=titanic, x="alive", y="age")

#    bar
sns.catplot(data=titanic, x="alive", col="deck", kind="count")



