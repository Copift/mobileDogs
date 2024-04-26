
from pydantic import BaseModel



class User(BaseModel):
    collars: list
    nicname: str
    password: str
    email: str | None = None

