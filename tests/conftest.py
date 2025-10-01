import pytest
from fastapi.testclient import TestClient
from database import Base, engine, get_db, SessionLocal
from main import app

# override dependency
def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# สร้าง/ลบ schema ก่อนและหลังแต่ละ test
@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

# client fixture ใช้ร่วมกันทุก test
@pytest.fixture
def client():
    return TestClient(app)
