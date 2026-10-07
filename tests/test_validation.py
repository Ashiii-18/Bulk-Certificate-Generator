from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_invalid_email():

    response = client.post(
        "/jobs",
        json={
            "event_name": "Python Workshop",
            "certificate_title": "Certificate of Participation",
            "recipients": [
                {
                    "name": "Test User",
                    "email": "invalid-email"
                }
            ]
        }
    )

    assert response.status_code == 422


def test_empty_recipients():

    response = client.post(
        "/jobs",
        json={
            "event_name": "Python Workshop",
            "certificate_title": "Certificate of Participation",
            "recipients": []
        }
    )

    assert response.status_code == 422


def test_short_name():

    response = client.post(
        "/jobs",
        json={
            "event_name": "Python Workshop",
            "certificate_title": "Certificate of Participation",
            "recipients": [
                {
                    "name": "A",
                    "email": "test@example.com"
                }
            ]
        }
    )

    assert response.status_code == 422