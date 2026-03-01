"""
Teradata GroupBy Execution Framework
=====================================

Provides a set of runner classes for executing multiple GROUP BY / aggregation
queries against a Teradata table via SQLAlchemy.  Three execution strategies are
offered:

* :class:`SequentialGroupByRunner` – runs queries one-by-one in the calling thread.
* :class:`ParallelGroupByRunner` – runs queries concurrently using a
  ``ThreadPoolExecutor`` and SQLAlchemy connection pooling.
* :class:`ServerSideGroupByRunner` – loads queries into a driver table and
  executes them via a Teradata stored procedure, minimising round-trips.

Use :func:`get_advanced_groupby_runner` to pick the best strategy automatically
based on the number of queries, estimated cost, and estimated spool risk.

Example
-------
>>> from sqlalchemy import create_engine
>>> engine = create_engine("teradatasql://user:pass@host/db",
...                        connect_args={"autocommit": True})
>>> queries = [
...     "SELECT colA, COUNT(*) AS cnt FROM vt_subset GROUP BY colA",
...     "SELECT colB, SUM(x) AS total FROM vt_subset GROUP BY colB",
... ]
>>> runner = get_advanced_groupby_runner(
...     engine, base_table="big_table",
...     subset_filter="event_date >= DATE - 30",
...     subset_table="vt_subset", queries=queries
... )
>>> results = runner.run(queries)
"""

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor
from typing import List, Optional

import pandas as pd
from loguru import logger
from sqlalchemy import text
from sqlalchemy.engine import Engine

# ---------------------------------------------------------------------------
#  Cost + Spool Estimation Helpers
# ---------------------------------------------------------------------------


def estimate_query_cost(sql: str) -> int:
    """
    Heuristically estimate the computational cost of a SQL query.

    Scoring:
        - ``JOIN``     → +2
        - ``GROUP BY`` → +2
        - ``DISTINCT`` → +1
        - Aggregation (``SUM``, ``AVG``, ``COUNT``) → +1

    Args:
        sql: SQL query string.

    Returns:
        Integer cost score (typically 0–6 for standard queries; can be
        higher if a query contains multiple aggregate functions).
    """
    sql_lower = sql.lower()
    cost = 0
    if "join" in sql_lower:
        cost += 2
    if "group by" in sql_lower:
        cost += 2
    if "distinct" in sql_lower:
        cost += 1
    if "sum(" in sql_lower or "avg(" in sql_lower or "count(" in sql_lower:
        cost += 1
    logger.debug("Estimated cost for query: {}", cost)
    return cost


def estimate_spool_risk(sql: str) -> int:
    """
    Heuristically estimate the spool (temp-space) risk of a SQL query.

    Scoring:
        - ``GROUP BY`` → +1
        - ``JOIN``     → +1
        - Missing ``WHERE`` (full-table scan) → +2

    Args:
        sql: SQL query string.

    Returns:
        Integer risk score (typically 0–4 for standard queries; can exceed
        this if a query contains multiple JOIN clauses).
    """
    sql_lower = sql.lower()
    risk = 0
    if "group by" in sql_lower:
        risk += 1
    if "join" in sql_lower:
        risk += 1
    if "where" not in sql_lower:
        risk += 2  # full-table scan
    logger.debug("Estimated spool risk for query: {}", risk)
    return risk


def get_session_limit() -> int:
    """
    Return the maximum number of concurrent Teradata sessions to allow.

    This value can be sourced from configuration or queried from DBC.  The
    default is ``10``.

    Returns:
        Maximum concurrent session count.
    """
    return 10


# ---------------------------------------------------------------------------
#  Base Class
# ---------------------------------------------------------------------------


class BaseGroupByRunner(ABC):
    """
    Abstract base class for all GroupBy runner strategies.

    Manages an optional volatile-table subset that can be materialised once
    and then referenced by every downstream query, reducing repeated full-table
    scans.

    Args:
        engine: SQLAlchemy :class:`~sqlalchemy.engine.Engine` connected to
            Teradata.
        base_table: Name of the source table to read from.
        subset_filter: Optional SQL ``WHERE`` clause fragment (without the
            ``WHERE`` keyword) used when materialising the subset.
        subset_table: Name of the volatile table to create for the subset.
            Defaults to ``"vt_subset"``.
    """

    def __init__(
        self,
        engine: Engine,
        base_table: str,
        subset_filter: Optional[str] = None,
        subset_table: str = "vt_subset",
    ) -> None:
        self.engine = engine
        self.base_table = base_table
        self.subset_filter = subset_filter
        self.subset_table = subset_table

    def create_subset(self) -> None:
        """
        Materialise a volatile-table subset of :attr:`base_table`.

        The table is created with ``ON COMMIT PRESERVE ROWS`` so that it
        persists for the duration of the session.
        """
        logger.info(
            "Creating volatile subset table '{}' from '{}'",
            self.subset_table,
            self.base_table,
        )
        where_clause = f"WHERE {self.subset_filter}" if self.subset_filter else ""
        sql = f"""
            CREATE VOLATILE TABLE {self.subset_table} AS (
                SELECT *
                FROM {self.base_table}
                {where_clause}
            ) WITH DATA
            PRIMARY INDEX (1)
            ON COMMIT PRESERVE ROWS;
        """
        with self.engine.begin() as conn:
            conn.execute(text(sql))
        logger.info(
            "Volatile subset table '{}' created successfully", self.subset_table
        )

    @abstractmethod
    def run(self, queries: List[str], materialise_subset: bool = True) -> object:
        """
        Execute the list of aggregation queries and return results.

        Args:
            queries: List of SQL strings to execute.
            materialise_subset: When ``True``, call :meth:`create_subset`
                before running queries.

        Returns:
            Runner-specific result object (list of DataFrames or a single
            DataFrame for server-side runners).
        """


# ---------------------------------------------------------------------------
#  Sequential Runner
# ---------------------------------------------------------------------------


class SequentialGroupByRunner(BaseGroupByRunner):
    """
    Execute aggregation queries sequentially in a single connection.

    This is the simplest strategy and is best for small query lists or
    low-cost queries where concurrency overhead is not justified.

    Args:
        engine: SQLAlchemy engine connected to Teradata.
        base_table: Name of the source table.
        subset_filter: Optional ``WHERE`` clause fragment.
        subset_table: Name of the volatile subset table.
    """

    def run(
        self, queries: List[str], materialise_subset: bool = True
    ) -> List[pd.DataFrame]:
        """
        Run all *queries* one after another.

        Args:
            queries: SQL strings to execute.
            materialise_subset: Create the volatile subset before querying.

        Returns:
            List of :class:`pandas.DataFrame`, one per query, in input order.
        """
        logger.info("SequentialGroupByRunner: running {} queries", len(queries))
        if materialise_subset:
            self.create_subset()

        results: List[pd.DataFrame] = []
        with self.engine.begin() as conn:
            for idx, sql in enumerate(queries, start=1):
                logger.debug("Executing query {}/{}", idx, len(queries))
                df = pd.read_sql(text(sql), conn)
                results.append(df)
                logger.debug("Query {}/{} returned {} rows", idx, len(queries), len(df))

        logger.info("SequentialGroupByRunner: all queries completed")
        return results


# ---------------------------------------------------------------------------
#  Parallel Runner (ThreadPool + SQLAlchemy Pooling)
# ---------------------------------------------------------------------------


class ParallelGroupByRunner(BaseGroupByRunner):
    """
    Execute aggregation queries concurrently via a ``ThreadPoolExecutor``.

    Each thread borrows a connection from the SQLAlchemy connection pool,
    so the *max_workers* value should not exceed the pool capacity.

    Args:
        engine: SQLAlchemy engine connected to Teradata.
        base_table: Name of the source table.
        subset_filter: Optional ``WHERE`` clause fragment.
        subset_table: Name of the volatile subset table.
        max_workers: Maximum number of worker threads.  Defaults to ``6``.
    """

    def __init__(
        self,
        engine: Engine,
        base_table: str,
        subset_filter: Optional[str] = None,
        subset_table: str = "vt_subset",
        max_workers: int = 6,
    ) -> None:
        super().__init__(engine, base_table, subset_filter, subset_table)
        self.max_workers = max_workers

    def _run_single(self, sql: str) -> pd.DataFrame:
        """
        Execute a single query in its own connection.

        Args:
            sql: SQL string to execute.

        Returns:
            :class:`pandas.DataFrame` with query results.
        """
        logger.debug("Thread executing query: {}", sql[:60])
        with self.engine.begin() as conn:
            return pd.read_sql(text(sql), conn)

    def run(
        self, queries: List[str], materialise_subset: bool = True
    ) -> List[pd.DataFrame]:
        """
        Run all *queries* concurrently using a thread pool.

        Args:
            queries: SQL strings to execute.
            materialise_subset: Create the volatile subset before querying.

        Returns:
            List of :class:`pandas.DataFrame`, one per query, in input order.
        """
        logger.info(
            "ParallelGroupByRunner: running {} queries with {} workers",
            len(queries),
            self.max_workers,
        )
        if materialise_subset:
            self.create_subset()

        with ThreadPoolExecutor(max_workers=self.max_workers) as pool:
            futures = [pool.submit(self._run_single, q) for q in queries]
            results = [f.result() for f in futures]

        logger.info("ParallelGroupByRunner: all queries completed")
        return results


# ---------------------------------------------------------------------------
#  Server-Side Runner (Dynamic SQL + Driver Table)
# ---------------------------------------------------------------------------


class ServerSideGroupByRunner(BaseGroupByRunner):
    """
    Execute aggregation queries server-side via a Teradata stored procedure.

    Queries are loaded into an ``agg_jobs`` driver table and dispatched by
    calling ``run_dynamic_aggs()``.  Results are collected from the
    ``agg_out`` output table.

    This strategy minimises client–server round-trips and is well-suited for
    large query lists or high-latency connections.

    Args:
        engine: SQLAlchemy engine connected to Teradata.
        base_table: Name of the source table.
        subset_filter: Optional ``WHERE`` clause fragment.
        subset_table: Name of the volatile subset table.
    """

    def __init__(
        self,
        engine: Engine,
        base_table: str,
        subset_filter: Optional[str] = None,
        subset_table: str = "vt_subset",
        agg_jobs_table: str = "test_agg_jobs",
        agg_out_table: str = "test_agg_out",
        runner_proc: str = "test_run_dynamic_aggs",
    ) -> None:
        super().__init__(engine, base_table, subset_filter, subset_table)
        self.agg_jobs_table = agg_jobs_table
        self.agg_out_table = agg_out_table
        self.runner_proc = runner_proc

        self.drop_tables_and_proc()

    # ------------------------------------------------------------------
    #  Schema helpers
    # ------------------------------------------------------------------

    def drop_tables_and_proc(self) -> None:
        """Drop the driver table, output table, and stored procedure if they exist."""
        logger.debug("Dropping existing tables and procedure if they exist")
        try:
            with self.engine.begin() as conn:
                conn.execute(text(f"DROP TABLE {self.agg_jobs_table}"))
        except Exception as e:
            logger.warning(
                "Could not drop driver table '{}': {}", self.agg_jobs_table, e
            )

        try:
            with self.engine.begin() as conn:
                conn.execute(text(f"DROP TABLE {self.agg_out_table}"))
        except Exception as e:
            logger.warning(
                "Could not drop output table '{}': {}", self.agg_out_table, e
            )

        # try:
        #     with self.engine.begin() as conn:
        #         conn.execute(text(f"DROP PROCEDURE {self.runner_proc}"))
        # except Exception as e:
        #     logger.warning(
        #         "Could not drop stored procedure '{}': {}", self.runner_proc, e
        #     )

    def ensure_driver_table(self) -> None:
        """Create the driver table if it does not exist."""
        logger.debug(f"Ensuring driver table '{self.agg_jobs_table}' exists")
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    f"""
                    CREATE TABLE {self.agg_jobs_table} (
                        job_id INTEGER,
                        sql_text VARCHAR(32000)
                    );
                    """
                )
            )

    def ensure_output_table(self) -> None:
        """Create the output table if it does not exist."""
        logger.debug(f"Ensuring output table '{self.agg_out_table}' exists")
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    f"""
                    CREATE TABLE {self.agg_out_table} (
                        job_id INTEGER,
                        group_key_json VARCHAR(32000),
                        metric_name VARCHAR(200),
                        metric_value VARCHAR(200)
                    );
                    """
                )
            )

    def ensure_stored_procedure(self) -> None:
        """Create or replace the stored procedure."""
        logger.debug(f"Ensuring stored procedure '{self.runner_proc}' exists")
        with self.engine.begin() as conn:
            conn.execute(
                text(
                    f"""
                    REPLACE PROCEDURE {self.runner_proc}()
                    --SQL SECURITY INVOKER
                    BEGIN
                        DECLARE stmt VARCHAR(32000);
                        FOR cur AS c1 CURSOR FOR
                            SELECT sql_text FROM {self.agg_jobs_table} ORDER BY job_id
                        DO
                            SET stmt = cur.sql_text;
                            CALL DBC.SysExecSQL(:stmt);
                        END FOR;
                    END;
                    """
                )
            )

    # ------------------------------------------------------------------
    #  Data helpers
    # ------------------------------------------------------------------

    def validate_queries(self, queries: List[str]) -> None:
        """
        Verify that every query references the subset table.

        Args:
            queries: SQL strings to validate.

        Raises:
            ValueError: If any query does not reference :attr:`subset_table`.
        """
        for q in queries:
            if self.subset_table.lower() not in q.lower():
                raise ValueError(
                    f"Query does not reference subset table "
                    f"'{self.subset_table}': {q}"
                )

    def load_driver_table(self, queries: List[str]) -> None:
        """
        Populate the driver table with *queries*.

        Any existing rows are deleted first.

        Args:
            queries: SQL strings to load.
        """
        logger.info(
            f"Loading {len(queries)} queries into driver table '{self.agg_jobs_table}'"
        )
        with self.engine.begin() as conn:
            conn.execute(text(f"DELETE FROM {self.agg_jobs_table}"))
            for job_id, sql in enumerate(queries, start=1):
                conn.execute(
                    text(
                        f"INSERT INTO {self.agg_jobs_table} (job_id, sql_text) VALUES (:id, :sql)"
                    ),
                    {"id": job_id, "sql": sql},
                )

    def execute_server_side(self) -> None:
        """Invoke the stored procedure."""
        logger.info(
            f"Calling stored procedure '{self.runner_proc}' to execute queries server-side"
        )
        with self.engine.begin() as conn:
            conn.execute(text(f"CALL {self.runner_proc}()"))

    def fetch_results(self) -> pd.DataFrame:
        """
        Retrieve results from the output table.

        Returns:
            :class:`pandas.DataFrame` containing all rows from output table,
            ordered by ``job_id``.
        """
        logger.info(f"Fetching results from '{self.agg_out_table}' output table")
        return pd.read_sql(
            f"SELECT * FROM {self.agg_out_table} ORDER BY job_id", self.engine
        )

    # ------------------------------------------------------------------
    #  Main run
    # ------------------------------------------------------------------

    def run(self, queries: List[str], materialise_subset: bool = True) -> pd.DataFrame:
        """
        Execute all *queries* server-side and return consolidated results.

        Args:
            queries: SQL strings to execute.  Each must reference
                :attr:`subset_table`.
            materialise_subset: Create the volatile subset before executing.

        Returns:
            :class:`pandas.DataFrame` from ``agg_out``, ordered by
            ``job_id``.

        Raises:
            ValueError: If any query does not reference :attr:`subset_table`.
        """
        logger.info(
            f"ServerSideGroupByRunner: starting run with {len(queries)} queries"
        )
        self.validate_queries(queries)
        self.ensure_driver_table()
        self.ensure_output_table()
        self.ensure_stored_procedure()

        if materialise_subset:
            self.create_subset()

        self.load_driver_table(queries)
        self.execute_server_side()
        result = self.fetch_results()
        logger.info(
            f"ServerSideGroupByRunner: run completed, {len(result)} rows fetched"
        )
        return result


# ---------------------------------------------------------------------------
#  Advanced Factory
# ---------------------------------------------------------------------------


def get_advanced_groupby_runner(
    engine: Engine,
    base_table: str,
    subset_filter: Optional[str],
    subset_table: str,
    queries: List[str],
) -> BaseGroupByRunner:
    """
    Select the optimal runner strategy based on query characteristics.

    Decision rules:

    1. **Sequential** – ``n ≤ 5``, ``max_cost ≤ 2``, ``max_spool ≤ 1``.
    2. **Parallel** – ``6 ≤ n ≤ 20``, ``avg_cost ≤ 3``, ``avg_spool ≤ 2``,
       ``session_limit ≥ 6``.
    3. **Server-side** – all other cases.

    Args:
        engine: SQLAlchemy engine connected to Teradata.
        base_table: Name of the source table.
        subset_filter: Optional ``WHERE`` clause fragment.
        subset_table: Name of the volatile subset table.
        queries: The SQL queries that will be executed; used only for
            heuristic scoring.

    Returns:
        A concrete :class:`BaseGroupByRunner` instance.
    """
    n = len(queries)
    costs = [estimate_query_cost(q) for q in queries]
    spool_risks = [estimate_spool_risk(q) for q in queries]

    avg_cost = sum(costs) / n
    max_cost = max(costs)
    avg_spool = sum(spool_risks) / n
    max_spool = max(spool_risks)

    session_limit = get_session_limit()

    logger.info(
        f"Factory: n={n}, avg_cost={avg_cost:.2f}, max_cost={max_cost}, avg_spool={avg_spool:.2f}, "
        f"max_spool={max_spool}, session_limit={session_limit}"
    )

    # Strategy 1: Sequential
    if n <= 5 and max_cost <= 2 and max_spool <= 1:
        logger.info("Factory: selected SequentialGroupByRunner")
        return SequentialGroupByRunner(engine, base_table, subset_filter, subset_table)

    # Strategy 2: Client-side parallel
    if 6 <= n <= 20 and avg_cost <= 3 and avg_spool <= 2 and session_limit >= 6:
        logger.info("Factory: selected ParallelGroupByRunner")
        return ParallelGroupByRunner(
            engine, base_table, subset_filter, subset_table, max_workers=6
        )

    # Strategy 3: Server-side
    logger.info("Factory: selected ServerSideGroupByRunner")
    return ServerSideGroupByRunner(engine, base_table, subset_filter, subset_table)
