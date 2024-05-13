import http
from datetime import timedelta, datetime, timezone

from sqlalchemy.orm import Session
import users.roles as roles
import mainModels
import tasks.models
from database import DBSession
from config import pwd_context,oauth2_scheme
from config import  SECRET_KEY, ALGORITHM
import  users.models as models
import users.schemas as schemas
import collar.schemas as collarSchemas
import collar.models as collarModels
import support.schemas as supportSchemas
import support.models as supportModels
import tasks.schemas as tasksSchemas
import tasks.taskStatuses as statuses
import tasks.taskTypes as types
import tasks.taskVerifyTypes as verifyes
import tasks.models as tasksModels
from jose import JWTError, jwt
from fastapi.routing import Annotated,HTTPException
from fastapi import status,Depends

def get_collars(db: Session,user:schemas.UserInDB):
    """
     Retrieves all collars owned by the given user.

     Args:
     db (Session): The database session.
     user (schemas.UserInDB): The user object representing the authenticated user.

     Returns:
     List[collarModels.Collar]: A list of all collars owned by the given user.
     """
    collars=db.query(collarModels.Collar).filter(collarModels.Collar.owner_id==user.id).all()
    return collars

def add_collar(db: Session,user:schemas.UserInDB, collar:collarSchemas.CollarBase):
    """
       Adds a new collar to the database, associating it with the given user.

       Args:
       db (Session): The database session.
       user (schemas.UserInDB): The user object representing the authenticated user.
       collar (collarSchemas.CollarBase): The collar object to be added.

       Returns:
       mainModels.Status: A status object indicating the success of the operation.
       """
    collar=db.query(collarModels.Collar).filter(collarModels.Collar.mac == collar.mac).one_or_none()
    if collar is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find collar with this mac",

    )
    setattr(collar, 'owner_id', user.id)

    db.commit()
    db.refresh(collar)
    return  mainModels.Status(status=True)

def create_user(db: Session, user: schemas.UserAdd,role_id) -> http.HTTPStatus.CREATED:
     """
       Creates a new user in the database, assigning the given role to the user.

       Args:
       db (Session): The database session.
       user (schemas.UserAdd): The user object to be added.
       role_id (int): The ID of the role to be assigned to the user.

       Returns:
       http.HTTPStatus.CREATED: A status code indicating the success of the operation.
     """
     db_user = models.User(nicname=user.nicname, email =user.email,hashed_password=get_password_hash(user.password),role_id=
                           role_id)
     db.add(db_user)
     db.commit()
     db.refresh(db_user)
     return db_user


def verify_password(plain_password, hashed_password):
    """
       Verifies if the given plain password matches the hashed password stored in the database.

       Args:
       plain_password (str): The plain password to be verified.
       hashed_password (str): The hashed password stored in the database.

       Returns:
       bool: True if the plain password matches the hashed password, False otherwise.
       """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hashes the given password using the PBKDF2 algorithm.

    Args:
    password (str): The password to be hashed.

    Returns:
    str: The hashed password.
    """
    return pwd_context.hash(password)


def get_user(db: Session, username: str):
    """
       Retrieves a user from the database based on the given username.

       Args:
       db (Session): The database session.
       username (str): The username of the user to be retrieved.

       Returns:
       Optional[models.User]: The user object if found, None otherwise.
       """
    user= db.query(models.User).filter(models.User.nicname == username).one_or_none()
    if user:
        return user
    else:
        return None
def create_alert(db: Session, alert:supportSchemas.Alert):
    """
       Creates a new alert in the database.

       Args:
       db (Session): The database session.
       alert (supportSchemas.Alert): The alert object to be added.

       Returns:
       supportModels.Alert: The newly created alert object.
       """
    if db.query(supportModels.Alert).filter(supportModels.Alert.collar_mac==alert.collar_mac,supportModels.Alert.closed==False).count()!=0:
        raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="already_exists")
    collar:collarModels.Collar=db.query(collarModels.Collar).get(alert.collar_mac)
    if collar==None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find collar with this mac",
        )
    for task in collar.tasks:
        task.status_id=statuses.closed.id
    alert= supportModels.Alert(desc=alert.desc,collar_mac=alert.collar_mac,closed=False)
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return alert


def authenticate_user(fake_db, username: str, password: str):
    """
       Authenticates a user based on the given username and password.

       Args:
       fake_db (Session): A mock database session for testing purposes.
       username (str): The username of the user to be authenticated.
       password (str): The password of the user to be authenticated.

       Returns:
       bool: True if the user is authenticated, False otherwise.
       """
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Creates a JWT access token based on the given data and optional expiration time.

    Args:
    data (dict): The data to be included in the access token.
    expires_delta (timedelta | None): The optional expiration time for the access token.

    Returns:
    str: The JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
def get_db():
    """
      Yields a database session for use in the application.

      Yields:
      Session: The database session.
      """
    db = DBSession()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db : DBSession = Depends(get_db)):
    """
       Retrieves the current user from the database based on the given token.

       Args:
       token (str): The token to be used for authentication.
       db (DBSession): The database session.

       Returns:
       models.User: The user object representing the authenticated user.
       """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = schemas.TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
class PermissionChecker:
    """
        A class that checks if the user has the required permissions.

        Args:
        required_permissions (str): The required permissions for the user.

        Methods:
        __call__(self, user:schemas.UserInDB = Depends(get_current_user)) -> bool:
            Checks if the user has the required permissions. If not, it raises an HTTPException with status code 401 and a message indicating that the permissions are not allowed.
        """
    def __init__(self, required_permissions: str) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user:schemas.UserInDB = Depends(get_current_user)) -> bool:
            """
              Checks if the user has the required permissions. If not, it raises an HTTPException with status code 401 and a message indicating that the permissions are not allowed.

              Args:
              user (schemas.UserInDB): The user object representing the authenticated user.

              Returns:
              bool: True if the user has the required permissions, False otherwise.
              """
            print(self.required_permissions,user.role.name,'!!!!!!!!!!!!')
            if  not (self.required_permissions == user.role.name):
                print(self.required_permissions, user.role.name, '!!!!!!!!!!!!')
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail='Permissions dont allowed'
                )
            return user

def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)],
):
    """
      Retrieves the current active user from the database based on the token provided in the request header.

      Args:
      current_user (schemas.User): The user object representing the authenticated user.

      Returns:
      schemas.User: The user object representing the authenticated user.
      """
    return current_user


def get_user_id(
            db: Session, userId:mainModels.Id,
    ):
    """
     Retrieves a user from the database based on the given user ID.

     Args:
     db (Session): The database session.
     userId (mainModels.Id): The ID of the user to be retrieved.

     Returns:
     schemas.UserInDBWithCollarsCheck: The user object if found, None otherwise.
     """
    user=db.query(models.User).get(userId.id)
    if user==None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not find user with this id",
        )
    answer=schemas.UserInDBWithCollarsCheck(user=schemas.UserShow(nicname=user.nicname,id=user.id,email=user.email),collars=[])
    collars=[]
    for collar in user.collars:
        checks=db.query(tasksModels.Task).filter(tasksModels.Task.collar_mac==collar.mac,
                                                 tasksModels.Task.status_id==statuses.inProgress.id).all()
        if checks != None:
            checks = [tasksSchemas.TaskType(id=item.type.id,
                                            name=item.type.name,
                                            deadline_time=item.type.deadline_time,
                                            desc=item.type.desc)
                      for item in checks]
        else: checks=None
        collars.append(collarSchemas.CollarWithCheck(mac=collar.mac,description=collar.description,migrate=collar.migrate[:6],
                                                         checks=checks))
    answer.collars=collars
    return answer
