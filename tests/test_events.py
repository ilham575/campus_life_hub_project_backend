def test_create_event(client):
    response = client.post("/events/", json={
        "user_id": "u1",
        "title": "Hello",
        "description": "World",
        "start_time": "2024-01-01T10:00:00",
        "end_time": "2024-01-01T11:00:00"
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Hello"

def test_read_events(client):
    response = client.get("/events/?user_id=u1")
    assert response.status_code == 200

def test_read_event_not_found(client):
    response = client.get("/events/999?user_id=u1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

def test_update_event_not_found(client):
    response = client.put("/events/999", json={
        "user_id": "u1",
        "title": "Updated Event",
        "description": "Updated Description",
        "start_time": "2024-01-01T10:00:00",
        "end_time": "2024-01-01T11:00:00"
    })
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"

def test_delete_event_not_found(client):
    response = client.delete("/events/999?user_id=u1")
    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"
