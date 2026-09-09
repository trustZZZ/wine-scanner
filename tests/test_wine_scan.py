import pytest
from unittest.mock import patch, MagicMock
from tests.mock_data import MOCK_IMAGE_BYTES


@pytest.mark.asyncio
async def test_scan_requires_auth(client):
    response = await client.post(
        "/api/v1/scan/scan-upload",
        files={"file": ("test.jpg", MOCK_IMAGE_BYTES, "image/jpeg")},
        data={"user_id": "00000000-0000-0000-0000-000000000001"},
    )
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_scan_rejects_non_image(client, auth_headers):
    response = await client.post(
        "/api/v1/scan/scan-upload",
        headers=auth_headers,
        data={"user_id": "00000000-0000-0000-0000-000000000001"},
        files={"file": ("test.txt", b"hello", "text/plain")},
    )
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_scan_accepts_image(client, auth_headers):
    with patch("app.api.v1.scan.upload_image") as mock_upload, \
         patch("app.api.v1.scan.scan_wine_label") as mock_celery:
        mock_upload.return_value = "wine-labels/test.jpg"
        mock_celery.delay.return_value = MagicMock(id="fake-task-id")

        response = await client.post(
            "/api/v1/scan/scan-upload",
            headers=auth_headers,
            data={"user_id": "00000000-0000-0000-0000-000000000001"},
            files={"file": ("label.jpg", MOCK_IMAGE_BYTES, "image/jpeg")},
        )
        assert response.status_code == 200
        data = response.json()
        assert "task_id" in data


@pytest.mark.asyncio
async def test_task_status_not_found(client, auth_headers):
    mock_result = MagicMock()
    mock_result.state = "PENDING"
    mock_result.status = "PENDING"

    with patch("app.api.v1.scan.scan_wine_label") as mock_task:
        mock_task.AsyncResult.return_value = mock_result
        response = await client.get(
            "/api/v1/scan/00000000-0000-0000-0000-000000000000",
            headers=auth_headers,
        )
        assert response.status_code == 404

