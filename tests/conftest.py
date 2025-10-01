import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import Base, get_db
from main import app

# ⭐ import models ทั้งหมด เพื่อ register ตารางกับ Base
from models import user, events, announcement, bookmark

from models.user import User
from routers.auth import get_current_user

# ใช้ shared memory DB (คง schema ตลอด session)
SQLALCHEMY_DATABASE_URL = "sqlite:///file:test.db?mode=memory&cache=shared"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False, "uri": True}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# -------- Overrides --------
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
app.dependency_overrides[get_db] = override_get_db


def override_get_current_user():
    return User(
        id=1,
        username="testuser",
        hashed_password="fakehashedpw",
        name="Test User",
        student_id="6510110575",
        faculty="Engineering",
        year=4
    )
app.dependency_overrides[get_current_user] = override_get_current_user


# -------- Fixtures --------
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # ✅ สร้าง schema ให้ครบ
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def create_test_user():
    db = TestingSessionLocal()
    if not db.query(User).filter(User.id == 1).first():
        db.add(User(
            id=1,   # ✅ fix id ให้ตรงกับ test
            username="testuser",
            hashed_password="fakehashedpw",
            name="Test User",
            student_id="6510110575",
            faculty="Engineering",
            year=4
        ))
        db.commit()
    db.close()



@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c
