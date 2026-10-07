from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_certificate_not_found():

    response = client.get(
        "/certificates/999999"
    )

    assert response.status_code == 404