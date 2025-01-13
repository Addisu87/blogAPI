import logging

from fastapi import APIRouter, HTTPException, status

from blogapi.core.database import database, user_table
from blogapi.core.security import get_user
from blogapi.schemas.user import UserIn

logger = logging.getLogger(__name__)

router = APIRouter(tags=["users"])


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists!",
        )
    # This is bad habit, the password is not save as a plain text, you should hashed it
    query = user_table.insert().values(email=user.email, password=user.password)

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User Created."}
