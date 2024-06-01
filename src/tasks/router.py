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
from logger import logger
from database import DBSession
import tasks.crud as crud

from users.crud import authenticate_user, create_access_token, get_current_active_user,PermissionChecker
from users.schemas import Token,User,UserInDB



router = APIRouter(prefix='/tasks', tags=["tasks"])
from database import get_db



@router.put("/add_task")
async def add_task(
        current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
       task:schemas.TaskBase,
        db: DBSession = Depends(get_db)
) :
    """
         add task :
    -- **collar_mac**:str  to collar mac
    -- **send_to_id**: id  to user
    -- **type_id**: id of type
         """
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
    logger.info(
        f"Adding task for collar with mac {task.collar_mac} and description {task.description} for user with id {current_user.id}")
    return newTask


@router.post("/my_task/",response_model=list[schemas.Task])
async def my_task(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        status: schemas.getTasks,
        db: DBSession = Depends(get_db),

):
    """
       **Name:** my_task
       **Description:** This function retrieves tasks for the current user based on the specified status.
       **Parameters:**
           - **current_user** (UserInDB): The authenticated user object.
           - **status** (schemas.getTasks): A schema object containing the status type id.
           - **db** (DBSession): The database session object.
       **Returns:**
           - **my_tasks** (list[schemas.Task]): A list of tasks matching the specified status for the current user.
       """
    user=current_user
    logger.info(f"Getting tasks for user with id {current_user.id} with status {status.status}")
    my_tasks=crud.get_my_task(db=db,user=user,status=status)
    return my_tasks


@router.put("/add_verify/")
async def add_verify(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        verify: schemas.Verify,

        taskId:mainModels.Id=None,
        db: DBSession = Depends(get_db),

):
    """
       **Name:** add_verify
       **Description:** This function adds a verify for a task associated with the current user.
       **Parameters:**
           - **current_user** (UserInDB): The authenticated user object.
       - **verify** (schemas.Verify): A schema object containing the verify details.
       - **taskId** (mainModels.Id=None): The id of the task to which the verify is being added. If not provided, it defaults to None.
       - **db** (DBSession = Depends(get_db)): The database session object.
       **Returns:**
           - **new_verify** (schemas.Verify): A schema object containing the newly added verify details.
       """
    logger.info(f"Adding verify for task with id {taskId} for user with id {current_user.id}")
    new_verify=crud.send_verify(db=db,verify=verify,Id=taskId,user=current_user)
    return new_verify
@router.post("/get_verify/")
async def check_verify(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        task_id: mainModels.Id,
        db: DBSession = Depends(get_db),

):
    """
     **Name:** get_verify
     **Description:** This function retrieves the verify for a task associated with the current user.
     **Parameters:**
         - **current_user** (UserInDB): The authenticated user object.
         - **task_id** (mainModels.Id): The id of the task for which the verify is being retrieved.
         - **db** (DBSession = Depends(get_db)): The database session object.
     **Returns:**
         - **verify** (schemas.Verify): A schema object containing the verify details for the task.
     """
    logger.info(f"Getting verify for task with id {task_id} for user with id {current_user.id}")
    verify=crud.getVerify(db=db,id=task_id,user=current_user)
    return verify

@router.post("/final_task/")
async def check_verify(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        task_id: mainModels.Id,
        db: DBSession = Depends(get_db),

):
    """
        **Name:** final_task
        **Description:** This function checks if a task has reached its final state for the current user.
        **Parameters:**
            - **current_user** (UserInDB): The authenticated user object.
            - **task_id** (mainModels.Id): The id of the task for which the final state is being checked.
            - **db** (DBSession = Depends(get_db)): The database session object.
        **Returns:**
            - **task** (schemas.Task): A schema object containing the task details.
        """
    logger.info(f"Checking final task for task with id {task_id} for user with id {current_user.id}")
    task=crud.final_task(db=db,id=task_id,user=current_user)
    return task

@router.post("/final_task_without_award/")
async def check_verify(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        task_id: mainModels.Id,
        db: DBSession = Depends(get_db),

):
    """
    **Name:** final_task_without_award
    **Description:** This function checks if a task has reached its final state for the current user without awarding points.
    **Parameters:**
        - **current_user** (UserInDB): The authenticated user object.
        - **task_id** (mainModels.Id): The id of the task for which the final state is being checked.
        - **db** (DBSession = Depends(get_db)): The database session object.
    **Returns:**
        - **task** (schemas.Task): A schema object containing the task details.
    """
    logger.info(f"Checking final task without award for task with id {task_id} for user with id {current_user.id}")
    task=crud.final_task_without_award(db=db,id=task_id,user=current_user)
    return task


@router.post("/restart_task/")
async def check_verify(
    current_user: Annotated[UserInDB, Depends(PermissionChecker( required_permissions="standard"))],
        task_id: mainModels.Id,
        db: DBSession = Depends(get_db),

):
    """
       Restarts a task for the current user.

       Args:
           current_user (UserInDB): The authenticated user object.
           task_id (mainModels.Id): The id of the task to be restarted.
           db (DBSession): The database session object.

       Returns:
           task (schemas.Task): A schema object containing the task details after restarting.

       Raises:
           HTTPException: If the task or user is not found.
       """
    logger.info(f"Restarting task for task with id {task_id} for user with id {current_user.id}")
    task=crud.restart_task(db=db,id=task_id,user=current_user)
    return task


@router.get("/statuses/",response_model=list[schemas.TaskStatus])
async def my_task(

        db: DBSession = Depends(get_db)
):
    """
    **Name:** get_statuses
    **Description:** This function retrieves all task statuses from the database.
    **Parameters:**
        - **db** (DBSession = Depends(get_db)): The database session object.
    **Returns:**
        - **statuses** (list[schemas.TaskStatus]): A list of task statuses.
    """
    logger.info(f"Getting statuses")
    statuses=crud.get_statuses(db=db)
    return statuses


@router.get("/types/", response_model=list[schemas.TaskType])
async def my_task(

        db: DBSession = Depends(get_db)
):
    """
    **Name:** get_types
    **Description:** This function retrieves all task types from the database.
    **Parameters:**
        - **db** (DBSession = Depends(get_db)): The database session object.
    **Returns:**
        - **types** (list[schemas.TaskType]): A list of task types.
    """
    logger.info(f"Getting types")
    statuses = crud.get_types(db=db)
    return statuses
