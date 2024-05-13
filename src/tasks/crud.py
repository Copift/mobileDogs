

import http
from datetime import timedelta, datetime, timezone

from sqlalchemy.orm import Session
import mainModels
from database import DBSession
import  tasks.models as models
import tasks.schemas as schemas
import users.schemas as usersSchemas
import users.models as usersModels
from jose import JWTError, jwt
from fastapi.routing import Annotated,HTTPException
from fastapi import status,Depends
import tasks.taskTypes as types
import tasks.taskStatuses as statuses
import tasks.taskVerifyTypes as taskVerifys
from users.crud import get_current_user
from mainModels import Id
from collar.models import Collar

def send_verify(db:Session,Id:Id,verify:schemas.Verify,user:usersSchemas.UserInDB):
    """
       Sends a verify for a specific task.

       Args:
           db (Session): The database session.
           Id (Id): The ID of the task.
           verify (schemas.Verify): The verify data.
           user (usersSchemas.UserInDB): The user who is interacting with the task.

       Raises:
           HTTPException: If the task is not found, if the user is not allowed to interact with the task, if the task already has a verify, if the verify data does not match the task's verify type.

       Returns:
           models.Verify: The newly created verify.
       """
    task:models.Task =db.query(models.Task).get(Id.id)
    print(task)
    if task==None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find task with this id",
        )
    if task.send_to.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dont allowed to this task",
        )
    if task.verify_id!=None:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task already verified",
        )

    verifyType=task.type.verify
    print(verify.model_dump(),verifyType.name,verify.model_dump()[verifyType.name],'!~!!!!~~~!!!')

    if verify.model_dump()[verifyType.name] == None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="verify type doesnt match verify data",
        )
    newVerify=models.Verify(verify_type=verifyType.id,comment=verify.comment,img=verify.img,geo=verify.geo)
    db.add(newVerify)
    db.commit()

    task.status_id=statuses.atVerify.id

    task.verify=newVerify
    db.commit()
    db.refresh(task)
    print(newVerify.id)
    return newVerify
def getVerify(db:Session,id:Id,user:usersSchemas.UserInDB):
    """
      Retrieves a verify for a specific task.

      Args:
          db (Session): The database session.
          id (Id): The ID of the task.
          user (usersSchemas.UserInDB): The user who is interacting with the task.

      Raises:
          HTTPException: If the task is not found, if the user is not allowed to interact with the task, if the task does not have a verify.

      Returns:
          models.Verify: The verify associated with the task.
      """
    task:models.Task =db.query(models.Task).get(id.id)
    if task==None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find task with this id",
        )

    if  task.created_by.id != user.id and task.send_to.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dont allowed to this task",
        )
    if task.verify_id==None:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task dont have verify",
        )
    if task.status_id!=statuses.atVerify.id:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task dont at verify",
        )
    verify=db.query(models.Verify).get(task.verify_id)

    return verify
def final_task(db:Session,id:Id,user:usersSchemas.UserInDB):
    """
       Finalizes a task.

       Args:
           db (Session): The database session.
           id (Id): The ID of the task.
           user (usersSchemas.UserInDB): The user who is interacting with the task.

       Raises:
           HTTPException: If the task is not found, if the user is not allowed to interact with the task, if the task does not have a verify.

       Returns:
           models.Task: The task after it has been finalized.
       """
    task:models.Task =db.query(models.Task).get(id.id)

    if task==None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find task with this id",
        )
    if task.created_by.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task dont created by this user",
        )

    if task.status_id!=statuses.atVerify.id:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task dont at verify",
        )
    if task.verify_id==None:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task dont have verify",
        )
    task.status_id=statuses.closed.id
    task.send_to.score+=task.type.award
    db.commit()
    db.refresh(task)
    return task
def final_task_without_award(db:Session,id:Id,user:usersSchemas.UserInDB):
    """
     Finalizes a task without awarding points.

     Args:
         db (Session): The database session.
         id (Id): The ID of the task.
         user (usersSchemas.UserInDB): The user who is interacting with the task.

     Raises:
         HTTPException: If the task is not found, if the user is not allowed to interact with the task, if the task does not have a verify.

     Returns:
         models.Task: The task after it has been finalized without awarding points.
     """
    task:models.Task =db.query(models.Task).get(id.id)


    if task==None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find task with this id",
        )
    print('!!!!!!!!!!!!!!',statuses.atVerify.id)
    if task.status_id!=statuses.atVerify.id:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task dont at verify",
        )
    if task.created_by.id != user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task dont created by this user",
        )
    if task.restarted==False:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not final without award task which doesnt restarted",
        )
    if task.verify_id==None:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task dont have verify",
        )
    task.status_id=statuses.closed_without_award.id
    task.send_to.score-=task.type.award
    db.commit()
    db.refresh(task)
    return task
def restart_task(db:Session,id:Id,user:usersSchemas.UserInDB):
    """
      Restarts a task.

      Args:
          db (Session): The database session.
          id (Id): The ID of the task.
          user (usersSchemas.UserInDB): The user who is interacting with the task.

      Raises:
          HTTPException: If the task is not found, if the user is not allowed to interact with the task, if the task does not have a verify.

      Returns:
          models.Task: The task after it has been restarted.
      """
    task:models.Task =db.query(models.Task).get(id.id)
    if task.created_by.id!=user.id:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task dont created by this user",
        )
    if task==None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find task with this id",
        )
    if task.verify_id==None:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task dont have verify",
        )
    if task.status_id!=statuses.atVerify.id:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Task dont at verify",
        )
    task.status_id=statuses.inProgress.id
    task.verify_id=None
    task.restarted=True
    task.datetime_start=datetime.now()
    task.datetime_end=datetime.now()+timedelta(days=task.type.deadline_time)
    db.commit()
    db.refresh(task)
    return task



def add_task(db: Session,user:usersSchemas.UserInDB,task:schemas.TaskBase):
    """
      Restarts a task.

      Args:
          db (Session): The database session.
          id (Id): The ID of the task.
          user (usersSchemas.UserInDB): The user who is interacting with the task.

      Raises:
          HTTPException: If the task is not found, if the user is not allowed to interact with the task, if the task does not have a verify.

      Returns:
          models.Task: The task after it has been restarted.
      """
    taskType=db.query(models.TaskType).get(task.type_id)
    userInDb = db.query(usersModels.User).get(task.send_to_id)
    if userInDb == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user with this id",
        )

    if taskType==None:
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
    collar=db.query(Collar).get(task.collar_mac)
    if collar.alert!=None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This collar at AlertList",
        )
    newTask=models.Task(created_by_id=user.id,
                        send_to_id=task.send_to_id,
                        type_id=taskType.id,
                        verify_id=None,
                        status_id=statuses.inProgress.id,
                        collar_mac=task.collar_mac,
                        datetime_start=datetime.now(),
                        datetime_end=datetime.now()+timedelta(days=taskType.deadline_time))
    db.add(newTask)
    db.commit()
    db.refresh(newTask)
    return newTask

def get_my_task(
        db: Session, user,status=schemas.getTasks
):
    """
       Retrieves tasks for the specified user based on the provided status.

       Args:
           db (Session): The database session.
           user (usersSchemas.UserInDB): The user whose tasks are to be retrieved.
           status (schemas.getTasks, optional): The status of the tasks to be retrieved. Defaults to None.

       Returns:
           List[models.Task]: A list of tasks associated with the specified user based on the provided status.
       """
    statusCriterion = True
    tasks=[]
    if status.status_id!=None:
        statusCriterion = models.Task.status_id.in_(status.status_id)
    if  status.created_by==True:
        tasks += db.query(models.Task).filter(statusCriterion, models.Task.created_by_id==user.id).all()
    if status.sended_to==True:
        tasks += db.query(models.Task).filter(statusCriterion, models.Task.send_to_id==user.id).all()
    return tasks
def get_statuses(
        db: Session
):
    """
    Retrieves all task statuses from the database.

    Args:
        db (Session): The database session.

    Returns:
        List[models.TaskStatus]: A list of all task statuses.
    """
    statuses= db.query(models.TaskStatus).all()

    return statuses


def get_types(
        db: Session
):
    """
       Retrieves all task types from the database.

       Args:
           db (Session): The database session.

       Returns:
           List[models.TaskType]: A list of all task types.
    """

    types = db.query(models.TaskType).all()

    return types
