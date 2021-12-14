from pydantic import BaseModel
import datetime


class Task(BaseModel):
    type: str  # user_task/group_task
    entity_id: int  # id of user/group
    name: str
    description: str
    priority: int
    start_time: datetime.datetime
    end_time: datetime.datetime


class TaskUser(BaseModel):
    user_id: int
    task_id: int
