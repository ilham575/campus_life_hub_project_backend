from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.timetable import Timetable
from schemas.timetable import TimetableCreate, TimetableResponse
from typing import List

# ✅ prefix = /timetable
router = APIRouter(prefix="/timetable", tags=["Timetable"])

# 🔹 ดึงตารางเรียนของ user
@router.get("/{user_id}", response_model=List[TimetableResponse])
def get_timetable(user_id: str, db: Session = Depends(get_db)):
    return db.query(Timetable).filter(Timetable.user_id == user_id).all()

# 🔹 เพิ่มตารางเรียนใหม่ (POST)
# ❌ เดิม: @router.post("/") 
# ✅ ใหม่: @router.post("")
@router.post("", response_model=TimetableResponse)
def create_timetable(item: TimetableCreate, db: Session = Depends(get_db)):
    db_item = Timetable(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

# 🔹 ลบตารางเรียน
@router.delete("/{item_id}")
def delete_timetable(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Timetable).filter(Timetable.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
    return {"message": "Deleted successfully"}

# 🔹 แก้ไขตารางเรียน (PUT)
@router.put("/{item_id}", response_model=TimetableResponse)
def update_timetable(item_id: int, item: TimetableCreate, db: Session = Depends(get_db)):
    db_item = db.query(Timetable).filter(Timetable.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.user_id = item.user_id
    db_item.day = item.day
    db_item.time = item.time
    db_item.subject = item.subject

    db.commit()
    db.refresh(db_item)
    return db_item
