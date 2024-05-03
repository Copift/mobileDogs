
from collar.router import router as collarRouter
from database import BaseDBModel, engine, DBSession
from tasks.router import router as taskRouter
from users.router import router as userRouter
from tasks.taskStatuses import create_in_db as statuses_create
from tasks.taskTypes import create_in_db as types_create
from tasks.taskVerifyTypes import create_in_db as verify_create
from fastapi import  FastAPI



BaseDBModel.metadata.create_all(bind=engine)
def create_items(db):

    statuses_create(db)
    types_create(db)
    verify_create(db)

    print()
try:
    create_items(DBSession())
except Exception as err:
    print(err)
app = FastAPI()
app.include_router(collarRouter)
app.include_router(userRouter)
app.include_router(taskRouter)



