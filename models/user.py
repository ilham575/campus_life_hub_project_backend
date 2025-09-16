from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firebase_uid = Column(String, unique=True, nullable=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)  # เพิ่ม field นี้
