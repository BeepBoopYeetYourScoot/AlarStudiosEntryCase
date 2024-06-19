import http
from unittest.mock import patch

import pytest

from api.tests.constants import (
    DATA_ENDPOINT_INITIAL_TEST_DATA,
    DATA_ENDPOINT_URL,
)


@pytest.mark.asyncio
async def test_data_endpoint(client, initial_data):
    """
    Check the correct flow of data acquisition
    """
    response = await client.get(url=DATA_ENDPOINT_URL)
    assert response.status_code == http.HTTPStatus.OK
    assert len(response.json()) == len(DATA_ENDPOINT_INITIAL_TEST_DATA)
    assert response.json() == DATA_ENDPOINT_INITIAL_TEST_DATA


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
