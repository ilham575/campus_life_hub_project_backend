import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import get_db, Base
from main import app
from models.events import Event as EventModel
from models.user import User

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_events.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_event():
    # สร้าง user ทดสอบ
    db = TestingSessionLocal()
    test_user = User(id="test_user", name="Test User", email="test@test.com")
    db.add(test_user)
    db.commit()
    db.close()
    
    response = client.post("/events/", json={
        "user_id": "test_user",
        "title": "Test Event",
        "description": "Test Description",
        "start_time": "2024-01-01T10:00:00",
        "end_time": "2024-01-01T11:00:00"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Event"

def test_read_events():
    response = client.get("/events/?user_id=test_user")
    assert response.status_code == 200

def test_read_event_not_found():
    response = client.get("/events/999?user_id=test_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

def test_update_event_not_found():
    response = client.put("/events/999", json={
        "user_id": "test_user",
        "title": "Updated Event",
        "description": "Updated Description",
        "start_time": "2024-01-01T10:00:00",
        "end_time": "2024-01-01T11:00:00"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

def test_delete_event_not_found():
    response = client.delete("/events/999?user_id=test_user")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"