from urllib.parse import quote

import httpx

from app.config.settings import Settings
from app.modules.image_generation.exceptions import ImageGenerationRateLimitError
from app.modules.image_generation.schemas import ImageGenerationRequest


class PollinationsImageGenerator:
	def __init__(self, settings: Settings) -> None:
		self.api_key = settings.pollinations_api_key

	async def generate(
		self,
		request: ImageGenerationRequest,
	) -> tuple[str, bytes]:
		width, height = self._dimensions(request)
		prompt = quote(request.prompt, safe="")
		url = f"https://gen.pollinations.ai/image/{prompt}"

		try:
			async with httpx.AsyncClient(timeout=120) as client:
				response = await client.get(
					url,
					params={
						"model": "z-image-turbo",
						"width": width,
						"height": height,
					},
					headers={"Authorization": f"Bearer {self.api_key}"},
				)
				response.raise_for_status()
		except httpx.HTTPStatusError as error:
			if error.response.status_code == 429:
				raise ImageGenerationRateLimitError from error
			raise RuntimeError("Pollinations image generation failed") from error
		except httpx.HTTPError as error:
			raise RuntimeError("Pollinations image generation failed") from error

		return response.headers.get("content-type", "image/png"), response.content

	@staticmethod
	def _dimensions(request: ImageGenerationRequest) -> tuple[int, int]:
		size = {"512px": 512, "1K": 1024, "2K": 2048, "4K": 4096}[request.image_size]
		ratios = {
			"1:1": (1, 1),
			"4:5": (4, 5),
			"9:16": (9, 16),
			"16:9": (16, 9),
		}
		ratio_width, ratio_height = ratios[request.aspect_ratio]

		if ratio_width >= ratio_height:
			return size, round(size * ratio_height / ratio_width)
		return round(size * ratio_width / ratio_height), size
