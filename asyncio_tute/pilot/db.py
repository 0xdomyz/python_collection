# example of using asyncio to run long running sql queries in the background
import asyncio
import time

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# create the engine
engine = create_async_engine(
    "postgresql+asyncpg://test_db_user:1234@localhost/test_db",
    echo=True,
)

# create a configured "Session" class
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


# async func to run a long running query
async def long_running_query():
    async with Session() as session:
        # run a statement
        print("running long running query")
        result = await session.execute(
            "SELECT count(*) FROM iris WHERE sepal_length > 5"
        )
        print("long running query done")
        print(result.scalar())


async def main():
    res = await asyncio.gather(
        long_running_query(), long_running_query(), long_running_query()
    )
    print(res)


if __name__ == "__main__":
    asyncio.run(main())
