"""Pytest configuration and fixtures."""

import os
from unittest.mock import MagicMock, Mock, patch

import pytest


@pytest.fixture
def mock_env_vars(monkeypatch):
    """Mock environment variables for testing."""
    env_vars = {
        "TERADATA_HOST": "test-host.com",
        "TERADATA_USER": "test_user",
        "TERADATA_PASSWORD": "test_password",
        "TERADATA_DATABASE": "TEST_DB",
        "TERADATA_LOGMECH": "TD2",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars


@pytest.fixture
def mock_database_config(mock_env_vars):
    """Create a mock DatabaseConfig from environment variables."""
    from db_query_lib import DatabaseConfig

    return DatabaseConfig.from_env(required=False)


@pytest.fixture
def mock_sqlalchemy_engine():
    """Create a mock SQLAlchemy engine."""
    engine = MagicMock()
    pool = MagicMock()
    pool.checkedout.return_value = 2
    engine.pool = pool
    return engine


@pytest.fixture
def mock_executing_query_result():
    """Create a mock query result."""
    import pandas as pd

    return pd.DataFrame(
        {
            "id": [1, 2, 3],
            "name": ["Alice", "Bob", "Charlie"],
            "value": [100, 200, 300],
        }
    )
