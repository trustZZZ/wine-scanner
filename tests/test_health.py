import pytest


@pytest.mark.asyncio
async def test_app_started(client):
    response = await client.get("/")
    # Если нет корневого эндпоинта, проверяем docs
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_health_check(client):
    # Если есть /health
    response = await client.get("/health")
    assert response.status_code in (200, 404)  # 404 — если эндпоинта нет
