from sqlalchemy import Column, Integer, String,DATETIME,DateTime, ForeignKey
from sqlalchemy.types import BLOB
from sqlalchemy.orm import relationship
from database import BaseDBModel, engine, DBSession


class Task(BaseDBModel):
    __tablename__ = "tasks"
    id = Column(Integer,autoincrement=True, primary_key=True)
    created_by_id = Column(Integer,ForeignKey("users.id"), default=None)
    send_to_id = Column(Integer,ForeignKey("users.id"), default=None)
    type_id =Column(Integer, ForeignKey("TaskType.id"), default=None)
    verify_id=Column(Integer, ForeignKey("Verify.id"), default=None)
    status_id=Column(Integer, ForeignKey("TaskStatus.id"), default=None)
    datetime_start = Column(DATETIME)
    created_by = relationship("users.models.User", back_populates="tasksCreated", foreign_keys="Task.created_by_id")
    send_to = relationship("users.models.User", back_populates="tasksGeted", foreign_keys="Task.send_to_id")
    type = relationship("TaskType", back_populates="tasks", uselist=False, foreign_keys="Task.type_id")
    status = relationship("TaskStatus", back_populates="tasks", uselist=False, foreign_keys="Task.status_id")

class TaskType(BaseDBModel):
    __tablename__ = "TaskType"
    id = Column(Integer, autoincrement=True, primary_key=True)
    deadline_time=Column(Integer)
    name=Column(String,unique=True)
    desc = Column(String)
    verify_type=Column(Integer, ForeignKey("VerifyType.id"))
    tasks=relationship("Task", back_populates="type")
    verify = relationship("VerifyType", uselist=False)
class TaskStatus(BaseDBModel):
    __tablename__ = "TaskStatus"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name=Column(String,unique=True)
    desc=Column(String)
    tasks=relationship("Task", back_populates="status")

class Verify(BaseDBModel):
    __tablename__ = "Verify"
    id = Column(Integer, autoincrement=True, primary_key=True)
    verify_type=Column(Integer, ForeignKey("VerifyType.id"))
    comment=Column(String,default=None)
    img = Column(BLOB, default=None)
    geo=Column(String,default=None)
    verify_type_rel = relationship("VerifyType", uselist=False)
class VerifyType(BaseDBModel):
    __tablename__ = "VerifyType"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name=Column(String,unique=True)
    verify = relationship("Verify")
    task_type = relationship("TaskType")


