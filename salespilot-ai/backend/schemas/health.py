"""Pydantic response schemas for the health endpoint."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Standard health check response body."""

    status: str = Field(..., description="Service health status, e.g. 'healthy'")
    application: str = Field(..., description="Application name")
