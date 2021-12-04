from fastapi import APIRouter, Depends
from app.authorization.service import get_db, get_current_user
from sqlalchemy.orm import Session
from app.groups.models import Group
from app.groups.service import create_group, get_groups_user, get_groups
from app.users.models import User

router = APIRouter()


@router.post("/groups/add/")
def add_group(group: Group, db: Session = Depends(get_db)):
    return create_group(db=db, group=group)


@router.get("/groups/all/")
def get_all_groups(db: Session = Depends(get_db)):
    return get_groups(db=db)


@router.get("/groups/user_id/{user_id}/")
def get_task(user_id, db: Session = Depends(get_db)):
    return get_groups_user(db=db, user_id=user_id)


@router.get("/groups/me/")
async def get_tasks_me(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_groups_user(db=db, user_id=current_user.id)
