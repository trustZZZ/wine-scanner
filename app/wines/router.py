from fastapi import APIRouter, Depends
from app.users.dependencies import get_current_user

router = APIRouter(prefix="/wines", tags=["Вина"])


@router.get("/search")
async def search_wines(q: str, current_user = Depends(get_current_user)):
    """Заглушка: поиск вина по названию."""
    return {"query": q, "results": [], "message": "Поиск будет доступен после подключения БД вин"}


@router.post("/scan")
async def scan_wine_label(current_user = Depends(get_current_user)):
    """Заглушка: сканирование фото винной полки."""
    return {"results": [], "message": "OCR и поиск будут доступны позже"}
