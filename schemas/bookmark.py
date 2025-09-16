from pydantic import BaseModel

class BookmarkBase(BaseModel):
    user_id: str  # เปลี่ยนจาก int เป็น str
    announcement_id: int

class BookmarkCreate(BookmarkBase):
    pass

class Bookmark(BookmarkBase):
    id: int

    class Config:
        orm_mode = True