import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient

os.environ["ENV_STATE"] = "test"

from blogapi.core.database import database, metadata, user_table
from blogapi.main import app


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    """
    Synchronous test client fixture.
    """
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    # Clear the database tables by truncating them, restarting identity, and cascading
    await database.connect()
    for table in reversed(metadata.sorted_tables):
        await database.execute(
            f'TRUNCATE TABLE "{table.name}" RESTART IDENTITY CASCADE;'
        )
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    """
    Asynchronous test client fixture for testing async endpoints.
    """
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url=client.base_url
    ) as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@example.com", "password": "1234"}
    await async_client.post("/register", json=user_details)
    query = user_table.select().where(
        user_table.c.email == user_details["email"],
    )
    user = await database.fetch_one(query)
    user_details["id"] = user.id
    return user_details
