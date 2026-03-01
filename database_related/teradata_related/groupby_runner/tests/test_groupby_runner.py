"""Tests for groupby_runner module (mocked DB calls)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, call, patch

import pandas as pd
import pytest

# ---------------------------------------------------------------------------
# Ensure the teradata_related package is importable from this test file
# ---------------------------------------------------------------------------
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

from database_related.teradata_related.groupby_runner import (
    BaseGroupByRunner,
    ParallelGroupByRunner,
    SequentialGroupByRunner,
    ServerSideGroupByRunner,
    estimate_query_cost,
    estimate_spool_risk,
    get_advanced_groupby_runner,
    get_session_limit,
)


# ---------------------------------------------------------------------------
#  Helpers / fixtures
# ---------------------------------------------------------------------------


def _make_engine():
    """Return a MagicMock that behaves like a minimal SQLAlchemy engine."""
    engine = MagicMock()
    conn = MagicMock()
    ctx = MagicMock()
    ctx.__enter__ = MagicMock(return_value=conn)
    ctx.__exit__ = MagicMock(return_value=False)
    engine.begin.return_value = ctx
    return engine, conn


@pytest.fixture
def mock_engine():
    engine, _ = _make_engine()
    return engine


@pytest.fixture
def sample_df():
    return pd.DataFrame({"col": [1, 2, 3]})


SIMPLE_QUERY = "SELECT colA, COUNT(*) AS cnt FROM vt_subset GROUP BY colA"
FULL_SCAN_QUERY = "SELECT col FROM big_table"


# ---------------------------------------------------------------------------
#  estimate_query_cost
# ---------------------------------------------------------------------------


class TestEstimateQueryCost:
    def test_empty_query(self):
        assert estimate_query_cost("SELECT 1") == 0

    def test_join_adds_two(self):
        assert estimate_query_cost("SELECT * FROM a JOIN b ON a.id = b.id") == 2

    def test_group_by_adds_two(self):
        assert estimate_query_cost("SELECT x, COUNT(*) FROM t GROUP BY x") == 3  # GROUP BY + COUNT

    def test_distinct_adds_one(self):
        assert estimate_query_cost("SELECT DISTINCT col FROM t") == 1

    def test_aggregate_functions(self):
        assert estimate_query_cost("SELECT SUM(x) FROM t") == 1
        assert estimate_query_cost("SELECT AVG(x) FROM t") == 1
        assert estimate_query_cost("SELECT COUNT(*) FROM t") == 1

    def test_complex_query_max_cost(self):
        sql = "SELECT DISTINCT a, SUM(b) FROM t JOIN s ON t.id = s.id GROUP BY a"
        cost = estimate_query_cost(sql)
        assert cost == 6  # join(2) + group by(2) + distinct(1) + SUM(1)

    def test_case_insensitive(self):
        assert estimate_query_cost("select * from a JOIN b on a.id=b.id") == 2


# ---------------------------------------------------------------------------
#  estimate_spool_risk
# ---------------------------------------------------------------------------


class TestEstimateSpoolRisk:
    def test_no_risk_query(self):
        # Has WHERE, no JOIN, no GROUP BY
        assert estimate_spool_risk("SELECT x FROM t WHERE x = 1") == 0

    def test_group_by_adds_one(self):
        assert estimate_spool_risk("SELECT x FROM t WHERE x=1 GROUP BY x") == 1

    def test_join_adds_one(self):
        assert estimate_spool_risk("SELECT * FROM a JOIN b ON a.id=b.id WHERE 1=1") == 1

    def test_no_where_adds_two(self):
        assert estimate_spool_risk("SELECT col FROM big_table") == 2

    def test_full_scan_join_group_by_max(self):
        sql = "SELECT a, COUNT(*) FROM t JOIN s ON t.id=s.id GROUP BY a"
        assert estimate_spool_risk(sql) == 4  # group_by(1)+join(1)+no_where(2)

    def test_case_insensitive(self):
        assert estimate_spool_risk("SELECT col FROM t GROUP BY col WHERE col>0") == 1


# ---------------------------------------------------------------------------
#  get_session_limit
# ---------------------------------------------------------------------------


class TestGetSessionLimit:
    def test_returns_integer(self):
        assert isinstance(get_session_limit(), int)
        assert get_session_limit() >= 1


# ---------------------------------------------------------------------------
#  BaseGroupByRunner.create_subset
# ---------------------------------------------------------------------------


class TestCreateSubset:
    def test_create_subset_without_filter(self, mock_engine):
        runner = SequentialGroupByRunner(mock_engine, "big_table")
        runner.create_subset()
        mock_engine.begin.assert_called()

    def test_create_subset_with_filter(self, mock_engine):
        runner = SequentialGroupByRunner(
            mock_engine, "big_table", subset_filter="event_date >= DATE - 30"
        )
        runner.create_subset()
        # Verify connection was used
        mock_engine.begin.assert_called()


# ---------------------------------------------------------------------------
#  SequentialGroupByRunner
# ---------------------------------------------------------------------------


class TestSequentialGroupByRunner:
    def test_run_returns_list_of_dataframes(self, mock_engine, sample_df):
        with patch(
            "database_related.teradata_related.groupby_runner.runner.pd.read_sql",
            return_value=sample_df,
        ) as mock_read:
            runner = SequentialGroupByRunner(mock_engine, "big_table")
            results = runner.run([SIMPLE_QUERY, SIMPLE_QUERY], materialise_subset=False)

        assert isinstance(results, list)
        assert len(results) == 2
        assert all(isinstance(df, pd.DataFrame) for df in results)
        assert mock_read.call_count == 2

    def test_run_calls_create_subset_when_flag_true(self, mock_engine, sample_df):
        with patch(
            "database_related.teradata_related.groupby_runner.runner.pd.read_sql",
            return_value=sample_df,
        ):
            runner = SequentialGroupByRunner(mock_engine, "big_table")
            with patch.object(runner, "create_subset") as mock_cs:
                runner.run([SIMPLE_QUERY], materialise_subset=True)
                mock_cs.assert_called_once()

    def test_run_skips_create_subset_when_flag_false(self, mock_engine, sample_df):
        with patch(
            "database_related.teradata_related.groupby_runner.runner.pd.read_sql",
            return_value=sample_df,
        ):
            runner = SequentialGroupByRunner(mock_engine, "big_table")
            with patch.object(runner, "create_subset") as mock_cs:
                runner.run([SIMPLE_QUERY], materialise_subset=False)
                mock_cs.assert_not_called()

    def test_run_empty_queries(self, mock_engine):
        runner = SequentialGroupByRunner(mock_engine, "big_table")
        results = runner.run([], materialise_subset=False)
        assert results == []

    def test_default_subset_table_name(self, mock_engine):
        runner = SequentialGroupByRunner(mock_engine, "big_table")
        assert runner.subset_table == "vt_subset"

    def test_custom_subset_table_name(self, mock_engine):
        runner = SequentialGroupByRunner(
            mock_engine, "big_table", subset_table="my_subset"
        )
        assert runner.subset_table == "my_subset"


# ---------------------------------------------------------------------------
#  ParallelGroupByRunner
# ---------------------------------------------------------------------------


class TestParallelGroupByRunner:
    def test_run_returns_list_of_dataframes(self, mock_engine, sample_df):
        with patch(
            "database_related.teradata_related.groupby_runner.runner.pd.read_sql",
            return_value=sample_df,
        ) as mock_read:
            runner = ParallelGroupByRunner(mock_engine, "big_table", max_workers=2)
            results = runner.run([SIMPLE_QUERY, SIMPLE_QUERY], materialise_subset=False)

        assert isinstance(results, list)
        assert len(results) == 2
        assert all(isinstance(df, pd.DataFrame) for df in results)
        assert mock_read.call_count == 2

    def test_default_max_workers(self, mock_engine):
        runner = ParallelGroupByRunner(mock_engine, "big_table")
        assert runner.max_workers == 6

    def test_custom_max_workers(self, mock_engine):
        runner = ParallelGroupByRunner(mock_engine, "big_table", max_workers=3)
        assert runner.max_workers == 3

    def test_run_calls_create_subset_when_flag_true(self, mock_engine, sample_df):
        with patch(
            "database_related.teradata_related.groupby_runner.runner.pd.read_sql",
            return_value=sample_df,
        ):
            runner = ParallelGroupByRunner(mock_engine, "big_table")
            with patch.object(runner, "create_subset") as mock_cs:
                runner.run([SIMPLE_QUERY], materialise_subset=True)
                mock_cs.assert_called_once()

    def test_run_skips_create_subset_when_flag_false(self, mock_engine, sample_df):
        with patch(
            "database_related.teradata_related.groupby_runner.runner.pd.read_sql",
            return_value=sample_df,
        ):
            runner = ParallelGroupByRunner(mock_engine, "big_table")
            with patch.object(runner, "create_subset") as mock_cs:
                runner.run([SIMPLE_QUERY], materialise_subset=False)
                mock_cs.assert_not_called()


# ---------------------------------------------------------------------------
#  ServerSideGroupByRunner
# ---------------------------------------------------------------------------


class TestServerSideGroupByRunner:
    def _make_runner(self, engine=None):
        if engine is None:
            engine, _ = _make_engine()
        return ServerSideGroupByRunner(
            engine, "big_table", subset_table="vt_subset"
        )

    def test_validate_queries_passes_when_subset_table_present(self):
        runner = self._make_runner()
        # Should not raise
        runner.validate_queries(
            ["SELECT colA FROM vt_subset GROUP BY colA"]
        )

    def test_validate_queries_raises_when_subset_table_missing(self):
        runner = self._make_runner()
        with pytest.raises(ValueError, match="vt_subset"):
            runner.validate_queries(["SELECT colA FROM other_table GROUP BY colA"])

    def test_validate_queries_case_insensitive(self):
        runner = self._make_runner()
        # Upper-case reference should still pass
        runner.validate_queries(["SELECT colA FROM VT_SUBSET GROUP BY colA"])

    def test_ensure_driver_table(self, mock_engine):
        runner = self._make_runner(mock_engine)
        runner.ensure_driver_table()
        mock_engine.begin.assert_called()

    def test_ensure_output_table(self, mock_engine):
        runner = self._make_runner(mock_engine)
        runner.ensure_output_table()
        mock_engine.begin.assert_called()

    def test_ensure_stored_procedure(self, mock_engine):
        runner = self._make_runner(mock_engine)
        runner.ensure_stored_procedure()
        mock_engine.begin.assert_called()

    def test_load_driver_table(self, mock_engine):
        runner = self._make_runner(mock_engine)
        queries = [
            "SELECT a FROM vt_subset GROUP BY a",
            "SELECT b FROM vt_subset GROUP BY b",
        ]
        runner.load_driver_table(queries)
        # begin() should have been called for the load transaction
        mock_engine.begin.assert_called()

    def test_execute_server_side(self, mock_engine):
        runner = self._make_runner(mock_engine)
        runner.execute_server_side()
        mock_engine.begin.assert_called()

    def test_fetch_results(self, mock_engine, sample_df):
        runner = self._make_runner(mock_engine)
        with patch(
            "database_related.teradata_related.groupby_runner.runner.pd.read_sql",
            return_value=sample_df,
        ) as mock_read:
            result = runner.fetch_results()
        assert isinstance(result, pd.DataFrame)
        mock_read.assert_called_once()

    def test_run_full_flow(self, mock_engine, sample_df):
        """Full run: all helper methods called in order."""
        runner = self._make_runner(mock_engine)
        queries = ["SELECT a FROM vt_subset GROUP BY a"]

        with patch.object(runner, "validate_queries") as mock_vq, \
             patch.object(runner, "ensure_driver_table") as mock_edt, \
             patch.object(runner, "ensure_output_table") as mock_eot, \
             patch.object(runner, "ensure_stored_procedure") as mock_esp, \
             patch.object(runner, "create_subset") as mock_cs, \
             patch.object(runner, "load_driver_table") as mock_ldt, \
             patch.object(runner, "execute_server_side") as mock_ess, \
             patch.object(runner, "fetch_results", return_value=sample_df) as mock_fr:

            result = runner.run(queries, materialise_subset=True)

        mock_vq.assert_called_once_with(queries)
        mock_edt.assert_called_once()
        mock_eot.assert_called_once()
        mock_esp.assert_called_once()
        mock_cs.assert_called_once()
        mock_ldt.assert_called_once_with(queries)
        mock_ess.assert_called_once()
        mock_fr.assert_called_once()
        assert isinstance(result, pd.DataFrame)

    def test_run_skips_subset_when_flag_false(self, mock_engine, sample_df):
        runner = self._make_runner(mock_engine)
        queries = ["SELECT a FROM vt_subset GROUP BY a"]

        with patch.object(runner, "validate_queries"), \
             patch.object(runner, "ensure_driver_table"), \
             patch.object(runner, "ensure_output_table"), \
             patch.object(runner, "ensure_stored_procedure"), \
             patch.object(runner, "create_subset") as mock_cs, \
             patch.object(runner, "load_driver_table"), \
             patch.object(runner, "execute_server_side"), \
             patch.object(runner, "fetch_results", return_value=sample_df):

            runner.run(queries, materialise_subset=False)

        mock_cs.assert_not_called()


# ---------------------------------------------------------------------------
#  get_advanced_groupby_runner (factory)
# ---------------------------------------------------------------------------


class TestGetAdvancedGroupByRunner:
    """Test the factory heuristic selection logic."""

    def test_selects_sequential_for_small_cheap_queries(self, mock_engine):
        # 2 simple queries with no joins, no group by → cost=0, spool=2 (no WHERE)
        # Use queries with WHERE to keep spool low
        queries = [
            "SELECT a FROM t WHERE a=1",
            "SELECT b FROM t WHERE b=2",
        ]
        runner = get_advanced_groupby_runner(
            mock_engine, "big_table", None, "vt_subset", queries
        )
        assert isinstance(runner, SequentialGroupByRunner)

    def test_selects_parallel_for_medium_queries(self, mock_engine):
        # Build 8 queries that sit in the parallel range:
        # avg_cost ≤ 3, avg_spool ≤ 2, session_limit >= 6
        # Each query: GROUP BY (cost +2, spool +1) + WHERE (spool stays at 1)
        base = "SELECT col{i}, COUNT(*) FROM t WHERE col{i}>0 GROUP BY col{i}"
        queries = [base.format(i=i) for i in range(8)]
        runner = get_advanced_groupby_runner(
            mock_engine, "big_table", None, "vt_subset", queries
        )
        assert isinstance(runner, ParallelGroupByRunner)

    def test_selects_server_side_for_large_query_list(self, mock_engine):
        # 30 queries → forces server-side
        base = "SELECT col{i} FROM t GROUP BY col{i}"
        queries = [base.format(i=i) for i in range(30)]
        runner = get_advanced_groupby_runner(
            mock_engine, "big_table", None, "vt_subset", queries
        )
        assert isinstance(runner, ServerSideGroupByRunner)

    def test_selects_server_side_for_high_cost_queries(self, mock_engine):
        # 5 queries but with high cost: JOIN + GROUP BY + SUM + DISTINCT = 6
        high_cost_q = (
            "SELECT DISTINCT a, SUM(b) FROM t JOIN s ON t.id=s.id "
            "WHERE x=1 GROUP BY a"
        )
        queries = [high_cost_q] * 5
        runner = get_advanced_groupby_runner(
            mock_engine, "big_table", None, "vt_subset", queries
        )
        # max_cost=6 > 2 → not sequential; n=5 < 6 → not parallel → server-side
        assert isinstance(runner, ServerSideGroupByRunner)

    def test_runner_attributes_propagated(self, mock_engine):
        queries = ["SELECT a FROM t WHERE a=1"]
        runner = get_advanced_groupby_runner(
            mock_engine, "my_table", "dt >= DATE - 7", "my_subset", queries
        )
        assert runner.engine is mock_engine
        assert runner.base_table == "my_table"
        assert runner.subset_filter == "dt >= DATE - 7"
        assert runner.subset_table == "my_subset"
