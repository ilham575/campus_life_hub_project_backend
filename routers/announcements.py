from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db  # Import get_db from database.py
from models.announcement import Announcement
from schemas.announcement import AnnouncementCreate, AnnouncementResponse

router = APIRouter(prefix="/announcements")

# Create an announcement
@router.post("/", response_model=AnnouncementResponse)
def create_announcement(announcement: AnnouncementCreate, db: Session = Depends(get_db)):
    db_announcement = Announcement(**announcement.dict())
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

# Get all announcements
@router.get("/", response_model=list[AnnouncementResponse])
def read_announcements(db: Session = Depends(get_db)):
    return db.query(Announcement).all()

# Update an announcement
@router.put("/{announcement_id}", response_model=AnnouncementResponse)
def update_announcement(announcement_id: int, announcement: AnnouncementCreate, db: Session = Depends(get_db)):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    for key, value in announcement.dict().items():
        setattr(db_announcement, key, value)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

# Delete an announcement
@router.delete("/{announcement_id}")
def delete_announcement(announcement_id: int, db: Session = Depends(get_db)):
    db_announcement = db.query(Announcement).filter(Announcement.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    db.delete(db_announcement)
    db.commit()
    return {"message": "Announcement deleted"}