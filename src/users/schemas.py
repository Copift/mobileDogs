
from  mainModels import OrmBase
import collar.models as collarModels
import collar.schemas as collarSchemas
class UserAdd(OrmBase):
    nicname: str
    password: str
    email: str | None = None
class User(OrmBase):
    collars:list
    nicname: str
    password: str
    email: str | None = None

class UserData(OrmBase):
    nicname: str
    id:int


class Token(OrmBase):
    access_token: str
    token_type: str


class TokenData(OrmBase):
    username: str | None = None

class UserShow(OrmBase):
    nicname: str
    id:int

    email: str | None = None

class Role(OrmBase):
    id: int
    name: str
class UserInDB(OrmBase):
    id: int
    nicname: str
    email: str | None = None
    hashed_password: str
    collars: list
    role: Role
    tasksCreated: list| None = None
    tasksGeted: list| None = None

class UserInDBWithCollarsCheck(OrmBase):
    user:UserShow
    collars: list[collarSchemas.CollarWithCheck]

