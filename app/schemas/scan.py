from pydantic import BaseModel


class ScanRequest(BaseModel):
    image_url: str
    user_id: str


class ScanTaskResponse(BaseModel):
    task_id: str
    status: str
    message: str


class ScanResultResponse(BaseModel):
    task_id: str
    status: str
    wine_name: str | None = None
    wine_type: str | None = None
    region: str | None = None
    abv: str | None = None
    confidence: float | None = None
    image_url: str | None = None
    error: str | None = None
