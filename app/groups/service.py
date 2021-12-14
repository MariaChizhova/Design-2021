from fastapi import HTTPException, Request
from sqlalchemy.orm import Session
from app.groups.models import Group
from app.tasks.data import TaskGroupDB
from app.tasks.service import get_tasks_group
from app.users.data import UserDB
from app.utils.utils import templates
from app.tasks.service import unpack as tasks_unpack
from app.groups.data import GroupDB, GroupUserDB


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


def unpack(groups):
    groups = [{"id": group.id,
               "name": group.name,
               "admin_id": group.admin_id,
               "created_date": group.created_date.strftime("%m/%d/%Y, %H:%M:%S")} for group in groups]
    return groups


def get_groups(request: Request, db: Session, skip: int = 0, limit: int = 100):
    groups = db.query(GroupDB).offset(skip).limit(limit).all()
    return templates.TemplateResponse("groups/all_groups.html",
                                      {"request": request,
                                       "groups": unpack(groups)})


def get_groups_user(request: Request, db: Session, user_id: int):
    query = db.query(GroupUserDB).filter(GroupUserDB.user_id == user_id).with_entities(GroupUserDB.group_id).all()
    groups_ids = [item.group_id for item in query]
    groups = db.query(GroupDB).filter(GroupDB.id.in_(groups_ids)).all()
    return templates.TemplateResponse("groups/all_groups.html",
                                      {"request": request,
                                       "groups": unpack(groups)})


def delete_group_by_id(db: Session, group_id: int):
    db_group = db.query(GroupDB).filter(GroupDB.id == group_id).first()
    if not db_group:
        raise HTTPException(status_code=404, detail="Group_id not found")
    db.delete(db_group)
    db.query(GroupUserDB).filter(GroupUserDB.group_id == group_id).delete()
    db.query(TaskGroupDB).filter(TaskGroupDB.group_id == group_id).delete()
    db.commit()
    return db_group


def get_group_info(request: Request, db: Session, group_id: int):
    users_query = db.query(GroupUserDB).filter(GroupUserDB.group_id == group_id).with_entities(
        GroupUserDB.user_id).all()
    users_ids = [item.user_id for item in users_query]
    users = db.query(UserDB).filter(UserDB.id.in_(users_ids)).all()
    users = [{"id": user.id,
              "username": user.username,
              "is_active": str(user.is_active),
              "email": user.email} for user in users]
    group = db.query(GroupDB).filter(GroupDB.id == group_id).first()
    tasks = get_tasks_group(db=db, group_id=group_id)
    return templates.TemplateResponse("groups/group_info.html",
                                      {"request": request,
                                       "group": unpack([group])[0],
                                       "users": users,
                                       "tasks": tasks_unpack(tasks)})
