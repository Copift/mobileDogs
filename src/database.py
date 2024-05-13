from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import logging
from config import DATABASE_URL

engine = create_engine(
 DATABASE_URL,  echo=True, pool_pre_ping=True
)
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseDBModel = declarative_base()


logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)


