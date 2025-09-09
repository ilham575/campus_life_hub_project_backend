from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    announcement_id = Column(Integer, ForeignKey("announcements.id"), nullable=False)

    # Ensure that a user can bookmark an announcement only once
    __table_args__ = (UniqueConstraint("user_id", "announcement_id", name="unique_user_announcement"),)

    # Relationships (optional, for easier access)
    user = relationship("User", back_populates="bookmarks")
    announcement = relationship("Announcement", back_populates="bookmarks")