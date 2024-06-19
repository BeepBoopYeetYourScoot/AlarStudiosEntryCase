from contextlib import asynccontextmanager

import loguru
import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

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


async def get_test_session():
    async with TestSessionLocal() as session:
        yield session


app.dependency_overrides[get_session] = get_test_session


@pytest_asyncio.fixture
def client():
    return AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    )


@pytest_asyncio.fixture(scope="function")
async def async_session():
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_test_database():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def initial_data(async_session: AsyncSession):
    async with async_session.begin():
        loguru.logger.debug(f"Accessing {async_session}")
        async_session.add_all(
            [
                FirstTable(id=1, name="bruh"),
                SecondTable(id=11, name="bruh"),
                ThirdTable(id=21, name="bruh"),
            ]
        )
    await async_session.commit()
