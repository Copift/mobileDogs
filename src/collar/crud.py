import datetime
import http

from sqlalchemy.orm import Session


from . import models, schemas
import mainModels
from .models import Collar
from fastapi.routing import Annotated,HTTPException
from fastapi import status,Depends
def create_collar(db: Session, collar: schemas.Collar,support) -> schemas.Collar:
 """
 Create a new collar in the database.

 Args:
 db (Session): The database session.
 collar (schemas.Collar): The collar object to be created.
 support (object): The support object associated with the collar.

 Returns:
 schemas.Collar: The newly created collar object.

 Raises:
 Exception: If the database operation fails.

 This function creates a new collar in the database with the provided collar object and associates it with the given support object.
 It then commits the changes to the database and refreshes the collar object before returning it.
 """
 collars= db.query(models.Collar).filter(models.Collar.mac == collar.mac).first()
 if collars != None:

   raise HTTPException(
  status_code=status.HTTP_404_NOT_FOUND,
  detail="Already exists",
 )
 db_collar = models.Collar(mac=collar.mac, description =collar.description,
                            owner_id=None,support_id=support.id)
 db.add(db_collar)
 db.commit()
 db.refresh(db_collar)
 return db_collar

def send_cood(db: Session, collar: schemas.CollarSend) -> mainModels.Status:
 """
 Send the coordinates of a collar to the database.

 Args:
 db (Session): The database session.
 collar (schemas.CollarSend): The collar object containing the coordinates to be sent.

 Returns:
 mainModels.Status: A status object indicating the success of the operation.

 Raises:
 Exception: If the database operation fails.

 This function creates a new Migrate object with the provided collar's mac address, coordinates, and the current time, and adds it to the database. It then commits the changes to the database and refreshes the Migrate object before returning a status object indicating the success of the operation.
 """
 migrate = models.Migrate(mac=collar.mac, coord =collar.coord,
                          time = datetime.datetime.now())
 db.add(migrate)
 db.commit()
 db.refresh(migrate)
 return mainModels.Status(status=True)

def get_migrate(db: Session, collar: schemas.CollarBase) -> list:
 """
 Retrieve the Migrate object associated with the given collar's mac address from the database.

 Args:
 db (Session): The database session.
 collar (schemas.CollarBase): The collar object containing the mac address to search for.

 Returns:
 list: A list containing the Migrate object associated with the given collar's mac address.

 Raises:
 Exception: If the database operation fails.

 This function retrieves the Migrate object associated with the given collar's mac address from the database. It first queries the Collar table to find a Collar object with a matching mac address. If found, it retrieves the associated Migrate object and returns it as a list. If no matching Collar object is found, an empty list is returned.
 """
 collardb:Collar =db.query(Collar).filter(Collar.mac == collar.mac).one_or_none()
 migrate=collardb.migrate
 return migrate
def get_list(db: Session) -> list[schemas.Collar]:
 """
    Retrieve all Collar objects from the database and format their 'migrate' attribute.

    Args:
    db (Session): The database session.

    Returns:
    list[schemas.Collar]: A list of Collar objects retrieved from the database.

    The 'migrate' attribute of each Collar object in the list is formatted to display only the first 6 characters.
    """
 collardb =db.query(Collar).all()
 for collar in collardb:
  collar.migrate=collar.migrate[:6]
 return collardb


def get_list_avaible(db: Session) -> list:
 """
    Retrieve all Collar objects from the database that are not owned by any user.

    Args:
    db (Session): The database session.

    Returns:
    list: A list of Collar objects retrieved from the database that are not owned by any user.

    This function retrieves all Collar objects from the database that are not owned by any user (i.e., where the 'owner_id' attribute is None). It then returns a list of these Collar objects.
    """
 collardb =db.query(Collar).filter(Collar.owner_id==None).all()
 return collardb
