from datetime import datetime
from users.schemas import UserData
from pydantic import BaseModel, Field
from typing import Optional
from sqlalchemy.orm import Query

from pydantic import BaseModel, field_validator

from mainModels import OrmBase

class TaskType(OrmBase):
    id: int
    deadline_time: int
    name: str
    desc: Optional[str] | None


class TaskStatus(OrmBase):
    id: int
    name: str
    desc: Optional[str] = None

    class Config:
        orm_mode = True
class getTasks(OrmBase):
    status_id:Optional[list[int]] | None
    created_by:Optional[bool] | None
    sended_to: Optional[bool] | None

class Verify(OrmBase):


    comment: Optional[str] = None
    img: Optional[bytes] = None
    geo: Optional[str] = None

    class Config:
        orm_mode = True


class VerifyInDb(Verify):
    id: int
    canceled: bool


class VerifyType(OrmBase):
    id: int
    name: str
    verify_id: Optional[int] = None
    task_type_id: Optional[int] = None

    class Config:
        orm_mode = True


class Task(OrmBase):
    id: int
    created_by_id: int
    send_to_id: int
    type_id: int
    verify_id: Optional[int] = None
    status_id: int

    verify:Optional[Verify] =    None
    datetime_start: Optional[datetime] = None
    datetime_end: Optional[datetime] = None
    created_by: UserData
    send_to: UserData
    type: TaskType
    status: TaskStatus

    class Config:
        orm_mode = True
class TaskBase(OrmBase):
    # Fields that are common to all tasks
    collar_mac:str
    send_to_id: int
    type_id: int