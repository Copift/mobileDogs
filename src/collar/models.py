from sqlalchemy import Column, ForeignKey, Integer, String,DATETIME
from sqlalchemy.orm import relationship

from database import BaseDBModel, engine


class Collar(BaseDBModel):
    __tablename__ = "collar"

  #  id = Column(Integer,autoincrement=True,)
    mac = Column(String,unique=True, primary_key=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="collars")
    migrate = relationship("Migrate", back_populates="collar")
class Migrate(BaseDBModel):
    __tablename__ = "migrate"

    id = Column(Integer,autoincrement=True,primary_key=True)
    mac =  Column(String, ForeignKey("collar.mac"))
    coord = Column(String)
    time=Column(DATETIME)
    collar = relationship("Collar", back_populates="migrate")

BaseDBModel.metadata.create_all(bind=engine)