def test_create_announcement(client):
    response = client.post("/announcements/", json={
        "title": "Test Announcement",
        "content": "This is a test announcement.",
        "category": "General",
        "created_by": 1,
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Test Announcement"

def test_read_announcements(client):
    response = client.get("/announcements/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_announcement(client):
    # สร้าง announcement ก่อน
    client.post("/announcements/", json={
        "title": "Original",
        "content": "Original content",
        "category": "General",
        "created_by": 1,
    })
    # อัปเดต
    response = client.put("/announcements/1", json={
        "title": "Updated Announcement",
        "content": "Updated content",
        "category": "Updates",
        "created_by": 1,
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Announcement"

def test_delete_announcement(client):
    # สร้าง announcement ก่อน
    client.post("/announcements/", json={
        "title": "To Delete",
        "content": "Will be deleted",
        "category": "General",
        "created_by": 1,
    })
    # ลบ
    response = client.delete("/announcements/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Announcement deleted"}
