
from collar.router import router as collarRouter
from database import BaseDBModel, engine, DBSession
from users.router import router as userRouter

from fastapi import  FastAPI



BaseDBModel.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(collarRouter)
app.include_router(userRouter)



