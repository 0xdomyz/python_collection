from loguru import logger
import sqlalchemy as alc
import pandas as pd

logger.remove()


# add run method to engine
def run(self: alc.engine.Engine, sql: str) -> pd.DataFrame | None:
    with self.begin() as conn:
        res = conn.execute(alc.text(sql))
        if res.returns_rows:
            return pd.DataFrame(res.all(), columns=res.keys())


alc.engine.Engine.run = run


def _parse_schema_table_name(sch_tbl_name: str) -> tuple[str, str]:
    """
    Examples::

        print(f"{_parse_schema_table_name('ab') = }")
        print(f"{_parse_schema_table_name('Ab') = }")
        print(f"{_parse_schema_table_name('ab.ab') = }")
        print(f"{_parse_schema_table_name('Ab.Ab') = }")
        print(f"{_parse_schema_table_name('Ab.Ab.Ab') = }")
        print(f"{_parse_schema_table_name('') = }")
        print(f"{_parse_schema_table_name(None) = }")
        print(f"{_parse_schema_table_name(3) = }")
    """
    try:
        clean = sch_tbl_name.lower()
        items = clean.split(".")
    except AttributeError:
        schema_name = None
        table_name = None
    else:
        n = len(items)
        if n == 1:
            schema_name = None
            table_name = items[0]
        elif n == 2:
            schema_name = items[0]
            table_name = items[1]
        else:
            schema_name = items[0]
            table_name = ".".join(items[1:n])
    return schema_name, table_name


class PgInserter:
    def __init__(
        self, eng: alc.engine.Engine, schema_table_name: str, pkeys: list[str]
    ):
        """
        Example table creation qry::

            CREATE TABLE test_schema.taxi (
                pk BIGINT PRIMARY KEY,
                pickup TIMESTAMP WITHOUT TIME ZONE,
                dropoff TIMESTAMP WITHOUT TIME ZONE,
                passengers BIGINT,
                distance FLOAT(53)
            )
        """

        self.eng = eng
        self.schema, self.table_name = _parse_schema_table_name(schema_table_name)
        self.pkeys = pkeys

    def insert_non_duplicates(
        self, df: pd.DataFrame, potential_dups_condition: str = None
    ):
        for key in self.pkeys:
            assert key in df.columns, f"Missing primary key column: {key}"

        where_cls = (
            f"\nwhere {potential_dups_condition}" if potential_dups_condition else ""
        )
        try:
            db_tbl: pd.DataFrame = self.eng.run(
                f"select {','.join(self.pkeys)} from {self.schema}.{self.table_name} {where_cls}"
            )
            logger.debug(
                f"Selected {len(db_tbl)} rows from {self.schema}.{self.table_name} for deduplication"
            )
        except Exception as e:
            logger.warning(e)
            db_tbl = pd.DataFrame(columns=self.pkeys)

        df2 = df.copy()
        if not db_tbl.empty and not df2.empty:
            assert "_merge" not in df2.columns, "_merge column is reserved"
            deduped_tbl = (
                df2.merge(
                    db_tbl,
                    how="left",
                    on=self.pkeys,
                    validate="one_to_one",
                    indicator=True,
                )
                .loc[lambda x: x["_merge"] == "left_only", :]
                .drop(columns="_merge")
            )
        else:
            deduped_tbl = df2

        logger.debug(
            f"Inserting {len(deduped_tbl)} rows into {self.schema}.{self.table_name}"
        )
        deduped_tbl.to_sql(
            self.table_name,
            con=self.eng,
            schema=self.schema,
            if_exists="append",
            index=False,
        )
