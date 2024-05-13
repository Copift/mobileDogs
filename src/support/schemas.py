from datetime import datetime
from users.schemas import UserData
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Query

from pydantic import BaseModel, field_validator
from mainModels import OrmBase
from collar.schemas import Collar
from pydantic import BaseModel



class Alert(OrmBase):
    desc:str
    collar_mac:str

class AlertInDb(Alert):
    id:int
    closed:bool
    collar:Collar
    closed_by:Optional[UserData]

