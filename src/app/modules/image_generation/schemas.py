from typing import Literal

from pydantic import BaseModel, Field


class ImageGenerationRequest(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    aspect_ratio: Literal[
        "1:1",          #Square         — 1080 × 1080 px; works well across most platforms.
        "4:5",          #Portrait       — 1080 × 1350 px; often better for Instagram/Facebook feeds because it takes up more screen space.
        "9:16",         #Landscape      — 1920 × 1080 px; best for wide images/videos.
        "16:9",         #Vertical       — 1080 × 1920 px; standard for Stories, Reels, and TikTok.
    ] = "1:1"
    image_size: Literal["512px", "1K", "2K", "4K"] = "1K"

class ImageGenerationResponse(BaseModel):
    mime_type: str
    image_base64: str