from datetime import timedelta

from fastapi import APIRouter
from typing import Annotated
from typing import Union
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm

import collar
import mainModels
import support.schemas
from config import ACCESS_TOKEN_EXPIRE_MINUTES

from database import DBSession
from users import crud, roles
from users.crud import authenticate_user, create_access_token, get_current_active_user, PermissionChecker
from users.schemas import Token, User, UserInDB, UserAdd

#from tasks.router import router as taskRouter


router = APIRouter(prefix='/user', tags=["users"])
#router.include_router(taskRouter)
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.put("/add/", response_model=UserInDB)
def add(user: UserAdd, db : DBSession = Depends(get_db)):
    user=crud.create_user(db=db, user=user,role_id=roles.standard.id)
    return user
@router.put("/add_support/",dependencies=[Depends(PermissionChecker( required_permissions="admin"))], response_model=UserInDB)
def add(user: UserAdd, db : DBSession = Depends(get_db)):
    user=crud.create_user(db=db, user=user,role_id=roles.support.id)
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
    current_user: Annotated[User, Depends(PermissionChecker( required_permissions="standard"))],
):
    return current_user
@router.post("/add_collar/", response_model=mainModels.Status)
async def add_collar(
    current_user:Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        collar: collar.schemas.CollarBase,
db: DBSession = Depends(get_db)):
    status=crud.add_collar(db,current_user,collar)
    return status

@router.put("/add_alert/",response_model=support.schemas.AlertInDb)#,dependencies=[Depends(PermissionChecker( required_permissions="standard"))])
async def add_alert(
        current_user: Annotated[UserInDB, Depends(PermissionChecker(required_permissions="standard"))],
        alert: support.schemas.Alert,
db: DBSession = Depends(get_db)):
    alert=crud.create_alert(db,alert)
    return alert

@router.post("/get_user_by_id/")
async def add_collar(
    current_user:Annotated[UserInDB,  Depends(PermissionChecker( required_permissions="standard"))],
        id: mainModels.Id,
        db: DBSession = Depends(get_db),
):

    user=crud.get_user_id(db,id)
    return user


@router.get("/me/collars/")
async def read_own_items(
        current_user: Annotated[UserInDB,Depends(PermissionChecker( required_permissions="standard"))],
        db: DBSession = Depends(get_db),
):

    return current_user.collars