from sqlalchemy import Column, Integer, String,DATETIME,DateTime, ForeignKey,Boolean,ForeignKeyConstraint
from sqlalchemy.types import BLOB,LargeBinary,TIMESTAMP
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
    datetime_start = Column(TIMESTAMP)
    datetime_end = Column(TIMESTAMP)
    collar_mac=Column(String, ForeignKey("Collar.mac"))
    score=Column(Integer,default=0)
    restarted=Column(Boolean,default=False)
    collar=relationship("Collar", back_populates="tasks",foreign_keys='Task.collar_mac')

    created_by = relationship("User", back_populates="tasksCreated", foreign_keys="Task.created_by_id")
    send_to = relationship("User", back_populates="tasksGeted", foreign_keys="Task.send_to_id")
    type = relationship("TaskType", back_populates="tasks", uselist=False, foreign_keys="Task.type_id")
    status = relationship("TaskStatus", back_populates="tasks", uselist=False, foreign_keys="Task.status_id")
    verify=relationship("Verify", back_populates="task", foreign_keys="Task.verify_id")

class TaskType(BaseDBModel):
    __tablename__ = "TaskType"
    id = Column(Integer, autoincrement=True, primary_key=True)
    deadline_time=Column(Integer)
    name=Column(String,unique=True)
    desc = Column(String)
    award=Column(Integer)
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
    canceled=Column(Boolean,default=False)
    img = Column(LargeBinary, default=None)
    geo=Column(String,default=None)
    verify_type_rel = relationship("VerifyType", uselist=False,foreign_keys="Verify.verify_type")
    task=relationship("Task", back_populates="verify", uselist=False)
class VerifyType(BaseDBModel):
    __tablename__ = "VerifyType"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name=Column(String,unique=True)
    verify = relationship("Verify")
    task_type = relationship("TaskType")


