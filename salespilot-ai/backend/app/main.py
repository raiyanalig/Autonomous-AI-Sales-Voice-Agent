"""SalesPilot AI - FastAPI application entry point.

Run locally from the backend/ directory with:
    uvicorn app.main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import get_logger, setup_logging
from app.middleware.request_id import RequestIDMiddleware
from app.middleware.request_logging import RequestLoggingMiddleware

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown hooks (DB connections added in later modules)."""
    logger.info(
        "Starting %s v%s (%s)", settings.app_name, settings.app_version, settings.app_env
    )
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Application factory: builds and configures the FastAPI instance."""
    setup_logging()
    settings.validate_runtime()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=(
            "Autonomous AI sales agent and intelligent CRM - REST API. "
            "AI, RAG, memory and database features are added in later modules."
        ),
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # Middleware. Starlette runs the LAST-added middleware first, so
    # RequestID is outermost (request ID is generated before logging).
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        allow_headers=["Content-Type", "Authorization", "X-Request-ID"],
    )
    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(RequestIDMiddleware)

    # Global exception handlers
    register_exception_handlers(app)

    # Versioned API routes
    app.include_router(api_router)

    @app.get("/", tags=["root"])
    async def root() -> dict:
        """Root endpoint with API navigation links."""
        return {
            "application": settings.app_name,
            "version": settings.app_version,
            "docs": "/docs",
            "redoc": "/redoc",
            "openapi": "/openapi.json",
            "health": f"/api/{settings.api_version}/health",
        }

    return app


app = create_app()
