import datetime
from pydantic import BaseModel


class Message(BaseModel):
    id: int
    created_date: datetime
    content: str
    from_user_id: int
    to_user_id: int
