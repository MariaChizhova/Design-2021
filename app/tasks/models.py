from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey
from app.users.data import Base
import datetime


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String)
    description = Column(String)
    priority = Column(Integer)
    status = Column(Boolean, default=True)
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, default=datetime.datetime.utcnow)


class Task_User(Base):
    __tablename__ = "task_user"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)


class Task_Group(Base):
    __tablename__ = "task_group"
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
    task_id = Column(Integer, ForeignKey('tasks.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
