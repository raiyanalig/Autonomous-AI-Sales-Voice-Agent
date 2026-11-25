"""Logging configuration for the SalesPilot AI backend.

Uses a ContextVar + logging.Filter so the request ID flows into every log
line emitted while a request is being processed. This keeps logs greppable
and is compatible with structured logging / monitoring tools later.
"""

import logging
import sys
from contextvars import ContextVar

from app.core.config import settings

# Holds the current request ID for the active request context.
request_id_var: ContextVar[str | None] = ContextVar("request_id", default=None)

# Logger name used by the request logging middleware.
REQUEST_LOGGER_NAME = "app.request"


class RequestIDFilter(logging.Filter):
    """Attach the current request ID to every log record."""

    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_var.get() or "-"
        return True


def setup_logging() -> None:
    """Configure the root logger used across the application."""
    level = getattr(logging, settings.log_level.upper(), logging.INFO)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(request_id)-36s | %(name)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )
    handler.addFilter(RequestIDFilter())

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)

    # Reduce noise from third-party loggers during development
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger (call after setup_logging)."""
    return logging.getLogger(name)
