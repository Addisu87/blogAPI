import pytest

from blogapi.core.security import get_user


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await get_user(registered_user["email"])

    assert user.email == registered_user["email"]
