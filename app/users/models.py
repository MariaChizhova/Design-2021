from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String, DateTime
import datetime
from app.users.data import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)


class UserScheme(BaseModel):
    username: str


class UserCreate(UserScheme):
    password: str
    email: str
