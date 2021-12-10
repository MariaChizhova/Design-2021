from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter, Request
from app.authorization.service import get_db, get_current_user, create_user
from app.users.models import User
from app.users.service import get_users, delete_user_by_id, get_user_by_id
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/users/me/", response_class=HTMLResponse)
async def get_me(request: Request, current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users/user_id/{user_id}", response_class=HTMLResponse)
async def get_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    return get_user_by_id(request=request, user_id=user_id, db=db)


@router.get("/users/all/", response_class=HTMLResponse)
async def get_all(request: Request, db: Session = Depends(get_db)):
    return get_users(request=request, db=db)


@router.post("/users/add/")
def add_user(user: User, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)


@router.post("/users/delete/{user_id}/")
def delete_task(user_id: int, db: Session = Depends(get_db)):
    return delete_user_by_id(db=db, user_id=user_id)
