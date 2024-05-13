from datetime import timedelta

from fastapi import APIRouter
from typing import Annotated

from fastapi import Depends, HTTPException,status

import mainModels
import support.models as models
import support.schemas as schemas
from database import DBSession

from users.crud import get_current_active_user, PermissionChecker
from users.schemas import UserInDB
import support.crud as crud


router = APIRouter(prefix='/support', tags=["support"])
def get_db():
    db = DBSession()
    try:
        yield db
    finally:
        db.close()



@router.get("/get_alerts")
async def read_own_items(
        current_user: Annotated[UserInDB, Depends(PermissionChecker(required_permissions="support"))],
        db: DBSession = Depends(get_db),
):
    return crud.get_alerts(db)

@router.post("/finish_alert")
async def read_own_items(
        current_user: Annotated[UserInDB, Depends(PermissionChecker(required_permissions="support"))],
        alert_id: mainModels.Id,
        db: DBSession = Depends(get_db)

):
    return crud.finish_alert(db,current_user,alert_id)