"""
Example: SQLAlchemy Query Execution

This example demonstrates basic and concurrent query execution using SQLAlchemy.
Set environment variables before running:
    export TERADATA_HOST=your_host
    export TERADATA_USER=your_user
    export TERADATA_PASSWORD=your_password
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_query_lib import DatabaseConfig, SQLAlchemyClient
from db_query_lib.exceptions import ConfigurationError


def example_basic_queries():
    """Example 1: Basic synchronous queries."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic SQLAlchemy Queries")
    print("=" * 70)

    try:
        # Load configuration from environment
        config = DatabaseConfig.from_env()
        client = SQLAlchemyClient(config)

        # Simple SELECT query
        query = """
            SELECT TableKind, COUNT(*) AS Cnt
            FROM DBC.TablesV
            WHERE DataBaseName = 'DBC'
            GROUP BY TableKind
            LIMIT 10
        """

        print("\nExecuting: SELECT COUNT(*) FROM DBC.TablesV...")
        results = client.execute_query(query)
        print(f"✓ Retrieved {len(results)} rows")
        print(results.head())

        # Scalar query
        scalar_query = "SELECT COUNT(*) FROM DBC.TablesV WHERE DataBaseName = 'DBC'"
        count = client.execute_query_scalar(scalar_query)
        print(f"\n✓ Table count: {count}")

        # Query as list of dicts
        dict_query = """
            SELECT DatabaseName, TableCount
            FROM DBC.SummaryStats
            LIMIT 5
        """
        dict_results = client.execute_query_dict(dict_query)
        print(f"\n✓ Retrieved {len(dict_results)} rows as dictionaries")

        client.close()

    except ConfigurationError as e:
        print(f"✗ Configuration Error: {e}")
        print(
            "Please set environment variables: TERADATA_HOST, TERADATA_USER, TERADATA_PASSWORD"
        )
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")


def example_connection_pool():
    """Example 2: Understanding connection pooling."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Connection Pool Management")
    print("=" * 70)

    try:
        config = DatabaseConfig.from_env()

        # Create client with custom pool settings
        client = SQLAlchemyClient(
            config,
            pool_size=10,
            max_overflow=5,
            pool_timeout=30.0,
        )

        print("\nPool Configuration:")
        status = client.get_pool_status()
        for key, value in status.items():
            print(f"  {key}: {value}")

        # Execute some queries to show pool in use
        print("\nExecuting queries...")
        query = "SELECT DATABASE"
        for i in range(3):
            result = client.execute_query_scalar(query)
            print(f"  Query {i + 1}: {result}")

        print("\n✓ Pool demonstrates connection reuse for concurrent requests")

        client.close()

    except Exception as e:
        print(f"✗ Error: {e}")


def example_batch_queries():
    """Example 3: Execute multiple queries."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Batch Query Execution")
    print("=" * 70)

    try:
        config = DatabaseConfig.from_env()
        client = SQLAlchemyClient(config)

        queries = [
            "SELECT COUNT(*) AS cnt FROM DBC.TablesV",
            "SELECT COUNT(*) AS cnt FROM DBC.ColumnsV",
            "SELECT COUNT(*) AS cnt FROM DBC.DatabasesV",
        ]

        print("\nExecuting batch of 3 queries...")
        results = client.execute_many(queries)

        for i, result in enumerate(results, 1):
            if result is not None:
                print(f"  Query {i}: ✓ {len(result)} rows")
            else:
                print(f"  Query {i}: ✗ Failed")

        client.close()

    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    print("SQLAlchemy Database Examples")
    print("=" * 70)
    print("\nNote: These examples require a valid Teradata connection.")
    print("Set TERADATA_HOST, TERADATA_USER, TERADATA_PASSWORD environment variables.")

    # Uncomment to run examples:
    # example_basic_queries()
    # example_connection_pool()
    # example_batch_queries()

    print("\n✓ Examples ready to run. Uncomment the function calls to execute.")
