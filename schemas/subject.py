from pydantic import BaseModel
from typing import List, Optional

class ScheduleBase(BaseModel):
    day: str
    start_time: str
    end_time: str
    user_id: str

class ScheduleCreate(ScheduleBase):
    pass

class ScheduleResponse(BaseModel):
    id: int
    day: str
    start_time: str
    end_time: str

    class Config:
        orm_mode = True

class SubjectBase(BaseModel):
    name: str

class SubjectCreate(SubjectBase):
    schedules: List[ScheduleCreate]

class SubjectResponse(SubjectBase):
    id: int
    schedules: List[ScheduleResponse]

    class Config:
        orm_mode = True
