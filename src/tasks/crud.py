

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
import tasks.taskTypes
import tasks.taskStatuses
import tasks.taskVerifyTypes
from users.crud import get_current_user


def add_task(db: Session,user:usersSchemas.UserInDB,task:schemas.TaskBase):
    taskType=db.query(models.TaskType).get(task.type_id)
    newTask=models.Task(created_by_id=user.id,
                        send_to_id=task.send_to_id,
                        type_id=taskType.id,
                        verify_id=None,
                        status_id=1,
                        datetime_start=datetime.now(),
                        datetime_end=datetime.now()+timedelta(days=taskType.deadline_time))
    db.add(newTask)
    db.commit()
    db.refresh(newTask)
    return newTask

def get_my_task(
        db: Session, user: usersSchemas.UserInDB,
)->list[schemas.TaskinDb]:
    tasks= db.query(models.Task).filter(models.Task.created_by_id==user.id).all()
    print(tasks)
    return tasks
