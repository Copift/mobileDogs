from datetime import timedelta

from fastapi import APIRouter
from typing import Annotated
from typing import Union
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm

import collar
import mainModels
from config import ACCESS_TOKEN_EXPIRE_MINUTES

from database import DBSession
from users import crud
from users.crud import authenticate_user, create_access_token, get_current_active_user
from users.schemas import Token, User, UserInDB, UserAdd

#from tasks.router import router as taskRouter


router = APIRouter(prefix='/user')
#router.include_router(taskRouter)
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.post("/add/", response_model=UserInDB)
def add(user: UserAdd, db : DBSession = Depends(get_db)):
    user=crud.create_user(db=db, user=user)
    return user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: DBSession = Depends(get_db)
) -> Token:

    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.nicname}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me/", response_model=UserInDB)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
@router.post("/add_collar/", response_model=mainModels.Status)
async def add_collar(
    current_user:Annotated[UserInDB, Depends(get_current_active_user)],
        collar: collar.schemas.CollarBase,
db: DBSession = Depends(get_db),


):

    status=crud.add_collar(db,current_user,collar)
    return status



@router.get("/me/collars/")
async def read_own_items(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: DBSession = Depends(get_db),
):

    return current_user.collars