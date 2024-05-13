from tasks.models import VerifyType
from sqlalchemy.orm import Session
verifyGeo=VerifyType(name='geo')
verifyPhoto=VerifyType(name='img')
verifyString=VerifyType(name='comment')
def create_in_db(db:Session):
    # for item in db.query(VerifyType).all():
    #     db.delete(item)
    if db.query(VerifyType).count() == 0:
        db.commit()
        db.add(verifyGeo)
        db.add(verifyPhoto)
        db.add(verifyString)
        db.commit()
        db.refresh(verifyGeo)
        db.refresh(verifyPhoto)
        db.refresh(verifyString)
    else:
        verifyGeo.id=db.query(VerifyType).filter(VerifyType.name=='geo').first().id
        verifyPhoto.id=db.query(VerifyType).filter(VerifyType.name=='img').first().id
        verifyString.id=db.query(VerifyType).filter(VerifyType.name=='comment').first().id
