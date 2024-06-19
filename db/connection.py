from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from settings.settings import DATABASE

CONNECTION_STRING = (
    f"postgresql+asyncpg://"
    f"{DATABASE['USER']}:{DATABASE['PASSWORD']}@"
    f"{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}"
)

async_engine = create_async_engine(CONNECTION_STRING, echo=True, future=True)
AsyncSessionLocal = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()
