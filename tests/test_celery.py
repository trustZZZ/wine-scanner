import pytest
from unittest.mock import patch, MagicMock
from app.tasks.tasks import scan_wine_label, parse_ocr_to_card
from app.tasks.celery_app import celery_app
from app.tasks.tasks import scan_wine_label, parse_ocr_to_card
from tests.mock_data import MOCK_OCR_TEXT, MOCK_WINE_CARD


def test_parse_ocr_extracts_vintage():
    card = parse_ocr_to_card(MOCK_OCR_TEXT)
    assert card["vintage"] == 2015


def test_parse_ocr_extracts_varietal():
    card = parse_ocr_to_card(MOCK_OCR_TEXT)
    assert "Cabernet Sauvignon" in card["varietal"]
    assert "Merlot" in card["varietal"]


def test_parse_ocr_extracts_region():
    card = parse_ocr_to_card(MOCK_OCR_TEXT)
    assert card["region"] is not None
    assert "Бордо" in card["region"]


def test_parse_ocr_no_year():
    card = parse_ocr_to_card("Some wine without year")
    assert card["vintage"] is None


def test_celery_task_runs(monkeypatch):
    """
    Тест Celery-задачи в синхронном режиме (без брокера).
    """
    # Мокаем get_sync_db
    mock_db = MagicMock()
    mock_query = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None  # вино не найдено
    monkeypatch.setattr("app.tasks.tasks.get_sync_db", lambda: mock_db)
    monkeypatch.setattr("app.tasks.tasks.s3_client", MagicMock())

    # Мокаем создание Wine и Scan
    mock_wine = MagicMock(id="wine-uuid")
    mock_scan = MagicMock(id="scan-uuid")

    result = scan_wine_label.run(
        image_url="wine-labels/test.jpg",
        user_id="00000000-0000-0000-0000-000000000001",
    )

    # Проверяем, что задача вернула completed
    assert result["status"] == "completed"
    assert "wine_card" in result
