from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models import location as models
from schemas import location as schemas
from database import get_db

router = APIRouter(
    prefix="/locations",
    tags=["locations"],
)

@router.post("/", response_model=schemas.Location)
def create_location(location: schemas.LocationCreate, db: Session = Depends(get_db)):
    # ตรวจสอบว่ามีสถานที่ที่ชื่อซ้ำกันหรือไม่
    existing_location = db.query(models.Location).filter(models.Location.name == location.name).first()
    if existing_location:
        raise HTTPException(status_code=400, detail="สถานที่นี้มีอยู่แล้วในระบบ")

    # บันทึกสถานที่ใหม่
    db_location = models.Location(**location.dict())
    db.add(db_location)
    db.commit()
    db.refresh(db_location)
    return db_location

@router.get("/", response_model=list[schemas.Location])
def read_locations(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(models.Location).offset(skip).limit(limit).all()

@router.get("/all", response_model=list[schemas.Location])
def get_all_locations(db: Session = Depends(get_db)):
    return db.query(models.Location).all()

@router.put("/{location_id}", response_model=schemas.Location)
def update_location(location_id: int, updated: schemas.LocationCreate, db: Session = Depends(get_db)):
    # ค้นหาสถานที่ตาม id
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="ไม่พบสถานที่นี้")

    # ตรวจสอบชื่อซ้ำ (แต่ต้องยกเว้นตัวเอง)
    existing_location = (
        db.query(models.Location)
        .filter(models.Location.name == updated.name, models.Location.id != location_id)
        .first()
    )
    if existing_location:
        raise HTTPException(status_code=400, detail="มีสถานที่ชื่อนี้อยู่แล้ว")

    # อัพเดต field
    for key, value in updated.dict().items():
        setattr(db_location, key, value)

    db.commit()
    db.refresh(db_location)
    return db_location

@router.delete("/{location_id}", response_model=dict)
def delete_location(location_id: int, db: Session = Depends(get_db)):
    db_location = db.query(models.Location).filter(models.Location.id == location_id).first()
    if not db_location:
        raise HTTPException(status_code=404, detail="ไม่พบสถานที่นี้")

    db.delete(db_location)
    db.commit()
    return {"detail": "ลบสถานที่เรียบร้อยแล้ว", "id": location_id}