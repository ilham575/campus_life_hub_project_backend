from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: EmailStr  # email
    password: str
    name: Optional[str] = None
    student_id: Optional[str] = None
    faculty: Optional[str] = None
    year: Optional[int] = None
    role: str = "user"  # default role is "user"

class UserResponse(BaseModel):
    id: int
    username: str
    name: Optional[str] = None
    student_id: Optional[str] = None
    faculty: Optional[str] = None
    year: Optional[int] = None
    created_at: datetime
    role: str
    
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str] = None
    student_id: Optional[str] = None
    faculty: Optional[str] = None
    year: Optional[int] = None

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse

class TokenData(BaseModel):
    username: Optional[str] = None

class RoleUpdate(BaseModel):
    role: str  # e.g., "user", "admin"