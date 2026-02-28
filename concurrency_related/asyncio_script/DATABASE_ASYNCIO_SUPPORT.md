# Database Asyncio Support Guide

This document covers asyncio support for popular Python database libraries, with recommendations on which to use for async applications.

---

## Overview

When working with asyncio in Python, you need database drivers that support async/await patterns. The landscape has evolved significantly:

- **Traditional drivers**: Synchronous only, require `run_in_executor()` workaround
- **Async-native drivers**: Built for asyncio, far superior performance
- **Hybrid drivers**: Some support both sync and async modes

---

## Database Support Matrix

### Legend
- ✅ **Native Async**: Built-in asyncio support
- 🔄 **Workaround**: Must use `run_in_executor()`
- ❌ **Not Recommended**: Avoid for async code
- 📦 **Alternative**: Use a different driver

---

## Relational Databases

### PostgreSQL

#### psycopg2 (PostgreSQL)
- **Asyncio Support**: 🔄 **Workaround only**
- **Latest Version**: 2.9.x
- **Type**: Synchronous only
- **Status**: Mature, stable, but no async

```python
# ❌ Using with asyncio (not ideal)
import asyncio
import psycopg2

async def query_db():
    loop = asyncio.get_event_loop()
    
    def _execute():
        conn = psycopg2.connect("dbname=test user=postgres")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

**Pros**:
- Very stable and mature
- Excellent performance for sync code
- Large community

**Cons**:
- Blocks thread pool
- Adds overhead
- Not true async

---

#### asyncpg (PostgreSQL) ⭐ **RECOMMENDED**
- **Asyncio Support**: ✅ **Native async**
- **Latest Version**: 0.29.x
- **Type**: Asyncio-native
- **Status**: Excellent, actively maintained
- **Performance**: 2-5x faster than psycopg2

```python
# ✅ Using asyncpg (best practice)
import asyncio
import asyncpg

async def query_db():
    # Create connection pool for best performance
    pool = await asyncpg.create_pool(
        user='postgres',
        password='password',
        database='test',
        host='127.0.0.1',
        min_size=10,
        max_size=10,
    )
    
    async with pool.acquire() as connection:
        result = await connection.fetch('SELECT * FROM users')
        return result
```

**Pros**:
- ✨ Native asyncio support
- 🚀 2-5x faster than psycopg2
- 📚 Connection pooling built-in
- 🔒 Prepared statements support
- 🎯 Type mapping

**Cons**:
- PostgreSQL only
- Slightly less mature than psycopg2

---

### MySQL / MariaDB

#### mysql-connector-python
- **Asyncio Support**: 🔄 **Workaround only**
- **Latest Version**: 8.x
- **Type**: Synchronous
- **Status**: Official but no async support

```python
# ❌ Not recommended for async
import asyncio
import mysql.connector

async def query_db():
    loop = asyncio.get_event_loop()
    
    def _execute():
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="test"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

**Pros**: Official driver, good documentation
**Cons**: No async support, slow for concurrent operations

---

#### PyMySQL
- **Asyncio Support**: 🔄 **Workaround only**
- **Latest Version**: 1.x
- **Type**: Pure Python, Synchronous
- **Status**: Adequate but no async

```python
# ❌ Workaround needed
async def query_db():
    loop = asyncio.get_event_loop()
    
    def _execute():
        import pymysql
        conn = pymysql.connect(host='localhost', user='root', password='password', database='test')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

**Pros**: Pure Python, easy to debug
**Cons**: Slower, no async support

---

#### aiomysql ⭐ **RECOMMENDED**
- **Asyncio Support**: ✅ **Native async**
- **Latest Version**: 0.2.x
- **Type**: Asyncio-native (fork of PyMySQL)
- **Status**: Good, actively maintained
- **Performance**: ~2x faster than mysql.connector

```python
# ✅ Using aiomysql (best practice)
import asyncio
import aiomysql

async def query_db():
    pool = await aiomysql.create_pool(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        db='test',
        minsize=5,
        maxsize=15,
    )
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM users")
            result = await cursor.fetchall()
            return result
    
    pool.close()
    await pool.wait_closed()
```

**Pros**:
- ✨ Native asyncio
- 📚 Connection pooling
- 🎯 Good compatibility with PyMySQL syntax
- 🚀 Decent performance

**Cons**:
- Less mature than alternatives
- Smaller community

---

#### asyncmy
- **Asyncio Support**: ✅ **Native async**
- **Latest Version**: 0.2.x
- **Type**: Asyncio-native
- **Status**: Newer, gaining traction
- **Performance**: Comparable to aiomysql

```python
# ✅ Using asyncmy (newer option)
import asyncio
import asyncmy

async def query_db():
    pool = await asyncmy.create_pool(
        host='localhost',
        port=3306,
        user='root',
        password='password',
        db='test',
    )
    
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            await cursor.execute("SELECT * FROM users")
            result = await cursor.fetchall()
            return result
    
    pool.close()
```

**Pros**:
- ✨ Native asyncio
- 🚀 More performant than aiomysql
- 📦 Modern codebase

**Cons**:
- Newer, less battle-tested
- Smaller community

---

### SQLite

#### sqlite3 (Built-in)
- **Asyncio Support**: 🔄 **Workaround only**
- **Latest Version**: 3.x (Python standard library)
- **Type**: Synchronous
- **Status**: Standard library, mature
- **Note**: By design, SQLite is lightweight and not designed for async

```python
# ❌ Using with run_in_executor (the only way)
import asyncio
import sqlite3

async def query_db(db_path: str, query: str):
    loop = asyncio.get_event_loop()
    
    def _execute():
        conn = sqlite3.connect(db_path)
        try:
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            conn.close()
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

**Pros**:
- Standard library
- Lightweight
- Great for local development/testing

**Cons**:
- No true async support
- Blocks thread pool
- Not suitable for production high-concurrency

---

#### aiosqlite ⭐ **RECOMMENDED for SQLite**
- **Asyncio Support**: ✅ **Native async**
- **Latest Version**: 0.19.x
- **Type**: Asyncio wrapper around sqlite3
- **Status**: Well-maintained, widely used

```python
# ✅ Using aiosqlite (best practice)
import asyncio
import aiosqlite

async def query_db(db_path: str, query: str):
    async with aiosqlite.connect(db_path) as db:
        async with db.execute(query) as cursor:
            result = await cursor.fetchall()
            return result
```

**Pros**:
- ✨ True async API
- 🎯 Simple to use
- 📦 Well-maintained
- 🔒 Good for local development

**Cons**:
- Wrapper overhead
- Still single-file database

---

## NoSQL Databases

### MongoDB

#### pymongo
- **Asyncio Support**: 🔄 **Workaround only**
- **Latest Version**: 4.x
- **Type**: Synchronous
- **Status**: Official driver, no async

```python
# ❌ Workaround with run_in_executor
import asyncio
from pymongo import MongoClient

async def query_db():
    loop = asyncio.get_event_loop()
    
    def _execute():
        client = MongoClient('mongodb://localhost:27017/')
        db = client['test_db']
        return list(db.users.find({}, limit=10))
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

**Cons**: No async support, forced workaround

---

#### motor ⭐ **RECOMMENDED**
- **Asyncio Support**: ✅ **Native async**
- **Latest Version**: 3.x
- **Type**: Asyncio wrapper around pymongo
- **Status**: Official, actively maintained
- **Performance**: Excellent async support

```python
# ✅ Using motor (best practice)
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient

async def query_db():
    client = AsyncIOMotorClient('mongodb://localhost:27017/')
    db = client['test_db']
    
    result = await db.users.find({}, limit=10).to_list(length=None)
    return result
```

**Pros**:
- ✨ Official async driver
- 🚀 Excellent performance
- 🔒 Full pymongo compatibility
- 📚 Great documentation

**Cons**:
- Requires MongoDB setup
- Adds dependency

---

### Redis

#### redis-py
- **Asyncio Support**: 🔄 **Limited (v4.2+)**
- **Latest Version**: 5.x (has async support!)
- **Type**: Originally sync, now has async
- **Status**: Official driver, recently added async

```python
# ❌ Old way (redis-py < 4.2)
import asyncio
import redis

async def query_cache():
    loop = asyncio.get_event_loop()
    
    def _execute():
        r = redis.Redis(host='localhost', port=6379)
        return r.get('key')
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

```python
# ✅ New way (redis-py >= 4.2)
import asyncio
import redis.asyncio as redis

async def query_cache():
    r = await redis.from_url('redis://localhost')
    
    value = await r.get('key')
    await r.close()
    return value
```

**In redis-py 5.x**: Full async support built-in

---

#### aioredis (deprecated in favor of redis.asyncio)
- **Asyncio Support**: ✅ **Native async**
- **Latest Version**: 2.x (merged into redis-py)
- **Type**: Asyncio-native
- **Status**: Merged into redis-py 4.2+

```python
# Use redis.asyncio instead (modern approach)
import redis.asyncio

async def query_cache():
    r = redis.asyncio.from_url('redis://localhost')
    value = await r.get('key')
    await r.close()
```

**Note**: Use `redis.asyncio` from redis-py 5.x instead

---

## Data Warehouses

### DuckDB

#### duckdb
- **Asyncio Support**: ❌ **No native async**
- **Latest Version**: 0.9.x
- **Type**: Synchronous
- **Status**: Modern but no async planned

```python
# ❌ Workaround required
import asyncio
import duckdb

async def query_db():
    loop = asyncio.get_event_loop()
    
    def _execute():
        conn = duckdb.connect(':memory:')
        result = conn.execute("SELECT 42").fetchall()
        return result
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

**Note**: DuckDB is designed for analytical queries, not high-concurrency. Consider alternatives for async OLAP.

**Alternatives**: Polars with async I/O, or async DB with analytical capabilities

---

### Snowflake

#### snowflake-connector-python
- **Asyncio Support**: ❌ **No async**
- **Latest Version**: 3.x
- **Type**: Synchronous
- **Status**: Official but no async

```python
# ❌ Workaround needed
import asyncio
from snowflake.connector import connect

async def query_db():
    loop = asyncio.get_event_loop()
    
    def _execute():
        conn = connect(
            user='user',
            password='password',
            account='account'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM table")
        return cursor.fetchall()
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

**Note**: Use connection pooling to minimize overhead

---

### Oracle Database

#### cx_Oracle (now oracle-db-pythonlib)
- **Asyncio Support**: 🔄 **Workaround only**
- **Latest Version**: 9.x (cx_Oracle: legacy name)
- **Type**: Synchronous
- **Status**: Official Oracle driver, no native async (yet)

```python
# ❌ Using with workaround
import asyncio
import oracledb

async def query_db():
    loop = asyncio.get_event_loop()
    
    def _execute():
        conn = oracledb.connect(
            user="scott",
            password="tiger",
            dsn="localhost/xe"
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        return cursor.fetchall()
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

**Pros**:
- Official Oracle driver
- Production-grade stability
- Excellent documentation
- Rich feature set (LOBs, batching, etc.)

**Cons**:
- No native async support
- Blocks thread pool on concurrent queries
- Overhead for high-concurrency scenarios
- Oracle Instant Client dependency

**Note**: Oracle announced async support is under consideration but no ETA. For high-concurrency async workloads, consider connection pooling at application level or cloud DB alternatives.

---

#### oracledb (oracle-db-pythonlib - newer)
- **Asyncio Support**: 🔄 **Workaround only (under development)**
- **Latest Version**: 2.x
- **Type**: Synchronous (async planned)
- **Status**: Modern replacement for cx_Oracle, async coming in future releases

```python
# ✅ Still uses run_in_executor for now
import asyncio
import oracledb

async def query_db_async():
    loop = asyncio.get_event_loop()
    conn = oracledb.connect(user="scott", password="tiger", dsn="localhost/xe")
    
    try:
        def _execute(query):
            cursor = conn.cursor()
            cursor.execute(query)
            return cursor.fetchall()
        
        result = await loop.run_in_executor(None, _execute, "SELECT * FROM users")
        return result
    finally:
        conn.close()
```

**Pros**:
- Next-generation driver from Oracle
- Better performance than cx_Oracle
- Async support coming soon (watch roadmap)
- Pure Python or thin/thick client modes

**Cons**:
- No async yet (planned feature)
- Relatively new, smaller community
- Still requires workaround for async

**Watch**: Oracle has indicated async support will be added in future versions. Check [oracle-db-pythonlib releases](https://python-oracledb.readthedocs.io/) for updates.

---

### Teradata

#### teradataml
- **Asyncio Support**: ❌ **No async**
- **Latest Version**: 20.x
- **Type**: Synchronous
- **Status**: Official Teradata ML library, synchronous only

```python
# ❌ Workaround required
import asyncio
from teradataml import create_context, load_query

async def query_teradata():
    loop = asyncio.get_event_loop()
    
    def _execute():
        with create_context(
            host='teradata_host',
            username='user',
            password='password',
            database='db_name',
            logmech='LDAP'
        ) as ctx:
            result = load_query("SELECT COUNT(*) FROM my_table").to_pandas()
            return result
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

**Pros**:
- Official Teradata library
- Integrated ML capabilities
- Pandas/DataFrame integration
- Production-grade stability

**Cons**:
- No native async support
- Blocks thread pool
- Complex connection setup
- Heavy dependency footprint

**Note**: Teradata's architecture (MPP, distributed queries) doesn't align naturally with asyncio for true concurrency benefits. For high concurrency, consider:
1. Connection pooling via Teradata SQL Assistant or similar
2. Batch operations to minimize query count
3. Native Teradata parallel processing capabilities

---

#### teradata-sqlalchemy
- **Asyncio Support**: ❌ **No async**
- **Latest Version**: 2.x
- **Type**: SQLAlchemy dialect (synchronous)
- **Status**: Teradata SQLAlchemy driver, sync only

```python
# ❌ With workaround
import asyncio
from sqlalchemy import create_engine, text

async def query_teradata_sqlalchemy():
    loop = asyncio.get_event_loop()
    
    def _execute():
        # Create Teradata connection string
        engine = create_engine(
            'teradata://user:password@host/db_name'
        )
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM my_table LIMIT 10"))
            return [tuple(row) for row in result]
    
    result = await loop.run_in_executor(None, _execute)
    return result
```

**Pros**:
- SQLAlchemy integration (portable)
- ORM capabilities
- Connection pooling built-in
- Works with SQLAlchemy async (but Teradata doesn't)

**Cons**:
- Teradata dialect doesn't support async
- SQLAlchemy async mode can't be used with Teradata
- Still requires `run_in_executor()`

**Workaround**: Use SQLAlchemy's `create_engine()` with connection pool settings optimized for concurrency:

```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    'teradata://user:password@host/db_name',
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
)
```

---

## Summary Table

| Database | Sync Driver | Async Driver | Recommended |
|----------|------------|--------------|-------------|
| **PostgreSQL** | psycopg2 | asyncpg ⭐ | asyncpg |
| **MySQL** | mysql-connector | aiomysql ⭐ | aiomysql or asyncmy |
| **SQLite** | sqlite3 | aiosqlite ⭐ | aiosqlite |
| **MongoDB** | pymongo | motor ⭐ | motor |
| **Redis** | redis-py | redis.asyncio ⭐ | redis.asyncio |
| **Oracle** | oracledb | ❌ (async coming) | Workaround + pooling |
| **Teradata** | teradataml | ❌ None | Workaround + pooling |
| **DuckDB** | duckdb | ❌ None | Workaround |
| **Snowflake** | snowflake-connector | ❌ None | Workaround |

---

## Performance Comparison

### asyncio Native vs run_in_executor()

**Scenario**: 100 concurrent database queries

```
Native Asyncio (asyncpg):    0.45s ✅ Optimal
run_in_executor() (psycopg2): 2.5s ⚠️ 5.5x slower
```

**Why?**:
1. Native asyncio avoids thread pool overhead
2. Better scheduling and resource utilization
3. No context switching between threads

---

## Best Practices

### 1. Choose Native Async When Possible
```python
# ✅ Good
import asyncpg

async def get_users():
    pool = await asyncpg.create_pool('postgresql://...')
    async with pool.acquire() as conn:
        return await conn.fetch('SELECT * FROM users')

# ❌ Avoid
import psycopg2
import asyncio

async def get_users():
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, _psycopg2_query)
```

### 2. Use Connection Pooling
```python
# ✅ Good - Pool reuses connections
pool = await asyncpg.create_pool(
    'postgresql://...',
    min_size=5,
    max_size=20,
)

# ❌ Avoid - New connection per query
conn = await asyncpg.connect('postgresql://...')
```

### 3. Handle Timeouts
```python
# ✅ Good
try:
    result = await asyncio.wait_for(
        db_query(),
        timeout=5.0
    )
except asyncio.TimeoutError:
    logger.error("Query timeout")

# ❌ Avoid
result = await db_query()  # May hang indefinitely
```

### 4. Clean Up Resources
```python
# ✅ Good
async with aiosqlite.connect(db_path) as db:
    result = await db.execute(query)

# ❌ Avoid
db = await aiosqlite.connect(db_path)
result = await db.execute(query)
# Forgot to close!
```

---

## Decision Tree

```
Do you need asyncio?
├─ NO → Use traditional driver (psycopg2, sqlite3, etc.)
│
└─ YES → Which database?
    ├─ PostgreSQL → Use asyncpg ⭐
    ├─ MySQL → Use aiomysql or asyncmy ⭐
    ├─ SQLite → Use aiosqlite ⭐
    ├─ MongoDB → Use motor ⭐
    ├─ Redis → Use redis.asyncio ⭐
    └─ Other (DuckDB, Snowflake, etc.)
        └─ Check: Is async driver available?
            ├─ YES → Use it
            └─ NO → Use run_in_executor() workaround
```

---

## Installation Guide

### PostgreSQL with asyncpg
```bash
pip install asyncpg
```

### MySQL with aiomysql
```bash
pip install aiomysql
```

### SQLite with aiosqlite
```bash
pip install aiosqlite
```

### MongoDB with motor
```bash
pip install motor
```

### Redis with redis[asyncio]
```bash
pip install redis[asyncio]
```

---

## Common Pitfalls

### 1. Mixing Sync and Async
```python
# ❌ WRONG - psycopg2 is blocking
import psycopg2
import asyncio

async def my_async_function():
    conn = psycopg2.connect(...)  # This blocks!
    return conn.execute("SELECT ...")
```

### 2. Blocking in Executor Thread
```python
# ⚠️ OK but slow - blocks thread pool
async def query():
    loop = asyncio.get_event_loop()
    result = await loop.run_in_executor(None, blocking_db_call)
    # If many tasks do this, thread pool exhausted

# ✅ Better - native async doesn't block
async def query():
    result = await async_db.fetch(...)
```

### 3. No Timeout
```python
# ❌ Dangerous - may hang forever
result = await some_db_query()

# ✅ Safe
result = await asyncio.wait_for(some_db_query(), timeout=30)
```

### 4. Connection Leak
```python
# ❌ Bad - connection never closed
async def query():
    db = await aiosqlite.connect(':memory:')
    result = await db.execute("SELECT 1")
    return result  # db not closed!

# ✅ Good
async def query():
    async with aiosqlite.connect(':memory:') as db:
        result = await db.execute("SELECT 1")
        return result
```

---

## Conclusion

**For async Python applications:**

1. **Always prefer native async drivers** when available
2. **asyncpg** for PostgreSQL (2-5x faster)
3. **aiomysql/asyncmy** for MySQL (good performance)
4. **aiosqlite** for SQLite (simple and effective)
5. **motor** for MongoDB (official async driver)
6. **redis.asyncio** for Redis (native support in 5.x)

Only use `run_in_executor()` as a temporary workaround for databases without async support.

---

*Last Updated: February 28, 2026*
