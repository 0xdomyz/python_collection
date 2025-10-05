import logging
from contextlib import contextmanager

import dwopt
from dwopt import Pg
from nanoid import generate


@contextmanager
def temp_table(db: dwopt.dbo._Db, table_name: str, size: int = 4):
    while True:
        words = generate(size=size, alphabet="abcdefghijklmnopqrstuvwxyz0123456789")
        new_table_name = f"{table_name}_{words}"
        if db.exist(new_table_name):
            continue
        else:
            break

    try:
        yield new_table_name
    except UpdateTableError as e:
        raise e
    except Exception as e:
        db.drop(new_table_name)
        raise e
    else:
        db.drop(new_table_name)


# make a special error type that the context manager can catch then not run finally
class UpdateTableError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


def update_table(
    db: dwopt.dbo._Db, table_name: str, sql: str, primary_keys: list
) -> None:
    with temp_table(db, table_name) as new_table_name:
        # write sql to make new columns on a new table
        sql = f"CREATE TABLE {new_table_name} AS {sql}"
        db.run(sql)

        # check if primary key count is the same as the original table
        original_pk_count = db.qry(table_name).dist(primary_keys).squeeze()
        new_pk_count = db.qry(new_table_name).dist(primary_keys).squeeze()

        # check if length of primary table is the same as the new table
        original_len = db.qry(table_name).len()
        new_len = db.qry(new_table_name).len()

        # if all checks pass, then drop the original table and rename the new table
        condition = original_pk_count == new_pk_count and original_len == new_len
        if condition:
            db.drop(table_name)
            db.run(f"ALTER TABLE {new_table_name} RENAME TO {table_name}")
        else:
            raise UpdateTableError(
                "Failed a update check:\n"
                f"{table_name} has {original_pk_count = }\n"
                f"{new_table_name} has {new_pk_count = }\n"
                f"{table_name} has {original_len = }\n"
                f"{new_table_name} has {new_len = }\n"
            )


if __name__ == "__main__":
    logging.basicConfig()
    logging.getLogger("dwopt.dbo").setLevel(logging.INFO)

    db = Pg("postgresql://test_db_user:1234@localhost/test_db")

    # set up table
    db.iris()
    q = db.qry("iris")
    q.top()
    q.len()

    # usage if sql success
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

    q = db.qry(table_name)
    q.top()
    q.len()

    # usage if sql fail
    table_name = "iris"
    sql = """
    select
        a.*,
        b.species_count as new_col3
    from iris a
    cross join (
        select
            species,
            count(*) as species_count
        from iris
        group by species
    ) b
    """
    primary_keys = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
    update_table(db, table_name, sql, primary_keys)

    q = db.qry(table_name)
    q.top()
    q.len()
