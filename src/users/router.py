from datetime import timedelta

from fastapi import APIRouter
from typing import Annotated

from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm

import mainModels
from config import ACCESS_TOKEN_EXPIRE_MINUTES

from database import DBSession
from users import crud
from users.crud import authenticate_user, create_access_token, get_current_active_user
from users.schemas import Token,User,UserInDB



router = APIRouter(prefix='/user')
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.post("/add/", response_model=UserInDB)
def add(user: User, db : DBSession = Depends(get_db)):
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


@router.get("/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.nicname}]