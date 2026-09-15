from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.config.settings import Settings, get_settings
from app.modules.image_generation.exceptions import ImageGenerationRateLimitError
from app.modules.image_generation.providers.pollinations import (
    PollinationsImageGenerator,
)
from app.modules.image_generation.schemas import (
    ImageGenerationRequest,
    ImageGenerationResponse,
)
from app.modules.image_generation.service import ImageGenerationService

router = APIRouter(
    prefix="/images",
    tags=["Image Generation"],
)


def get_image_generation_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> ImageGenerationService:
    return ImageGenerationService(PollinationsImageGenerator(settings))


@router.post(
    "/generate",
    response_model=ImageGenerationResponse,
)
async def generate_image(
    request: ImageGenerationRequest,
    service: Annotated[
        ImageGenerationService,
        Depends(get_image_generation_service),
    ],
) -> ImageGenerationResponse:
    try:
        return await service.generate(request)
    except ImageGenerationRateLimitError as error:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Image generation quota is unavailable. Check your provider plan and billing details.",
            headers={"Retry-After": "8"},
        ) from error