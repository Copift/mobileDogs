from datetime import timedelta

from fastapi import APIRouter,Depends, HTTPException,status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm

import collar
import mainModels
import support.schemas
from config import ACCESS_TOKEN_EXPIRE_MINUTES

from database import DBSession, get_db
from logger import logger
from users import crud, roles
from users.crud import authenticate_user, create_access_token, PermissionChecker
from users.schemas import Token, User, UserInDB, UserAdd


router = APIRouter(prefix='/user', tags=["users"])

@router.put("/add/", response_model=UserInDB)
def add(user: UserAdd, db : DBSession = Depends(get_db)):
    """
          **Name:** add_support
          **Description:** This function adds a new user .
          **Parameters:**
               nicname: str
               password: str
               email: str | None = None

          **Returns:**
              - **user** (UserInDB): A dictionary containing the newly added user's details.
          """
    logger.info(f"Adding user {user.nicname} with role {roles.standard.name}")

    user=crud.create_user(db=db, user=user,role_id=roles.standard.id)
    return user
@router.put("/add_support/",dependencies=[Depends(PermissionChecker( required_permissions="admin"))], response_model=UserInDB)
def add(user: UserAdd, db : DBSession = Depends(get_db)):
    """
       **Name:** add_support
       **Description:** This function adds a new user with the support role.
       **Parameters:**
            nicname: str
            password: str
            email: str | None = None

       **Returns:**
           - **user** (UserInDB): A dictionary containing the newly added user's details.
       """
    logger.info(f"Adding user {user.nicname} with role {roles.support.name}")
    user=crud.create_user(db=db, user=user,role_id=roles.support.id)
    return user


@router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: DBSession = Depends(get_db)
) -> Token:
    """
    auth user and get token
    """
    logger.info(f"User {form_data.username} is trying to login")
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
    """  get information for user """
    logger.info(f"Getting user details for user with id {current_user.id}")
    return current_user
@router.post("/add_collar/", response_model=mainModels.Status)
async def add_collar(
    current_user:Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        collar: collar.schemas.CollarBase,
db: DBSession = Depends(get_db)):
    """
    **Name:** add_collar
    **Description:** This function creates a new collar for the authenticated user.
    **Parameters:**

        - **mac** (CollarBase): new collar mac

    **Returns:**
        - **status** (mainModels.Status): A dictionary containing the status of the collar creation operation.
    """
    status=crud.add_collar(db,current_user,collar)
    logger.info(f"Adding collar for user with id {current_user.id} with description {collar.description}")
    return status

@router.put("/add_alert/",response_model=support.schemas.AlertInDb)#,dependencies=[Depends(PermissionChecker( required_permissions="standard"))])
async def add_alert(
        current_user: Annotated[UserInDB, Depends(PermissionChecker(required_permissions="standard"))],
        alert: support.schemas.Alert,

db: DBSession = Depends(get_db)):
    """
    **Name:** add_alert
    **Description:** This function create a alert
    **Parameters:**
        - **collar_mac** collar mac
        - **desc** description for alert

    """
    alert=crud.create_alert(db,alert)
    logger.info(f"Adding alert for user with id {current_user.id} with description {alert.description}")
    return alert

@router.post("/get_user_by_id/")
async def add_collar(
    current_user:Annotated[UserInDB,  Depends(PermissionChecker( required_permissions="standard"))],
        id: mainModels.Id,
        db: DBSession = Depends(get_db),
):
    """
    **Name:**get user
    **Description:** This function return a user by id
    **Parameters:**
        - **id** user id

    """
    logger.info(f"Getting user details for user with id {id}")
    user=crud.get_user_id(db,id)
    return user


@router.get("/me/collars/")
async def read_own_items(
        current_user: Annotated[UserInDB,Depends(PermissionChecker( required_permissions="standard"))],
        db: DBSession = Depends(get_db),
):
    """
show user collars
    """
    logger.info(f"Getting collars for user with id {current_user.id}")
    return current_user.collars