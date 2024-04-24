
from pydantic import BaseModel



class User(BaseModel):
    collars: list
    nicname: str
    password: str
    email: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None





class UserInDB(BaseModel):
    id: int
    nicname: str
    email: str | None = None
    hashed_password: str
    collars: list


