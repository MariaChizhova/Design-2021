from fastapi import HTTPException

from app.groups.models import GroupUserDB
from app.tasks.models import TaskUserDB
from app.users.models import UserDB
from sqlalchemy.orm import Session


def get_user(db, username: str):
    return db.query(UserDB).filter(UserDB.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserDB).offset(skip).limit(limit).all()


def delete_user_by_id(db: Session, user_id: int):
    db_user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User_id not found")
    db.delete(db_user)
    db.query(TaskUserDB).filter(TaskUserDB.user_id == user_id).delete()
    db.query(GroupUserDB).filter(GroupUserDB.user_id == user_id).delete()
    db.commit()
    return db_user
