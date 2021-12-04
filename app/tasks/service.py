from sqlalchemy.orm import Session

from app.groups.models import GroupUserDB
from app.tasks.models import Task, TaskDB, TaskUserDB, TaskGroupDB


def create_task(db: Session, task: Task):
    db_task = TaskDB(name=task.name,
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
        query = db.query(GroupUserDB).filter(GroupUserDB.group_id == task.entity_id) \
            .with_entities(GroupUserDB.user_id).all()
        users = [item.user_id for item in query]
        for user_id in users:
            db_task_group = TaskGroupDB(task_id=db_task.id, group_id=task.entity_id)
            db.add(db_task_group)
            db.commit()
            db.refresh(db_task_group)

            db_task_user = TaskUserDB(task_id=db_task.id, user_id=user_id)
            db.add(db_task_user)
            db.commit()
            db.refresh(db_task_user)
    return db_task


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(TaskDB).offset(skip).limit(limit).all()


def get_tasks_user(db: Session, user_id: int):
    query = db.query(TaskUserDB).filter(TaskUserDB.user_id == user_id).with_entities(TaskUserDB.task_id).all()
    task_ids = [item.task_id for item in query]
    return db.query(TaskDB).filter(TaskDB.id.in_(task_ids)).all()
