from fastapi import APIRouter, Depends, Request
from starlette.responses import HTMLResponse

from app.authorization.service import get_db, get_current_user
from sqlalchemy.orm import Session
from app.groups.models import Group
from app.groups.service import create_group, get_groups_user, get_groups, delete_group_by_id, get_group_info
from app.users.models import User

router = APIRouter()


@router.post("/groups/add/")
def add_group(group: Group, db: Session = Depends(get_db)):
    return create_group(db=db, group=group)


@router.get("/groups/all/", response_class=HTMLResponse)
def get_all_groups(request: Request, db: Session = Depends(get_db)):
    return get_groups(request=request, db=db)


@router.get("/groups/user_id/{user_id}/", response_class=HTMLResponse)
def get_groups_by_user_id(request: Request, user_id, db: Session = Depends(get_db)):
    return get_groups_user(request=request, db=db, user_id=user_id)


@router.get("/groups/me/", response_class=HTMLResponse)
async def get_tasks_me(request: Request, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_groups_user(request=request, db=db, user_id=current_user.id)


@router.post("/groups/delete/{group_id}/")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    return delete_group_by_id(db=db, group_id=group_id)


@router.get("/groups/group_id/{group_id}/", response_class=HTMLResponse)
def get_group(request: Request, group_id: int, db: Session = Depends(get_db)):
    return get_group_info(request, db=db, group_id=group_id)
