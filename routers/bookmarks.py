from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.bookmark import Bookmark
from models.announcement import Announcement  # Import the Announcement model
from schemas.bookmark import BookmarkCreate, BookmarkResponse

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a bookmark
@router.post("/", response_model=BookmarkResponse)
def create_bookmark(bookmark: BookmarkCreate, db: Session = Depends(get_db)):
    # Check if the announcement exists
    announcement = db.query(Announcement).filter(Announcement.id == bookmark.announcement_id).first()
    if not announcement:
        raise HTTPException(status_code=404, detail="Announcement not found")

    # Check if the bookmark already exists
    existing_bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == bookmark.user_id,
        Bookmark.announcement_id == bookmark.announcement_id
    ).first()
    if existing_bookmark:
        raise HTTPException(status_code=400, detail="Bookmark already exists")

    db_bookmark = Bookmark(**bookmark.dict())
    db.add(db_bookmark)
    db.commit()
    db.refresh(db_bookmark)
    return db_bookmark

# Get all bookmarks
@router.get("/", response_model=list[BookmarkResponse])
def read_bookmarks(db: Session = Depends(get_db)):
    return db.query(Bookmark).all()

# Delete a bookmark
@router.delete("/{bookmark_id}")
def delete_bookmark(bookmark_id: int, db: Session = Depends(get_db)):
    db_bookmark = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if not db_bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    db.delete(db_bookmark)
    db.commit()
    return {"message": "Bookmark deleted"}