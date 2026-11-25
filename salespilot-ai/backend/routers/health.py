"""Health check endpoint.

Provides a lightweight readiness probe used by the frontend to verify
that the backend is reachable.
"""

from fastapi import APIRouter, status

from schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
)
async def health_check() -> HealthResponse:
    """Return service health status."""
    return HealthResponse(status="healthy", application="SalesPilot AI")
