from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

# Announcement model
class Announcement(BaseModel):
    id: int
    title: str
    content: str
    category: str
    created_at: datetime
    created_by: int

# In-memory database
announcements = []

@router.post("/announcements/", response_model=Announcement)
def create_announcement(announcement: Announcement):
    announcements.append(announcement)
    return announcement

@router.get("/announcements/", response_model=List[Announcement])
def get_announcements():
    return announcements

@router.get("/announcements/{announcement_id}", response_model=Announcement)
def get_announcement(announcement_id: int):
    for announcement in announcements:
        if announcement.id == announcement_id:
            return announcement
    raise HTTPException(status_code=404, detail="Announcement not found")

@router.put("/announcements/{announcement_id}", response_model=Announcement)
def update_announcement(announcement_id: int, updated_announcement: Announcement):
    for index, announcement in enumerate(announcements):
        if announcement.id == announcement_id:
            announcements[index] = updated_announcement
            return updated_announcement
    raise HTTPException(status_code=404, detail="Announcement not found")

@router.delete("/announcements/{announcement_id}", response_model=dict)
def delete_announcement(announcement_id: int):
    for index, announcement in enumerate(announcements):
        if announcement.id == announcement_id:
            del announcements[index]
            return {"message": "Announcement deleted successfully"}
    raise HTTPException(status_code=404, detail="Announcement not found")