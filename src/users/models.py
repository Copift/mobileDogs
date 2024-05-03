from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import BaseDBModel, engine

from tasks.models import Task
class User(BaseDBModel):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True, primary_key=True)
    nicname = Column(String)
    email = Column(String,default=None)
    hashed_password=Column(String)
    collars = relationship("Collar", back_populates="user")
    tasksCreated = relationship("tasks.models.Task", back_populates="created_by", foreign_keys="Task.created_by_id")
    tasksGeted=relationship("tasks.models.Task", back_populates="send_to", foreign_keys="Task.send_to_id")


