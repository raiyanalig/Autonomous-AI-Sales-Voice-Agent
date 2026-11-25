"""Reusable common response schemas."""

from typing import Any

from pydantic import BaseModel


class MessageResponse(BaseModel):
    """Simple success message, e.g. for actions without a payload."""

    message: str


class ErrorResponse(BaseModel):
    """Consistent error body returned by the global exception handlers."""

    status: str = "error"
    message: str
    detail: Any | None = None
