from sqlalchemy import Column, Integer, String
from database import Base

class Timetable(Base):
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True)   # อ้างถึงผู้ใช้
    day = Column(String, index=True)
    time = Column(String, index=True)
    subject = Column(String)
