from pydantic import BaseModel, Field

class LocationBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    description: str | None = None

class LocationCreate(LocationBase):
    pass

class Location(LocationBase):
    id: int

    class Config:
        orm_mode = True
