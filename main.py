from fastapi import FastAPI
from routers.announcements import router as announcements_router

app = FastAPI()

app.include_router(announcements_router, tags=["Announcements"])

@app.get("/")
def read_root():
    return {"Hello": "World"}
