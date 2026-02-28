"""Database Query Library - SQLAlchemy and Teradataml with threadpool support."""

from .config import DatabaseConfig
from .exceptions import (
    ConfigurationError,
    DatabaseConnectionError,
    QueryExecutionError,
    ThreadPoolExecutionError,
)
from .sqlalchemy_client import SQLAlchemyClient
from .teradataml_client import TeradataMLClient
from .threadpool_executor import ExecutionResult, ThreadPoolQueryExecutor

__version__ = "0.1.0"
__all__ = [
    "DatabaseConfig",
    "SQLAlchemyClient",
    "TeradataMLClient",
    "ThreadPoolQueryExecutor",
    "ExecutionResult",
    "ConfigurationError",
    "DatabaseConnectionError",
    "QueryExecutionError",
    "ThreadPoolExecutionError",
]
