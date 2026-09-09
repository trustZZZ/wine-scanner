from celery import shared_task
from sqlalchemy.orm import Session
from app.database import get_sync_db
from app.users.models import Scan
from app.wines.models import Wine
from uuid import UUID
from datetime import datetime, timezone
import json
from app.services.minio_service import s3_client, BUCKET_NAME


@shared_task(queue='scan', bind=True, max_retries=3)
def scan_wine_label(self, image_url: str, user_id: str):
    db: Session = get_sync_db()

    try:
        # --- 1. Скачиваем фото из MinIO ---
        # Если image_url — это полный путь вида "bucket/path/image.jpg",
        # нужно извлечь key:
        # object_key = image_url.split(f"{BUCKET_NAME}/")[-1]
        # response = s3_client.get_object(Bucket=BUCKET_NAME, Key=object_key)
        # image_bytes = response["Body"].read()

        # --- 2. OCR (заглушка) ---
        # В реальности: tesseract, EasyOCR, Yandex Vision, и т.д.
        ocr_raw_text = "Château Margaux 2015 Grand Vin Bordeaux Cabernet Sauvignon Merlot"
        confidence = 0.92

        # --- 3. Парсинг OCR → карточка ---
        wine_card = parse_ocr_to_card(ocr_raw_text)

        # --- 4. Поиск/создание Wine ---
        wine = db.query(Wine).filter(
            Wine.name == wine_card["brand"],
            Wine.vintage_year == wine_card.get("vintage"),
        ).first()

        if not wine:
            wine = Wine(
                name=wine_card["brand"],
                producer=wine_card.get("producer", wine_card["brand"]),
                vintage_year=wine_card.get("vintage"),
                region=wine_card.get("region"),
                grape_varieties=wine_card.get("varietal", []),
            )
            db.add(wine)
            db.flush()  # получаем wine.id без commit

        # --- 5. Сохранение Scan ---
        scan = Scan(
            user_id=UUID(user_id),
            photo_url=image_url,
            status="completed",
            ocr_raw_text=ocr_raw_text,
            wine_card=wine_card,
            wine_id=wine.id,
            confidence=confidence,
            completed_at=datetime.now(timezone.utc),
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)

        # --- 6. Метаданные в MinIO ---
        meta = {
            "scan_id": str(scan.id),
            "wine_id": str(wine.id),
            "wine_card": wine_card,
            "confidence": confidence,
            "photo_url": image_url,
            "user_id": user_id,
        }
        meta_key = f"meta/{scan.id}.json"
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=meta_key,
            Body=json.dumps(meta, ensure_ascii=False),
            ContentType="application/json",
        )

        return {
            "task_id": str(scan.id),
            "wine_id": str(wine.id),
            "status": "completed",
            "wine_card": wine_card,
            "confidence": confidence,
        }

    except Exception as exc:
        db.rollback()
        # Сохраняем ошибку в отдельной попытке
        try:
            scan = db.query(Scan).filter(Scan.photo_url == image_url).first()
            if scan:
                scan.status = "failed"
                scan.error_message = str(exc)[:500]
                db.commit()
        except Exception:
            pass
        raise self.retry(exc=exc, countdown=60)
    finally:
        db.close()


def parse_ocr_to_card(raw_text: str) -> dict:
    """
    Заглушка парсера. В реальности — NLP/регулярки/LLM.
    """
    text = raw_text.strip()

    # Год: ищем 4 цифры, начинающиеся с 19 или 20
    import re
    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", text)
    vintage = int(year_match.group(1)) if year_match else None

    # Марка/бренд: первое существительное до года (грубая заглушка)
    brand = text.split(str(vintage))[0].strip() if vintage else text[:50]

    # Сорта винограда: ищем известные
    known_varieties = [
        "Каберне Совиньон", "Мерло", "Пино Нуар", "Шардоне",
        "Совиньон Блан", "Рислинг", "Шираз", "Сира", "Темпранильо",
        "Cabernet Sauvignon", "Merlot", "Pinot Noir", "Chardonnay",
        "Sauvignon Blanc", "Riesling", "Shiraz", "Syrah", "Tempranillo",
    ]
    varietal = [v for v in known_varieties if v.lower() in text.lower()]

    # Регион (грубая заглушка)
    regions = {
        "бордо": "Бордо, Франция",
        "bordeaux": "Бордо, Франция",
        "тоскана": "Тоскана, Италия",
        "tuscany": "Тоскана, Италия",
        "крым": "Крым",
        "риоха": "Риоха, Испания",
    }
    region = None
    for keyword, region_name in regions.items():
        if keyword.lower() in text.lower():
            region = region_name
            break

    return {
        "brand": brand,
        "producer": brand,  # пока не отличаем
        "varietal": varietal or ["не определён"],
        "vintage": vintage,
        "region": region,
    }
