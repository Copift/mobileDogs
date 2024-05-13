from datetime import timedelta

from fastapi import APIRouter
from typing import Annotated
import  tasks.models as models
import tasks.schemas as schemas
import users.models as usersModels
from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm

import collar
import mainModels
from config import ACCESS_TOKEN_EXPIRE_MINUTES

from database import DBSession
import tasks.crud as crud

from users.crud import authenticate_user, create_access_token, get_current_active_user,PermissionChecker
from users.schemas import Token,User,UserInDB



router = APIRouter(prefix='/tasks', tags=["tasks"])
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()




@router.put("/add_task")
async def add_task(
        current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
       task:schemas.TaskBase,
        db: DBSession = Depends(get_db)
) :
    taskType = db.query(models.TaskType).get(task.type_id)
    userInDb = db.query(usersModels.User).get(task.send_to_id)
    if userInDb == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user with this id",
        )

    if taskType == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find task type with this id",
        )
    tasksAlready = db.query(models.Task).filter(models.Task.collar_mac == task.collar_mac).all()
    if taskType.id in [task.type.id for task in tasksAlready]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This collar already have this taskType",
        )
    collar = db.query(Collar).get(task.collar_mac)
    if collar.alert != None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This collar at AlertList",
        )
    newTask=crud.add_task(db=db,user=current_user,task=task)

    return newTask


@router.post("/my_task/",response_model=list[schemas.Task])
async def my_task(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        status: schemas.getTasks,
        db: DBSession = Depends(get_db),

):


    user=current_user
    my_tasks=crud.get_my_task(db=db,user=user,status=status)
    return my_tasks


@router.put("/add_verify/")
async def add_verify(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        verify: schemas.Verify,

        taskId:mainModels.Id=None,
        db: DBSession = Depends(get_db),

):

    new_verify=crud.send_verify(db=db,verify=verify,Id=taskId,user=current_user)
    return new_verify
@router.post("/get_verify/")
async def check_verify(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        task_id: mainModels.Id,
        db: DBSession = Depends(get_db),

):

    verify=crud.getVerify(db=db,id=task_id,user=current_user)
    return verify

@router.post("/final_task/")
async def check_verify(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        task_id: mainModels.Id,
        db: DBSession = Depends(get_db),

):

    task=crud.final_task(db=db,id=task_id,user=current_user)
    return task

@router.post("/final_task_without_award/")
async def check_verify(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        task_id: mainModels.Id,
        db: DBSession = Depends(get_db),

):

    task=crud.final_task_without_award(db=db,id=task_id,user=current_user)
    return task


@router.post("/restart_task/")
async def check_verify(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        task_id: mainModels.Id,
        db: DBSession = Depends(get_db),

):

    task=crud.restart_task(db=db,id=task_id,user=current_user)
    return task


@router.get("/statuses/",response_model=list[schemas.TaskStatus])
async def my_task(

        db: DBSession = Depends(get_db)
):
    statuses=crud.get_statuses(db=db)
    return statuses


@router.get("/types/", response_model=list[schemas.TaskType])
async def my_task(

        db: DBSession = Depends(get_db)
):
    statuses = crud.get_types(db=db)
    return statuses
