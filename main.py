from fastapi import FastAPI, Request

from app.authorization.api import router as auth_router
from app.users.api import router as users_router
from app.tasks.api import router as tasks_router
from app.groups.api import router as groups_router
from app.users.data import Base, engine
from fastapi.responses import HTMLResponse

from app.utils.utils import templates

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(tasks_router)
app.include_router(groups_router)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("root.html", {"request": request})
