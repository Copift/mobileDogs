from datetime import datetime
from tasks import models as models
from pydantic import BaseModel
from users.models import User
class TaskBase(BaseModel):
    # Fields that are common to all tasks
    created_by: User
    send_to: User
    type: models.TaskType
    status: models.TaskStatus
    datetime_start: datetime

class TaskInDB(TaskBase):
    # Fields that are returned when fetching a task type from the database
    id: int
