# example of using asyncio to run long running sql queries in the background
import asyncio
import time

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# create the engine
engine = create_async_engine(
    "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
    echo=True,
)

# create a configured "Session" class
Session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

# run the code
async def main():
    async with Session() as session:
        # run a statement
        result = await session.execute(
            sa.select(sa.func.count("*")).select_from(sa.table("users"))
        )
        print(result.scalar())


if __name__ == "__main__":
    asyncio.run(main())
