from fastapi import APIRouter

from .auth import router as auth_router
from .scan import router as scan_router
from app.wines.router import router as wines_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(scan_router)
router.include_router(wines_router)
