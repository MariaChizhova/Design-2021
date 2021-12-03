from sqlalchemy.orm import Session
from fastapi import Depends, APIRouter
from app.authorization.service import get_db, get_current_user, create_user, get_users
from app.users.models import User

router = APIRouter()


@router.get("/users/me/")
async def get_me(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users/all/")
async def get_all(db: Session = Depends(get_db)):
    return get_users(db=db)


@router.post("/users/add/")
def add_user(user: User, db: Session = Depends(get_db)):
    return create_user(db=db, user=user)
