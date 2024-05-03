from datetime import timedelta

from fastapi import APIRouter
from typing import Annotated
import  tasks.models as models
import tasks.schemas as schemas
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm

import collar
import mainModels
from config import ACCESS_TOKEN_EXPIRE_MINUTES

from database import DBSession
import tasks.crud as crud

from users.crud import authenticate_user, create_access_token, get_current_active_user
from users.schemas import Token,User,UserInDB



router = APIRouter(prefix='/tasks')
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()




@router.post("/add_task")
async def add_task(
        current_user: Annotated[UserInDB, Depends(get_current_active_user)],
       task:schemas.TaskBase,
        db: DBSession = Depends(get_db)
) :
    newTask=crud.add_task(db=db,user=current_user,task=task)

    return newTask


@router.get("/my_task/")
async def my_task(
    current_user: Annotated[UserInDB, Depends(get_current_active_user)],
        db: DBSession = Depends(get_db)
) :
    my_tasks=crud.get_my_task(db=db,user=current_user)
    return my_tasks
