from fastapi import FastAPI
from starlette.responses import RedirectResponse

from app.api.v1.api import api_router
from app.core.config import Settings


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        docs_url=f"{settings.API_V1_STR}/docs",
        redoc_url=f"{settings.API_V1_STR}/redoc"
    )

    @app.get("/")
    @app.get(f"{settings.API_V1_STR}/")
    def read_root():
        response = RedirectResponse(url=f"{settings.API_V1_STR}/docs")
        return response

    app.include_router(api_router, prefix=settings.API_V1_STR)
    return app
