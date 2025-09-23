from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    name = Column(String, nullable=True)
    student_id = Column(String, unique=True, index=True, nullable=True)
    faculty = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    announcements = relationship("Announcement", back_populates="created_by")