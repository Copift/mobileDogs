from typing import Annotated

from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

import errors
from users.crud import get_current_active_user, PermissionChecker
from users.schemas import UserInDB

from . import crud, schemas
from database import DBSession
import mainModels
router = APIRouter(prefix='/collar', tags=["collars"])

from database import get_db
from logger import logger

@router.put("/add/", response_model=schemas.Collar,
            responses=errors.collar_not_found.to_dict())
def add(collar: schemas.CollarCreate,
        support: Annotated[UserInDB,Depends(PermissionChecker(required_permissions="support"))],
        db :Session = Depends(get_db)):
    """
       Create a collar with all the information:
       - **mac**: mac address of collar
       - **description**:description  appearance of dog
       """
    logger.info(
        f"Adding collar with mac {collar.mac} and description {collar.description} for user with id {support.id}")
    return crud.create_collar(db=db, collar=collar, support=support)



@router.post("/send_coord/", response_model=mainModels.Status)
def send_coord(collar: schemas.CollarSend, db :Session = Depends(get_db)):
    """
         collar send coord method:
         - **mac**: mac address of collar
         - **coord**:string of coordinates
         """
    logger.info(f"Sending coordinates for collar with mac {collar.collar_mac}")
    return crud.send_cood(db=db, collar=collar)

@router.post("/get_migrate/")
def get_migrate(collar: schemas.CollarBase, db :Session = Depends(get_db),):
    """
        get a migrate of collar
         - **mac**: mac address of collar
         """
    logger.info(f"Getting migration for collar with mac {collar.collar_mac}")
    return crud.get_migrate(db=db, collar=collar)
@router.get("/get_list/", dependencies=[Depends(get_current_active_user)],response_model= list[schemas.Collar])
def get_list( db :Session = Depends(get_db)):
    """
         get list of collars:

         """
    logger.info(f"Getting list of collars")
    return crud.get_list(db=db)
@router.get("/get_list_avaible/", dependencies=[Depends(get_current_active_user)])
def get_list_avaible( db :Session = Depends(get_db)):
    """
         get list of avaible collars
         """
    logger.info(f"Getting list of available collars")
    return crud.get_list_avaible(db=db)

