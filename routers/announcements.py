from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models.announcement import Announcement as AnnouncementModel
from models.user import User as UserModel
from schemas.announcement import AnnouncementCreate, Announcement
from auth import get_current_user  # Import authentication function
from typing import List

router = APIRouter(prefix="/announcements")

# Create an announcement
@router.post("/", response_model=Announcement)
def create_announcement(
    announcement: AnnouncementCreate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)  # ดึง user จาก token
):
    # สร้าง announcement โดยใช้ user_id จาก current_user
    announcement_data = announcement.dict()
    announcement_data['created_by_id'] = current_user.id
    
    db_announcement = AnnouncementModel(**announcement_data)
    db.add(db_announcement)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

# Get all announcements
@router.get("/", response_model=List[Announcement])
def get_announcements(db: Session = Depends(get_db)):
    return db.query(AnnouncementModel).options(joinedload(AnnouncementModel.created_by)).all()

# Update an announcement
@router.put("/{announcement_id}", response_model=Announcement)
def update_announcement(
    announcement_id: int, 
    announcement: AnnouncementCreate, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)  # เพิ่ม auth
):
    db_announcement = db.query(AnnouncementModel).filter(AnnouncementModel.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    # ตรวจสอบว่าเป็นเจ้าของ announcement หรือไม่ (หรือเป็น admin)
    if db_announcement.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to edit this announcement")
    
    # อัปเดตประกาศ
    for key, value in announcement.dict().items():
        setattr(db_announcement, key, value)
    db.commit()
    db.refresh(db_announcement)
    return db_announcement

# Delete an announcement
@router.delete("/{announcement_id}")
def delete_announcement(
    announcement_id: int, 
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)  # เพิ่ม auth
):
    db_announcement = db.query(AnnouncementModel).filter(AnnouncementModel.id == announcement_id).first()
    if not db_announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")
    
    # ตรวจสอบว่าเป็นเจ้าของ announcement หรือไม่ (หรือเป็น admin)
    if db_announcement.created_by_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this announcement")
    
    db.delete(db_announcement)
    db.commit()
    return {"message": "Announcement deleted"}