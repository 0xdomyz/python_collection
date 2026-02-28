# %% [markdown]
# # Querying Teradata with TeradataML
#
# This notebook demonstrates how to connect to a Teradata database using the TeradataML library and execute queries with connection parameters loaded from system environment variables.

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
import warnings
from typing import Optional

import pandas as pd

warnings.filterwarnings("ignore")

# Load connection parameters from environment variables
teradata_host = os.getenv("TERADATA_HOST")
teradata_user = os.getenv("TERADATA_USER")
teradata_password = os.getenv("TERADATA_PASSWORD")
teradata_database = os.getenv(
    "TERADATA_DATABASE", "DBC"
)  # Default to DBC if not specified
teradata_logmech = os.getenv("TERADATA_LOGMECH", "TD2")

print("Environment Variables Status:")
print(f"  Host configured: {bool(teradata_host)}")
print(f"  User configured: {bool(teradata_user)}")
print(f"  Password configured: {bool(teradata_password)}")
print(f"  Database: {teradata_database}")
print(f"  Logmech: {teradata_logmech}")

# Validate required parameters
if not all([teradata_host, teradata_user, teradata_password]):
    print("\nâš ï¸  WARNING: Not all required environment variables are set!")
    print("Please set: TERADATA_HOST, TERADATA_USER, TERADATA_PASSWORD")

# %% [markdown]
# ## 2. Connect Using TeradataML
#
# TeradataML is Teradata's native Python library optimized for Teradata operations with specialized DataFrame capabilities.
#
# Install required packages (if not already installed):
# ```bash
# pip install teradataml pandas
# ```

# %%
try:
    from teradataml import DataFrame as TDDataFrame
    from teradataml import create_context, remove_context

    # Create Teradata context using environment variables
    context = None
    try:
        context = create_context(
            host=teradata_host,
            username=teradata_user,
            password=teradata_password,
            database=teradata_database,
            logmech=teradata_logmech,
        )
    except Exception:
        if teradata_logmech.upper() != "TD2":
            context = create_context(
                host=teradata_host,
                username=teradata_user,
                password=teradata_password,
                database=teradata_database,
                logmech="TD2",
            )
        else:
            raise

    print("âœ“ TeradataML context created successfully")
    print(f"âœ“ Connected to Teradata at {teradata_host}")
    current_db = getattr(context, "database", teradata_database)
    print(f"âœ“ Current context database: {current_db}")

except ImportError as e:
    print(f"âœ— TeradataML import failed: {str(e)}")
    print("   Ensure teradataml is installed in the active Python interpreter")
    context = None
except Exception as e:
    print(f"âœ— Connection failed: {type(e).__name__}: {str(e)}")
    context = None

# %% [markdown]
# ## 3. Execute Queries with TeradataML
#
# TeradataML provides a native DataFrame API alongside SQL query execution. This section covers both approaches.

# %%
# Example 1: Using TeradataML execute_sql for metadata queries
print("=" * 60)
print("Example 1: Metadata Query with TeradataML")
print("=" * 60)

if context is not None:
    try:
        from teradataml import execute_sql

        sql_query = """
        SELECT TOP 5
            DataBaseName,
            TableName,
            TableKind,
            CreateTimeStamp
        FROM DBC.TablesV
        WHERE DataBaseName = 'DBC'
        ORDER BY TableName
        """

        cursor = execute_sql(sql_query)
        rows = cursor.fetchall()
        columns = (
            [col[0] for col in cursor.description]
            if cursor.description is not None
            else []
        )
        result = pd.DataFrame(rows, columns=columns)

        print("System Tables (first 5):")
        print(result)
        print(f"\nShape: {len(result)} rows")

    except Exception as e:
        print(f"DataFrame query failed: {type(e).__name__}: {str(e)}")

# %%
# Example 2: Using SQL queries with TeradataML
print("\n" + "=" * 60)
print("Example 2: Using SQL Queries with TeradataML")
print("=" * 60)

if context is not None:
    try:
        from teradataml import execute_sql

        # Execute raw SQL query
        sql_query = """
        SELECT TOP 10
            TableName,
            TableKind,
            CreateTimeStamp
        FROM DBC.TablesV
        WHERE DataBaseName = 'DBC'
        """

        cursor = execute_sql(sql_query)
        rows = cursor.fetchall()
        columns = (
            [col[0] for col in cursor.description]
            if cursor.description is not None
            else []
        )
        result_df = pd.DataFrame(rows, columns=columns)
        print("Query Results:")
        print(result_df)
        print(f"\nRows returned: {len(result_df)}")

    except Exception as e:
        print(f"SQL query failed: {type(e).__name__}: {str(e)}")

# %%
# Example 3: TeradataML Aggregation Query
print("\n" + "=" * 60)
print("Example 3: Aggregation with TeradataML")
print("=" * 60)

if context is not None:
    try:
        from teradataml import execute_sql

        sql_query = """
        SELECT
            TableKind,
            COUNT(*) AS TableCount
        FROM DBC.TablesV
        WHERE DataBaseName = 'DBC'
        GROUP BY 1
        ORDER BY 2 DESC
        """

        cursor = execute_sql(sql_query)
        rows = cursor.fetchall()
        columns = (
            [col[0] for col in cursor.description]
            if cursor.description is not None
            else []
        )
        pandas_result = pd.DataFrame(rows, columns=columns)

        print("Table counts by kind in DBC:")
        print(pandas_result)
        print(f"\nData types:")
        print(pandas_result.dtypes)

    except Exception as e:
        print(f"DataFrame operations failed: {type(e).__name__}: {str(e)}")

# %% [markdown]
# ## 4. Context Management
#
# Best practices for managing TeradataML contexts:

# %%
# Check current context
if context is not None:
    print("Current TeradataML Context:")
    print(f"  Host: {getattr(context, 'host', teradata_host)}")
    print(f"  User: {getattr(context, 'user', teradata_user)}")
    print(f"  Database: {getattr(context, 'database', teradata_database)}")
    print(f"  Is closed: {getattr(context, 'is_closed', 'Unknown')}")

    # Optional: Create additional contexts for different databases
    # secondary_context = create_context(
    #     host=teradata_host,
    #     username=teradata_user,
    #     password=teradata_password,
    #     database='ANALYTICS'  # Different database
    # )

# %% [markdown]
# ## 5. TeradataML Advantages and Use Cases
#
# **Advantages:**
# - âœ“ Native Teradata optimization and performance
# - âœ“ DataFrame API similar to Pandas (lazy evaluation)
# - âœ“ Simplified connection with create_context()
# - âœ“ Native support for Teradata-specific SQL features
# - âœ“ Efficient data serialization
# - âœ“ Native integration with Teradata functions and UDTF
# - âœ“ Better performance for Teradata-specific operations
#
# **Best Use Cases:**
# - Data science workflows with Teradata as primary database
# - ETL operations optimized for Teradata
# - Leveraging Teradata-specific analytics functions
# - High-performance data analysis on large datasets
# - Organizations heavily invested in Teradata

# %% [markdown]
# ## 6. Cleanup
#
# Clean up resources when done:

# %%
# Close the TeradataML context
if context is not None and not bool(getattr(context, "is_closed", False)):
    remove_context()
    print("âœ“ TeradataML context closed and removed")
if context is not None and not bool(getattr(context, "is_closed", False)):
    remove_context()
    print("âœ“ TeradataML context closed and removed")
