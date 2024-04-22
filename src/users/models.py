from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from database import BaseDBModel, engine


class User(BaseDBModel):
    __tablename__ = "users"
    id = Column(Integer,autoincrement=True, primary_key=True)
    nicname = Column(String)
    email = Column(String,default=None)
    hashed_password=Column(String)
    collars = relationship("Collar", back_populates="user")


BaseDBModel.metadata.create_all(bind=engine)