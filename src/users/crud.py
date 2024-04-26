import http
from datetime import timedelta, datetime, timezone

from sqlalchemy.orm import Session

import collar.schemas
import mainModels
from database import DBSession
from config import pwd_context,oauth2_scheme
from config import  SECRET_KEY, ALGORITHM
import  users.models as models
import users.schemas as schemas
import collar.schemas as collarSchemas
import collar.models as collarModels
from jose import JWTError, jwt
from fastapi.routing import Annotated,HTTPException
import users.tasks.models
from fastapi import status,Depends

def get_collars(db: Session,user:schemas.UserInDB):
    collars=db.query(collarModels.Collar).filter(collarModels.Collar.owner_id==user.id).all()
    return collars

def add_collar(db: Session,user:schemas.UserInDB, collar:collarSchemas.CollarBase):

    collar=db.query(collarModels.Collar).filter(collarModels.Collar.mac == collar.mac).one_or_none()
    if collar is None:
        return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find collar with this mac",

    )
    setattr(collar, 'owner_id', user.id)

    db.commit()
    db.refresh(collar)
    return  mainModels.Status(status=True)

def create_user(db: Session, user: schemas.User) -> http.HTTPStatus.CREATED:

     db_user = models.User(nicname=user.nicname, email =user.email,hashed_password=get_password_hash(user.password))
     db.add(db_user)
     db.commit()
     db.refresh(db_user)
     return db_user
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    user=db.query(models.User).filter(models.User.nicname == username).first()
    if user:
        return user
    else:
        return None


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db : DBSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    return current_user
