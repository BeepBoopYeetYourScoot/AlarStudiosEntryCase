from typing import AsyncGenerator

import loguru
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from api.routers.data_collector import (
    get_sessions_for_tables,
)
from api.tests.constants import DATA_ENDPOINT_INITIAL_TEST_DATA
from db.models import Base
from main import app
from settings.settings import DATABASE

TEST_DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{DATABASE['USER']}:{DATABASE['PASSWORD']}@"
    f"{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['TEST_DB_NAME']}"
)

test_engine = engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=True,
    poolclass=NullPool,
    connect_args={"timeout": 2},
)

TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False)


def get_test_data_sources():
    return list(DATA_ENDPOINT_INITIAL_TEST_DATA.keys())


def get_test_sessions_for_tables():
    return [TestSessionLocal() for _ in range(len(get_test_data_sources()))]


app.dependency_overrides[get_sessions_for_tables] = (
    get_test_sessions_for_tables
)


@pytest_asyncio.fixture
def client() -> AsyncClient:
    return AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    )


@pytest_asyncio.fixture(scope="function")
async def async_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function", autouse=True)
async def create_test_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def initial_data(async_session: AsyncSession):
    async with async_session.begin():
        loguru.logger.debug(
            f"Accessing {async_session} inside {initial_data} method"
        )
        async_session.add_all(
            [
                table(**data)
                for table, data in DATA_ENDPOINT_INITIAL_TEST_DATA.items()
            ]
        )
    await async_session.commit()
