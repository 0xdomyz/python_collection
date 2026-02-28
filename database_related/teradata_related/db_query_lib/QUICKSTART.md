"""Quick start guide for db_query_lib."""

# QUICK START GUIDE
# ================

# 1. SETUP
# --------
# 
# Set environment variables:
#   export TERADATA_HOST=your_host
#   export TERADATA_USER=your_user
#   export TERADATA_PASSWORD=your_password
#
# Install dependencies:
#   pip install -r requirements.txt

# 2. BASIC SQLALCHEMY USAGE
# -------------------------

from db_query_lib import DatabaseConfig, SQLAlchemyClient

# Load config from environment
config = DatabaseConfig.from_env()

# Create client
client = SQLAlchemyClient(config)

# Execute queries
result = client.execute_query("SELECT * FROM DBC.TablesV LIMIT 10")
print(f"Got {len(result)} rows")

# Cleanup
client.close()


# 3. BASIC TERADATAML USAGE
# -------------------------

from db_query_lib import TeradataMLClient

config = DatabaseConfig.from_env()

# Using context manager (auto cleanup)
with TeradataMLClient(config) as client:
    result = client.execute_query("SELECT COUNT(*) FROM DBC.TablesV")
    print(f"Result: {result}")


# 4. CONCURRENT EXECUTION
# -----------------------

from db_query_lib import ThreadPoolQueryExecutor

def execute_single_query(client, query):
    """Helper to execute a single query."""
    return client.execute_query(query)

# Create multiple tasks
tasks = [
    {"client": client, "query": "SELECT COUNT(*) FROM DBC.TablesV"},
    {"client": client, "query": "SELECT COUNT(*) FROM DBC.ColumnsV"},
    {"client": client, "query": "SELECT COUNT(*) FROM DBC.DatabasesV"},
]

# Execute concurrently
executor = ThreadPoolQueryExecutor(max_workers=3)
results = executor.execute_function_concurrent(execute_single_query, tasks)

# Print results
executor.print_results(verbose=True)


# 5. RUN TESTS
# -----------
#
# pytest tests/
# pytest tests/test_sqlalchemy_client.py -v
# pytest tests/ --cov=db_query_lib


# 6. FULL EXAMPLES
# ----------------
#
# See examples/ folder:
#   - example_sqlalchemy.py - SQLAlchemy features
#   - example_teradataml.py - Teradataml features  
#   - example_threadpool.py - Concurrent execution


# TIPS
# ----
#
# 1. Always use context managers where possible (with statement)
# 2. Pool size should match your max concurrent queries
# 3. ThreadPool is best for I/O-bound operations (network/disk)
# 4. Check pool status with client.get_pool_status()
# 5. Run tests to verify setup: pytest tests/
