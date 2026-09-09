MOCK_OCR_TEXT = "Château Margaux 2015 Grand Vin Bordeaux Cabernet Sauvignon Merlot"

MOCK_WINE_CARD = {
    "brand": "Château Margaux",
    "producer": "Château Margaux",
    "varietal": ["Cabernet Sauvignon", "Merlot"],
    "vintage": 2015,
    "region": "Бордо, Франция",
}

MOCK_SCAN_RESPONSE = {
    "task_id": "test-task-id",
    "status": "completed",
    "wine_card": MOCK_WINE_CARD,
    "confidence": 0.92,
}

MOCK_IMAGE_BYTES = b"\xff\xd8\xff\xe0\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00"  # минимальный JPEG-хедер

MOCK_LOGIN_REQUEST = {
    "email": "test@example.com",
    "password": "secret123",
}

MOCK_REGISTER_REQUEST = {
    "email": "newuser@example.com",
    "password": "newpassword123",
}
