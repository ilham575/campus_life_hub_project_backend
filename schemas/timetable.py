from pydantic import BaseModel

class TimetableBase(BaseModel):
    day: str
    time: str
    subject: str

class TimetableCreate(TimetableBase):
    user_id: str

class TimetableResponse(TimetableBase):
    id: int
    user_id: str

    class Config:
        orm_mode = True
