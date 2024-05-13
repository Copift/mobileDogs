from sqlalchemy import Column, Integer, String,DATETIME,DateTime, ForeignKey,Boolean,ForeignKeyConstraint
from sqlalchemy.types import BLOB,LargeBinary,TIMESTAMP
from sqlalchemy.orm import relationship
from database import BaseDBModel, engine, DBSession

class Alert(BaseDBModel):
    __tablename__ = "Alert"
    id = Column(Integer, autoincrement=True, primary_key=True)
    desc=Column(String)
    closed=Column(Boolean)
    closed_by_id=Column(Integer, ForeignKey("users.id"),default=None)

    collar_mac=Column(String, ForeignKey("Collar.mac"))
    collar=relationship("Collar", back_populates="alert",foreign_keys='Alert.collar_mac',uselist=False)
    closed_by=relationship("User", back_populates="closed_alerts",foreign_keys='Alert.closed_by_id',uselist=False)