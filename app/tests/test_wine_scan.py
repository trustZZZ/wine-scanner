import pytest
from unittest.mock import patch, MagicMock
from tests.mock_data import MOCK_IMAGE_BYTES, MOCK_WINE_CARD


@pytest.mark.asyncio
async def test_scan_requires_auth(client):
    response = await client.post(
        "/api/v1/wine/scan",
        files={"file": ("test.jpg", MOCK_IMAGE_BYTES, "image/jpeg")},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_scan_rejects_non_image(client, auth_headers):
    response = await client.post(
        "/api/v1/wine/scan",
        headers=auth_headers,
        files={"file": ("test.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_scan_accepts_image(client, auth_headers):
    # Мокаем загрузку в MinIO и Celery-задачу
    with patch("app.api.v1.wine.upload_file") as mock_upload, \
         patch("app.api.v1.wine.process_wine_ocr") as mock_celery:
        mock_upload.return_value = None
        mock_celery.delay.return_value = MagicMock(id="fake-task-id")

        response = await client.post(
            "/api/v1/wine/scan",
            headers=auth_headers,
            files={"file": ("label.jpg", MOCK_IMAGE_BYTES, "image/jpeg")},
        )
        assert response.status_code == 202
        data = response.json()
        assert "task_id" in data
        assert data["status"] == "pending"


@pytest.mark.asyncio
async def test_task_status_not_found(client, auth_headers):
    response = await client.get(
        "/api/v1/wine/tasks/00000000-0000-0000-0000-000000000000",
        headers=auth_headers,
    )
    assert response.status_code == 404
