def test_create_subject(client):
    # สร้าง subject ใหม่พร้อม schedules
    subject_data = {
        "name": "Math",
        "schedules": [
            {
                "user_id": "user123",
                "day": "Monday",
                "start_time": "09:00",
                "end_time": "10:00"
            },
            {
                "user_id": "user123",
                "day": "Wednesday",
                "start_time": "11:00",
                "end_time": "12:00"
            }
        ]
    }
    response = client.post("/subjects/", json=subject_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Math"
    assert len(data["schedules"]) == 2
    assert data["schedules"][0]["day"] == "Monday"

def test_get_subjects(client):
    # เพิ่ม subject ก่อน
    client.post("/subjects/", json={
        "name": "Science",
        "schedules": [
            {
                "user_id": "user456",
                "day": "Tuesday",
                "start_time": "13:00",
                "end_time": "14:00"
            }
        ]
    })
    response = client.get("/subjects/user456")
    assert response.status_code == 200
    subjects = response.json()
    assert isinstance(subjects, list)
    assert any(s["name"] == "Science" for s in subjects)

def test_update_subject(client):
    # เพิ่ม subject ก่อน
    client.post("/subjects/", json={
        "name": "English",
        "schedules": [
            {
                "user_id": "user789",
                "day": "Thursday",
                "start_time": "15:00",
                "end_time": "16:00"
            }
        ]
    })
    # อัปเดต subject
    update_data = {
        "name": "English Updated",
        "schedules": [
            {
                "user_id": "user789",
                "day": "Friday",
                "start_time": "10:00",
                "end_time": "11:00"
            }
        ]
    }
    response = client.put("/subjects/1", json=update_data)
    assert response.status_code == 200
    updated = response.json()
    assert updated["name"] == "English Updated"
    assert updated["schedules"][0]["day"] == "Friday"

def test_delete_subject(client):
    # เพิ่ม subject ก่อน
    client.post("/subjects/", json={
        "name": "ToDelete",
        "schedules": [
            {
                "user_id": "user999",
                "day": "Saturday",
                "start_time": "08:00",
                "end_time": "09:00"
            }
        ]
    })
    response = client.delete("/subjects/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Subject deleted successfully"}

def test_delete_schedule(client):
    # เพิ่ม subject ก่อน
    resp = client.post("/subjects/", json={
        "name": "WithSchedule",
        "schedules": [
            {
                "user_id": "user321",
                "day": "Sunday",
                "start_time": "10:00",
                "end_time": "11:00"
            }
        ]
    })
    schedule_id = resp.json()["schedules"][0]["id"]
    response = client.delete(f"/subjects/schedule/{schedule_id}")
    assert response.status_code == 200
    assert response.json() == {"message": "Schedule deleted successfully"}