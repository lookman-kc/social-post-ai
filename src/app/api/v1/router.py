from fastapi import APIRouter

from app.modules.image_generation.router import router as image_generation_router

router = APIRouter(prefix="/api/v1")

router.include_router(image_generation_router)