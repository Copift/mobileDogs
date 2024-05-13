from sqlalchemy import Column, Integer, String,ForeignKey
from sqlalchemy.orm import relationship
from database import BaseDBModel, engine

from tasks.models import Task
class User(BaseDBModel):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True, primary_key=True)
    nicname = Column(String)
    email = Column(String,default=None)
    hashed_password=Column(String)
    score=Column(Integer,default=0)
    role_id=Column(Integer,ForeignKey("Role.id"))
    collars = relationship("Collar", back_populates="user",foreign_keys="Collar.owner_id")
    support_collars=relationship("Collar", back_populates="support",foreign_keys="Collar.support_id")
    closed_alerts=relationship("Alert", back_populates="closed_by",foreign_keys="Alert.closed_by_id")
    tasksCreated = relationship("Task", back_populates="created_by", foreign_keys="Task.created_by_id")
    tasksGeted=relationship("Task", back_populates="send_to", foreign_keys="Task.send_to_id")
    role=relationship("Role",back_populates="users",foreign_keys="User.role_id")


class Role(BaseDBModel):
    __tablename__ = "Role"
    id=Column(Integer,autoincrement=True,primary_key=True)
    name=Column(String,unique=True)
    users=relationship("User",back_populates="role")