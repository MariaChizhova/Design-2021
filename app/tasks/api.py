from fastapi import Depends, APIRouter, Request
from app.authorization.service import get_current_user
from app.tasks.models import Task
from app.tasks.service import create_task, get_tasks_user, get_tasks, get_tasks_group, delete_task_by_id
from app.users.models import User
from fastapi.responses import HTMLResponse
from dependency_injector.wiring import inject, Provide
from dependencies import Container, Service

router = APIRouter()


@router.post("/tasks/add/")
@inject
def add_task(task: Task, db: Service = Depends(Provide[Container.db])):
    return create_task(db=next(db.get_db()), task=task)


@router.get("/tasks/all/", response_class=HTMLResponse)
@inject
def get_all_tasks(request: Request, db: Service = Depends(Provide[Container.db])):
    return get_tasks(request=request, db=next(db.get_db()))


@router.get("/tasks/user_id/{user_id}/", response_class=HTMLResponse)
@inject
def get_task(request: Request, user_id: int, db: Service = Depends(Provide[Container.db])):
    return get_tasks_user(request=request, db=next(db.get_db()), user_id=user_id)


@router.get("/tasks/me/", response_class=HTMLResponse)
@inject
async def get_tasks_me(request: Request, db: Service = Depends(Provide[Container.db]),
                       current_user: User = Depends(get_current_user)):
    return get_tasks_user(request=request, db=next(db.get_db()), user_id=current_user.id)


@router.get("/tasks/group/")
@inject
async def get_group_tasks(group_id: int, db: Service = Depends(Provide[Container.db])):
    return get_tasks_group(db=next(db.get_db()), group_id=group_id)


@router.post("/tasks/delete/{task_id}/")
@inject
def delete_task(task_id: int, db: Service = Depends(Provide[Container.db])):
    return delete_task_by_id(db=next(db.get_db()), task_id=task_id)
