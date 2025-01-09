from fastapi import FastAPI

from blogapi.routers import post, user

app = FastAPI()
print("FastAPI app instance created:", app)


app.include_router(user.router)
app.include_router(post.router)


@app.get("/")
async def root():
    return {"msg": "Hello World!"}
