from fastapi import APIRouter

from app.api.v1.endpoints import urls, projects, users

api_router = APIRouter()

api_router.include_router(urls.router, prefix="/urls")
api_router.include_router(projects.router, prefix="/projects")
api_router.include_router(users.router, prefix="/users")
