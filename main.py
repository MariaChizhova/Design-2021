import sys

from fastapi import FastAPI, Request

from app.authorization.api import router as auth_router
from app.users.api import router as users_router
from app.tasks.api import router as tasks_router
from app.groups.api import router as groups_router
from fastapi.responses import HTMLResponse
from dependencies import Base, engine, Container
from app.utils.utils import templates
from app import authorization
from app import groups
from app import users
from app import tasks

Base.metadata.create_all(bind=engine)

container = Container()
container.wire(packages=[authorization])
container.wire(packages=[tasks])
container.wire(packages=[groups])
container.wire(packages=[users])

app = FastAPI()
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(groups_router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})
