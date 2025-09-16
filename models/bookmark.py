from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from database import Base

class Bookmark(Base):
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)  # Firebase UID (String)
    announcement_id = Column(Integer, ForeignKey("announcements.id"), nullable=False)

    __table_args__ = (UniqueConstraint("user_id", "announcement_id", name="unique_user_announcement"),)