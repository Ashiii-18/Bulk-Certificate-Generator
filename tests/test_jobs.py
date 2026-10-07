from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_create_generation_job():

    response = client.post(
        "/jobs",
        json={
            "event_name": "Python Workshop",
            "certificate_title": "Certificate of Participation",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "test@example.com"
                },
                {
                    "name": "Another User",
                    "email": "another@example.com"
                }
            ]
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "job_id" in data
    assert data["status"] == "queued"
    assert data["total"] == 2

def test_get_job_status():

    response = client.post(
        "/jobs",
        json={
            "event_name": "Status Test",
            "certificate_title": "Certificate",
            "recipients": [
                {
                    "name": "Status User",
                    "email": "status@example.com"
                }
            ]
        }
    )

    job_id = response.json()["job_id"]

    response = client.get(
        f"/jobs/{job_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["job_id"] == job_id
    assert data["total"] == 1
    assert "completed" in data
    assert "successful" in data
    assert "failed" in data