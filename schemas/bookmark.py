from pydantic import BaseModel

class BookmarkBase(BaseModel):
    user_id: int
    announcement_id: int

class BookmarkCreate(BookmarkBase):
    pass

class BookmarkResponse(BookmarkBase):
    id: int

    class Config:
        orm_mode = True