from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session
from users.crud import get_current_active_user, PermissionChecker
from users.schemas import UserInDB

from . import crud, schemas
from database import DBSession
import mainModels
router = APIRouter(prefix='/collar', tags=["collars"])

def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()


@router.put("/add/", response_model=schemas.Collar,)
def add(collar: schemas.CollarCreate, support: Annotated[UserInDB,
Depends(PermissionChecker(required_permissions="support"))], db :Session = Depends(get_db)):
    return crud.create_collar(db=db, collar=collar,support=support)



@router.post("/send_coord/", response_model=mainModels.Status)
def send_coord(collar: schemas.CollarSend, db :Session = Depends(get_db)):
    return crud.send_cood(db=db, collar=collar)

@router.post("/get_migrate/")
def get_migrate(collar: schemas.CollarBase, db :Session = Depends(get_db),):
    return crud.get_migrate(db=db, collar=collar)
@router.get("/get_list/", dependencies=[Depends(get_current_active_user)],response_model= list[schemas.Collar])
def get_list( db :Session = Depends(get_db)):
    return crud.get_list(db=db)
@router.get("/get_list_avaible/", dependencies=[Depends(get_current_active_user)])
def get_list_avaible( db :Session = Depends(get_db)):
    return crud.get_list_avaible(db=db)

