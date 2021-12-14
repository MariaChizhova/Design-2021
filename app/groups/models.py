from typing import List
from pydantic import BaseModel


class Group(BaseModel):
    admin_id: int
    name: str
    users_list: List[int]
