from pydantic import BaseModel


class User(BaseModel):
    id: str
    username: str
    email: str


class UserInDB(User):
    # password: str
    pass
