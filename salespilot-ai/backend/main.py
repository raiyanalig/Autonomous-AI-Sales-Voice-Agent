"""SalesPilot AI - FastAPI application entry point.

Run locally with:
    uvicorn main:app --reload
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.exceptions import register_exception_handlers
from core.logging import get_logger, setup_logging
from routers import api_router

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application startup/shutdown hooks (DB connections added in later modules)."""
    logger.info("Starting %s v%s (%s)", settings.app_name, settings.app_version, settings.app_env)
    yield
    logger.info("Shutting down %s", settings.app_name)


def create_app() -> FastAPI:
    """Application factory: builds and configures the FastAPI instance."""
    setup_logging()

    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Autonomous AI sales agent and intelligent CRM - API.",
        docs_url="/docs",
        redoc_url="/redoc",
        lifespan=lifespan,
    )

    # CORS - allow the Vite dev server to call the API
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global exception handlers
    register_exception_handlers(app)

    # Routers
    app.include_router(api_router)

    @app.get("/", tags=["root"])
    async def root() -> dict:
        """Simple root endpoint with API navigation links."""
        return {
            "application": settings.app_name,
            "docs": "/docs",
            "health": "/api/v1/health",
        }

    return app


app = create_app()
