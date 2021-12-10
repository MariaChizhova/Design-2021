from fastapi import HTTPException, Request

from app.groups.models import GroupUserDB
from app.tasks.models import TaskUserDB
from app.tasks.service import get_tasks_by_user_id, unpack as tasks_unpack
from app.users.models import UserDB
from sqlalchemy.orm import Session

from app.utils.utils import templates


def get_user(db, username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()


def unpack(users):
    users = [{"created_date": user.created_date.strftime("%m/%d/%Y, %H:%M:%S"),
              "id": user.id,
              "username": user.username,
              "is_active": str(user.is_active),
              "email": user.email} for user in users]
    return users


def get_user_by_id(request: Request, db, user_id: int):
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    tasks = get_tasks_by_user_id(db=db, user_id=user_id)
    return templates.TemplateResponse("users/user_info.html",
                                      {"request": request,
                                       "user": unpack([user])[0],
                                       "tasks": tasks_unpack(tasks)})


def get_users(request: Request, db: Session, skip: int = 0, limit: int = 100):
    users = db.query(UserDB).offset(skip).limit(limit).all()
    return templates.TemplateResponse("users/all_users.html",
                                      {"request": request,
                                       "users": unpack(users)})


def delete_user_by_id(db: Session, user_id: int):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User_id not found")
    db.delete(db_user)
    db.query(TaskUserDB).filter(TaskUserDB.user_id == user_id).delete()
    db.query(GroupUserDB).filter(GroupUserDB.user_id == user_id).delete()
    db.commit()
    return db_user
