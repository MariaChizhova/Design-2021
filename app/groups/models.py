from typing import List

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.users.data import Base
import datetime
from pydantic import BaseModel


class Group(BaseModel):
    admin_id: int
    name: str
    users_list: List[int]


class GroupDB(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    admin_id = Column(Integer)
    name = Column(String)


class GroupUserDB(Base):
    __tablename__ = "group_user"
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    group_id = Column(Integer, ForeignKey('groups.id'), primary_key=True)
