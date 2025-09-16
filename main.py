from fastapi import FastAPI
from database import engine, Base
from routers.announcements import router as announcements_router
from routers.bookmarks import router as bookmarks_router
from routers.auth import router as auth_router

# Import models เพื่อให้ Base รู้จัก tables
# from models.announcement import Announcement
# from models.bookmark import Bookmark
# from models.user import User

# สร้าง tables ทั้งหมด
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Life Hub API")

# Include routers
app.include_router(announcements_router, tags=["Announcements"])
app.include_router(bookmarks_router)
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "Campus Life Hub API"}
