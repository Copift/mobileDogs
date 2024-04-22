
from pydantic import BaseModel



class User(BaseModel):
    nicname: str
    password: str
    email: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None





class UserInDB(BaseModel):
    nicname: str
    email: str | None = None
    hashed_password: str



