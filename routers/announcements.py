from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db  # Import get_db from database.py
from models.announcement import Announcement as AnnouncementModel
from schemas.announcement import AnnouncementCreate, Announcement
from datetime import datetime
from typing import List

router = APIRouter(prefix="/announcements")

# Create an announcement
@router.post("/", response_model=Announcement)
def create_announcement(announcement: AnnouncementCreate, db: Session = Depends(get_db)):
    db_announcement = AnnouncementModel(**announcement.dict())
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

# Get all announcements
@router.get("/", response_model=List[Announcement])
def get_announcements(db: Session = Depends(get_db)):
    return db.query(AnnouncementModel).all()

# Update an announcement
@router.put("/{announcement_id}", response_model=Announcement)
def update_announcement(announcement_id: int, announcement: AnnouncementCreate, db: Session = Depends(get_db)):
    db_announcement = db.query(AnnouncementModel).filter(AnnouncementModel.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    # --- เก็บประวัติการแก้ไขใน edit_history --- 
    # (ถ้าไม่มี field edit_history ให้ลบส่วนนี้ออก)
    # --- อัปเดตประกาศ ---
    for key, value in announcement.dict().items():
        setattr(db_announcement, key, value)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

# Delete an announcement
@router.delete("/{announcement_id}")
def delete_announcement(announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = db.query(AnnouncementModel).filter(AnnouncementModel.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    db.delete(db_announcement)
    db.commit()
    return {"message": "Announcement deleted"}