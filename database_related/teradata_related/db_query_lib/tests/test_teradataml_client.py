"""Tests for TeradataMLClient."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_query_lib import DatabaseConfig, TeradataMLClient
from db_query_lib.exceptions import DatabaseConnectionError, QueryExecutionError


class TestTeradataMLClient:
    """Test cases for TeradataMLClient."""

    def test_init_with_valid_config(self, mock_database_config):
        """Test client initialization with valid config."""
        with patch("db_query_lib.teradataml_client.create_context") as mock_ctx:
            with patch("db_query_lib.teradataml_client.execute_sql") as mock_exec_sql:
                mock_cursor = MagicMock()
                mock_cursor.fetchone.return_value = ["TEST_DB"]
                mock_exec_sql.return_value = mock_cursor

                with patch("db_query_lib.teradataml_client.remove_context"):
                    client = TeradataMLClient(mock_database_config)
                    assert client.context is not None

    def test_init_without_teradataml_installed(self, mock_database_config):
        """Test initialization fails gracefully without teradataml."""
        with patch.dict("sys.modules", {"teradataml": None}):
            with pytest.raises(DatabaseConnectionError) as exc_info:
                # Force import error
                with patch(
                    "db_query_lib.teradataml_client.create_context",
                    side_effect=ImportError,
                ):
                    TeradataMLClient(mock_database_config)

            assert "teradataml" in str(exc_info.value).lower()

    def test_execute_query_success(self, mock_database_config):
        """Test successful query execution."""
        test_result = [("Alice", 100), ("Bob", 200)]

        with patch("db_query_lib.teradataml_client.create_context"):
            with patch("db_query_lib.teradataml_client.execute_sql") as mock_exec_sql:
                mock_cursor = MagicMock()
                mock_cursor.fetchone.return_value = ["TEST_DB"]
                mock_cursor.fetchall.return_value = test_result
                mock_exec_sql.return_value = mock_cursor

                with patch("db_query_lib.teradataml_client.remove_context"):
                    client = TeradataMLClient(mock_database_config)

                    # Reset mock for actual query test
                    mock_exec_sql.reset_mock()
                    mock_cursor.fetchall.return_value = test_result
                    mock_exec_sql.return_value = mock_cursor

                    result = client.execute_query("SELECT * FROM test")
                    assert result == test_result

    def test_execute_query_scalar_success(self, mock_database_config):
        """Test successful scalar query execution."""
        with patch("db_query_lib.teradataml_client.create_context"):
            with patch("db_query_lib.teradataml_client.execute_sql") as mock_exec_sql:
                mock_cursor = MagicMock()
                mock_cursor.fetchone.side_effect = [["TEST_DB"], [42]]
                mock_exec_sql.return_value = mock_cursor

                with patch("db_query_lib.teradataml_client.remove_context"):
                    client = TeradataMLClient(mock_database_config)
                    result = client.execute_query_scalar("SELECT COUNT(*)")
                    assert result == 42

    def test_execute_query_dict_success(self, mock_database_config):
        """Test successful dict query execution."""
        test_data = [("Alice", 100), ("Bob", 200)]

        with patch("db_query_lib.teradataml_client.create_context"):
            with patch("db_query_lib.teradataml_client.execute_sql") as mock_exec_sql:
                mock_cursor = MagicMock()
                mock_cursor.fetchone.return_value = ["TEST_DB"]
                mock_cursor.description = [
                    ("name", None),
                    ("value", None),
                ]
                mock_cursor.fetchall.return_value = test_data
                mock_exec_sql.return_value = mock_cursor

                with patch("db_query_lib.teradataml_client.remove_context"):
                    client = TeradataMLClient(mock_database_config)

                    # Reset mock for actual query test
                    mock_exec_sql.reset_mock()
                    mock_cursor.fetchall.return_value = test_data
                    mock_exec_sql.return_value = mock_cursor

                    result = client.execute_query_dict("SELECT * FROM test")

                    assert isinstance(result, list)
                    assert len(result) == 2
                    assert all(isinstance(row, dict) for row in result)

    def test_close_context(self, mock_database_config):
        """Test closing the Teradataml context."""
        with patch("db_query_lib.teradataml_client.create_context"):
            with patch("db_query_lib.teradataml_client.execute_sql") as mock_exec_sql:
                mock_cursor = MagicMock()
                mock_cursor.fetchone.return_value = ["TEST_DB"]
                mock_exec_sql.return_value = mock_cursor

                with patch(
                    "db_query_lib.teradataml_client.remove_context"
                ) as mock_remove:
                    client = TeradataMLClient(mock_database_config)
                    client.close()

                    mock_remove.assert_called()
                    assert client.context is None

    def test_context_manager(self, mock_database_config):
        """Test using client as context manager."""
        with patch("db_query_lib.teradataml_client.create_context"):
            with patch("db_query_lib.teradataml_client.execute_sql") as mock_exec_sql:
                mock_cursor = MagicMock()
                mock_cursor.fetchone.return_value = ["TEST_DB"]
                mock_exec_sql.return_value = mock_cursor

                with patch(
                    "db_query_lib.teradataml_client.remove_context"
                ) as mock_remove:
                    with TeradataMLClient(mock_database_config) as client:
                        assert client.context is not None

                    mock_remove.assert_called()
                    mock_remove.assert_called()
