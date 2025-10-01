import pytest
from models.bookmark import Bookmark

def test_get_bookmarks_empty(client):
    response = client.get("/bookmarks/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_bookmark(client):
    # สร้าง bookmark ใหม่
    response = client.post("/bookmarks/", json={"announcement_id": 123})
    assert response.status_code == 200
    data = response.json()
    assert data["announcement_id"] == 123
    assert data["user_id"] == 1

def test_create_duplicate_bookmark(client):
    # สร้าง bookmark เดิมซ้ำ
    client.post("/bookmarks/", json={"announcement_id": 456})
    response = client.post("/bookmarks/", json={"announcement_id": 456})
    assert response.status_code == 400
    assert response.json()["detail"] == "Bookmark already exists"

def test_delete_bookmark_by_announcement(client):
    # สร้าง bookmark ก่อน
    client.post("/bookmarks/", json={"announcement_id": 789})
    # ลบ bookmark
    response = client.delete("/bookmarks/by-announcement/789")
    assert response.status_code == 200
    assert response.json()["message"] == "Bookmark deleted successfully"

def test_delete_bookmark_not_found(client):
    response = client.delete("/bookmarks/by-announcement/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Bookmark not found"