from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Union

class EventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: datetime
    end_time: datetime

class EventCreate(EventBase):
    user_id: Union[str, int] = Field(..., description="User ID as string or int")

class Event(EventBase):
    id: int
    user_id: str 

    class Config:
        from_attributes = True  # เปลี่ยนจาก orm_mode