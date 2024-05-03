from datetime import datetime
from users.schemas import UserInDB
from pydantic import BaseModel, Field
from typing import Optional

class TaskType(BaseModel):
    id: int
    deadline_time: int
    name: str
    desc: Optional[str] = None
    verify_type_id: int

    class Config:
        orm_mode = True


class TaskStatus(BaseModel):
    id: int
    name: str
    desc: Optional[str] = None

    class Config:
        orm_mode = True


class Verify(BaseModel):
    id: int
    verify_type_id: int
    comment: Optional[str] = None
    img: Optional[bytes] = None
    geo: Optional[str] = None

    class Config:
        orm_mode = True


class VerifyType(BaseModel):
    id: int
    name: str
    verify_id: Optional[int] = None
    task_type_id: Optional[int] = None

    class Config:
        orm_mode = True


class TaskinDb(BaseModel):
    id: int
    created_by_id: int
    send_to_id: int
    type_id: int
    verify_id: int
    status_id: int
    datetime_start: Optional[datetime] = None
    datetime_end: Optional[datetime] = None
    created_by: Optional['UserInDB']
    send_to: Optional['UserInDB'] = None
    type: Optional['TaskType'] = None
    status: Optional['TaskStatus'] = None

    class Config:
        orm_mode = True
class TaskBase(BaseModel):
    # Fields that are common to all tasks

    send_to_id: int
    type_id: int