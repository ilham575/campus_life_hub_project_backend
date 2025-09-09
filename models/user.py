from sqlalchemy import Column, Integer, String
from database import Base
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    announcements = relationship("Announcement", back_populates="creator")
    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
