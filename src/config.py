from fastapi.security import OAuth2PasswordBearer

from passlib.context import CryptContext
SECRET_KEY = "09d25e094faa6ca2556c8h166ber9563b93f7099f6f0f4caa6ftyty6h768d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DATABASE_URL = "sqlite:///./user_devices.db"
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user/token")