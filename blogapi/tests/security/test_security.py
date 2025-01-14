import pytest

from blogapi.core.deps import get_user
from blogapi.core.security import get_password_hash, verify_password


def test_get_password_hash():
    password = "testpassword"
    assert verify_password(password, get_password_hash(password))


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await get_user(registered_user["email"])
    assert user is not None, "User not found"
    assert user["email"] == registered_user["email"]


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await get_user("test@example.com")
    assert user is None
