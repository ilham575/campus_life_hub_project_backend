from fastapi import FastAPI
from database import engine, Base
from routers.announcements import router as announcements_router
from routers.bookmarks import router as bookmarks_router
from routers.auth import router as auth_router
from routers.timetable import router as timetable_router  # ✅ เพิ่ม timetable router

# Import models เพื่อให้ Base รู้จัก tables (ถ้าต้องการ)
# from models.announcement import Announcement
# from models.bookmark import Bookmark
# from models.user import User
# from models.timetable import Timetable   # ✅ เพิ่มถ้าอยากสร้างตาราง timetable ด้วย

# Import models ให้ Base รู้จักตาราง
from models import timetable   # ✅ สำคัญ ต้อง import

# สร้าง tables ทั้งหมด
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Life Hub API")

# Include routers
app.include_router(announcements_router, tags=["Announcements"])
app.include_router(bookmarks_router, tags=["Bookmarks"])
app.include_router(auth_router, tags=["Auth"])
app.include_router(timetable_router, tags=["Timetable"])  # ✅ เชื่อม timetable

@app.get("/")
async def root():
    return {"message": "Campus Life Hub API"}
