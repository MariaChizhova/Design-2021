from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.groups.models import Group, GroupDB, GroupUserDB
from app.tasks.models import TaskGroupDB


def create_group(db: Session, group: Group):
    db_group = GroupDB(admin_id=group.admin_id, name=group.name)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)

    for user_id in group.users_list:
        db_group_user = GroupUserDB(group_id=db_group.id, user_id=user_id)
        db.add(db_group_user)
        db.commit()
        db.refresh(db_group_user)
    return db_group


def get_groups(db: Session, skip: int = 0, limit: int = 100):
    return db.query(GroupDB).offset(skip).limit(limit).all()


def get_groups_user(db: Session, user_id: int):
    query = db.query(GroupUserDB).filter(GroupUserDB.user_id == user_id).with_entities(GroupUserDB.group_id).all()
    groups_ids = [item.group_id for item in query]
    return db.query(GroupDB).filter(GroupDB.id.in_(groups_ids)).all()


def delete_group_by_id(db: Session, group_id: int):
    db_group = db.query(GroupDB).filter(GroupDB.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group_id not found")
    db.delete(db_group)
    db.query(GroupUserDB).filter(GroupUserDB.group_id == group_id).delete()
    db.query(TaskGroupDB).filter(TaskGroupDB.group_id == group_id).delete()
    db.commit()
    return db_group
