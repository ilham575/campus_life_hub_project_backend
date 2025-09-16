from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict

class AnnouncementBase(BaseModel):
    title: str
    category: str
    source: str | None = None
    detail: str | None = None

class AnnouncementCreate(AnnouncementBase):
    pass

class Announcement(AnnouncementBase):
    id: int

    class Config:
        orm_mode = True