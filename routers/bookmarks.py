from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.bookmark import Bookmark as BookmarkModel
from models.announcement import Announcement
from schemas.bookmark import BookmarkCreate, Bookmark
from typing import List

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])

# Create a bookmark - ไม่ต้อง authenticate
@router.post("/", response_model=Bookmark)
def create_bookmark(
    bookmark: BookmarkCreate, 
    db: Session = Depends(get_db)
):
    # Check if the announcement exists
    announcement = db.query(Announcement).filter(Announcement.id == bookmark.announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    # Check if the bookmark already exists
    existing_bookmark = db.query(BookmarkModel).filter(
        BookmarkModel.user_id == bookmark.user_id,
        BookmarkModel.announcement_id == bookmark.announcement_id
    ).first()
    if existing_bookmark:
        raise HTTPException(status_code=400, detail="Bookmark already exists")

    db_bookmark = BookmarkModel(**bookmark.dict())
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark

# Get bookmarks by user_id - ไม่ต้อง authenticate
@router.get("/", response_model=List[Bookmark])
def get_bookmarks(
    user_id: str,
    db: Session = Depends(get_db)
):
    return db.query(BookmarkModel).filter(BookmarkModel.user_id == user_id).all()

# Delete a bookmark - ไม่ต้อง authenticate
@router.delete("/{bookmark_id}")
def delete_bookmark(
    bookmark_id: int, 
    db: Session = Depends(get_db)
):
    db_bookmark = db.query(BookmarkModel).filter(BookmarkModel.id == bookmark_id).first()
    if not db_bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(db_bookmark)
    db.commit()
    return {"ok": True}

# เพิ่ม endpoint สำหรับหา bookmark ด้วย user_id และ announcement_id
@router.get("/find")
def find_bookmark(
    user_id: str,
    announcement_id: int,
    db: Session = Depends(get_db)
):
    bookmark = db.query(BookmarkModel).filter(
        BookmarkModel.user_id == user_id,
        BookmarkModel.announcement_id == announcement_id
    ).first()
    if bookmark:
        return bookmark
    return None