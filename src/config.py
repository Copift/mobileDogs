from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
SECRET_KEY = "09d25e094faa6ca2556c8h166ber9563b93f7099f6f0f4caa6ftyty6h768d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
from pydantic import PostgresDsn

#DATABASE_URL = "sqlite:///./user_devices.db"
#DATABASE_URL='postgresql+psycopg2://dank2:987654zZ$)(\
#@130.193.49.28:5432/collar'

DATABASE_URL = PostgresDsn.build(
    scheme="postgresql",
    username="dank2",
    password="987654zZ$)(",
    host="130.193.49.28",
    path=f"{'collar' or ''}",
).unicode_string()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")