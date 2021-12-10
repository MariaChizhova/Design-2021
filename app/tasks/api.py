from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request
from app.authorization.service import get_db, get_current_user
from app.tasks.models import Task
from app.tasks.service import create_task, get_tasks_user, get_tasks, get_tasks_group, delete_task_by_id
from app.users.models import User
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.post("/tasks/add/")
def add_task(task: Task, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)


@router.get("/tasks/all/", response_class=HTMLResponse)
def get_all_tasks(request: Request, db: Session = Depends(get_db)):
    return get_tasks(request=request, db=db)


@router.get("/tasks/user_id/{user_id}/", response_class=HTMLResponse)
def get_task(request: Request, user_id: int, db: Session = Depends(get_db)):
    return get_tasks_user(request=request, db=db, user_id=user_id)


@router.get("/tasks/me/", response_class=HTMLResponse)
async def get_tasks_me(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_tasks_user(request=request, db=db, user_id=current_user.id)


@router.get("/tasks/group/")
async def get_group_tasks(group_id: int, db: Session = Depends(get_db)):
    return get_tasks_group(db=db, group_id=group_id)


@router.post("/tasks/delete/{task_id}/")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return delete_task_by_id(db=db, task_id=task_id)
