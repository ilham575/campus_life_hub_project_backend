from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.bookmark import Bookmark
from models.user import User
from schemas.bookmark import BookmarkCreate, BookmarkResponse
from routers.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[BookmarkResponse])
def get_bookmarks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ดึง bookmarks ทั้งหมดของ user ปัจจุบัน"""
    return db.query(Bookmark).filter(Bookmark.user_id == current_user.id).all()

@router.post("/", response_model=BookmarkResponse)
def create_bookmark(
    bookmark: BookmarkCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """สร้าง bookmark ใหม่"""
    # ตรวจสอบว่ามี bookmark นี้อยู่แล้วหรือไม่
    existing = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.announcement_id == bookmark.announcement_id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Bookmark already exists")
    
    # สร้าง bookmark ใหม่
    db_bookmark = Bookmark(
        user_id=current_user.id,
        announcement_id=bookmark.announcement_id
    )
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark

@router.delete("/by-announcement/{announcement_id}")
def delete_bookmark_by_announcement(
    announcement_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """ลบ bookmark โดย announcement_id"""
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == current_user.id,
        Bookmark.announcement_id == announcement_id
    ).first()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    return {"message": "Bookmark deleted successfully"}