import add_test_data
from collar.router import router as collarRouter
from database import BaseDBModel, engine, DBSession
from tasks.router import router as taskRouter
from users.router import router as userRouter
from support.router import router as supportRouter





from fastapi import  FastAPI



BaseDBModel.metadata.create_all(bind=engine)
def create_items(db):


    import tasks.taskTypes
    import tasks.taskStatuses
    import users.roles
    from tasks.taskStatuses import create_in_db as statuses_create
    from tasks.taskTypes import create_in_db as types_create
    from users.roles import create_in_db as roles_create
    types_create(db)
    statuses_create(db)
    roles_create(db)


    print()
try:
    create_items(DBSession())
    add_test_data.add_test(DBSession())
except Exception as err:
    print(err)

tags_metadata = [
    {
        "name": "collars",
        "description": "Operations with collars. ",
    },
    {
        "name": "tasks",
        "description": "Operations with tasks. "
    },
    {
        "name": "users",
        "description": "Operations with users. "
    },
    {
        "name": "support",
        "description": "Operations with support. "
    },
]

app = FastAPI(openapi_tags=tags_metadata)


app.include_router(collarRouter)
app.include_router(userRouter)
app.include_router(taskRouter)
app.include_router(supportRouter)


