"""Request logging middleware.

Logs method, path, response status and processing duration for every
request. Only the URL path is logged - never query strings, headers,
bodies or anything that could contain credentials or PII.
"""

import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

from app.core.logging import REQUEST_LOGGER_NAME

logger = logging.getLogger(REQUEST_LOGGER_NAME)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Log a summary line for each request."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "method=%s path=%s status=%s duration_ms=%.1f",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
