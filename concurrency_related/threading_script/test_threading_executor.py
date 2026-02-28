"""Test file for ThreadingQueryExecutor using SQLite3."""

import sqlite3
import time
from pathlib import Path
from typing import Any, Dict

from loguru import logger
from threading_executor import ThreadingQueryExecutor

# Configure loguru logger
logger.remove()  # Remove default handler
logger.add(
    lambda msg: print(msg, end=""),
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    level="INFO",
)


def setup_test_database(db_path: str = "test_threading.db") -> None:
    """Create and populate a test SQLite database."""
    logger.info(f"Setting up test database: {db_path}")

    # Remove existing database
    if Path(db_path).exists():
        Path(db_path).unlink()

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create test tables
    cursor.execute(
        """
        CREATE TABLE users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            age INTEGER,
            city TEXT
        )
    """
    )

    cursor.execute(
        """
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            product TEXT,
            amount REAL,
            order_date TEXT,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """
    )

    # Insert test data
    users_data = [
        (1, "Alice Johnson", "alice@example.com", 28, "New York"),
        (2, "Bob Smith", "bob@example.com", 35, "Los Angeles"),
        (3, "Charlie Brown", "charlie@example.com", 42, "Chicago"),
        (4, "Diana Prince", "diana@example.com", 31, "Houston"),
        (5, "Eve Martinez", "eve@example.com", 26, "Phoenix"),
        (6, "Frank Wilson", "frank@example.com", 39, "Philadelphia"),
        (7, "Grace Lee", "grace@example.com", 33, "San Antonio"),
        (8, "Henry Davis", "henry@example.com", 45, "San Diego"),
    ]

    cursor.executemany("INSERT INTO users VALUES (?, ?, ?, ?, ?)", users_data)

    orders_data = [
        (1, 1, "Laptop", 1200.00, "2026-01-15"),
        (2, 1, "Mouse", 25.50, "2026-01-16"),
        (3, 2, "Keyboard", 75.00, "2026-01-20"),
        (4, 3, "Monitor", 350.00, "2026-02-01"),
        (5, 2, "Headphones", 150.00, "2026-02-05"),
        (6, 4, "USB Cable", 15.00, "2026-02-10"),
        (7, 5, "Webcam", 89.99, "2026-02-12"),
        (8, 1, "Desk Lamp", 45.00, "2026-02-15"),
        (9, 6, "Chair", 299.99, "2026-02-18"),
        (10, 7, "Notebook", 12.50, "2026-02-20"),
    ]

    cursor.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", orders_data)

    conn.commit()
    conn.close()

    logger.info(
        f"Database setup complete. Inserted {len(users_data)} users and {len(orders_data)} orders."
    )


def execute_query(db_path: str, query: str, delay: float = 0) -> Dict[str, Any]:
    """
    Execute a SQL query and return results.

    Args:
        db_path: Path to SQLite database
        query: SQL query to execute
        delay: Artificial delay to simulate slow query (seconds)

    Returns:
        Dictionary with query results and metadata
    """
    if delay > 0:
        time.sleep(delay)

    conn = None
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []

        return {"rows": results, "columns": columns, "row_count": len(results)}
    finally:
        if conn:
            conn.close()


def test_concurrent_queries():
    """Test concurrent query execution with threading."""
    db_path = "test_threading.db"

    # Setup test database
    setup_test_database(db_path)

    logger.info("\n" + "=" * 70)
    logger.info("Starting Threading Concurrent Query Test")
    logger.info("=" * 70)

    # Define test queries with different complexities
    test_queries = [
        {
            "query_id": "count_users",
            "kwargs": {
                "db_path": db_path,
                "query": "SELECT COUNT(*) as user_count FROM users",
                "delay": 0.1,
            },
        },
        {
            "query_id": "all_users",
            "kwargs": {
                "db_path": db_path,
                "query": "SELECT * FROM users ORDER BY name",
                "delay": 0.2,
            },
        },
        {
            "query_id": "users_by_city",
            "kwargs": {
                "db_path": db_path,
                "query": "SELECT city, COUNT(*) as count FROM users GROUP BY city ORDER BY count DESC",
                "delay": 0.15,
            },
        },
        {
            "query_id": "total_orders",
            "kwargs": {
                "db_path": db_path,
                "query": "SELECT SUM(amount) as total FROM orders",
                "delay": 0.1,
            },
        },
        {
            "query_id": "user_order_join",
            "kwargs": {
                "db_path": db_path,
                "query": """
                    SELECT u.name, COUNT(o.id) as order_count, SUM(o.amount) as total_spent
                    FROM users u
                    LEFT JOIN orders o ON u.id = o.user_id
                    GROUP BY u.id, u.name
                    ORDER BY total_spent DESC
                """,
                "delay": 0.3,
            },
        },
        {
            "query_id": "recent_orders",
            "kwargs": {
                "db_path": db_path,
                "query": "SELECT * FROM orders WHERE order_date >= '2026-02-01' ORDER BY order_date",
                "delay": 0.1,
            },
        },
        {
            "query_id": "avg_age",
            "kwargs": {
                "db_path": db_path,
                "query": "SELECT AVG(age) as avg_age, MIN(age) as min_age, MAX(age) as max_age FROM users",
                "delay": 0.05,
            },
        },
        {
            "query_id": "top_products",
            "kwargs": {
                "db_path": db_path,
                "query": "SELECT product, COUNT(*) as purchases FROM orders GROUP BY product ORDER BY purchases DESC LIMIT 5",
                "delay": 0.2,
            },
        },
    ]

    # Extract query IDs and arguments
    query_ids = [q["query_id"] for q in test_queries]
    arguments_list = [q["kwargs"] for q in test_queries]

    # Create executor and run queries
    logger.info(
        f"\nExecuting {len(test_queries)} queries concurrently with max_workers=4..."
    )

    executor = ThreadingQueryExecutor(max_workers=4, timeout=30.0)

    try:
        results = executor.execute_function_concurrent(
            function=execute_query, arguments_list=arguments_list, query_ids=query_ids
        )

        # Print summary results
        executor.print_results(verbose=True)

        # Display some sample results
        logger.info("\n" + "=" * 70)
        logger.info("Sample Query Results")
        logger.info("=" * 70)

        for result in results[:3]:  # Show first 3 results
            if result.is_success:
                logger.info(f"\n{result.query_id}:")
                data = result.result
                logger.info(f"  Columns: {data['columns']}")
                logger.info(f"  Row count: {data['row_count']}")
                if data["row_count"] > 0 and data["row_count"] <= 3:
                    logger.info(f"  Data: {data['rows']}")
                elif data["row_count"] > 3:
                    logger.info(f"  First row: {data['rows'][0]}")
            else:
                logger.error(f"\n{result.query_id}: FAILED")
                logger.error(f"  Error: {result.error}")

        logger.info("\n" + "=" * 70)
        logger.success("Test completed successfully!")

    except Exception as e:
        logger.error(f"Test failed with error: {e}")
        raise

    finally:
        # Cleanup
        time.sleep(0.5)
        if Path(db_path).exists():
            try:
                Path(db_path).unlink()
                logger.info(f"Cleaned up test database: {db_path}")
            except PermissionError:
                logger.warning(f"Could not delete {db_path} - file is still in use")


def test_error_handling():
    """Test error handling with invalid queries."""
    db_path = "test_threading.db"
    setup_test_database(db_path)

    logger.info("\n" + "=" * 70)
    logger.info("Testing Threading Error Handling")
    logger.info("=" * 70)

    test_queries = [
        {
            "query_id": "valid_query",
            "kwargs": {
                "db_path": db_path,
                "query": "SELECT COUNT(*) FROM users",
                "delay": 0.1,
            },
        },
        {
            "query_id": "invalid_table",
            "kwargs": {
                "db_path": db_path,
                "query": "SELECT * FROM nonexistent_table",
                "delay": 0.1,
            },
        },
        {
            "query_id": "syntax_error",
            "kwargs": {
                "db_path": db_path,
                "query": "SELECT * FORM users",  # Intentional typo
                "delay": 0.1,
            },
        },
    ]

    query_ids = [q["query_id"] for q in test_queries]
    arguments_list = [q["kwargs"] for q in test_queries]

    executor = ThreadingQueryExecutor(max_workers=2, timeout=10.0)
    results = executor.execute_function_concurrent(
        function=execute_query, arguments_list=arguments_list, query_ids=query_ids
    )

    executor.print_results(verbose=True)

    # Verify error handling
    successful = sum(1 for r in results if r.is_success)
    failed = sum(1 for r in results if not r.is_success)

    logger.info(
        f"\nError handling test: {successful} successful, {failed} failed (expected 1/2)"
    )

    # Cleanup
    time.sleep(0.5)
    if Path(db_path).exists():
        try:
            Path(db_path).unlink()
            logger.info(f"Cleaned up test database: {db_path}")
        except PermissionError:
            logger.warning(f"Could not delete {db_path} - file is still in use")


if __name__ == "__main__":
    logger.info("=" * 70)
    logger.info("ThreadingQueryExecutor Test Suite")
    logger.info("=" * 70)

    # Run tests
    test_concurrent_queries()
    print("\n")
    test_error_handling()

    logger.success("\nAll tests completed!")
