from fastapi.routing import Annotated,HTTPException
from fastapi import status,Depends
import mainModels
import support.models as models
from sqlalchemy.orm import Session
import users.schemas as usersSchemas
import users.models as usersModels
def get_alerts(
        db: Session
):
    """
    Retrieves all unclosed alerts from the database.

    Args:
    db (Session): The database session object.

    Returns:
    List[mainModels.Alert]: A list of unclosed alerts.

    Raises:
    HTTPException: If no alert with the given id is found.
    """
    alerts = db.query(models.Alert).filter(models.Alert.closed==False).all()
    return alerts
def finish_alert( db: Session,support:usersSchemas.UserInDB,alert:mainModels.Id):
    """
    Finishes an alert by marking it as closed and setting the user who closed it.

    Args:
    db (Session): The database session object.
    support (usersSchemas.UserInDB): The user who is closing the alert.
    alert (mainModels.Id): The ID of the alert to be finished.

    Returns:
    mainModels.Alert: The updated alert object with the 'closed' and 'closed_by_id' fields set.

    Raises:
    HTTPException: If the alert with the given id is not found.

    Note:
    This function assumes that the 'mainModels.Id' type has an 'id' attribute that corresponds to the ID of the alert in the database.
    """
    alert:models.Alert=db.query(models.Alert).get(alert.id)
    if alert==None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find alert with this id",
        )
    alert.closed=True
    alert.closed_by_id=support.id
    db.commit()
    db.refresh(alert)
    return alert


