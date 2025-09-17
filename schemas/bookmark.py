from pydantic import BaseModel
from datetime import datetime

class BookmarkCreate(BaseModel):
    announcement_id: int

class BookmarkResponse(BaseModel):
    id: int
    user_id: int
    announcement_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True