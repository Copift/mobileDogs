from sqlalchemy import Column, ForeignKey, Integer, String,DATETIME,TIMESTAMP
from sqlalchemy.orm import relationship

from database import BaseDBModel, engine

import support.models
class Collar(BaseDBModel):
    __tablename__ = "Collar"

    mac = Column(String,unique=True, primary_key=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    support_id=Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="collars",foreign_keys="Collar.owner_id")
    support = relationship("User", back_populates="support_collars",foreign_keys="Collar.support_id")
    migrate = relationship("Migrate", back_populates="collar")
    tasks = relationship("Task", back_populates="collar")
    alert = relationship("Alert", back_populates="collar",foreign_keys="Alert.collar_mac",uselist=False)
class Migrate(BaseDBModel):
    __tablename__ = "Migrate"

    id = Column(Integer,autoincrement=True,primary_key=True)
    mac =  Column(String, ForeignKey("Collar.mac"))
    coord = Column(String)
    time=Column(TIMESTAMP)
    collar = relationship("Collar", back_populates="migrate")
