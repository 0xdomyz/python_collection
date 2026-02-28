"""
Example: Teradataml Query Execution

This example demonstrates basic and concurrent query execution using Teradataml.
Set environment variables before running:
    export TERADATA_HOST=your_host
    export TERADATA_USER=your_user
    export TERADATA_PASSWORD=your_password
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from db_query_lib import DatabaseConfig, TeradataMLClient
from db_query_lib.exceptions import ConfigurationError


def example_basic_queries():
    """Example 1: Basic Teradataml queries."""
    print("\n" + "=" * 70)
    print("EXAMPLE 1: Basic Teradataml Queries")
    print("=" * 70)

    try:
        # Load configuration from environment
        config = DatabaseConfig.from_env()

        with TeradataMLClient(config) as client:
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
            for row in results[:3]:
                print(f"  {row}")

            # Scalar query
            scalar_query = "SELECT COUNT(*) FROM DBC.TablesV WHERE DataBaseName = 'DBC'"
            count = client.execute_query_scalar(scalar_query)
            print(f"\n✓ Table count: {count}")

            # Query as list of dicts
            dict_query = """
                SELECT TOP 5
                    DataBaseName,
                    TableName
                FROM DBC.TablesV
                WHERE DataBaseName = 'DBC'
            """
            dict_results = client.execute_query_dict(dict_query)
            print(f"\n✓ Retrieved {len(dict_results)} rows as dictionaries")
            for row in dict_results[:2]:
                print(f"  {row}")

    except ConfigurationError as e:
        print(f"✗ Configuration Error: {e}")
        print(
            "Please set environment variables: TERADATA_HOST, TERADATA_USER, TERADATA_PASSWORD"
        )
    except ImportError:
        print("✗ Teradataml not installed.")
        print("Install with: pip install teradataml")
    except Exception as e:
        print(f"✗ Error: {type(e).__name__}: {e}")


def example_context_manager():
    """Example 2: Using Teradataml client as context manager."""
    print("\n" + "=" * 70)
    print("EXAMPLE 2: Context Manager Usage")
    print("=" * 70)

    try:
        config = DatabaseConfig.from_env()

        # Using context manager ensures automatic cleanup
        print("\nUsing 'with' statement for automatic resource management...")
        with TeradataMLClient(config) as client:
            # Connection is automatically managed
            result = client.execute_query_scalar("SELECT database")
            print(f"✓ Current database: {result}")

        print("✓ Context manager cleaned up resources automatically")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_batch_queries():
    """Example 3: Execute multiple queries."""
    print("\n" + "=" * 70)
    print("EXAMPLE 3: Batch Query Execution")
    print("=" * 70)

    try:
        config = DatabaseConfig.from_env()

        with TeradataMLClient(config) as client:
            queries = [
                "SELECT COUNT(*) FROM DBC.TablesV",
                "SELECT COUNT(*) FROM DBC.ColumnsV",
                "SELECT COUNT(*) FROM DBC.DatabasesV",
            ]

            print("\nExecuting batch of 3 queries...")
            results = client.execute_many(queries)

            for i, result in enumerate(results, 1):
                if result is not None:
                    print(f"  Query {i}: ✓ {len(result)} rows")
                    if result:
                        print(f"    First result: {result[0]}")
                else:
                    print(f"  Query {i}: ✗ Failed")

    except Exception as e:
        print(f"✗ Error: {e}")


def example_error_handling():
    """Example 4: Error handling."""
    print("\n" + "=" * 70)
    print("EXAMPLE 4: Error Handling")
    print("=" * 70)

    try:
        config = DatabaseConfig.from_env()

        with TeradataMLClient(config) as client:
            print("\nAttempting invalid query...")
            try:
                result = client.execute_query("SELECT * FROM nonexistent_table")
            except Exception as e:
                print(f"✓ Caught error: {type(e).__name__}: {e}")

            print("\nClient continues to work after error...")
            result = client.execute_query_scalar("SELECT database")
            print(f"✓ Database: {result}")

    except Exception as e:
        print(f"✗ Error: {e}")


if __name__ == "__main__":
    print("Teradataml Database Examples")
    print("=" * 70)
    print("\nNote: These examples require a valid Teradata connection.")
    print("Set TERADATA_HOST, TERADATA_USER, TERADATA_PASSWORD environment variables.")

    # Uncomment to run examples:
    # example_basic_queries()
    # example_context_manager()
    # example_batch_queries()
    # example_error_handling()

    print("\n✓ Examples ready to run. Uncomment the function calls to execute.")
