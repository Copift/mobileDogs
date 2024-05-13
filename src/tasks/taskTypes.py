from datetime import timedelta, datetime
from sqlalchemy.orm import Session
from tasks.models import TaskType



food=TaskType(deadline_time=7,name='food',award=5,desc='покорми собаку',verify_type=None)
wash=TaskType(deadline_time=4,name='wash',award=15,desc='помой собаку',verify_type=None)
play=TaskType(deadline_time=13,name='play',award=10,desc='поиграй с собакой',verify_type=None)
def create_in_db(db:Session):
    import tasks.taskVerifyTypes
    from tasks.taskVerifyTypes import create_in_db as verify_create
    verify_create(db)
    from tasks.taskVerifyTypes import verifyGeo, verifyPhoto, verifyString

    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!', verifyString.id, verifyPhoto, verifyGeo)
    food.verify_type=verifyString.id
    wash.verify_type = verifyPhoto.id
    play.verify_type = verifyGeo.id
    # for item in db.query(TaskType).all():
    #     db.delete(item)
    if db.query(TaskType).count() == 0:

        db.commit()
        db.add(food)
        db.add(wash)
        db.add(play)
        db.commit()

        db.refresh(food)
        db.refresh(wash)
        db.refresh(play)
    else:
        food.id=db.query(TaskType).filter(TaskType.name=='food').first().id
        wash.id=db.query(TaskType).filter(TaskType.name=='wash').first().id
        play.id=db.query(TaskType).filter(TaskType.name=='play').first().id
