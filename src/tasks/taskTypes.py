from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from tasks.models import TaskType
from tasks.taskVerifyTypes import verifyGeo, verifyPhoto, verifyString

food=TaskType(deadline_time=7,name='food',desc='покорми собаку',verify_type=verifyString.id)
wash=TaskType(deadline_time=4,name='wash',desc='помой собаку',verify_type=verifyPhoto.id)
play=TaskType(deadline_time=13,name='play',desc='поиграй с собакой',verify_type=verifyGeo.id)
def create_in_db(db:Session):
    db.add(food)
    db.add(wash)
    db.add(play)
    db.commit()
