import datetime
import http

from sqlalchemy.orm import Session


from . import models, schemas
import mainModels
from .models import Collar


def create_collar(db: Session, collar: schemas.Collar) -> http.HTTPStatus.CREATED:

 db_collar = models.Collar(mac=collar.mac, description =collar.description,
                            owner_id=None)
 db.add(db_collar)
 db.commit()
 db.refresh(db_collar)
 return db_collar
def send_cood(db: Session, collar: schemas.CollarSend) -> mainModels.Status:

 migrate = models.Migrate(mac=collar.mac, coord =collar.coord,
                          time = datetime.datetime.now())
 db.add(migrate)
 db.commit()
 db.refresh(migrate)
 return mainModels.Status(status=True)
def get_migrate(db: Session, collar: schemas.CollarBase) -> list:
 collardb:Collar =db.query(Collar).filter(Collar.mac == collar.mac).one_or_none()
 migrate=collardb.migrate
 return migrate
def get_list(db: Session) -> list:
 collardb =db.query(Collar).all()
 return collardb

def get_list_avaible(db: Session) -> list:
 collardb =db.query(Collar).filter(Collar.owner_id==None).all()
 return collardb
