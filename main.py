from fastapi import FastAPI

from app.authorization.api import router as auth_router
from app.users.api import router as users_router
from app.tasks.api import router as tasks_router
from app.users.data import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)
