from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from config import DATABASE_URL

engine = create_engine(
 DATABASE_URL,  echo=True,connect_args={"check_same_thread": False}
)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseDBModel = declarative_base()


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


