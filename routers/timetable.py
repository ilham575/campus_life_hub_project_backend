from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.timetable import Timetable
from models.user import User
from schemas.timetable import TimetableCreate, TimetableResponse
from typing import List
from routers.auth import get_current_user  # ปรับ path ให้ตรงกับโปรเจ็คของคุณ

router = APIRouter(prefix="/timetable", tags=["Timetable"])

# 🔹 ดึงตารางเรียนของ user ที่ล็อกอิน
@router.get("/", response_model=List[TimetableResponse])
def get_timetable(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Timetable).filter(Timetable.user_id == str(current_user.id)).all()

# 🔹 เพิ่มตารางเรียนใหม่ (POST)
@router.post("/", response_model=TimetableResponse)
def create_timetable(
    item: TimetableCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = Timetable(
        user_id=str(current_user.id),
        day=item.day,
        time=item.time,
        subject=item.subject
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 🔹 ลบตารางเรียน
@router.delete("/{item_id}")
def delete_timetable(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(Timetable).filter(Timetable.id == item_id, Timetable.user_id == str(current_user.id)).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found or not authorized")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# 🔹 แก้ไขตารางเรียน (PUT)
@router.put("/{item_id}", response_model=TimetableResponse)
def update_timetable(
    item_id: int,
    item: TimetableCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_item = db.query(Timetable).filter(Timetable.id == item_id, Timetable.user_id == str(current_user.id)).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found or not authorized")
    db_item.day = item.day
    db_item.time = item.time
    db_item.subject = item.subject
    db.commit()
    db.refresh(db_item)
    return db_item