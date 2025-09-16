from fastapi import FastAPI
from database import engine, Base

# Import models เพื่อให้ Base รู้จัก tables
from models.announcement import Announcement
from models.bookmark import Bookmark
from models.user import User

app = FastAPI()

# สร้าง tables ทั้งหมด
Base.metadata.create_all(bind=engine)

from routers.announcements import router as announcements_router
from routers.bookmarks import router as bookmarks_router

app.include_router(announcements_router, tags=["Announcements"])
app.include_router(bookmarks_router, tags=["Bookmarks"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
