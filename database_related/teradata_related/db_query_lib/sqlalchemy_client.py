"""SQLAlchemy database client with sync and threadpool support."""

from typing import Any, Dict, List, Optional

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.pool import QueuePool

from .config import DatabaseConfig
from .exceptions import DatabaseConnectionError, QueryExecutionError


class SQLAlchemyClient:
    """SQLAlchemy client for Teradata database operations."""

    def __init__(
        self,
        config: DatabaseConfig,
        pool_size: int = 5,
        max_overflow: int = 10,
        pool_timeout: float = 30.0,
        pool_pre_ping: bool = True,
    ):
        """
        Initialize SQLAlchemy client with connection pool.

        Args:
            config: DatabaseConfig instance
            pool_size: Number of connections to maintain
            max_overflow: Number of additional connections allowed
            pool_timeout: Timeout for acquiring connection from pool
            pool_pre_ping: Test connections before using (ping before checkout)
        """
        self.config = config
        self.pool_size = pool_size
        self.max_overflow = max_overflow

        try:
            connection_string = config.get_sqlalchemy_connection_string()
            self.engine: Engine = create_engine(
                connection_string,
                echo=False,
                poolclass=QueuePool,
                pool_size=pool_size,
                max_overflow=max_overflow,
                pool_timeout=pool_timeout,
                pool_pre_ping=pool_pre_ping,
                pool_recycle=1800,
            )
            self._test_connection()
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to create SQLAlchemy engine: {e}")

    def _test_connection(self) -> None:
        """Test that connection works."""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text("SELECT database"))
                db_name = result.scalar()
                print(f"✓ Connected to Teradata database: {db_name}")
        except Exception as e:
            raise DatabaseConnectionError(f"Connection test failed: {e}")

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a SQL query and return results as DataFrame.

        Args:
            query: SQL query string

        Returns:
            pandas DataFrame with results

        Raises:
            QueryExecutionError: If query execution fails
        """
        try:
            df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            raise QueryExecutionError(f"Query execution failed: {e}")

    def execute_query_scalar(self, query: str) -> Any:
        """
        Execute query and return single scalar value.

        Args:
            query: SQL query string

        Returns:
            Scalar value from first row, first column

        Raises:
            QueryExecutionError: If query execution fails
        """
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(query))
                return result.scalar()
        except Exception as e:
            raise QueryExecutionError(f"Scalar query execution failed: {e}")

    def execute_query_dict(self, query: str) -> List[Dict]:
        """
        Execute query and return results as list of dicts.

        Args:
            query: SQL query string

        Returns:
            List of dictionaries with column names as keys

        Raises:
            QueryExecutionError: If query execution fails
        """
        try:
            df = self.execute_query(query)
            return df.to_dict("records")
        except Exception as e:
            raise QueryExecutionError(f"Dict query execution failed: {e}")

    def execute_many(self, queries: List[str]) -> List[Optional[pd.DataFrame]]:
        """
        Execute multiple queries sequentially.

        Args:
            queries: List of SQL query strings

        Returns:
            List of DataFrames for each query
        """
        results = []
        for query in queries:
            try:
                results.append(self.execute_query(query))
            except QueryExecutionError as e:
                print(f"Warning: Query failed: {e}")
                results.append(None)
        return results

    def close(self) -> None:
        """Close all connections in the pool."""
        try:
            self.engine.dispose()
            print("✓ Connection pool disposed")
        except Exception as e:
            raise DatabaseConnectionError(f"Error closing connections: {e}")

    def get_pool_status(self) -> Dict[str, Any]:
        """Get connection pool status information."""
        pool = self.engine.pool
        return {
            "pool_size": self.pool_size,
            "max_overflow": self.max_overflow,
            "checked_out": pool.checkedout() if hasattr(pool, "checkedout") else None,
            "pool_type": type(pool).__name__,
        }
