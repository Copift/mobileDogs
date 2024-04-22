import datetime
from typing import Optional, Union
from pydantic import BaseModel, Field

from pydantic import (
 BaseModel,
 EmailStr
)
class CollarBase(BaseModel):
 mac: str

class CollarSend(CollarBase):
 coord: str

class Collar(CollarBase):
 description: str
 owner_id: Optional[str] = Field(default=None)
 

class Migrate(BaseModel):
 mac:str
 coord:str
 time: datetime.datetime

