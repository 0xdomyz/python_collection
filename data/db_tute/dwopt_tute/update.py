"""
Set up a test postgres database::

    sudo su postgres
    psql
    CREATE DATABASE test_db;
    CREATE USER test_db_user WITH PASSWORD '1234';
    GRANT ALL PRIVILEGES ON DATABASE test_db to test_db_user;
    \q
    exit
"""

import logging
from contextlib import contextmanager

import dwopt
from dwopt import Pg
from nanoid import generate


@contextmanager
def temp_table(db: dwopt.dbo._Db, table_name: str):
    while True:
        new_table_name = f"{table_name}_{generate(size=5)}"
        if db.exist(new_table_name):
            continue
        else:
            break

    try:
        yield new_table_name
    except UpdateTableError:
        pass
    except Exception as e:
        db.drop(new_table_name)


# make a special error type that the context manager can catch then not run finally
class UpdateTableError(Exception):
    pass


def update_table(db: dwopt.dbo._Db, table_name: str, sql: str, primary_keys: list):
    with temp_table(db, table_name) as new_table_name:
        # write sql to make new columns on a new table
        sql = f"CREATE TABLE {new_table_name} AS {sql}"
        db.run(sql)

        # check if primary key count is the same as the original table
        original = db.qry(table_name).dist(primary_keys).squeeze()
        new = db.qry(new_table_name).dist(primary_keys).squeeze()
        primary_keys_count_is_the_same = original == new

        # if same, then drop the original table and rename the new table
        if primary_keys_count_is_the_same:
            db.drop(table_name)
            db.run(f"ALTER TABLE {table_name} RENAME TO {new_table_name}")
        else:
            raise ValueError(
                "Primary key count is not the same as the original table."
                f"{table_name} has {original} rows, but {new_table_name} has {new} rows."
            )


if __name__ == "__main__":

    logging.basicConfig()
    logging.getLogger("dwopt.dbo").setLevel(logging.INFO)

    db = Pg("postgresql://test_db_user:1234@localhost/test_db")

    # set up table
    db.iris()
    db.qry("iris").top()

    # usage
    table_name = "iris"
    sql = """
    select
        a.*,
        1 as new_col1,
        2 as new_col2,
        b.species_count
    from iris a
    left join (
        select
            species,
            count(*) as species_count
        from iris
        group by species
    ) b on a.species = b.species
    """
    primary_keys = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    update_table(db, table_name, sql, primary_keys)

    db.qry(table_name).top()
