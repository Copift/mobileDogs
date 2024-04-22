from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from collar import models
from config import DATABASE_URL

engine = create_engine(
 DATABASE_URL, connect_args={"check_same_thread": False}
)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseDBModel = declarative_base()


