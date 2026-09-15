from typing import Annotated

from fastapi import Depends, FastAPI

from app.api.v1.router import router as api_v1_router
from app.config.settings import Settings, get_settings

app = FastAPI(
    title="Social Post AI",
    version="0.1.0"
)

@app.get("/health")
def health_check(
    settings: Annotated[Settings, Depends(get_settings)]
):
    return {
        "status": "ok",
        "environment": settings.app_env
    }

app.include_router(api_v1_router)