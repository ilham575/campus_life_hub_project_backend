from sqlalchemy import Column, Integer, String
from database import Base

class Timetable(Base):
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)   # อ้างถึงผู้ใช้, ไม่ควรเป็น null
    day = Column(String, index=True, nullable=False)
    time = Column(String, index=True, nullable=False)
    subject = Column(String, nullable=False)