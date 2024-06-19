import loguru
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import get_session
from db.models import FirstTable, SecondTable, ThirdTable

router = APIRouter()


@router.get("/collect-data")
async def collect_data(session: AsyncSession = Depends(get_session)):
    result = []
    for table in (FirstTable, SecondTable, ThirdTable):
        try:
            result.extend(
                (await session.execute(select(table))).scalars().all()
            )
        except Exception as e:
            loguru.logger.debug(
                f"Got {e} when accessing {table.__tablename__}"
            )
    result.sort(key=lambda obj: obj.id)
    return result
