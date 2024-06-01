import datetime
from typing import Optional, Union
from pydantic import Field

from mainModels import OrmBase


class CollarBase(OrmBase):
 mac: str


class CollarCreate(CollarBase):
 description: str

class CollarSend(CollarBase):
 coord: str

class Migrate(OrmBase):
 mac:str
 coord:str
 time: datetime.datetime

class Collar(CollarBase):
 description: str
 migrate: Optional[list[Migrate]]
 owner_id: Optional[int] = Field(default=None)



class CollarWithCheck(Collar):
    checks:list |None
