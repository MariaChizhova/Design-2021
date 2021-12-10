from fastapi import HTTPException, Request
from sqlalchemy.orm import Session

from app.groups.models import GroupUserDB
from app.tasks.models import Task, TaskDB, TaskUserDB, TaskGroupDB
from app.utils.utils import templates


def create_task(db: Session, task: Task):
    db_task = TaskDB(type=task.type,
                     name=task.name,
                     description=task.description,
                     priority=task.priority,
                     start_time=task.start_time,
                     end_time=task.end_time)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    if task.type == "user_task":
        db_task_user = TaskUserDB(task_id=db_task.id, user_id=task.entity_id)
        db.add(db_task_user)
        db.commit()
        db.refresh(db_task_user)
    elif task.type == "group_task":
        db_task_group = TaskGroupDB(task_id=db_task.id, group_id=task.entity_id)
        db.add(db_task_group)
        db.commit()
        db.refresh(db_task_group)
        query = db.query(GroupUserDB).filter(GroupUserDB.group_id == task.entity_id) \
            .with_entities(GroupUserDB.user_id).all()
        users = [item.user_id for item in query]
        for user_id in users:
            db_task_user = TaskUserDB(task_id=db_task.id, user_id=user_id)
            db.add(db_task_user)
            db.commit()
            db.refresh(db_task_user)
    return db_task


def unpack(tasks):
    tasks = [{"type": task.type,
              "entity_id": task.id,
              "name": task.name,
              "description": task.description,
              "priority": task.priority,
              "start_time": task.start_time.strftime("%m/%d/%Y, %H:%M:%S"),
              "end_time": task.end_time.strftime("%m/%d/%Y, %H:%M:%S")} for task in tasks]
    return tasks


def get_tasks(request: Request, db: Session, skip: int = 0, limit: int = 100):
    tasks = db.query(TaskDB).offset(skip).limit(limit).all()
    return templates.TemplateResponse("tasks/all_tasks.html",
                                      {"request": request,
                                       "tasks": unpack(tasks)})


def get_tasks_by_user_id(db: Session, user_id: int):
    query = db.query(TaskUserDB).filter(TaskUserDB.user_id == user_id).with_entities(TaskUserDB.task_id).all()
    task_ids = [item.task_id for item in query]
    tasks = db.query(TaskDB).filter(TaskDB.id.in_(task_ids)).all()
    return tasks


def get_tasks_user(request: Request, db: Session, user_id: int):
    tasks = get_tasks_by_user_id(db=db, user_id=user_id)
    return templates.TemplateResponse("tasks/all_tasks.html",
                                      {"request": request,
                                       "tasks": unpack(tasks)})


def get_tasks_group(db: Session, group_id: int):
    query = db.query(TaskGroupDB).filter(TaskGroupDB.group_id == group_id).with_entities(TaskGroupDB.task_id).all()
    task_ids = [item.task_id for item in query]
    return db.query(TaskDB).filter(TaskDB.id.in_(task_ids)).all()


def delete_task_by_id(db: Session, task_id: int):
    db_task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not db_task:
        raise HTTPException(status_code=404, detail="Task_id not found")
    db.delete(db_task)
    db.query(TaskUserDB).filter(TaskUserDB.task_id == task_id).delete()
    db.query(TaskGroupDB).filter(TaskGroupDB.task_id == task_id).delete()
    db.commit()
    return db_task
