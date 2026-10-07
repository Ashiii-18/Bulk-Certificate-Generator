from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app
from app.services.certificate_generator import generate_certificate


client = TestClient(app)


def test_generate_certificate():

    file_path = generate_certificate(
        certificate_id=999,
        recipient_name="Test User",
        event_name="Python Workshop 2026",
        certificate_title="Certificate of Participation"
    )

    file = Path(file_path)

    assert file.exists()
    assert file.stat().st_size > 0

    file.unlink()


def test_certificate_generation_failure_does_not_crash():

    with patch(
        "app.routes.jobs.generate_certificate",
        side_effect=Exception("PDF generation failed")
    ):

        response = client.post(
            "/jobs",
            json={
                "event_name": "Failure Test",
                "certificate_title": "Certificate",
                "recipients": [
                    {
                        "name": "Fail User",
                        "email": "fail@example.com"
                    }
                ]
            }
        )

        assert response.status_code == 200