"""Database Query Library - README with setup and usage instructions."""

# Database Query Library

A comprehensive Python library for concurrent database query execution with SQLAlchemy and Teradataml, featuring threadpool-based parallelization and environment-based configuration.

## Features

✓ **SQLAlchemy Client** - Execute queries with connection pooling
✓ **Teradataml Client** - Native Teradata operations  
✓ **ThreadPool Executor** - Concurrent execution with detailed metrics
✓ **Environment Configuration** - Load credentials from env vars
✓ **Error Handling** - Custom exceptions and resilience
✓ **Pytest Tests** - Comprehensive test suite
✓ **Examples** - Working examples for all components

## Installation

### Requirements
- Python 3.7+
- pandas
- sqlalchemy
- teradatasql  
- teradataml (optional, for Teradataml support)

### Setup

1. **Create virtual environment**:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

2. **Install dependencies**:
```bash
pip install pandas sqlalchemy teradatasql
pip install teradataml  # Optional, for Teradataml support
pip install pytest      # For running tests
```

3. **Set environment variables**:
```bash
export TERADATA_HOST=your_host
export TERADATA_USER=your_user
export TERADATA_PASSWORD=your_password
export TERADATA_DATABASE=DBC  # Optional
```

## Usage

### 1. SQLAlchemy Client - Basic Queries

```python
from db_query_lib import DatabaseConfig, SQLAlchemyClient

# Load config from environment
config = DatabaseConfig.from_env()
client = SQLAlchemyClient(config)

# Simple query
result = client.execute_query("SELECT * FROM table LIMIT 10")

# Scalar query
count = client.execute_query_scalar("SELECT COUNT(*) FROM table")

# Query as dictionaries
rows = client.execute_query_dict("SELECT id, name FROM table LIMIT 5")

# Batch queries
results = client.execute_many([query1, query2, query3])

client.close()
```

### 2. SQLAlchemy Client - Connection Pooling

```python
# Custom pool settings for high concurrency
client = SQLAlchemyClient(
    config,
    pool_size=10,      # Maintain 10 connections
    max_overflow=5,    # Allow 5 additional during peaks
    pool_timeout=30.0, # Timeout for acquiring connection
)

# Check pool status
status = client.get_pool_status()
print(f"Checked out: {status['checked_out']}")
```

### 3. Teradataml Client

```python
from db_query_lib import DatabaseConfig, TeradataMLClient

config = DatabaseConfig.from_env()

# Using context manager (auto cleanup)
with TeradataMLClient(config) as client:
    result = client.execute_query("SELECT * FROM table")
    scalar = client.execute_query_scalar("SELECT COUNT(*)")
    dicts = client.execute_query_dict("SELECT * FROM table")
```

### 4. Concurrent Query Execution

The `ThreadPoolQueryExecutor` is **mechanism-agnostic** - it works with any function and any client (SQLAlchemy, Teradataml, or custom). It distributes work across multiple worker threads for concurrent execution.

```python
from db_query_lib import ThreadPoolQueryExecutor

# Define function to execute (works with ANY client or function)
def my_query(client, query):
    return client.execute_query(query)

# Prepare arguments for concurrent execution
tasks = [
    {"client": client, "query": "SELECT * FROM table1"},
    {"client": client, "query": "SELECT * FROM table2"},
    {"client": client, "query": "SELECT * FROM table3"},
]

# Execute concurrently across worker threads
executor = ThreadPoolQueryExecutor(max_workers=5, timeout=60)
results = executor.execute_function_concurrent(my_query, tasks)

# Print summary with timing and speedup metrics
executor.print_results(verbose=True)
```

**Key point**: The executor doesn't care *how* you execute queries - whether using SQLAlchemy, Teradataml, or any other mechanism. The concurrency happens at the thread level, so your function can wrap any database client, API, or I/O operation.

### 5. Execution Results and Metrics

```python
# Results are ExecutionResult objects with metrics
for result in results:
    print(f"Query: {result.query_id}")
    print(f"Thread: {result.thread_id}")
    print(f"Duration: {result.duration_seconds:.3f}s")
    print(f"Success: {result.is_success}")
    
# Summary statistics
summary = executor.get_summary()
print(f"Total time: {summary['total_execution_time']:.2f}s")
print(f"Wall clock: {summary['wall_clock_time']:.2f}s")
print(f"Speedup: {summary['speedup']:.2f}x")
```

## Project Structure

```
db_query_lib/
├── __init__.py               # Package initialization
├── config.py                 # Configuration management
├── exceptions.py             # Custom exceptions
├── sqlalchemy_client.py       # SQLAlchemy wrapper
├── teradataml_client.py       # Teradataml wrapper
├── threadpool_executor.py     # ThreadPool utilities
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Pytest fixtures
│   ├── test_sqlalchemy_client.py
│   ├── test_teradataml_client.py
│   └── test_threadpool_executor.py
└── examples/
    ├── __init__.py
    ├── example_sqlalchemy.py  # SQLAlchemy examples
    ├── example_teradataml.py  # Teradataml examples
    └── example_threadpool.py  # Concurrent execution examples
```

## Running Tests

```bash
# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_sqlalchemy_client.py -v

# Run with coverage
pytest tests/ --cov=db_query_lib

# Run only passing tests
pytest tests/ -v
```

## Examples

### Run examples:

```bash
# SQLAlchemy examples (edit file to uncomment)
python db_query_lib/examples/example_sqlalchemy.py

# Teradataml examples
python db_query_lib/examples/example_teradataml.py

# ThreadPool examples (includes non-database tests)
python db_query_lib/examples/example_threadpool.py
```

## Configuration

### Environment Variables

- `TERADATA_HOST` (required) - Teradata server hostname
- `TERADATA_USER` (required) - Database username
- `TERADATA_PASSWORD` (required) - Database password
- `TERADATA_DATABASE` (optional, default: DBC) - Default database
- `TERADATA_LOGMECH` (optional, default: TD2) - Authentication mechanism
- `TERADATA_CHARSET` (optional, default: UTF8) - Character set

### DatabaseConfig Class

```python
from db_query_lib import DatabaseConfig

# Load from environment
config = DatabaseConfig.from_env(required=True)

# Or create manually
config = DatabaseConfig(
    host "localhost",
    user="user",
    password="pass",
    database="DBC",
)

# Get connection strings
sql_alchemy_connstr = config.get_sqlalchemy_connection_string()
teradataml_params = config.get_teradataml_params()
```

## Exception Handling

```python
from db_query_lib.exceptions import (
    ConfigurationError,
    DatabaseConnectionError,
    QueryExecutionError,
    ThreadPoolExecutionError,
)

try:
    client = SQLAlchemyClient(config)
except ConfigurationError:
    print("Configuration missing")
except DatabaseConnectionError:
    print("Connection failed")

try:
    result = client.execute_query(query)
except QueryExecutionError:
    print("Query execution failed")
```

## Performance Considerations

### Connection Pooling
- **pool_size**: Number of connections to keep open (default: 5)
- **max_overflow**: Additional connections during peak load (default: 10)
- Best for: Frequent, short-lived queries

### ThreadPool Concurrency
- **max_workers**: Number of worker threads (default: 5)
- Each thread uses one connection from the pool
- Works best with I/O-bound operations (database queries)
- CPU-bound operations benefit less due to Python's GIL

### Typical Speedup
- **Sequential**: N queries × T time per query = N×T total
- **Concurrent**: With network latency, often near N×T / max_workers
- Actual speedup depends on query complexity and network conditions

## Troubleshooting

### "Connection failed" error
- Verify environment variables are set correctly
- Check Teradata server is accessible
- Ensure credentials are valid

### "Module not found: teradataml"
- Install with: `pip install teradataml`
- Or catch ImportError if optional

### Slow query execution
- Check connection pool settings
- Increase pool_size if many concurrent queries
- Review query optimization
- Check network/database server load

## See Also

- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Teradataml Documentation](https://docs.teradata.com/)
- [Python threading](https://docs.python.org/3/library/threading.html)
- [Pytest Documentation](https://docs.pytest.org/)

## License

MIT License - See LICENSE file for details
