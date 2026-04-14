# %% [markdown]
# # Querying Teradata with SQLAlchemy
#
# This notebook demonstrates how to connect to a Teradata database using SQLAlchemy and execute queries with connection parameters loaded from system environment variables.

# %% [markdown]
# ## 1. Set Up Environment Variables
#
# Before running this notebook, ensure the following environment variables are configured:
# - `TERADATA_HOST`: Teradata database host/server name
# - `TERADATA_USER`: Username for authentication
# - `TERADATA_PASSWORD`: Password for authentication
# - `TERADATA_DATABASE`: Default database name (optional)
#
# These credentials will be loaded from your system environment.

# %%
import os
from typing import Optional

import pandas as pd

# Load connection parameters from environment variables
teradata_host = os.getenv("TERADATA_HOST")
teradata_user = os.getenv("TERADATA_USER")
teradata_password = os.getenv("TERADATA_PASSWORD")
teradata_database = os.getenv(
    "TERADATA_DATABASE", "DBC"
)  # Default to DBC if not specified

print("Environment Variables Status:")
print(f"  Host configured: {bool(teradata_host)}")
print(f"  User configured: {bool(teradata_user)}")
print(f"  Password configured: {bool(teradata_password)}")
print(f"  Database: {teradata_database}")

# Validate required parameters
if not all([teradata_host, teradata_user, teradata_password]):
    print("\nâš ï¸  WARNING: Not all required environment variables are set!")
    print("Please set: TERADATA_HOST, TERADATA_USER, TERADATA_PASSWORD")

# %% [markdown]
# ## 2. Connect Using SQLAlchemy
#
# SQLAlchemy is a powerful SQL toolkit and Object-Relational Mapping (ORM) library. To connect to Teradata, we use the `teradatasql` dialect.
#
# Install required packages (if not already installed):
# ```bash
# pip install sqlalchemy teradatasql pandas
# ```

# %%
from sqlalchemy import create_engine, text

# Create connection string using environment variables
# Format: teradata://{user}:{password}@{host}/{database}
connection_string = f"teradatasql://{teradata_user}:{teradata_password}@{teradata_host}/{teradata_database}"

try:
    # Create SQLAlchemy engine
    engine = create_engine(connection_string, echo=False)
    print("âœ“ SQLAlchemy engine created successfully")

    # Test the connection
    with engine.connect() as connection:
        result = connection.execute(text("SELECT database"))
        db_name = result.scalar()
        print(f"âœ“ Connected to database: {db_name}")
        print(f"âœ“ Connection test passed!")

except Exception as e:
    print(f"âœ— Connection failed: {type(e).__name__}: {str(e)}")
    engine = None

# %% [markdown]
# ## 3. Execute Queries with SQLAlchemy
#
# Now that we have an active connection, we can execute SQL queries and retrieve results using SQLAlchemy.


# %%
def execute_query_sqlalchemy(query: str) -> Optional[pd.DataFrame]:
    """
    Execute a SQL query using SQLAlchemy and return results as a pandas DataFrame.

    Args:
        query: SQL query string

    Returns:
        pandas DataFrame with query results, or None if query fails
    """
    if engine is None:
        print("Error: No active database connection")
        return None

    try:
        df = pd.read_sql(query, engine)
        return df
    except Exception as e:
        print(f"Query execution failed: {type(e).__name__}: {str(e)}")
        return None


# Example 1: Query system tables (list tables in DBC database)
print("=" * 60)
print("Example 1: List tables in DBC database")
print("=" * 60)
query1 = """
SELECT TOP 10
    TableName,
    TableKind,
    CreateTimeStamp
FROM DBC.TablesV
WHERE DataBaseName = 'DBC'
"""

result_df = execute_query_sqlalchemy(query1)
if result_df is not None:
    print(f"Found {len(result_df)} tables")
    print(result_df)
else:
    print("Query returned no results")

# %%
# Example 2: Get system information
print("\n" + "=" * 60)
print("Example 2: System Information")
print("=" * 60)
query2 = """
SELECT 
    DataBaseName,
    OwnerName,
    DBKind,
    ProtectionType
FROM DBC.DatabasesV
ORDER BY DataBaseName
SAMPLE 5
"""

result_df = execute_query_sqlalchemy(query2)
if result_df is not None:
    print(result_df)
else:
    print("Could not retrieve system information")

# %%
# Example 3: Using SQLAlchemy's text() for parameterized queries
print("\n" + "=" * 60)
print("Example 3: Parameterized Query with SQLAlchemy")
print("=" * 60)

if engine is not None:
    try:
        # Using parameterized queries for safety
        query3 = text(
            """
        SELECT TOP 5
            DatabaseName,
            TableName,
            TableKind
        FROM DBC.TablesV
        WHERE DatabaseName = :database_name
        ORDER BY TableName
        """
        )

        with engine.connect() as connection:
            result = connection.execute(query3, {"database_name": "DBC"})
            df = pd.DataFrame(result.fetchall(), columns=result.keys())
            print(f"Found {len(df)} sample tables in DBC")
            print(df)

    except Exception as e:
        print(f"Parameterized query failed: {type(e).__name__}: {str(e)}")

# %% [markdown]
# ## 4. Connection Management
#
# Best practices for managing SQLAlchemy connections:

# %%
# Connection pooling is automatic with SQLAlchemy
# The engine manages a pool of connections for better performance

# Get engine pool statistics
if engine is not None:
    pool = engine.pool

    def pool_stat_value(name: str, default="n/a"):
        value = getattr(pool, name, None)
        if value is None:
            return default
        if callable(value):
            try:
                return value()
            except TypeError:
                return value
        return value

    print(f"Connection Pool Statistics:")
    print(f"  Pool size: {pool_stat_value('size')}")
    print(f"  Checked-in connections: {pool_stat_value('checkedin')}")
    print(f"  Is disposed: {pool_stat_value('disposed')}")

    # To close all connections when done
    # engine.dispose()  # Uncomment when done with all queries

# %% [markdown]
# ## 5. SQLAlchemy Advantages and Use Cases
#
# **Advantages:**
# - âœ“ Platform-independent ORM abstraction
# - âœ“ Built-in connection pooling
# - âœ“ Support for multiple databases
# - âœ“ Parameterized queries prevent SQL injection
# - âœ“ Rich ecosystem with many extensions
# - âœ“ Good for complex queries with joins and subqueries
#
# **Best Use Cases:**
# - Building applications that may use multiple databases
# - Data transformation and ETL workflows
# - Applications requiring ORM capabilities
# - When you need a declarative query interface

# %% [markdown]
# ## 6. Cleanup
#
# Clean up resources when done:

# %%
# Properly dispose of the engine to close all connections
if engine is not None:
    engine.dispose()
    print("âœ“ All connections closed and engine disposed")
    print("âœ“ All connections closed and engine disposed")
