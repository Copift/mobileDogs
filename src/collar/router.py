from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from . import crud, schemas
from database import DBSession
import mainModels
router = APIRouter(prefix='/collar')

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

@router.post("/add/", response_model=schemas.Collar)
def add(collar: schemas.Collar, db :Session = Depends(get_db)):
    return crud.create_collar(db=db, collar=collar)

@router.post("/send_coord/", response_model=mainModels.Status)
def send_coord(collar: schemas.CollarSend, db :Session = Depends(get_db)):
    return crud.send_cood(db=db, collar=collar)

