"""Tests for SQLAlchemyClient."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, Mock, patch

import pandas as pd
import pytest

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_query_lib import DatabaseConfig, SQLAlchemyClient
from db_query_lib.exceptions import DatabaseConnectionError, QueryExecutionError


class TestSQLAlchemyClient:
    """Test cases for SQLAlchemyClient."""

    def test_init_with_valid_config(self, mock_database_config):
        """Test client initialization with valid config."""
        with patch(
            "db_query_lib.sqlalchemy_client.create_engine"
        ) as mock_create_engine:
            mock_engine = MagicMock()
            mock_create_engine.return_value = mock_engine

            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__ = MagicMock(
                return_value=mock_conn
            )
            mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
            mock_result = MagicMock()
            mock_result.scalar.return_value = "TEST_DB"
            mock_conn.execute.return_value = mock_result

            client = SQLAlchemyClient(mock_database_config)
            assert client.engine is not None
            assert client.pool_size == 5
            assert client.max_overflow == 10

    def test_init_with_custom_pool_settings(self, mock_database_config):
        """Test client initialization with custom pool settings."""
        with patch(
            "db_query_lib.sqlalchemy_client.create_engine"
        ) as mock_create_engine:
            mock_engine = MagicMock()
            mock_create_engine.return_value = mock_engine

            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__ = MagicMock(
                return_value=mock_conn
            )
            mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
            mock_result = MagicMock()
            mock_result.scalar.return_value = "TEST_DB"
            mock_conn.execute.return_value = mock_result

            client = SQLAlchemyClient(
                mock_database_config, pool_size=10, max_overflow=20
            )
            assert client.pool_size == 10
            assert client.max_overflow == 20

    def test_execute_query_success(self, mock_database_config):
        """Test successful query execution."""
        test_df = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})

        with patch(
            "db_query_lib.sqlalchemy_client.create_engine"
        ) as mock_create_engine:
            mock_engine = MagicMock()
            mock_create_engine.return_value = mock_engine

            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__ = MagicMock(
                return_value=mock_conn
            )
            mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
            mock_result = MagicMock()
            mock_result.scalar.return_value = "TEST_DB"
            mock_conn.execute.return_value = mock_result

            with patch("db_query_lib.sqlalchemy_client.pd.read_sql") as mock_read_sql:
                mock_read_sql.return_value = test_df

                client = SQLAlchemyClient(mock_database_config)
                result = client.execute_query("SELECT * FROM test")

                assert isinstance(result, pd.DataFrame)
                assert len(result) == 2
                mock_read_sql.assert_called()

    def test_execute_query_scalar_success(self, mock_database_config):
        """Test successful scalar query execution."""
        with patch(
            "db_query_lib.sqlalchemy_client.create_engine"
        ) as mock_create_engine:
            mock_engine = MagicMock()
            mock_create_engine.return_value = mock_engine

            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__ = MagicMock(
                return_value=mock_conn
            )
            mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)

            mock_result1 = MagicMock()
            mock_result1.scalar.return_value = "TEST_DB"
            mock_result2 = MagicMock()
            mock_result2.scalar.return_value = 42

            mock_conn.execute.side_effect = [mock_result1, mock_result2]

            client = SQLAlchemyClient(mock_database_config)
            result = client.execute_query_scalar("SELECT COUNT(*)")

            assert result == 42

    def test_execute_query_dict_success(self, mock_database_config):
        """Test successful dict query execution."""
        test_df = pd.DataFrame({"id": [1, 2], "name": ["Alice", "Bob"]})

        with patch(
            "db_query_lib.sqlalchemy_client.create_engine"
        ) as mock_create_engine:
            mock_engine = MagicMock()
            mock_create_engine.return_value = mock_engine

            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__ = MagicMock(
                return_value=mock_conn
            )
            mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
            mock_result = MagicMock()
            mock_result.scalar.return_value = "TEST_DB"
            mock_conn.execute.return_value = mock_result

            with patch("db_query_lib.sqlalchemy_client.pd.read_sql") as mock_read_sql:
                mock_read_sql.return_value = test_df

                client = SQLAlchemyClient(mock_database_config)
                result = client.execute_query_dict("SELECT * FROM test")

                assert isinstance(result, list)
                assert len(result) == 2
                assert all(isinstance(row, dict) for row in result)

    def test_get_pool_status(self, mock_database_config):
        """Test getting pool status information."""
        with patch(
            "db_query_lib.sqlalchemy_client.create_engine"
        ) as mock_create_engine:
            mock_engine = MagicMock()
            mock_pool = MagicMock()
            mock_pool.checkedout.return_value = 3
            mock_engine.pool = mock_pool
            mock_create_engine.return_value = mock_engine

            mock_conn = MagicMock()
            mock_engine.connect.return_value.__enter__ = MagicMock(
                return_value=mock_conn
            )
            mock_engine.connect.return_value.__exit__ = MagicMock(return_value=False)
            mock_result = MagicMock()
            mock_result.scalar.return_value = "TEST_DB"
            mock_conn.execute.return_value = mock_result

            client = SQLAlchemyClient(mock_database_config)
            status = client.get_pool_status()

            assert status["pool_size"] == 5
            assert status["max_overflow"] == 10
            assert status["checked_out"] == 3


class TestDatabaseConfig:
    """Test cases for DatabaseConfig."""

    def test_config_from_env(self, mock_env_vars):
        """Test creating config from environment variables."""
        config = DatabaseConfig.from_env(required=False)

        assert config.host == "test-host.com"
        assert config.user == "test_user"
        assert config.password == "test_password"
        assert config.database == "TEST_DB"

    def test_connection_string_generation(self, mock_database_config):
        """Test SQLAlchemy connection string generation."""
        conn_str = mock_database_config.get_sqlalchemy_connection_string()

        assert "teradatasql://" in conn_str
        assert "test_user" in conn_str
        assert "test-host.com" in conn_str
        assert "TEST_DB" in conn_str

    def test_teradataml_params(self, mock_database_config):
        """Test Teradataml parameter generation."""
        params = mock_database_config.get_teradataml_params()

        assert params["host"] == "test-host.com"
        assert params["username"] == "test_user"
        assert params["password"] == "test_password"
        assert params["database"] == "TEST_DB"
        assert params["database"] == "TEST_DB"
