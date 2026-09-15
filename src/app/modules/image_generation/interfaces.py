from typing import Protocol

from app.modules.image_generation.schemas import ImageGenerationRequest


class ImageGenerator(Protocol):
    async def generate(
        self,
        request: ImageGenerationRequest,
    ) -> tuple[str, bytes]:
        """
        Returns:
            mime_type, image_bytes
        """
        ...