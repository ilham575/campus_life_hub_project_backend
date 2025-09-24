from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.subject import Subject, Schedule
from models.user import User
from schemas.subject import SubjectCreate, SubjectResponse
from typing import List
from routers.auth import get_current_user

router = APIRouter(prefix="/subjects", tags=["Subjects"])

# 🔹 ดึงรายวิชาทั้งหมดของ user ที่ล็อกอิน
@router.get("/{user_id}", response_model=List[SubjectResponse])
def get_subjects(
    user_id: str,
    db: Session = Depends(get_db)
):
    subjects = db.query(Subject).filter(Subject.user_id == user_id).all()
    return subjects

# 🔹 เพิ่มรายวิชาใหม่พร้อมตารางเวลา
@router.post("/", response_model=SubjectResponse)
def create_subject(
    subject_data: SubjectCreate,
    db: Session = Depends(get_db)
):
    # สร้าง Subject ใหม่
    db_subject = Subject(
        user_id=subject_data.schedules[0].user_id if subject_data.schedules else "",
        name=subject_data.name
    )
    db.add(db_subject)
    db.commit()
    db.refresh(db_subject)
    
    # เพิ่ม Schedules ทั้งหมด
    for schedule_data in subject_data.schedules:
        db_schedule = Schedule(
            subject_id=db_subject.id,
            user_id=schedule_data.user_id,
            day=schedule_data.day,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time
        )
        db.add(db_schedule)
    
    db.commit()
    db.refresh(db_subject)
    return db_subject

# 🔹 ลบรายวิชา
@router.delete("/{subject_id}")
def delete_subject(
    subject_id: int,
    db: Session = Depends(get_db)
):
    subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    db.delete(subject)
    db.commit()
    return {"message": "Subject deleted successfully"}

@router.delete("/schedule/{schedule_id}")
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db)
):
    schedule = db.query(Schedule).filter(Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    db.delete(schedule)
    db.commit()
    return {"message": "Schedule deleted successfully"}

# 🔹 แก้ไขรายวิชา
@router.put("/{subject_id}", response_model=SubjectResponse)
def update_subject(
    subject_id: int,
    subject_data: SubjectCreate,
    db: Session = Depends(get_db)
):
    db_subject = db.query(Subject).filter(Subject.id == subject_id).first()
    if not db_subject:
        raise HTTPException(status_code=404, detail="Subject not found")
    
    # อัพเดตชื่อวิชา
    db_subject.name = subject_data.name
    
    # ลบ schedules เก่าทั้งหมด
    db.query(Schedule).filter(Schedule.subject_id == subject_id).delete()
    
    # เพิ่ม schedules ใหม่
    for schedule_data in subject_data.schedules:
        db_schedule = Schedule(
            subject_id=subject_id,
            user_id=schedule_data.user_id,
            day=schedule_data.day,
            start_time=schedule_data.start_time,
            end_time=schedule_data.end_time
        )
        db.add(db_schedule)
    
    db.commit()
    db.refresh(db_subject)
    return db_subject
