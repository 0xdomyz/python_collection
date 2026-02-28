from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# create an engine to connect to a database
engine = create_engine("sqlite:///example.db", echo=True)

# create a session factory
Session = sessionmaker(bind=engine)

# create a base class for declarative models
Base = declarative_base()


# define a model for a table
class MyTable(Base):
    __tablename__ = "my_table"

    id = Column(Integer, primary_key=True)
    column1 = Column(String)
    column2 = Column(String)
    column3 = Column(Integer)
    column4 = Column(String)


# create a session
session = Session()

# create a query that selects, filters, and groups data
query = (
    session.query(
        MyTable.column1, MyTable.column2, func.sum(MyTable.column3).label("total")
    )
    .filter(MyTable.column4 == "value")
    .group_by(MyTable.column1, MyTable.column2)
)

# execute the query and print the results
for row in query:
    print(row.column1, row.column2, row.total)

# In this example, we use the SQLAlchemy library to create and run a SQL select, filter, then group by query.
# We first create an engine to connect to a database using the `create_engine()` function from SQLAlchemy.
# Then, we create a session factory using the `sessionmaker()` function, and a base class for declarative models using the `declarative_base()` function.
# We define a model for a table using the base class, and create a session using the session factory.
# Next, we create a query that selects, filters, and groups data using the `query()` method of the session object.
# We use the `filter()` method to filter the results to only include rows where `column4` equals `'value'`, and the `group_by()` method to group the results by `column1` and `column2`.
# Finally, we execute the query using a `for` loop and print the results.
