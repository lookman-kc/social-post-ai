import base64

from app.modules.image_generation.interfaces import ImageGenerator
from app.modules.image_generation.schemas import (
    ImageGenerationRequest,
    ImageGenerationResponse,
)


class ImageGenerationService:
    def __init__(self, generator: ImageGenerator) -> None:
        self.generator = generator

    async def generate(
        self,
        request: ImageGenerationRequest,
    ) -> ImageGenerationResponse:
        mime_type, image_bytes = await self.generator.generate(request)

        return ImageGenerationResponse(
            mime_type=mime_type,
            image_base64=base64.b64encode(image_bytes).decode("utf-8"),
        )