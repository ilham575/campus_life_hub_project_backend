from pydantic import BaseModel
from datetime import datetime
from .user import UserInfo

class AnnouncementBase(BaseModel):
    title: str
    category: str
    source: str | None = None
    detail: str | None = None

class AnnouncementCreate(AnnouncementBase):
    pass  

class Announcement(AnnouncementBase):
    id: int
    created_by_id: int
    created_at: datetime
    created_by: UserInfo  

    class Config:
        from_attributes = True