from fastapi import FastAPI
from database import engine
from models.announcement import Base
from routers.announcements import router as announcements_router
from models.user import User
from routers.bookmarks import router as bookmarks_router

app = FastAPI()
Base.metadata.create_all(bind=engine)
app.include_router(announcements_router, tags=["Announcements"])
app.include_router(bookmarks_router, tags=["Bookmarks"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
