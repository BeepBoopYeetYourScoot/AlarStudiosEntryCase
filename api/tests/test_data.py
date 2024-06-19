import loguru
import pytest


@pytest.mark.asyncio
async def test_data_endpoint(client, async_session, initial_data):
    async with client:
        response = await client.get(url="/data")
    assert response.status_code == 200
    assert len(response.json()) == 3
    loguru.logger.debug(f"{response.json()}")
    assert response.json() == [
        {
            "id": 1,
            "name": "bruh",
        },
        {
            "id": 11,
            "name": "bruh",
        },
        {
            "id": 21,
            "name": "bruh",
        },
    ]
