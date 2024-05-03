

from sqlalchemy.orm import Session

from tasks.models import TaskStatus

inProgress=TaskStatus(name="In Progress",desc="1")
atVerify=TaskStatus(name="At Verify",desc="1")
closed=TaskStatus(name="closed",desc="1")


def create_in_db(db:Session):
    db.add(inProgress)
    db.add(atVerify)
    db.add(closed)
    db.commit()
