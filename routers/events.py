from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.events import Event as EventModel
from models.user import User
from schemas.events import Event, EventCreate

router = APIRouter()

EVENT_NOT_FOUND = "Event not found"

@router.post("/", response_model=Event)
def create_event(event: EventCreate, db: Session = Depends(get_db)):
    # แปลง user_id เป็น string
    user_id_str = str(event.user_id)
    
    # เช็ค user_id ว่ามีจริงในตาราง User
    user = db.query(User).filter(User.id == user_id_str).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_event = EventModel(
        user_id=user_id_str,
        title=event.title,
        description=event.description,
        start_time=event.start_time,
        end_time=event.end_time
    )
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=List[Event])
def read_events(
    user_id: str = Query(..., description="User ID"),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(EventModel).filter(EventModel.user_id == user_id).offset(skip).limit(limit).all()

@router.get("/{event_id}", response_model=Event)
def read_event(event_id: int, user_id: str = Query(...), db: Session = Depends(get_db)):
    event = db.query(EventModel).filter(EventModel.id == event_id, EventModel.user_id == user_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail=EVENT_NOT_FOUND)
    return event

@router.put("/{event_id}", response_model=Event)
def update_event(event_id: int, event: EventCreate, user_id: str = Query(...), db: Session = Depends(get_db)):
    db_event = db.query(EventModel).filter(EventModel.id == event_id, EventModel.user_id == user_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail=EVENT_NOT_FOUND)
    db_event.title = event.title
    db_event.description = event.description
    db_event.start_time = event.start_time
    db_event.end_time = event.end_time
    db.commit()
    db.refresh(db_event)
    return db_event

@router.delete("/{event_id}")
def delete_event(event_id: int, user_id: str = Query(...), db: Session = Depends(get_db)):
    db_event = db.query(EventModel).filter(EventModel.id == event_id, EventModel.user_id == user_id).first()
    if db_event is None:
        raise HTTPException(status_code=404, detail=EVENT_NOT_FOUND)
    db.delete(db_event)
    db.commit()
    return {"message": "Event deleted"}