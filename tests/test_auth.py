import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

access_token = None  # ใช้ global ตัวแปรนี้

def test_register_user():
    data = {
        "username": "testuser1@example.com",
        "password": "testpass123",
        "name": "Test User",
        "student_id": "65000001",
        "faculty": "Engineering",
        "year": 1,
        "roles": ["user"]
    }
    response = client.post("/auth/register", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["username"] == "testuser1@example.com"
    assert "id" in result

def test_register_duplicate_email():
    data = {
        "username": "testuser1@example.com",
        "password": "testpass123",
        "name": "Test User",
        "student_id": "65000002",
        "faculty": "Engineering",
        "year": 1,
        "roles": ["user"]
    }
    response = client.post("/auth/register", json=data)
    assert response.status_code == 400
    assert "Email already registered" in response.text

def test_login_for_access_token():
    global access_token
    data = {
        "username": "testuser1@example.com",
        "password": "testpass123"
    }
    response = client.post("/auth/token", data=data)
    assert response.status_code == 200
    result = response.json()
    assert "access_token" in result
    assert result["token_type"] == "bearer"
    assert result["user"]["username"] == "testuser1@example.com"
    access_token = result["access_token"]

# หมายเหตุ: การทดสอบ endpoint ที่ต้องใช้สิทธิ์ admin เช่น /users, /users/{user_id}/role
# ควรสร้าง user ที่มี role admin และใช้ token ของ admin ในการทดสอบ