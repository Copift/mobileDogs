

from sqlalchemy.orm import Session

from tasks.models import TaskStatus

inProgress=TaskStatus(name="In Progress",desc="task in progress and wait data to verify")
atVerify=TaskStatus(name="At Verify",desc="task at verify, wait check by user")
closed=TaskStatus(name="closed",desc="closed")
closed_without_award=TaskStatus(name="closed without award",desc=" score - award ")
dead=TaskStatus(name="dead",desc="deadline past")


def create_in_db(db:Session):
    # for item in  db.query(TaskStatus).all() :
    #     db.delete(item)
    if db.query(TaskStatus).count()==0:
        db.commit()
        db.add(inProgress)
        db.add(atVerify)
        db.add(closed)
        db.add(dead)
        db.add(closed_without_award)
        db.commit()
        db.refresh(inProgress)
        db.refresh(atVerify)
        db.refresh(closed)
        db.refresh(dead)
        db.refresh(closed_without_award)
    else:
        inProgress.id=db.query(TaskStatus).filter(TaskStatus.name=="In Progress").first().id
        atVerify.id=db.query(TaskStatus).filter(TaskStatus.name=="At Verify").first().id
        closed.id=db.query(TaskStatus).filter(TaskStatus.name=="closed").first().id
        closed_without_award.id=db.query(TaskStatus).filter(TaskStatus.name=="closed without award").first().id
        dead.id=db.query(TaskStatus).filter(TaskStatus.name=="dead").first().id

