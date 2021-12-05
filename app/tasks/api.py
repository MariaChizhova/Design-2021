from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from app.authorization.service import get_db, get_current_user
from app.tasks.models import Task
from app.tasks.service import create_task, get_tasks_user, get_tasks, get_tasks_group, delete_task_by_id
from app.users.models import User

router = APIRouter()


@router.post("/tasks/add/")
def add_task(task: Task, db: Session = Depends(get_db)):
    return create_task(db=db, task=task)


@router.get("/tasks/all/")
def get_all_tasks(db: Session = Depends(get_db)):
    return get_tasks(db=db)


@router.get("/tasks/user_id/{user_id}/")
def get_task(user_id: int, db: Session = Depends(get_db)):
    return get_tasks_user(db=db, user_id=user_id)


@router.get("/tasks/me/")
async def get_tasks_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_tasks_user(db=db, user_id=current_user.id)


@router.get("/tasks/group/")
async def get_group_tasks(group_id: int, db: Session = Depends(get_db)):
    return get_tasks_group(db=db, group_id=group_id)


@router.post("/tasks/delete/{task_id}/")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    return delete_task_by_id(db=db, task_id=task_id)
