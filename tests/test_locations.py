import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_location():
    data = {
        "name": "Library",
        "latitude": 13.7367,
        "longitude": 100.5231,
        "description": "Main campus library"
    }
    response = client.post("/locations/", json=data)
    assert response.status_code == 200
    result = response.json()
    assert result["name"] == "Library"
    assert result["description"] == "Main campus library"

def test_create_location_duplicate():
    data = {
        "name": "Library",
        "latitude": 13.7367,
        "longitude": 100.5231,
        "description": "Another library"
    }
    response = client.post("/locations/", json=data)
    assert response.status_code == 400
    assert "สถานที่นี้มีอยู่แล้วในระบบ" in response.text

def test_read_locations():
    response = client.get("/locations/")
    assert response.status_code == 200
    locations = response.json()
    assert isinstance(locations, list)
    assert any(loc["name"] == "Library" for loc in locations)

def test_get_all_locations():
    response = client.get("/locations/all")
    assert response.status_code == 200
    locations = response.json()
    assert isinstance(locations, list)
    assert any(loc["name"] == "Library" for loc in locations)

def test_update_location():
    # สมมติว่า id=1 คือ Library ที่สร้างไว้
    data = {
        "name": "Library Updated",
        "latitude": 13.7367,
        "longitude": 100.5231,
        "description": "Updated desc"
    }
    response = client.put("/locations/1", json=data)
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "Library Updated"
    assert updated["description"] == "Updated desc"

def test_update_location_duplicate_name():
    # สร้าง location ใหม่
    client.post("/locations/", json={
        "name": "Canteen",
        "latitude": 13.7370,
        "longitude": 100.5235,
        "description": "Food court"
    })
    # พยายามอัปเดตชื่อซ้ำกับ Canteen
    data = {
        "name": "Canteen",
        "latitude": 13.7367,
        "longitude": 100.5231,
        "description": "Try duplicate"
    }
    response = client.put("/locations/1", json=data)
    assert response.status_code == 400
    assert "มีสถานที่ชื่อนี้อยู่แล้ว" in response.text

def test_delete_location():
    # สมมติว่า id=1 คือ Library Updated
    response = client.delete("/locations/1")
    assert response.status_code == 200
    assert response.json()["detail"] == "ลบสถานที่เรียบร้อยแล้ว"