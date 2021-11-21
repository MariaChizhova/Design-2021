from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app.users.data import Base
import datetime


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(String)
    from_user_id = Column(Integer, ForeignKey('users.id'))
    to_user_id = Column(Integer, ForeignKey('users.id'))
