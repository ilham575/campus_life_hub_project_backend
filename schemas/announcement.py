from pydantic import BaseModel
from datetime import datetime

class AnnouncementBase(BaseModel):
    title: str
    content: str
    category: str

class AnnouncementCreate(AnnouncementBase):
    created_by: int

class AnnouncementResponse(AnnouncementBase):
    id: int
    created_at: datetime
    created_by: int

    class Config:
        orm_mode = True