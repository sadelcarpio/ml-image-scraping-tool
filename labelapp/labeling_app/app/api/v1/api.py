from fastapi import APIRouter
from app.api.v1.endpoints import urls

api_router = APIRouter()

api_router.include_router(urls.router, prefix="/urls")
