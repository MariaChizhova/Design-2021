from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, DateTime
import datetime
from app.users.data import Base


class User(BaseModel):
    email: str
    username: str
    password: str


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
