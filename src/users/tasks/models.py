from sqlalchemy import Column, Integer, String,DATETIME,DateTime, ForeignKey
from sqlalchemy.types import BLOB
from sqlalchemy.orm import relationship
from database import BaseDBModel, engine


import users.models
class Task(BaseDBModel):
    __tablename__ = "tasks"
    id = Column(Integer,autoincrement=True, primary_key=True)
    created_by_id = Column(Integer,ForeignKey("users.id"))
    send_to_id = Column(Integer,ForeignKey("users.id"))
    type_id =Column(Integer, ForeignKey("TaskType.id"))
    verify_id=Column(Integer, ForeignKey("Verify.id"))
    status_id=Column(Integer, ForeignKey("TaskStatus.id"))
    datetime_start = Column(DATETIME)
    created_by = relationship("users", back_populates="tasksCreated")
    send_to = relationship("users", back_populates="tasksGeted")
    type = relationship("TaskType", back_populates="tasks", uselist=False)
    status = relationship("TaskStatus", back_populates="tasks", uselist=False)

class TaskType(BaseDBModel):
    __tablename__ = "TaskType"
    id = Column(Integer, autoincrement=True, primary_key=True)
    deadline_time=Column(DATETIME)
    name=Column(String)
    verify_type=Column(Integer, ForeignKey("VerifyType.id"))
    tasks=relationship("tasks", back_populates="type")
    verify = relationship("VerifyType", uselist=False)
class TaskStatus(BaseDBModel):
    __tablename__ = "TaskStatus"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name=Column(String)
    tasks=relationship("tasks", back_populates="status")

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
    name=Column(String)
    verify = relationship("Verify")
    task_type = relationship("TaskType")


BaseDBModel.metadata.create_all(bind=engine)