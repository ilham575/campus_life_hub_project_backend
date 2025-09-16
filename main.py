from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
from routers import auth, announcements, bookmarks

# สร้าง tables ทั้งหมด
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Campus Life Hub API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ในการใช้งานจริงควรจำกัด origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["authentication"])
app.include_router(announcements.router, prefix="/announcements", tags=["announcements"])
app.include_router(bookmarks.router, prefix="/bookmarks", tags=["bookmarks"])


@app.get("/")
def read_root():
    return {"message": "Campus Life Hub API v2.0 - Firebase Free!"}


@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
