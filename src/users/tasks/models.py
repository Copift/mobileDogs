from sqlalchemy import Column, Integer, String,DATETIME
from sqlalchemy.orm import relationship

from database import BaseDBModel, engine


class Task(BaseDBModel):
    __tablename__ = "tasks"
    id = Column(Integer,autoincrement=True, primary_key=True)
    created_by_id = Column(Integer)
    send_to_id=Column(Integer)
    type_id = Column(Integer,default=None)
    deadline_type=Column(Integer)
    datetime_start=Column(DATETIME)


    collars = relationship("Collar", back_populates="user")


BaseDBModel.metadata.create_all(bind=engine)