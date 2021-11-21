from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.users.data import Base
import datetime
from pydantic import BaseModel


class Message(BaseModel):
    id: int
    created_date: datetime
    content: str
    from_user_id: int
    to_user_id: int


class MessageDB(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(String)
    from_user_id = Column(Integer, ForeignKey('users.id'))
    to_user_id = Column(Integer, ForeignKey('users.id'))
