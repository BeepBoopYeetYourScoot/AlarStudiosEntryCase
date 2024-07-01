import asyncio
import http
from asyncio import gather
from unittest.mock import patch

import loguru
import pytest

from api.tests.constants import (
    DATA_ENDPOINT_URL,
    DATA_ENDPOINT_MERGED_RESULT,
)


@pytest.mark.asyncio
async def test_data_endpoint(client, initial_data):
    """
    Check the correct flow of data acquisition
    """
    response = await client.get(url=DATA_ENDPOINT_URL)
    assert response.status_code == http.HTTPStatus.OK
    data = response.json()
    assert data == DATA_ENDPOINT_MERGED_RESULT
    ids = [obj["id"] for obj in data]
    assert ids == sorted(ids)


@pytest.mark.asyncio
async def test_data_endpoint_wrong_methods(client, initial_data):
    not_allowed_methods = ("post", "put", "patch", "delete")
    responses = [
        await getattr(client, method)(url=DATA_ENDPOINT_URL)
        for method in not_allowed_methods
    ]
    for response in responses:
        assert response.status_code == http.HTTPStatus.METHOD_NOT_ALLOWED


@pytest.mark.asyncio
async def test_data_endpoint_execute_throws_error(client, initial_data):
    """
    Check the flow if session.execute() throws errors.
    """

    with patch(
        "sqlalchemy.ext.asyncio.AsyncSession.execute",
        side_effect=ConnectionError("Mock connection error"),
    ):
        response = await client.get(url=DATA_ENDPOINT_URL)
        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == []


@pytest.mark.asyncio
async def test_data_endpoint_empty_response_on_timeout(client, initial_data):

    async def gather_patch(*args, **kwargs):
        await asyncio.sleep(3)
        loguru.logger.debug(f"Waited 3 seconds")
        return await gather(*args, **kwargs)

    with patch("api.routers.data_collector.asyncio.gather", gather_patch):
        response = await client.get(url=DATA_ENDPOINT_URL)
        assert response.status_code == http.HTTPStatus.OK
        assert response.json() == []
