import pytest
from fastapi import HTTPException
from jose import jwt

from blogapi.core.deps import (
    authenticate_user,
    get_current_user,
    get_subject_for_token_type,
    get_user,
)
from blogapi.core.security import (
    ALGORITHM,
    SECRET_KEY,
    access_token_expire_minutes,
    confirm_token_expire_minutes,
    create_access_token,
    create_confirmation_token,
    get_password_hash,
    verify_password,
)


def test_access_token_expire_minutes():
    assert access_token_expire_minutes() == 30


def test_confirm_token_expire_minutes():
    assert confirm_token_expire_minutes() == 1440


def test_create_access_token():
    token = create_access_token("123")

    assert {"sub": "123", "type": "access"}.items() <= jwt.decode(
        token, key=SECRET_KEY, algorithms=[ALGORITHM]
    ).items()


def test_confirmation_access_token():
    token = create_confirmation_token("123")

    assert {"sub": "123", "type": "confirmation"}.items() <= jwt.decode(
        token, key=SECRET_KEY, algorithms=[ALGORITHM]
    ).items()


def test_get_subject_for_token_type_valid_access():
    email = "test@example.com"
    token = create_access_token(email)

    assert email == get_subject_for_token_type(token, "access")


def test_get_subject_for_token_type_valid_confirmation():
    email = "test@example.com"
    token = create_confirmation_token(email)

    assert email == get_subject_for_token_type(token, "confirmation")


def test_get_subject_for_token_type_expired(mocker):
    mocker.patch("blogapi.core.security.access_token_expire_minutes", return_value=-1)
    email = "test@example.com"
    token = create_access_token(email)
    with pytest.raises(HTTPException) as exc_info:
        get_subject_for_token_type(token, "access")

    assert "Token has expired" == exc_info.value.detail


def test_get_subject_for_token_type_invalid_token():
    token = "invalid token"
    with pytest.raises(HTTPException) as exc_info:
        get_subject_for_token_type(token, "access")

    assert "Invalid token" == exc_info.value.detail


def test_get_subject_for_token_type_missing_sub():
    email = "text@example.com"
    token = create_access_token(email)
    payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    del payload["sub"]

    token = jwt.encode(payload, key=SECRET_KEY, algorithm=ALGORITHM)

    with pytest.raises(HTTPException) as exc_info:
        get_subject_for_token_type(token, "access")

    assert "Token is missing 'sub' field" == exc_info.value.detail


def test_get_subject_for_token_type_wrong_type():
    email = "test@example.com"
    token = create_confirmation_token(email)
    with pytest.raises(HTTPException) as exc_info:
        get_subject_for_token_type(token, "access")

    assert "Token has incorrect type, expected 'access'" == exc_info.value.detail


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


@pytest.mark.anyio
async def test_get_current_user(registered_user: dict):
    token = create_access_token(registered_user["email"])
    user = await get_current_user(token)
    assert user["email"] == registered_user["email"]


@pytest.mark.anyio
async def test_get_current_user_invalid_token():
    with pytest.raises(HTTPException):
        await get_current_user("invalid token")


@pytest.mark.anyio
async def test_get_current_user_wrong_type_token(registered_user: dict):
    token = create_confirmation_token(registered_user["email"])

    with pytest.raises(HTTPException):
        await get_current_user(token)
