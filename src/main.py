
from collar.router import router as collarRouter
from users.router import router as userRouter


from fastapi import  FastAPI



app = FastAPI()
app.include_router(collarRouter)
app.include_router(userRouter)


