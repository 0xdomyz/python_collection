"""Teradataml database client with sync and threadpool support."""

from typing import Any, Dict, List, Optional

from .config import DatabaseConfig
from .exceptions import DatabaseConnectionError, QueryExecutionError

# Try to import teradataml at module level
try:
    from teradataml import create_context, execute_sql, remove_context
except ImportError:
    create_context = None  # type: ignore
    execute_sql = None  # type: ignore
    remove_context = None  # type: ignore


class TeradataMLClient:
    """Teradataml client for Teradata database operations."""

    def __init__(self, config: DatabaseConfig):
        """
        Initialize Teradataml client.

        Args:
            config: DatabaseConfig instance

        Raises:
            DatabaseConnectionError: If connection fails
        """
        self.config = config
        self.context = None
        self._connect()

    def _connect(self) -> None:
        """
        Create Teradataml context and test connection.

        Raises:
            DatabaseConnectionError: If connection fails
        """
        try:
            if create_context is None:
                raise DatabaseConnectionError(
                    "teradataml not installed. Install with: pip install teradataml"
                )

            params = self.config.get_teradataml_params()
            self.context = create_context(**params)
            self._test_connection()
        except DatabaseConnectionError:
            raise
        except Exception as e:
            raise DatabaseConnectionError(f"Failed to create Teradataml context: {e}")

    def _test_connection(self) -> None:
        """Test that connection works."""
        try:
            cursor = execute_sql("SELECT database")
            db_name = cursor.fetchone()[0]
            print(f"✓ Connected to Teradata database: {db_name}")
        except Exception as e:
            raise DatabaseConnectionError(f"Connection test failed: {e}")

    def execute_query(self, query: str) -> List[tuple]:
        """
        Execute a SQL query and return results as list of tuples.

        Args:
            query: SQL query string

        Returns:
            List of tuples representing rows

        Raises:
            QueryExecutionError: If query execution fails
        """
        try:
            cursor = execute_sql(query)
            return cursor.fetchall()
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
            cursor = execute_sql(query)
            result = cursor.fetchone()
            return result[0] if result else None
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
            cursor = execute_sql(query)
            columns = (
                [desc[0] for desc in cursor.description] if cursor.description else []
            )
            rows = cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        except Exception as e:
            raise QueryExecutionError(f"Dict query execution failed: {e}")

    def execute_many(self, queries: List[str]) -> List[Optional[List[tuple]]]:
        """
        Execute multiple queries sequentially.

        Args:
            queries: List of SQL query strings

        Returns:
            List of results for each query
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
        """Close Teradataml context."""
        try:
            if self.context:
                remove_context()
                self.context = None
                print("✓ Teradataml context removed")
        except Exception as e:
            raise DatabaseConnectionError(f"Error closing context: {e}")

    def __enter__(self):
        """Context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()
