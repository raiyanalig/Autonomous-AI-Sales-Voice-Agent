"""API routers for the SalesPilot AI backend."""

from fastapi import APIRouter

from routers.health import router as health_router

# Aggregate all v1 routers under a single /api/v1 prefix
api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health_router)
