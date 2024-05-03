from tasks.models import VerifyType
from sqlalchemy.orm import Session
verifyGeo=VerifyType(name='geo')
verifyPhoto=VerifyType(name='photo')
verifyString=VerifyType(name='string')
def create_in_db(db:Session):
    db.add(verifyGeo)
    db.add(verifyPhoto)
    db.add(verifyString)
    db.commit()
