import pytest
from fastapi import HTTPException
from jose import jwt

from blogapi.core.deps import authenticate_user, get_user
from blogapi.core.security import (
    ALGORITHM,
    SECRET_KEY,
    access_token_expire_minutes,
    create_access_token,
    get_password_hash,
    verify_password,
)


def test_access_token_expire_minutes():
    assert access_token_expire_minutes() == 30


def test_create_access_token():
    token = create_access_token("123")

    assert {"sub": "123"}.items() <= jwt.decode(
        token, key=SECRET_KEY, algorithms=[ALGORITHM]
    ).items()


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


@pytest.mark.anyio
async def test_authenticate_user(registered_user: dict):
    user = await authenticate_user(
        registered_user["email"],
        registered_user["password"],
    )
    assert user["email"] == registered_user["email"]


@pytest.mark.anyio
async def test_authenticate_user_not_found():
    with pytest.raises(HTTPException):
        await authenticate_user("test@example.com", "1234")


@pytest.mark.anyio
async def test_authenticate_user_wrong_password(registered_user: dict):
    with pytest.raises(HTTPException):
        await authenticate_user(registered_user["email"], "wrong password")
