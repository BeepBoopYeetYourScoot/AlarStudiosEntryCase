from typing import AsyncGenerator

import loguru
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from api.tests.constants import DATA_ENDPOINT_INITIAL_TEST_DATA
from db.connection import get_session
from db.models import Base, FirstTable, SecondTable, ThirdTable
from main import app

TEST_DATABASE_URL = (
    "postgresql+asyncpg://postgres:root_password@localhost:5432/test"
)

test_engine = engine = create_async_engine(
    TEST_DATABASE_URL, echo=True, poolclass=NullPool
)

TestSessionLocal = sessionmaker(
    test_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


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
                FirstTable(**DATA_ENDPOINT_INITIAL_TEST_DATA[0]),
                SecondTable(**DATA_ENDPOINT_INITIAL_TEST_DATA[1]),
                ThirdTable(**DATA_ENDPOINT_INITIAL_TEST_DATA[2]),
            ]
        )
    await async_session.commit()
