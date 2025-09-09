from pydantic import BaseModel
from datetime import datetime

class Announcement(BaseModel):
    id: int
    title: str
    content: str
    category: str
    created_at: datetime
    created_by: int