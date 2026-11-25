"""Pydantic schemas for the health/readiness endpoints."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Liveness check response body."""

    status: str = Field(..., description="Service health status, e.g. 'healthy'")
    application: str = Field(..., description="Application name")


class DependencyCheck(BaseModel):
    """Status of a single dependency checked by the readiness probe."""

    name: str = Field(..., description="Dependency name, e.g. 'database'")
    status: str = Field(..., description="'ok', 'not_configured' or 'degraded'")


class ReadinessResponse(BaseModel):
    """Readiness check response body."""

    status: str = Field(..., description="Overall readiness, e.g. 'ready'")
    application: str = Field(..., description="Application name")
    checks: list[DependencyCheck] = Field(
        ..., description="Dependencies currently checked (DB added in a later module)"
    )
