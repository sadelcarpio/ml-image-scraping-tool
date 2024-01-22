from fastapi import FastAPI

from app.api.v1.api import api_router
from app.core.config import settings
from app.db.init_db import init_db

app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc"
)

app.include_router(api_router, prefix=settings.API_V1_STR)

init_db()
