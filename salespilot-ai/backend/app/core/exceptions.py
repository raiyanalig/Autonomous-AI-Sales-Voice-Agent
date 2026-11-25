"""Central exception handling.

Converts expected and unexpected failures into consistent JSON responses.
Stack traces are logged server-side but never returned to clients.
"""

import logging

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base class for expected application errors."""

    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


def _error_response(status_code: int, message: str, detail=None) -> JSONResponse:
    """Build a consistent error JSON body."""
    body = {"status": "error", "message": message}
    if detail is not None:
        body["detail"] = detail
    return JSONResponse(status_code=status_code, content=body)


def register_exception_handlers(app: FastAPI) -> None:
    """Attach global exception handlers to the FastAPI app."""

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError) -> JSONResponse:
        logger.warning("AppError: %s", exc.message)
        return _error_response(exc.status_code, exc.message)

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
        logger.info("HTTP %s on %s", exc.status_code, request.url.path)
        return _error_response(exc.status_code, str(exc.detail))

    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> JSONResponse:
        logger.warning("Validation error on %s: %s", request.url.path, exc.errors())
        return _error_response(422, "Request validation failed", detail=exc.errors())

    @app.exception_handler(Exception)
    async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
        # Log the full traceback server-side; never expose it to clients.
        logger.exception("Unhandled error on %s", request.url.path)
        return _error_response(500, "Internal server error")
