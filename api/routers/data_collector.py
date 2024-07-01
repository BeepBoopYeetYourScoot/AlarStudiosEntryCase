import asyncio

import loguru
from fastapi import APIRouter, Depends
from sqlalchemy import select

from db.connection import AsyncSessionLocal
from db.models import FirstTable, SecondTable, ThirdTable

data_collection_router = APIRouter()


async def get_data_sources():
    return FirstTable, SecondTable, ThirdTable


async def get_sessions_for_tables(tables=Depends(get_data_sources)):
    """
    Each concurrent query needs its separate connection
    """
    assert isinstance(tables, tuple)
    return [AsyncSessionLocal() for _ in range(len(tables))]


@data_collection_router.get("/collect-data")
async def collect_data(
    tables=Depends(get_data_sources),
    sessions=Depends(get_sessions_for_tables),
):
    loguru.logger.debug(f"Querying {tables=} with {sessions=}")
    queries = [
        session.execute(select(table))
        for session, table in zip(sessions, tables)
    ]
    gathered_data = await asyncio.gather(*queries, return_exceptions=True)
    results = []
    for result in gathered_data:
        if not isinstance(result, Exception):
            results.extend(result.scalars().all())
        else:
            loguru.logger.debug(
                f"Got error='{result}' when accessing sources."
            )
    await asyncio.gather(
        *[session.close() for session in sessions], return_exceptions=True
    )
    results.sort(key=lambda obj: obj.id)
    return results
