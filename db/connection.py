from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
)

from settings.settings import DATABASE

CONNECTION_STRING = (
    f"postgresql+asyncpg://"
    f"{DATABASE['USER']}:{DATABASE['PASSWORD']}@"
    f"{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}"
)

async_engine = create_async_engine(
    CONNECTION_STRING,
    echo=True,
    future=True,
    connect_args={"timeout": 2},
)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
