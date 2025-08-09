import asyncio

import asyncpg


async def run():
    conn = await asyncpg.connect(
        user="test_db_user", password="1234", database="test_db", host="localhost"
    )
    values = await conn.fetch(
        "SELECT count(*) FROM iris WHERE sepal_length > $1",
        1,
    )
    await conn.close()
    return values


loop = asyncio.get_event_loop()
res = loop.run_until_complete(run())
print(res)
