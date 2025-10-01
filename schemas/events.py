from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class EventCreate(EventBase):
    user_id: str

class Event(EventBase):
    id: int
    user_id: str 

    class Config:
        orm_mode = True