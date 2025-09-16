import sys
import os
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__) + "/.."))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ..database import Base, get_db
from ..main import app

# Create a test database (SQLite in-memory database)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the database dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply the override and create the database schema
app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)

# Create a TestClient
client = TestClient(app)

# Test creating an announcement
def test_create_announcement():
    response = client.post(
        "/announcements/",
        json={
            "title": "Test Announcement",
            "content": "This is a test announcement.",
            "category": "General",
            "created_by": 1,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Test Announcement"
    assert response.json()["content"] == "This is a test announcement."

# Test reading all announcements
def test_read_announcements():
    response = client.get("/announcements/")
    assert response.status_code == 200
    assert len(response.json()) > 0

# Test updating an announcement
def test_update_announcement():
    response = client.put(
        "/announcements/1",
        json={
            "title": "Updated Announcement",
            "content": "This is an updated test announcement.",
            "category": "Updates",
            "created_by": 1,
        },
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Announcement"

# Test deleting an announcement
def test_delete_announcement():
    response = client.delete("/announcements/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Announcement deleted"}