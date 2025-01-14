import logging

from fastapi import APIRouter, HTTPException, status

from blogapi.core.deps import get_user
from blogapi.core.security import get_password_hash
from blogapi.database.database import database, user_table
from blogapi.models.user import UserIn

logger = logging.getLogger(__name__)

router = APIRouter(tags=["users"])


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with that email already exists!",
        )
    #    Hashed password
    hashed_password = get_password_hash(user.password)
    query = user_table.insert().values(email=user.email, password=hashed_password)

    logger.debug(query)

    await database.execute(query)
    return {"detail": "User Created."}
