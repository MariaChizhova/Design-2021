from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from app.users.data import Base
import datetime


class Task(BaseModel):
    type: str  # user_task/group_task
    entity_id: int  # id of user/group
    name: str
    description: str
    priority: int
    start_time: datetime.datetime
    end_time: datetime.datetime


class TaskDB(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String)
    description = Column(String)
    priority = Column(Integer)
    status = Column(Boolean, default=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, default=datetime.datetime.utcnow)


class TaskUser(BaseModel):
    user_id: int
    task_id: int


class TaskUserDB(Base):
    __tablename__ = "task_user"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)


class TaskGroupDB(Base):
    __tablename__ = "task_group"
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
