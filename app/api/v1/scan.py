import logging
from app.tasks.tasks import scan_wine_label
from celery.result import AsyncResult
from app.users.dependencies import get_current_user
from app.schemas.scan import ScanRequest, ScanResultResponse, ScanTaskResponse
from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Depends
from app.services.minio_service import upload_image

import uuid


router = APIRouter(prefix="/scan", tags=["scan"])
logger = logging.getLogger(__name__)


@router.post("/scan-upload")
async def scan_upload(file: UploadFile = File(...), user_id: str = Form(...), current_user=Depends(get_current_user),):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Файл должен быть изображением")

    file_bytes = await file.read()
    object_name = f"{user_id}/{uuid.uuid4().hex}.jpg"
    image_url = upload_image(file_bytes, object_name)

    task = scan_wine_label.delay(image_url=image_url, user_id=user_id)

    return {
        "task_id": task.id,
        "image_url": image_url,
    }


@router.post("", response_model=ScanTaskResponse, status_code=202)
def create_scan(request: ScanRequest) -> ScanTaskResponse:
    """Отправить фото на распознавание. Возвращает task_id."""
    task = scan_wine_label.delay(
        image_url=request.image_url,
        user_id=request.user_id,
    )
    logger.info(f"Создана задача scan_wine_label: {task.id}")
    return ScanTaskResponse(
        task_id=task.id,
        status="pending",
        message="Задача отправлена в очередь",
    )


@router.get("/{task_id}", response_model=ScanResultResponse)
def get_scan_result(task_id: str) -> ScanResultResponse:
    """Получить результат сканирования по task_id."""
    result: AsyncResult = scan_wine_label.AsyncResult(task_id)

    response = ScanResultResponse(task_id=task_id, status=result.status.lower())

    if result.state == "PENDING":
        raise HTTPException(status_code=404, detail="Задача не найдена")

    if result.state == "STARTED":
        return response

    if result.state == "SUCCESS":
        data = result.result
        response.status = "success"
        response.wine_name = data.get("wine_name")
        response.wine_type = data.get("wine_type")
        response.region = data.get("region")
        response.abv = data.get("abv")
        response.confidence = data.get("confidence")
        response.image_url = data.get("image_url")
        return response

    if result.state == "FAILURE":
        response.status = "failed"
        response.error = str(result.result)
        return response

    return response
