"""Central v1 router.

Registers all v1 endpoint routers under the /api/v1 prefix so that
main.py stays clean and new endpoints are added in one place.
"""

from fastapi import APIRouter

from app.api.v1.endpoints.demo import router as demo_router
from app.api.v1.endpoints.health import router as health_router

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
api_router.include_router(demo_router)
