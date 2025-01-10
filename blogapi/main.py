from contextlib import asynccontextmanager

from fastapi import FastAPI

from blogapi.core.database import database
from blogapi.routers.post import router as post_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.connect()
    yield
    await database.disconnect()


app = FastAPI(lifespan=lifespan)


app.include_router(post_router)


# @app.get("/")
# async def root():
#     return {"msg": "Hello World!"}
